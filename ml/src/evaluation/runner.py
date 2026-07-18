"""Validation-led candidate selection and a single protected test evaluation."""

from __future__ import annotations

import io
import json
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence

import joblib
import numpy as np
from sklearn.base import ClassifierMixin

from experiments.config import ExperimentConfig
from experiments.metrics import MetricsResult, calculate_metrics
from features.config import FeatureConfig
from features.models import FeatureDocument
from features.pipeline import FeaturePipeline
from models.factory import BaselineModelFactory


@dataclass(frozen=True)
class EvaluationDocument:
    """A processed, labelled record with only non-text audit metadata."""

    document_id: str
    processed_text: str
    label: int
    duplicate_cluster_id: str
    partition: str
    source: str | None
    raw_character_count: int


@dataclass(frozen=True)
class _FittedCandidate:
    config: ExperimentConfig
    pipeline: FeaturePipeline
    model: ClassifierMixin
    training_time_ms: int
    model_size_bytes: int
    estimated_memory_bytes: int


class BaselineEvaluationRunner:
    """Evaluate registered baselines without accessing raw text or test data early."""

    def __init__(self, feature_config: FeatureConfig, factory: BaselineModelFactory | None = None) -> None:
        self.feature_config = feature_config
        self.factory = factory or BaselineModelFactory()

    def run_and_write(
        self,
        *,
        configs: Sequence[ExperimentConfig],
        train: Iterable[EvaluationDocument],
        validation: Iterable[EvaluationDocument],
        test: Iterable[EvaluationDocument],
        dataset_version: str,
        split_id: str,
        output_directory: Path,
    ) -> dict[str, Any]:
        """Select on validation Macro F1, then use test once for the selected candidate."""
        train_rows, validation_rows, test_rows = tuple(train), tuple(validation), tuple(test)
        _validate_partitions(train_rows, validation_rows, test_rows)
        if output_directory.exists():
            raise FileExistsError(f"Refusing to overwrite evaluation output: {output_directory}")
        output_directory.mkdir(parents=True)

        candidates: dict[str, _FittedCandidate] = {}
        validation_results: dict[str, dict[str, Any]] = {}
        curve_payload: dict[str, dict[str, list[float] | list[int] | bool]] = {}
        for config in configs:
            candidate = self._fit(config, train_rows)
            prediction = self._predict(candidate, validation_rows)
            candidates[config.model] = candidate
            validation_results[config.model] = {
                "model": config.model,
                "model_version": config.model_version,
                "hyperparameters": config.hyperparameters,
                "metrics": prediction["metrics"].to_dict(),
                "training_time_ms": candidate.training_time_ms,
                "inference_time_ms": prediction["inference_time_ms"],
                "model_size_bytes": candidate.model_size_bytes,
                "estimated_memory_bytes": candidate.estimated_memory_bytes,
                "feature_vocabulary_size": len(candidate.pipeline.extractor.feature_names),
            }
            curve_payload[config.model] = prediction["curve"]

        selected_model = sorted(
            validation_results,
            key=lambda name: (-validation_results[name]["metrics"]["macro_f1"], name),
        )[0]
        selected_config = candidates[selected_model].config
        final_candidate = self._fit(selected_config, (*train_rows, *validation_rows))
        test_prediction = self._predict(final_candidate, test_rows)
        model_path = output_directory / "selected-model.joblib"
        extractor_path = output_directory / "selected-feature-extractor.joblib"
        joblib.dump(final_candidate.model, model_path)
        joblib.dump(final_candidate.pipeline.extractor, extractor_path)

        feature_importance = {
            name: _feature_importance(candidate) for name, candidate in candidates.items()
            if name in {"logistic_regression", "linear_svm"}
        }
        errors = _error_analysis(test_rows, test_prediction["predicted_labels"])
        result: dict[str, Any] = {
            "artifact_type": "phase_3_8_baseline_evaluation",
            "dataset_version": dataset_version,
            "split_id": split_id,
            "selection_rule": "highest validation macro_f1; lexical model-name tie-break only",
            "test_access": "single protected test evaluation after validation selection",
            "validation_results": validation_results,
            "selected_model": {
                "model": selected_model,
                "model_version": selected_config.model_version,
                "selection_metric": "macro_f1",
                "validation_macro_f1": validation_results[selected_model]["metrics"]["macro_f1"],
                "train_validation_refit_document_count": len(train_rows) + len(validation_rows),
                "test_result": {
                    "metrics": test_prediction["metrics"].to_dict(),
                    "training_time_ms": final_candidate.training_time_ms,
                    "inference_time_ms": test_prediction["inference_time_ms"],
                    "model_size_bytes": _serialized_size(final_candidate.model),
                    "estimated_memory_bytes": _estimated_memory(final_candidate.model),
                    "feature_vocabulary_size": len(final_candidate.pipeline.extractor.feature_names),
                    "model_artifact": str(model_path),
                    "extractor_artifact": str(extractor_path),
                },
            },
            "validation_curve_data": curve_payload,
            "test_curve_data": test_prediction["curve"],
            "feature_importance": feature_importance,
            "error_analysis": errors,
        }
        (output_directory / "evaluation-result.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (output_directory / "selected-test-errors.json").write_text(
            json.dumps(errors["misclassifications"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        return result

    def _fit(self, config: ExperimentConfig, rows: Sequence[EvaluationDocument]) -> _FittedCandidate:
        pipeline = FeaturePipeline(self.feature_config)
        matrix = pipeline.fit_transform(_feature_documents(rows))
        model = self.factory.create(config, config.random_seed)
        started = time.perf_counter()
        model.fit(matrix.matrix, np.asarray([row.label for row in rows]))
        return _FittedCandidate(
            config=config,
            pipeline=pipeline,
            model=model,
            training_time_ms=round((time.perf_counter() - started) * 1000),
            model_size_bytes=_serialized_size(model),
            estimated_memory_bytes=_estimated_memory(model),
        )

    def _predict(self, candidate: _FittedCandidate, rows: Sequence[EvaluationDocument]) -> dict[str, Any]:
        matrix = candidate.pipeline.transform(_feature_documents(rows))
        started = time.perf_counter()
        predicted = np.asarray(candidate.model.predict(matrix.matrix), dtype=int)
        scores, probabilities = _continuous_scores(candidate.model, matrix.matrix)
        elapsed = round((time.perf_counter() - started) * 1000)
        labels = np.asarray([row.label for row in rows], dtype=int)
        metrics = calculate_metrics(labels, predicted, candidate.config.metrics, scores, probabilities)
        return {
            "metrics": metrics,
            "predicted_labels": predicted,
            "inference_time_ms": elapsed,
            "curve": {
                "true_labels": labels.astype(int).tolist(),
                "scores": scores.astype(float).tolist() if scores is not None else [],
                "probability_scores": probabilities,
            },
        }


def _feature_documents(rows: Sequence[EvaluationDocument]) -> tuple[FeatureDocument, ...]:
    return tuple(FeatureDocument(document_id=row.document_id, processed_text=row.processed_text) for row in rows)


def _validate_partitions(
    train: Sequence[EvaluationDocument], validation: Sequence[EvaluationDocument], test: Sequence[EvaluationDocument]
) -> None:
    expected = (("train", train), ("validation", validation), ("test", test))
    all_rows = (*train, *validation, *test)
    if any(not rows or any(row.partition != name for row in rows) for name, rows in expected):
        raise ValueError("Each nonempty input must contain only its declared frozen partition.")
    ids = [row.document_id for row in all_rows]
    if len(ids) != len(set(ids)):
        raise ValueError("A document appears in more than one partition.")
    group_partitions: dict[str, set[str]] = defaultdict(set)
    for row in all_rows:
        group_partitions[row.duplicate_cluster_id].add(row.partition)
    if any(len(partitions) > 1 for partitions in group_partitions.values()):
        raise ValueError("A duplicate group crosses a frozen partition.")


def _continuous_scores(model: ClassifierMixin, matrix) -> tuple[np.ndarray | None, bool]:
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(matrix)
        positive_index = int(np.where(model.classes_ == 1)[0][0])
        return np.asarray(probabilities[:, positive_index]), True
    if hasattr(model, "decision_function"):
        scores = np.asarray(model.decision_function(matrix))
        return (scores if scores.ndim == 1 else scores[:, int(np.where(model.classes_ == 1)[0][0])]), False
    return None, False


def _serialized_size(model: ClassifierMixin) -> int:
    buffer = io.BytesIO()
    joblib.dump(model, buffer)
    return buffer.tell()


def _estimated_memory(model: ClassifierMixin) -> int:
    total = 0
    for value in vars(model).values():
        if isinstance(value, np.ndarray):
            total += int(value.nbytes)
        elif hasattr(value, "data") and hasattr(value, "indices") and hasattr(value, "indptr"):
            total += int(value.data.nbytes + value.indices.nbytes + value.indptr.nbytes)
    return total


def _feature_importance(candidate: _FittedCandidate, limit: int = 20) -> dict[str, list[dict[str, float | str]]]:
    coefficients = getattr(candidate.model, "coef_", None)
    if coefficients is None:
        return {}
    names = candidate.pipeline.extractor.feature_names
    values = np.asarray(coefficients).reshape(-1)
    positive = np.argsort(values)[-limit:][::-1]
    negative = np.argsort(values)[:limit]
    return {
        "fake_indicative": [{"feature": names[index], "weight": round(float(values[index]), 8)} for index in positive],
        "real_indicative": [{"feature": names[index], "weight": round(float(values[index]), 8)} for index in negative],
    }


def _error_analysis(rows: Sequence[EvaluationDocument], predicted: np.ndarray) -> dict[str, Any]:
    totals: dict[str, Counter[str]] = defaultdict(Counter)
    errors: list[dict[str, Any]] = []
    for row, predicted_label in zip(rows, predicted, strict=True):
        bucket = _length_bucket(row.raw_character_count)
        correct = int(predicted_label) == row.label
        totals[f"source:{row.source or 'Unknown'}"]["correct" if correct else "error"] += 1
        totals[f"length:{bucket}"]["correct" if correct else "error"] += 1
        totals[f"class:{'FAKE' if row.label else 'REAL'}"]["correct" if correct else "error"] += 1
        if not correct:
            errors.append(
                {
                    "document_id": row.document_id,
                    "true_label": "FAKE" if row.label else "REAL",
                    "predicted_label": "FAKE" if predicted_label else "REAL",
                    "source": row.source,
                    "raw_character_count": row.raw_character_count,
                    "length_bucket": bucket,
                }
            )
    return {
        "total_errors": len(errors),
        "error_rates": {
            key: {
                "count": values["correct"] + values["error"],
                "errors": values["error"],
                "error_rate": round(values["error"] / (values["correct"] + values["error"]), 8),
            }
            for key, values in sorted(totals.items())
        },
        "misclassifications": errors,
    }


def _length_bucket(characters: int) -> str:
    if characters < 500:
        return "<500"
    if characters < 1500:
        return "500-1499"
    if characters < 3000:
        return "1500-2999"
    return "3000+"
