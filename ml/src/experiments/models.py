"""Typed records for cross-validated baseline-model experiments."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from experiments.metrics import MetricsResult


@dataclass(frozen=True)
class ExperimentDocument:
    """One approved preprocessed text/label pair for a training-partition experiment."""

    document_id: str
    processed_text: str
    label: int
    group: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.document_id, str) or not self.document_id.strip():
            raise ValueError("Experiment document_id must be a nonempty string.")
        if not isinstance(self.processed_text, str):
            raise TypeError("Experiment processed_text must be a string.")
        if self.label not in {0, 1}:
            raise ValueError("Experiment labels must be binary 0 or 1.")
        if self.group is not None and (not isinstance(self.group, str) or not self.group.strip()):
            raise ValueError("Experiment group must be a nonempty string when supplied.")


@dataclass(frozen=True)
class FoldResult:
    """Metrics and resource evidence for one held-out cross-validation fold."""

    fold_index: int
    train_document_count: int
    validation_document_count: int
    feature_vocabulary_size: int
    feature_dimensions: dict[str, int]
    model_training_time_ms: int
    inference_time_ms: int
    metrics: MetricsResult

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["metrics"] = self.metrics.to_dict()
        return value


@dataclass(frozen=True)
class OutOfFoldPrediction:
    """One held-out prediction, retaining no raw text."""

    document_id: str
    fold_index: int
    true_label: int
    predicted_label: int
    score: float | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExperimentRecord:
    """Immutable evidence for one complete cross-validated baseline experiment."""

    experiment_id: str
    status: str
    dataset_version: str
    dataset_hash: str
    split_id: str
    preprocessing_version: str
    preprocessing_configuration_sha256: str
    feature_engineering_version: str
    feature_configuration_sha256: str
    feature_configuration: dict[str, Any]
    source_manifest_sha256: str
    model: str
    model_version: str
    hyperparameters: dict[str, Any]
    experiment_configuration_sha256: str
    random_seed: int
    deterministic_settings: dict[str, int | str]
    cross_validation: dict[str, Any]
    started_at: str
    completed_at: str
    total_training_time_ms: int
    total_inference_time_ms: int
    aggregate_metrics: MetricsResult
    fold_results: tuple[FoldResult, ...]
    notes: str

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["aggregate_metrics"] = self.aggregate_metrics.to_dict()
        value["fold_results"] = [fold.to_dict() for fold in self.fold_results]
        return value


@dataclass(frozen=True)
class ModelRegistryRecord:
    """Candidate-model registry entry produced from one experiment artifact bundle."""

    model_id: str
    model_version: str
    status: str
    dataset_version: str
    dataset_hash: str
    feature_engineering_version: str
    feature_configuration_sha256: str
    experiment_id: str
    performance_metrics: MetricsResult
    artifact_location: str
    training_date: str
    notes: str

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["performance_metrics"] = self.performance_metrics.to_dict()
        return value
