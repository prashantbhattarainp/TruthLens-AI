"""Safe writing of feature matrices and their reproducibility records."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import joblib
from scipy.sparse import save_npz

from features.exceptions import FeatureGovernanceError
from features.models import FeatureExperiment, FeatureMatrix
from features.run_logging import FeatureRunLogger


PROJECT_ROOT = Path(__file__).resolve().parents[3]
RAW_DATA_DIRECTORY = PROJECT_ROOT / "ml" / "data" / "raw"
FEATURE_DATA_DIRECTORY = PROJECT_ROOT / "ml" / "data" / "features"


def assert_not_raw_path(path: Path) -> None:
    """Reject raw-data paths before a feature runner can access an input or manifest."""
    if _is_relative_to(path.resolve(), RAW_DATA_DIRECTORY.resolve()):
        raise FeatureGovernanceError("Feature extraction accepts approved derivatives, never ml/data/raw paths.")


def assert_feature_output_path(path: Path) -> None:
    """Require command-line feature artifacts to remain in the dedicated feature-data area."""
    resolved = path.resolve()
    assert_not_raw_path(resolved)
    if not _is_relative_to(resolved, FEATURE_DATA_DIRECTORY.resolve()):
        raise FeatureGovernanceError(
            "Feature CLI outputs must be written beneath ml/data/features/<dataset-version>/<experiment-id>."
        )


def write_feature_artifacts(
    output_directory: Path,
    experiment: FeatureExperiment,
    feature_matrix: FeatureMatrix,
    extractor: object,
    logger: FeatureRunLogger,
) -> dict[str, str]:
    """Write a new feature run without copying raw text or overwriting prior output."""
    output_directory = output_directory.resolve()
    assert_not_raw_path(output_directory)
    if output_directory.exists():
        raise FeatureGovernanceError(f"Refusing to overwrite existing feature output: {output_directory}")
    output_directory.mkdir(parents=True)

    matrix_path = output_directory / "feature-matrix.npz"
    vocabulary_path = output_directory / "feature-vocabulary.json"
    record_ids_path = output_directory / "feature-record-ids.json"
    config_path = output_directory / "feature-configuration.json"
    validation_path = output_directory / "feature-validation-report.json"
    experiment_path = output_directory / "feature-experiment.json"
    vectorizer_path = output_directory / "fitted-feature-extractor.joblib"
    log_path = output_directory / "feature-run-log.jsonl"
    manifest_path = output_directory / "manifest.json"

    save_npz(matrix_path, feature_matrix.matrix, compressed=True)
    vocabulary_path.write_text(
        json.dumps(list(feature_matrix.feature_names), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    record_ids_path.write_text(
        json.dumps(list(feature_matrix.document_ids), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    config_path.write_text(
        json.dumps(experiment.configuration, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    validation_path.write_text(
        json.dumps(experiment.validation.to_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    experiment_path.write_text(
        json.dumps(experiment.to_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    joblib.dump(extractor, vectorizer_path)
    logger.write_jsonl(log_path)

    manifest: dict[str, Any] = {
        "artifact_type": "feature_extraction_run",
        "experiment_id": experiment.experiment_id,
        "dataset_version": experiment.dataset_version,
        "split_id": experiment.split_id,
        "fit_partition": experiment.fit_partition,
        "feature_method": experiment.feature_method,
        "feature_pipeline_version": experiment.feature_pipeline_version,
        "configuration_sha256": experiment.configuration_sha256,
        "source_manifest_sha256": experiment.source_manifest_sha256,
        "files": {
            matrix_path.name: _sha256_file(matrix_path),
            vocabulary_path.name: _sha256_file(vocabulary_path),
            record_ids_path.name: _sha256_file(record_ids_path),
            config_path.name: _sha256_file(config_path),
            validation_path.name: _sha256_file(validation_path),
            experiment_path.name: _sha256_file(experiment_path),
            vectorizer_path.name: _sha256_file(vectorizer_path),
            log_path.name: _sha256_file(log_path),
        },
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "matrix": str(matrix_path),
        "vocabulary": str(vocabulary_path),
        "record_ids": str(record_ids_path),
        "configuration": str(config_path),
        "validation": str(validation_path),
        "experiment": str(experiment_path),
        "extractor": str(vectorizer_path),
        "log": str(log_path),
        "manifest": str(manifest_path),
    }


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
