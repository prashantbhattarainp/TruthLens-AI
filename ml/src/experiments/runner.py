"""Leakage-aware orchestration for cross-validated baseline experiments."""

from __future__ import annotations

import hashlib
import time
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from sklearn.base import ClassifierMixin

from experiments.artifacts import assert_not_raw_path, write_experiment_artifacts
from experiments.config import ExperimentConfig
from experiments.cross_validation import build_cross_validation_folds
from experiments.exceptions import ExperimentInputError
from experiments.metrics import MetricsResult, calculate_metrics
from experiments.model_registry import build_candidate_model_record
from experiments.models import ExperimentDocument, ExperimentRecord, FoldResult, OutOfFoldPrediction
from experiments.seed import apply_random_seed
from experiments.tracking import ExperimentRunLogger, generate_experiment_id
from features.config import FeatureConfig
from features.models import FeatureDocument
from features.pipeline import FeaturePipeline
from models.factory import BaselineModelFactory


@dataclass(frozen=True)
class ExperimentContext:
    """Governance and lineage fields supplied by an approved future training workflow."""

    dataset_version: str
    split_id: str
    preprocessing_version: str
    preprocessing_configuration_sha256: str
    source_manifest_path: Path
    notes: str
    dataset_hash: str


class ExperimentRunner:
    """Fit feature representations within every CV training fold, then train an approved model."""

    def __init__(
        self,
        experiment_config: ExperimentConfig,
        feature_config: FeatureConfig,
        model_factory: BaselineModelFactory | None = None,
    ) -> None:
        self.experiment_config = experiment_config
        self.feature_config = feature_config
        self.model_factory = model_factory or BaselineModelFactory()

    def run_and_write(
        self,
        *,
        context: ExperimentContext,
        documents: Iterable[ExperimentDocument],
        output_root: Path,
    ) -> tuple[ExperimentRecord, dict[str, str]]:
        """Execute configured CV and write a candidate-model evidence bundle."""
        _validate_context(context)
        assert_not_raw_path(context.source_manifest_path)
        assert_not_raw_path(output_root)
        materialized = _materialize_documents(documents)
        labels = tuple(document.label for document in materialized)
        groups = _groups_for_cross_validation(materialized, self.experiment_config.cross_validation.strategy)
        folds = build_cross_validation_folds(
            labels,
            self.experiment_config.cross_validation,
            self.experiment_config.random_seed,
            groups,
        )
        seed_evidence = apply_random_seed(self.experiment_config.random_seed)
        source_manifest_sha256 = _sha256_file(context.source_manifest_path)
        started_at = datetime.now(timezone.utc)
        started_clock = time.perf_counter()
        experiment_id = generate_experiment_id(self.experiment_config.model, started_at)
        output_directory = output_root / experiment_id
        logger = ExperimentRunLogger()
        logger.record(
            "experiment_started",
            experiment_id=experiment_id,
            dataset_version=context.dataset_version,
            split_id=context.split_id,
            model=self.experiment_config.model,
            experiment_configuration_sha256=self.experiment_config.sha256,
            feature_configuration_sha256=self.feature_config.sha256,
            random_seed=self.experiment_config.random_seed,
            cross_validation=self.experiment_config.cross_validation.__dict__,
            source_manifest_sha256=source_manifest_sha256,
        )

        fold_results: list[FoldResult] = []
        predictions_with_position: list[tuple[int, OutOfFoldPrediction]] = []
        fold_artifacts: list[tuple[int, object, object]] = []
        for fold in folds:
            train_documents = tuple(materialized[index] for index in fold.train_indices)
            validation_documents = tuple(materialized[index] for index in fold.validation_indices)
            feature_pipeline = FeaturePipeline(self.feature_config)
            training_matrix = feature_pipeline.fit_transform(_feature_documents(train_documents))
            validation_matrix = feature_pipeline.transform(_feature_documents(validation_documents))
            model = self.model_factory.create(
                self.experiment_config,
                self.experiment_config.random_seed + fold.fold_index,
            )
            train_labels = np.asarray([document.label for document in train_documents])
            validation_labels = np.asarray([document.label for document in validation_documents])
            training_clock = time.perf_counter()
            model.fit(training_matrix.matrix, train_labels)
            training_time_ms = round((time.perf_counter() - training_clock) * 1000)
            inference_clock = time.perf_counter()
            predicted_labels = model.predict(validation_matrix.matrix)
            scores, probability_scores = _continuous_scores(model, validation_matrix.matrix)
            inference_time_ms = round((time.perf_counter() - inference_clock) * 1000)
            metrics = calculate_metrics(
                validation_labels,
                predicted_labels,
                self.experiment_config.metrics,
                scores,
                probability_scores,
            )
            fold_results.append(
                FoldResult(
                    fold_index=fold.fold_index,
                    train_document_count=len(train_documents),
                    validation_document_count=len(validation_documents),
                    feature_vocabulary_size=training_matrix.vocabulary_size,
                    feature_dimensions={
                        "train_rows": training_matrix.matrix.shape[0],
                        "validation_rows": validation_matrix.matrix.shape[0],
                        "columns": training_matrix.matrix.shape[1],
                    },
                    model_training_time_ms=training_time_ms,
                    inference_time_ms=inference_time_ms,
                    metrics=metrics,
                )
            )
            for source_index, document, prediction_index in zip(
                fold.validation_indices, validation_documents, range(len(validation_documents)), strict=True
            ):
                predictions_with_position.append(
                    (
                        source_index,
                        OutOfFoldPrediction(
                            document_id=document.document_id,
                            fold_index=fold.fold_index,
                            true_label=document.label,
                            predicted_label=int(predicted_labels[prediction_index]),
                            score=(float(scores[prediction_index]) if scores is not None else None),
                        ),
                    )
                )
            fold_artifacts.append((fold.fold_index, model, feature_pipeline.extractor))
            logger.record(
                "cross_validation_fold_completed",
                experiment_id=experiment_id,
                fold_index=fold.fold_index,
                train_document_count=len(train_documents),
                validation_document_count=len(validation_documents),
                feature_vocabulary_size=training_matrix.vocabulary_size,
                model_training_time_ms=training_time_ms,
                inference_time_ms=inference_time_ms,
                macro_f1=metrics.macro_f1,
            )

        predictions = tuple(prediction for _, prediction in sorted(predictions_with_position))
        aggregate_metrics = calculate_metrics(
            [prediction.true_label for prediction in predictions],
            [prediction.predicted_label for prediction in predictions],
            self.experiment_config.metrics,
            [prediction.score for prediction in predictions] if all(prediction.score is not None for prediction in predictions) else None,
            self.experiment_config.model != "linear_svm",
        )
        completed_at = datetime.now(timezone.utc)
        experiment = ExperimentRecord(
            experiment_id=experiment_id,
            status="completed",
            dataset_version=context.dataset_version,
            dataset_hash=context.dataset_hash,
            split_id=context.split_id,
            preprocessing_version=context.preprocessing_version,
            preprocessing_configuration_sha256=context.preprocessing_configuration_sha256,
            feature_engineering_version=self.feature_config.feature_pipeline_version,
            feature_configuration_sha256=self.feature_config.sha256,
            feature_configuration=self.feature_config.to_dict(),
            source_manifest_sha256=source_manifest_sha256,
            model=self.experiment_config.model,
            model_version=self.experiment_config.model_version,
            hyperparameters=dict(self.experiment_config.hyperparameters),
            experiment_configuration_sha256=self.experiment_config.sha256,
            random_seed=self.experiment_config.random_seed,
            deterministic_settings=seed_evidence,
            cross_validation=self.experiment_config.cross_validation.__dict__.copy(),
            started_at=started_at.isoformat(),
            completed_at=completed_at.isoformat(),
            total_training_time_ms=sum(result.model_training_time_ms for result in fold_results),
            total_inference_time_ms=sum(result.inference_time_ms for result in fold_results),
            aggregate_metrics=aggregate_metrics,
            fold_results=tuple(fold_results),
            notes=context.notes,
        )
        registry_record = build_candidate_model_record(experiment, output_directory)
        logger.record(
            "experiment_completed",
            experiment_id=experiment_id,
            model=experiment.model,
            total_duration_ms=round((time.perf_counter() - started_clock) * 1000),
            total_training_time_ms=experiment.total_training_time_ms,
            total_inference_time_ms=experiment.total_inference_time_ms,
            macro_f1=aggregate_metrics.macro_f1,
            weighted_f1=aggregate_metrics.weighted_f1,
            roc_auc=aggregate_metrics.roc_auc,
        )
        artifacts = write_experiment_artifacts(
            output_directory,
            experiment,
            registry_record,
            predictions,
            fold_artifacts,
            logger,
        )
        return experiment, artifacts


def _validate_context(context: ExperimentContext) -> None:
    for name in (
        "dataset_version",
        "split_id",
        "preprocessing_version",
        "preprocessing_configuration_sha256",
    ):
        value = getattr(context, name)
        if not isinstance(value, str) or not value.strip():
            raise ExperimentInputError(f"{name} must be a nonempty string.")
    if not isinstance(context.notes, str):
        raise ExperimentInputError("notes must be a string.")
    if not isinstance(context.dataset_hash, str) or len(context.dataset_hash) != 64:
        raise ExperimentInputError("dataset_hash must be a 64-character SHA-256 string.")
    try:
        int(context.dataset_hash, 16)
    except ValueError as error:
        raise ExperimentInputError("dataset_hash must be a 64-character SHA-256 string.") from error


def _materialize_documents(documents: Iterable[ExperimentDocument]) -> tuple[ExperimentDocument, ...]:
    materialized = tuple(documents)
    if not materialized:
        raise ExperimentInputError("An experiment requires at least one labelled preprocessed document.")
    identifiers = [document.document_id for document in materialized]
    if len(set(identifiers)) != len(identifiers):
        raise ExperimentInputError("Experiment document IDs must be unique.")
    return materialized


def _groups_for_cross_validation(
    documents: Sequence[ExperimentDocument], strategy: str
) -> tuple[str, ...] | None:
    if strategy == "stratified_kfold":
        return None
    return tuple(document.group or "" for document in documents)


def _feature_documents(documents: Sequence[ExperimentDocument]) -> tuple[FeatureDocument, ...]:
    return tuple(
        FeatureDocument(document_id=document.document_id, processed_text=document.processed_text)
        for document in documents
    )


def _continuous_scores(model: ClassifierMixin, matrix) -> tuple[np.ndarray | None, bool]:
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(matrix)
        positive_index = int(np.where(model.classes_ == 1)[0][0])
        return np.asarray(probabilities[:, positive_index]), True
    if hasattr(model, "decision_function"):
        scores = np.asarray(model.decision_function(matrix))
        if scores.ndim == 1:
            return scores, False
        positive_index = int(np.where(model.classes_ == 1)[0][0])
        return scores[:, positive_index], False
    return None, False


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
