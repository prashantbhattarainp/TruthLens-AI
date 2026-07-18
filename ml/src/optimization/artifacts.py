"""Immutable, non-raw artifact writing for Phase 3.9 optimisation runs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import joblib


def write_optimization_artifacts(
    output_directory: Path,
    *,
    result: dict[str, Any],
    search_results: list[dict[str, Any]],
    oof_predictions: list[dict[str, Any]],
    fitted_pipeline: object,
) -> dict[str, str]:
    """Write one new complete bundle without raw text or test predictions."""
    if output_directory.exists():
        raise FileExistsError(f"Refusing to overwrite optimization output: {output_directory}")
    output_directory.mkdir(parents=True)
    result_path = output_directory / "optimization-result.json"
    search_path = output_directory / "search-results.json"
    predictions_path = output_directory / "out-of-fold-predictions.jsonl"
    model_path = output_directory / "fitted-validation-candidate.joblib"
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    search_path.write_text(json.dumps(search_results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    predictions_path.write_text(
        "\n".join(json.dumps(item, ensure_ascii=False) for item in oof_predictions) + "\n", encoding="utf-8"
    )
    joblib.dump(fitted_pipeline, model_path)
    files = [result_path, search_path, predictions_path, model_path]
    manifest_path = output_directory / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "artifact_type": "phase_3_9_hyperparameter_optimization",
                "optimization_id": result["optimization_id"],
                "dataset_version": result["dataset_version"],
                "split_id": result["split_id"],
                "test_access": "none",
                "files": {path.name: _sha256(path) for path in files},
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return {
        "result": str(result_path),
        "search_results": str(search_path),
        "oof_predictions": str(predictions_path),
        "model": str(model_path),
        "manifest": str(manifest_path),
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
