"""Run orchestration that binds pipeline, validation, artifacts, and run logging."""

from __future__ import annotations

import hashlib
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import spacy

from preprocessing.artifacts import write_run_artifacts
from preprocessing.config import PreprocessingConfig
from preprocessing.models import InputDocument, PreprocessingRun
from preprocessing.pipeline import PreprocessingPipeline
from preprocessing.run_logging import PreprocessingRunLogger
from preprocessing.validation import validate_processing_result


class PreprocessingRunner:
    """Execute an already-authorised derivative input with auditable outputs."""

    def __init__(self, config: PreprocessingConfig) -> None:
        self.pipeline = PreprocessingPipeline(config)

    def run(
        self,
        *,
        run_id: str,
        dataset_version: str,
        source_manifest_path: Path,
        documents: Iterable[InputDocument],
        output_directory: Path,
    ) -> tuple[PreprocessingRun, dict[str, str]]:
        if not run_id.strip() or not dataset_version.strip():
            raise ValueError("run_id and dataset_version must be nonempty.")
        manifest_hash = _sha256_file(source_manifest_path)
        logger = PreprocessingRunLogger()
        started_at = datetime.now(timezone.utc)
        started_clock = time.perf_counter()
        logger.record(
            "preprocessing_started",
            run_id=run_id,
            dataset_version=dataset_version,
            pipeline_version=self.pipeline.config.pipeline_version,
            configuration_sha256=self.pipeline.config.sha256,
            configuration=self.pipeline.config.to_dict(),
            source_manifest_sha256=manifest_hash,
            runtime_model=self.pipeline.runtime.model_identifier,
            model_fallback_used=self.pipeline.runtime.fallback_used,
        )

        result = self.pipeline.process_documents(documents)
        validation = validate_processing_result(result, self.pipeline.config)
        completed_at = datetime.now(timezone.utc)
        duration_ms = round((time.perf_counter() - started_clock) * 1000)
        run = PreprocessingRun(
            run_id=run_id,
            dataset_version=dataset_version,
            pipeline_version=self.pipeline.config.pipeline_version,
            configuration_sha256=self.pipeline.config.sha256,
            configuration=self.pipeline.config.to_dict(),
            source_manifest_sha256=manifest_hash,
            spacy_version=spacy.__version__,
            runtime_model=self.pipeline.runtime.model_identifier,
            model_fallback_used=self.pipeline.runtime.fallback_used,
            started_at=started_at.isoformat(),
            completed_at=completed_at.isoformat(),
            duration_ms=duration_ms,
            attempted_document_count=result.attempted_count,
            processed_document_count=len(result.documents),
            error_count=len(result.failures),
            validation=validation,
        )
        logger.record(
            "preprocessing_completed",
            run_id=run_id,
            dataset_version=dataset_version,
            pipeline_version=self.pipeline.config.pipeline_version,
            configuration_sha256=self.pipeline.config.sha256,
            configuration=self.pipeline.config.to_dict(),
            duration_ms=duration_ms,
            attempted_document_count=result.attempted_count,
            processed_document_count=len(result.documents),
            error_count=len(result.failures),
            failure_summaries=validation.failure_summaries,
            validation_is_valid=validation.is_valid,
            empty_processed_document_count=validation.empty_processed_document_count,
            vocabulary_size=validation.vocabulary_size,
        )
        artifacts = write_run_artifacts(output_directory, run, result, logger)
        return run, artifacts


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
