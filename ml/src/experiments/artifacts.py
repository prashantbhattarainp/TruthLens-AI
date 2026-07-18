"""Safe writing of model-experiment artifacts outside immutable raw data."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import joblib
from PIL import Image, ImageDraw, ImageFont

from experiments.exceptions import ExperimentGovernanceError
from experiments.models import ExperimentRecord, ModelRegistryRecord, OutOfFoldPrediction
from experiments.registry import build_experiment_registry_entry
from experiments.tracking import ExperimentRunLogger


PROJECT_ROOT = Path(__file__).resolve().parents[3]
RAW_DATA_DIRECTORY = PROJECT_ROOT / "ml" / "data" / "raw"
EXPERIMENT_DATA_DIRECTORY = PROJECT_ROOT / "ml" / "data" / "experiments"


def assert_not_raw_path(path: Path) -> None:
    """Reject raw paths before an experiment can use an input manifest or write artifacts."""
    if _is_relative_to(path.resolve(), RAW_DATA_DIRECTORY.resolve()):
        raise ExperimentGovernanceError("Experiments accept approved derivatives, never ml/data/raw paths.")


def assert_experiment_output_path(path: Path) -> None:
    """Require CLI-created experiment bundles to stay in the dedicated data area."""
    resolved = path.resolve()
    assert_not_raw_path(resolved)
    if not _is_relative_to(resolved, EXPERIMENT_DATA_DIRECTORY.resolve()):
        raise ExperimentGovernanceError(
            "Experiment CLI outputs must be written beneath ml/data/experiments/<dataset-version>/<experiment-id>."
        )


def write_experiment_artifacts(
    output_directory: Path,
    experiment: ExperimentRecord,
    model_registry: ModelRegistryRecord,
    predictions: Sequence[OutOfFoldPrediction],
    fold_artifacts: Sequence[tuple[int, object, object]],
    logger: ExperimentRunLogger,
) -> dict[str, str]:
    """Write one immutable candidate bundle without copying raw or preprocessed input text."""
    output_directory = output_directory.resolve()
    assert_not_raw_path(output_directory)
    if output_directory.exists():
        raise ExperimentGovernanceError(f"Refusing to overwrite existing experiment output: {output_directory}")
    output_directory.mkdir(parents=True)
    folds_directory = output_directory / "folds"
    folds_directory.mkdir()

    experiment_path = output_directory / "experiment-record.json"
    config_path = output_directory / "config.json"
    metrics_path = output_directory / "metrics.json"
    cv_path = output_directory / "cross-validation-results.json"
    classification_report_path = output_directory / "classification_report.json"
    confusion_matrix_json_path = output_directory / "confusion_matrix.json"
    confusion_matrix_png_path = output_directory / "confusion_matrix.png"
    notes_path = output_directory / "notes.md"
    prediction_path = output_directory / "out-of-fold-predictions.jsonl"
    feature_configuration_path = output_directory / "feature-configuration.json"
    model_configuration_path = output_directory / "model-configuration.json"
    registry_path = output_directory / "model-registry-record.json"
    experiment_registry_path = output_directory / "experiment-registry-entry.json"
    log_path = output_directory / "experiment-log.jsonl"
    manifest_path = output_directory / "manifest.json"

    experiment_path.write_text(
        json.dumps(experiment.to_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    config_path.write_text(
        json.dumps(
            {
                "dataset_version": experiment.dataset_version,
                "dataset_hash": experiment.dataset_hash,
                "split_id": experiment.split_id,
                "preprocessing_version": experiment.preprocessing_version,
                "preprocessing_configuration_sha256": experiment.preprocessing_configuration_sha256,
                "feature_engineering_version": experiment.feature_engineering_version,
                "feature_configuration_sha256": experiment.feature_configuration_sha256,
                "feature_configuration": experiment.feature_configuration,
                "model": experiment.model,
                "model_version": experiment.model_version,
                "hyperparameters": experiment.hyperparameters,
                "experiment_configuration_sha256": experiment.experiment_configuration_sha256,
                "random_seed": experiment.random_seed,
                "cross_validation": experiment.cross_validation,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    metrics_path.write_text(
        json.dumps(
            {
                "primary_metric": "macro_f1",
                "aggregate_metrics": experiment.aggregate_metrics.to_dict(),
                "total_training_time_ms": experiment.total_training_time_ms,
                "total_inference_time_ms": experiment.total_inference_time_ms,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    cv_path.write_text(
        json.dumps(
            {
                "aggregate_metrics": experiment.aggregate_metrics.to_dict(),
                "fold_results": [fold.to_dict() for fold in experiment.fold_results],
                "total_training_time_ms": experiment.total_training_time_ms,
                "total_inference_time_ms": experiment.total_inference_time_ms,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    classification_report_path.write_text(
        json.dumps(experiment.aggregate_metrics.classification_report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    confusion_matrix_json_path.write_text(
        json.dumps(experiment.aggregate_metrics.confusion_matrix, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    _write_confusion_matrix_png(experiment.aggregate_metrics.confusion_matrix, confusion_matrix_png_path)
    notes_path.write_text(f"# Experiment Notes\n\n{experiment.notes.strip()}\n", encoding="utf-8")
    prediction_path.write_text(
        "\n".join(json.dumps(prediction.to_dict(), ensure_ascii=False) for prediction in predictions) + "\n",
        encoding="utf-8",
    )
    feature_configuration_path.write_text(
        json.dumps(experiment.feature_configuration, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    model_configuration_path.write_text(
        json.dumps(
            {
                "model": experiment.model,
                "model_version": experiment.model_version,
                "hyperparameters": experiment.hyperparameters,
                "experiment_configuration_sha256": experiment.experiment_configuration_sha256,
                "random_seed": experiment.random_seed,
                "cross_validation": experiment.cross_validation,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    registry_path.write_text(
        json.dumps(model_registry.to_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    experiment_registry_path.write_text(
        json.dumps(
            build_experiment_registry_entry(experiment, output_directory).to_dict(),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    for fold_index, model, extractor in fold_artifacts:
        joblib.dump(model, folds_directory / f"fold-{fold_index}-model.joblib")
        joblib.dump(extractor, folds_directory / f"fold-{fold_index}-feature-extractor.joblib")
    logger.write_jsonl(log_path)

    artifact_paths = [
        experiment_path,
        config_path,
        metrics_path,
        cv_path,
        classification_report_path,
        confusion_matrix_json_path,
        confusion_matrix_png_path,
        notes_path,
        prediction_path,
        feature_configuration_path,
        model_configuration_path,
        registry_path,
        experiment_registry_path,
        log_path,
        *sorted(folds_directory.glob("*.joblib")),
    ]
    manifest: dict[str, Any] = {
        "artifact_type": "baseline_model_experiment",
        "experiment_id": experiment.experiment_id,
        "dataset_version": experiment.dataset_version,
        "dataset_hash": experiment.dataset_hash,
        "split_id": experiment.split_id,
        "model": experiment.model,
        "model_version": experiment.model_version,
        "experiment_configuration_sha256": experiment.experiment_configuration_sha256,
        "feature_configuration_sha256": experiment.feature_configuration_sha256,
        "source_manifest_sha256": experiment.source_manifest_sha256,
        "files": {
            str(path.relative_to(output_directory)): _sha256_file(path) for path in artifact_paths
        },
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "experiment": str(experiment_path),
        "config": str(config_path),
        "metrics": str(metrics_path),
        "cross_validation": str(cv_path),
        "classification_report": str(classification_report_path),
        "confusion_matrix": str(confusion_matrix_png_path),
        "notes": str(notes_path),
        "predictions": str(prediction_path),
        "feature_configuration": str(feature_configuration_path),
        "model_configuration": str(model_configuration_path),
        "model_registry": str(registry_path),
        "experiment_registry": str(experiment_registry_path),
        "folds": str(folds_directory),
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


def _write_confusion_matrix_png(matrix: list[list[int]], path: Path) -> None:
    """Render a dependency-managed two-class confusion-matrix heatmap as a portable PNG."""
    image = Image.new("RGB", (720, 560), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    title_font = ImageFont.load_default()
    left, top, cell = 210, 150, 180
    maximum = max(max(row) for row in matrix) or 1
    labels = ("REAL", "FAKE")

    _draw_centered_text(draw, "Confusion Matrix", 360, 42, title_font, "#172033")
    _draw_centered_text(draw, "Predicted label", 390, 102, font, "#172033")
    _draw_centered_text(draw, "True label", 70, 330, font, "#172033")
    for index, label in enumerate(labels):
        _draw_centered_text(draw, label, left + cell * index + cell // 2, top - 24, font, "#172033")
        _draw_centered_text(draw, label, left - 54, top + cell * index + cell // 2, font, "#172033")
    for row_index, row in enumerate(matrix):
        for column_index, value in enumerate(row):
            intensity = value / maximum
            color = (
                int(235 - 155 * intensity),
                int(244 - 110 * intensity),
                int(255 - 35 * intensity),
            )
            x0, y0 = left + column_index * cell, top + row_index * cell
            draw.rectangle((x0, y0, x0 + cell, y0 + cell), fill=color, outline="#3b5575", width=2)
            text_color = "white" if intensity > 0.62 else "#172033"
            _draw_centered_text(draw, str(value), x0 + cell // 2, y0 + cell // 2, font, text_color)
    image.save(path, format="PNG")


def _draw_centered_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    center_x: int,
    center_y: int,
    font: ImageFont.ImageFont,
    fill: str,
) -> None:
    bounding_box = draw.textbbox((0, 0), text, font=font)
    width, height = bounding_box[2] - bounding_box[0], bounding_box[3] - bounding_box[1]
    draw.text((center_x - width // 2, center_y - height // 2), text, font=font, fill=fill)
