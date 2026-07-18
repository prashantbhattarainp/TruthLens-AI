"""Typed records shared by feature extractors, validation, and tracking."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from scipy.sparse import csr_matrix


@dataclass(frozen=True)
class FeatureDocument:
    """One preprocessed document supplied to a feature extractor."""

    document_id: str
    processed_text: str

    def __post_init__(self) -> None:
        if not isinstance(self.document_id, str) or not self.document_id.strip():
            raise ValueError("Feature document_id must be a nonempty string.")
        if not isinstance(self.processed_text, str):
            raise TypeError("Feature processed_text must be a string.")


@dataclass(frozen=True)
class FeatureMatrix:
    """A row-aligned sparse feature matrix plus its fitted vocabulary."""

    document_ids: tuple[str, ...]
    matrix: csr_matrix
    feature_names: tuple[str, ...]
    method: str

    def __post_init__(self) -> None:
        if self.matrix.shape != (len(self.document_ids), len(self.feature_names)):
            raise ValueError("Feature matrix dimensions do not match its document IDs and vocabulary.")

    @property
    def vocabulary_size(self) -> int:
        return len(self.feature_names)


@dataclass(frozen=True)
class FeatureValidationReport:
    """Non-destructive checks calculated from one generated feature matrix."""

    is_valid: bool
    document_count: int
    vocabulary_size: int
    feature_dimensions: dict[str, int]
    nonzero_count: int
    density: float
    sparsity: float
    empty_feature_vector_count: int
    empty_feature_vector_rate: float
    matrix_memory_bytes: int
    processing_duration_ms: int
    checks: dict[str, bool]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FeatureExperiment:
    """Immutable metadata for one fitted feature-representation run."""

    experiment_id: str
    dataset_version: str
    split_id: str
    fit_partition: str
    feature_method: str
    feature_pipeline_version: str
    configuration_sha256: str
    configuration: dict[str, Any]
    source_manifest_sha256: str
    created_at: str
    completed_at: str
    processing_duration_ms: int
    notes: str
    validation: FeatureValidationReport

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
