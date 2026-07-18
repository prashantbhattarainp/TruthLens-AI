"""Immutable data models used by the preprocessing pipeline."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class InputDocument:
    """A source document supplied by an already-approved derivative input."""

    document_id: str
    text: str


@dataclass(frozen=True)
class ProcessedDocument:
    """A processed representation that never embeds the raw source text."""

    document_id: str
    source_text_sha256: str
    processed_text: str
    tokens: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["tokens"] = list(self.tokens)
        return value


@dataclass(frozen=True)
class ProcessingFailure:
    """A document-level failure retained for audit rather than silently dropped."""

    document_id: str
    error_type: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class ProcessingResult:
    """Ordered result of one batch with successes and retained failures."""

    documents: tuple[ProcessedDocument, ...]
    failures: tuple[ProcessingFailure, ...]
    attempted_count: int


@dataclass(frozen=True)
class ValidationReport:
    """Aggregate validation outcomes for one preprocessing run."""

    is_valid: bool
    processed_document_count: int
    failure_count: int
    empty_processed_document_count: int
    token_statistics: dict[str, int | float]
    vocabulary_size: int
    unexpected_output_counts: dict[str, int]
    failure_summaries: dict[str, int]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PreprocessingRun:
    """Persistable metadata that explains a processed-data artifact."""

    run_id: str
    dataset_version: str
    pipeline_version: str
    configuration_sha256: str
    configuration: dict[str, Any]
    source_manifest_sha256: str
    spacy_version: str
    runtime_model: str
    model_fallback_used: bool
    started_at: str
    completed_at: str
    duration_ms: int
    attempted_document_count: int
    processed_document_count: int
    error_count: int
    validation: ValidationReport

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["validation"] = self.validation.to_dict()
        return value
