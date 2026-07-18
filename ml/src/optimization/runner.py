"""Grouped-CV search runner using the frozen TruthLens feature protocol."""

from __future__ import annotations

import hashlib
import io
import json
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence

import joblib
import numpy as np
from sklearn.base import ClassifierMixin, clone
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import f1_score, make_scorer
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

from experiments.config import ExperimentConfig
from experiments.cross_validation import CrossValidationFold, build_cross_validation_folds
from experiments.metrics import calculate_metrics
from features.config import FeatureConfig, VectorizerParameters
from models.factory import BaselineModelFactory
from optimization.artifacts import write_optimization_artifacts
from optimization.config import OptimizationConfig


@dataclass(frozen=True)
class OptimizationDocument:
    """A frozen-partition processed record; raw text is never accepted here."""

    document_id: str
    processed_text: str
    label: int
    group: str


@dataclass(frozen=True)
class OptimizationContext:
    """Lineage needed to make one search independently auditable."""

    dataset_version: str
    dataset_hash: str
    split_id: str
    preprocessing_version: str
    preprocessing_configuration_sha256: str
    source_manifest_path: Path
    baseline_experiment_path: Path
    baseline_validation_result_path: Path


class OptimizationRunner:
    """Tune one baseline on training CV, then compare it once on frozen validation."""

    def __init__(
        self,
        optimization_config: OptimizationConfig,
        baseline_config: ExperimentConfig,
        feature_config: FeatureConfig,
        factory: BaselineModelFactory | None = None,
    ) -> None:
        if optimization_config.model != baseline_config.model:
            raise ValueError("Optimization and baseline model configuration must name the same model.")
        if (
            baseline_config.random_seed != optimization_config.random_seed
            or baseline_config.cross_validation.n_splits != optimization_config.n_splits
            or baseline_config.cross_validation.strategy != "stratified_group_kfold"
        ):
            raise ValueError("Optimization must use the frozen grouped five-fold baseline protocol and seed.")
        if feature_config.method != "tfidf":
            raise ValueError("Phase 3.9 optimizes the frozen TF-IDF baseline representation only.")
        self.optimization_config = optimization_config
        self.baseline_config = baseline_config
        self.feature_config = feature_config
        self.factory = factory or BaselineModelFactory()

    def run_and_write(
        self,
        *,
        context: OptimizationContext,
        train_documents: Iterable[OptimizationDocument],
        validation_documents: Iterable[OptimizationDocument],
        output_root: Path,
    ) -> tuple[dict[str, Any], dict[str, str]]:
        """Perform CV search and validation evaluation; test data is deliberately absent."""
        _validate_context(context)
        train, validation = tuple(train_documents), tuple(validation_documents)
        _validate_documents(train, expected_partition="train")
        _validate_documents(validation, expected_partition="validation")
        if set(document.document_id for document in train) & set(document.document_id for document in validation):
            raise ValueError("Training and validation documents must be disjoint.")

        labels = np.asarray([document.label for document in train], dtype=int)
        groups = tuple(document.group for document in train)
        folds = build_cross_validation_folds(
            labels, self.baseline_config.cross_validation, self.optimization_config.random_seed, groups
        )
        optimization_id = _optimization_id(self.optimization_config.model)
        started_at = datetime.now(timezone.utc)
        started = time.perf_counter()
        search = GridSearchCV(
            estimator=self._pipeline(),
            param_grid=_prefixed_grid(self.optimization_config.parameter_grid),
            scoring=make_scorer(f1_score, average="macro", zero_division=0),
            cv=[(fold.train_indices, fold.validation_indices) for fold in folds],
            n_jobs=1,
            refit=True,
            return_train_score=True,
            error_score="raise",
        )
        search.fit([document.processed_text for document in train], labels, groups=groups)
        search_duration_ms = round((time.perf_counter() - started) * 1000)
        fitted_pipeline: Pipeline = search.best_estimator_

        oof_predictions, fold_metrics, fold_resource = self._out_of_fold_predictions(
            fitted_pipeline, train, folds
        )
        oof_labels = [item["true_label"] for item in oof_predictions]
        oof_predicted = [item["predicted_label"] for item in oof_predictions]
        oof_scores = [item["score"] for item in oof_predictions]
        probability_scores = self.optimization_config.model != "linear_svm"
        oof_metrics = calculate_metrics(
            oof_labels, oof_predicted, self.baseline_config.metrics, oof_scores, probability_scores
        ).to_dict()

        train_prediction = _predict(fitted_pipeline, train, self.baseline_config.metrics)
        validation_prediction = _predict(fitted_pipeline, validation, self.baseline_config.metrics)
        baseline_experiment = _read_json(context.baseline_experiment_path)
        baseline_validation = _read_json(context.baseline_validation_result_path)["validation_results"][
            self.optimization_config.model
        ]["metrics"]
        best_params = _unprefix(search.best_params_)
        search_rows = _search_rows(search.cv_results_)
        result: dict[str, Any] = {
            "artifact_type": "phase_3_9_hyperparameter_optimization",
            "optimization_id": optimization_id,
            "dataset_version": context.dataset_version,
            "dataset_hash": context.dataset_hash,
            "split_id": context.split_id,
            "source_manifest_sha256": _sha256(context.source_manifest_path),
            "preprocessing_version": context.preprocessing_version,
            "preprocessing_configuration_sha256": context.preprocessing_configuration_sha256,
            "feature_engineering_version": self.feature_config.feature_pipeline_version,
            "feature_configuration_sha256": self.feature_config.sha256,
            "model": self.optimization_config.model,
            "model_version": self.optimization_config.model_version,
            "random_seed": self.optimization_config.random_seed,
            "cross_validation": {
                "strategy": "stratified_group_kfold",
                "n_splits": self.optimization_config.n_splits,
                "shuffle": True,
                "fit_partition": "train",
            },
            "test_access": "none; the Phase 3.8 protected test result is not reused after tuning",
            "optimization_configuration": self.optimization_config.to_dict(),
            "optimization_configuration_sha256": self.optimization_config.sha256,
            "search_analysis": {
                "strategy": "GridSearchCV",
                "scoring": "macro_f1",
                "configuration_count": self.optimization_config.configuration_count,
                "fit_count": self.optimization_config.configuration_count * self.optimization_config.n_splits,
                "best_parameters": best_params,
                "best_cv_macro_f1": round(float(search.best_score_), 10),
                "best_cv_macro_f1_std": round(float(search.cv_results_["std_test_score"][search.best_index_]), 10),
                "search_duration_ms": search_duration_ms,
                "top_configurations": search_rows[:10],
            },
            "tuned_cross_validation": {
                "aggregate_metrics": oof_metrics,
                "fold_metrics": fold_metrics,
                "mean_fold_training_time_ms": round(float(np.mean(fold_resource["training_time_ms"])), 4),
                "mean_fold_inference_time_ms": round(float(np.mean(fold_resource["inference_time_ms"])), 4),
            },
            "baseline_comparison": {
                "baseline_experiment_id": baseline_experiment["experiment_id"],
                "baseline_cv_metrics": baseline_experiment["aggregate_metrics"],
                "baseline_validation_metrics": baseline_validation,
                "tuned_validation_metrics": validation_prediction["metrics"],
                "validation_metric_delta": _metric_delta(validation_prediction["metrics"], baseline_validation),
                "cv_macro_f1_delta": round(
                    oof_metrics["macro_f1"] - float(baseline_experiment["aggregate_metrics"]["macro_f1"]), 10
                ),
            },
            "overfitting_analysis": {
                "training_metrics": train_prediction["metrics"],
                "validation_metrics": validation_prediction["metrics"],
                "macro_f1_train_validation_gap": round(
                    train_prediction["metrics"]["macro_f1"] - validation_prediction["metrics"]["macro_f1"], 10
                ),
                "cv_macro_f1_standard_deviation": round(
                    float(np.std([fold["metrics"]["macro_f1"] for fold in fold_metrics], ddof=1)), 10
                ),
            },
            "resources": {
                "final_refit_training_time_ms": round(float(search.refit_time_) * 1000),
                "validation_inference_time_ms": validation_prediction["inference_time_ms"],
                "pipeline_serialized_size_bytes": _serialized_size(fitted_pipeline),
                "classifier_estimated_memory_bytes": _estimated_memory(fitted_pipeline.named_steps["classifier"]),
                "feature_vocabulary_size": len(fitted_pipeline.named_steps["tfidf"].get_feature_names_out()),
            },
            "created_at": started_at.isoformat(),
            "completed_at": datetime.now(timezone.utc).isoformat(),
        }
        artifacts = write_optimization_artifacts(
            output_root / optimization_id,
            result=result,
            search_results=search_rows,
            oof_predictions=oof_predictions,
            fitted_pipeline=fitted_pipeline,
        )
        return result, artifacts

    def _pipeline(self) -> Pipeline:
        parameters = VectorizerParameters.from_mapping(self.feature_config.parameters)
        norm = None if parameters.normalization == "none" else parameters.normalization
        vectorizer = TfidfVectorizer(
            analyzer="word",
            tokenizer=str.split,
            token_pattern=None,
            preprocessor=None,
            lowercase=False,
            ngram_range=parameters.ngram_range,
            max_features=parameters.max_features,
            min_df=parameters.min_df,
            max_df=parameters.max_df,
            norm=norm,
            dtype=np.float32,
        )
        classifier = self.factory.create(
            _without_hyperparameters(self.baseline_config), self.optimization_config.random_seed
        )
        return Pipeline((("tfidf", vectorizer), ("classifier", classifier)))

    def _out_of_fold_predictions(
        self,
        fitted_pipeline: Pipeline,
        documents: Sequence[OptimizationDocument],
        folds: Sequence[CrossValidationFold],
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, list[int]]]:
        predictions: list[dict[str, Any]] = []
        fold_metrics: list[dict[str, Any]] = []
        resources: dict[str, list[int]] = {"training_time_ms": [], "inference_time_ms": []}
        for fold in folds:
            candidate = clone(fitted_pipeline)
            train_rows = [documents[index] for index in fold.train_indices]
            fold_validation = [documents[index] for index in fold.validation_indices]
            started = time.perf_counter()
            candidate.fit([row.processed_text for row in train_rows], [row.label for row in train_rows])
            training_time_ms = round((time.perf_counter() - started) * 1000)
            prediction = _predict(candidate, fold_validation, self.baseline_config.metrics)
            resources["training_time_ms"].append(training_time_ms)
            resources["inference_time_ms"].append(prediction["inference_time_ms"])
            fold_metrics.append(
                {
                    "fold_index": fold.fold_index,
                    "train_document_count": len(train_rows),
                    "validation_document_count": len(fold_validation),
                    "metrics": prediction["metrics"],
                    "training_time_ms": training_time_ms,
                    "inference_time_ms": prediction["inference_time_ms"],
                }
            )
            for row, predicted, score in zip(
                fold_validation, prediction["predicted_labels"], prediction["scores"], strict=True
            ):
                predictions.append(
                    {
                        "document_id": row.document_id,
                        "fold_index": fold.fold_index,
                        "true_label": row.label,
                        "predicted_label": int(predicted),
                        "score": float(score),
                    }
                )
        return sorted(predictions, key=lambda item: item["document_id"]), fold_metrics, resources


def _predict(pipeline: Pipeline, documents: Sequence[OptimizationDocument], settings) -> dict[str, Any]:
    texts, labels = [row.processed_text for row in documents], [row.label for row in documents]
    started = time.perf_counter()
    predicted = np.asarray(pipeline.predict(texts), dtype=int)
    scores, probability_scores = _continuous_scores(pipeline, texts)
    inference_time_ms = round((time.perf_counter() - started) * 1000)
    return {
        "metrics": calculate_metrics(labels, predicted, settings, scores, probability_scores).to_dict(),
        "predicted_labels": predicted.tolist(),
        "scores": scores.astype(float).tolist(),
        "inference_time_ms": inference_time_ms,
        "training_time_ms": 0,
    }


def _continuous_scores(pipeline: Pipeline, texts: Sequence[str]) -> tuple[np.ndarray, bool]:
    classifier: ClassifierMixin = pipeline.named_steps["classifier"]
    matrix = pipeline.named_steps["tfidf"].transform(texts)
    if hasattr(classifier, "predict_proba"):
        probabilities = classifier.predict_proba(matrix)
        index = int(np.where(classifier.classes_ == 1)[0][0])
        return np.asarray(probabilities[:, index]), True
    scores = np.asarray(classifier.decision_function(matrix))
    if scores.ndim == 1:
        return scores, False
    index = int(np.where(classifier.classes_ == 1)[0][0])
    return scores[:, index], False


def _prefixed_grid(grid: Sequence[dict[str, Sequence[Any]]]) -> list[dict[str, Sequence[Any]]]:
    return [{f"classifier__{key}": values for key, values in branch.items()} for branch in grid]


def _unprefix(parameters: dict[str, Any]) -> dict[str, Any]:
    return {key.removeprefix("classifier__"): value for key, value in parameters.items()}


def _search_rows(cv_results: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for index, parameters in enumerate(cv_results["params"]):
        rows.append(
            {
                "rank": int(cv_results["rank_test_score"][index]),
                "parameters": _unprefix(parameters),
                "mean_cv_macro_f1": round(float(cv_results["mean_test_score"][index]), 10),
                "std_cv_macro_f1": round(float(cv_results["std_test_score"][index]), 10),
                "mean_train_macro_f1": round(float(cv_results["mean_train_score"][index]), 10),
                "mean_fit_time_seconds": round(float(cv_results["mean_fit_time"][index]), 6),
            }
        )
    return sorted(rows, key=lambda row: (row["rank"], json.dumps(row["parameters"], sort_keys=True, default=str)))


def _metric_delta(tuned: dict[str, Any], baseline: dict[str, Any]) -> dict[str, float | None]:
    return {
        key: (round(float(tuned[key]) - float(baseline[key]), 10) if tuned.get(key) is not None and baseline.get(key) is not None else None)
        for key in (
            "accuracy", "precision", "recall", "macro_precision", "macro_recall", "macro_f1",
            "weighted_precision", "weighted_recall", "weighted_f1", "balanced_accuracy", "roc_auc",
            "pr_auc", "log_loss", "matthews_correlation_coefficient", "cohen_kappa",
        )
    }


def _without_hyperparameters(config: ExperimentConfig) -> ExperimentConfig:
    return ExperimentConfig(
        experiment_framework_version=config.experiment_framework_version,
        model=config.model,
        model_version=config.model_version,
        hyperparameters={},
        cross_validation=config.cross_validation,
        random_seed=config.random_seed,
        metrics=config.metrics,
    )


def _validate_context(context: OptimizationContext) -> None:
    if len(context.dataset_hash) != 64 or any(character not in "0123456789abcdef" for character in context.dataset_hash):
        raise ValueError("dataset_hash must be a lowercase SHA-256 value.")
    for path in (context.source_manifest_path, context.baseline_experiment_path, context.baseline_validation_result_path):
        if not path.exists():
            raise FileNotFoundError(path)


def _validate_documents(documents: Sequence[OptimizationDocument], *, expected_partition: str) -> None:
    if not documents:
        raise ValueError(f"The {expected_partition} partition is empty.")
    identifiers = [document.document_id for document in documents]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError(f"Duplicate document IDs in {expected_partition} partition.")
    if any(document.label not in {0, 1} or not document.group.strip() for document in documents):
        raise ValueError("Optimization documents require binary labels and non-empty duplicate groups.")


def _optimization_id(model: str) -> str:
    return f"OPT-{datetime.now(timezone.utc):%Y%m%d}-{model.replace('_', '-')}-{uuid.uuid4().hex[:10]}"


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _serialized_size(value: object) -> int:
    buffer = io.BytesIO()
    joblib.dump(value, buffer)
    return buffer.tell()


def _estimated_memory(model: object) -> int:
    total = 0
    for value in vars(model).values():
        if isinstance(value, np.ndarray):
            total += int(value.nbytes)
        elif hasattr(value, "data") and hasattr(value, "indices") and hasattr(value, "indptr"):
            total += int(value.data.nbytes + value.indices.nbytes + value.indptr.nbytes)
    return total
