"""Run orchestration that binds a feature pipeline to validation and provenance artifacts."""

from __future__ import annotations

import hashlib
import time
from collections.abc import Iterable
from datetime import datetime, timezone
from pathlib import Path

from features.artifacts import assert_not_raw_path, write_feature_artifacts
from features.config import FeatureConfig
from features.models import FeatureDocument, FeatureExperiment
from features.pipeline import FeaturePipeline
from features.run_logging import FeatureRunLogger
from features.validation import validate_feature_matrix


class FeatureRunner:
    """Fit one approved training-partition representation and retain its evidence."""

    def __init__(self, config: FeatureConfig) -> None:
        self.pipeline = FeaturePipeline(config)

    def fit_and_write(
        self,
        *,
        experiment_id: str,
        dataset_version: str,
        split_id: str,
        fit_partition: str,
        source_manifest_path: Path,
        documents: Iterable[FeatureDocument],
        notes: str,
        output_directory: Path,
    ) -> tuple[FeatureExperiment, dict[str, str]]:
        """Fit features, validate the matrix, then write one new reproducible artifact bundle."""
        _require_nonempty(
            experiment_id=experiment_id,
            dataset_version=dataset_version,
            split_id=split_id,
            fit_partition=fit_partition,
        )
        if not isinstance(notes, str):
            raise TypeError("notes must be a string.")
        assert_not_raw_path(source_manifest_path)
        assert_not_raw_path(output_directory)
        source_manifest_sha256 = _sha256_file(source_manifest_path)
        logger = FeatureRunLogger()
        started_at = datetime.now(timezone.utc)
        started_clock = time.perf_counter()
        logger.record(
            "feature_extraction_started",
            experiment_id=experiment_id,
            dataset_version=dataset_version,
            split_id=split_id,
            fit_partition=fit_partition,
            feature_method=self.pipeline.config.method,
            feature_pipeline_version=self.pipeline.config.feature_pipeline_version,
            configuration_sha256=self.pipeline.config.sha256,
            configuration=self.pipeline.config.to_dict(),
            source_manifest_sha256=source_manifest_sha256,
        )

        feature_matrix = self.pipeline.fit_transform(documents)
        completed_at = datetime.now(timezone.utc)
        duration_ms = round((time.perf_counter() - started_clock) * 1000)
        validation = validate_feature_matrix(feature_matrix, self.pipeline.config, duration_ms)
        experiment = FeatureExperiment(
            experiment_id=experiment_id,
            dataset_version=dataset_version,
            split_id=split_id,
            fit_partition=fit_partition,
            feature_method=feature_matrix.method,
            feature_pipeline_version=self.pipeline.config.feature_pipeline_version,
            configuration_sha256=self.pipeline.config.sha256,
            configuration=self.pipeline.config.to_dict(),
            source_manifest_sha256=source_manifest_sha256,
            created_at=started_at.isoformat(),
            completed_at=completed_at.isoformat(),
            processing_duration_ms=duration_ms,
            notes=notes,
            validation=validation,
        )
        logger.record(
            "feature_extraction_completed",
            experiment_id=experiment_id,
            dataset_version=dataset_version,
            split_id=split_id,
            fit_partition=fit_partition,
            feature_method=feature_matrix.method,
            configuration_sha256=self.pipeline.config.sha256,
            processing_duration_ms=duration_ms,
            vocabulary_size=validation.vocabulary_size,
            feature_dimensions=validation.feature_dimensions,
            sparsity=validation.sparsity,
            empty_feature_vector_count=validation.empty_feature_vector_count,
            matrix_memory_bytes=validation.matrix_memory_bytes,
            validation_is_valid=validation.is_valid,
        )
        artifacts = write_feature_artifacts(
            output_directory,
            experiment,
            feature_matrix,
            self.pipeline.extractor,
            logger,
        )
        return experiment, artifacts


def _require_nonempty(**values: str) -> None:
    for name, value in values.items():
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must be a nonempty string.")


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
