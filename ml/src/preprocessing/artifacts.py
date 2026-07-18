"""Separate processed-data artifact writing with immutable-raw safeguards."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from preprocessing.exceptions import GovernanceError
from preprocessing.models import PreprocessingRun, ProcessingResult
from preprocessing.run_logging import PreprocessingRunLogger


PROJECT_ROOT = Path(__file__).resolve().parents[3]
RAW_DATA_DIRECTORY = PROJECT_ROOT / "ml" / "data" / "raw"


def write_run_artifacts(
    output_directory: Path,
    run: PreprocessingRun,
    result: ProcessingResult,
    logger: PreprocessingRunLogger,
) -> dict[str, str]:
    """Write JSONL, report, manifest, and logs only to a new processed-data directory."""
    output_directory = output_directory.resolve()
    _assert_separate_from_raw(output_directory)
    if output_directory.exists():
        raise GovernanceError(f"Refusing to overwrite existing preprocessing output: {output_directory}")
    output_directory.mkdir(parents=True)

    documents_path = output_directory / "processed-documents.jsonl"
    failures_path = output_directory / "processing-failures.json"
    run_path = output_directory / "preprocessing-run.json"
    report_path = output_directory / "preprocessing-report.json"
    manifest_path = output_directory / "manifest.json"
    log_path = output_directory / "run-log.jsonl"

    documents_path.write_text(
        "\n".join(json.dumps(document.to_dict(), ensure_ascii=False) for document in result.documents) + "\n",
        encoding="utf-8",
    )
    failures_path.write_text(
        json.dumps([failure.to_dict() for failure in result.failures], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    run_path.write_text(json.dumps(run.to_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_path.write_text(
        json.dumps(run.validation.to_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    logger.write_jsonl(log_path)

    manifest: dict[str, Any] = {
        "artifact_type": "processed_text_run",
        "run_id": run.run_id,
        "dataset_version": run.dataset_version,
        "pipeline_version": run.pipeline_version,
        "configuration_sha256": run.configuration_sha256,
        "source_manifest_sha256": run.source_manifest_sha256,
        "files": {
            documents_path.name: _sha256_file(documents_path),
            failures_path.name: _sha256_file(failures_path),
            run_path.name: _sha256_file(run_path),
            report_path.name: _sha256_file(report_path),
            log_path.name: _sha256_file(log_path),
        },
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {name: str(path) for name, path in {
        "documents": documents_path,
        "failures": failures_path,
        "run": run_path,
        "report": report_path,
        "manifest": manifest_path,
        "log": log_path,
    }.items()}


def assert_not_raw_input(path: Path) -> None:
    """Reject a direct raw-data input path in the command-line entry point."""
    resolved = path.resolve()
    if _is_relative_to(resolved, RAW_DATA_DIRECTORY.resolve()):
        raise GovernanceError("The preprocessing CLI accepts approved derivatives, never ml/data/raw inputs.")


def _assert_separate_from_raw(path: Path) -> None:
    if _is_relative_to(path, RAW_DATA_DIRECTORY.resolve()):
        raise GovernanceError("Processed artifacts must never be written inside ml/data/raw.")


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
