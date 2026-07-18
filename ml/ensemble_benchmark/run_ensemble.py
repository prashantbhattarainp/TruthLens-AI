"""Run the governed Phase 4.3 classical ensemble benchmark.

The runner uses immutable Phase 3.9 component pipelines and their train-only
OOF scores. It evaluates the frozen validation partition only; it does not
generate a protected-test prediction, alter the incumbent, or integrate an
ensemble into the prediction service.

Usage from repository root::

    .\\ml-service\\.venv\\Scripts\\python.exe -m ml.ensemble_benchmark.run_ensemble
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from collections import Counter, defaultdict
from datetime import UTC, datetime
from importlib import metadata
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import psutil
from sklearn.linear_model import LogisticRegression

from ml.transformer_benchmark.metrics import classification_metrics, error_slice_summary

from .protocol import BASE_MODELS, DATASET_SHA256, EnsembleProtocol, protocol_dict


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DERIVATIVE_PATH = REPOSITORY_ROOT / "ml/data/derived/TL-BFNK-EN-v1.0/DER-20260718-r2/split-documents.jsonl"
OPTIMIZATION_ROOT = REPOSITORY_ROOT / "ml/data/optimization/TL-BFNK-EN-v1.0/phase-3-9-r1"
PREPROCESSING_CONFIG = (
    REPOSITORY_ROOT
    / "ml-service/artifacts/candidate/TL-LSVM-TFIDF-v1.1.0-rc.1/preprocessing-configuration.json"
)
DEFAULT_OUTPUT_ROOT = REPOSITORY_ROOT / "ml/data/ensemble-benchmarks"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _git_revision() -> str | None:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=REPOSITORY_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return completed.stdout.strip() if completed.returncode == 0 else None


def _read_validation_only(path: Path) -> tuple[list[dict[str, Any]], dict[str, int]]:
    """Read train/validation records while deliberately excluding test fields.

    The immutable file hash covers the complete derivative. Test rows are only
    counted for split-integrity routing and are never retained, transformed,
    labelled for a model, or sent to a component pipeline.
    """

    actual_hash = _sha256(path)
    if actual_hash != DATASET_SHA256:
        raise ValueError(f"Frozen derivative hash mismatch: expected {DATASET_SHA256}, got {actual_hash}")
    validation: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            partition = row.get("partition")
            counts[str(partition)] += 1
            if partition != "validation":
                continue
            if row.get("label") not in (0, 1):
                raise ValueError(f"Unexpected validation label {row.get('label')!r}")
            validation.append(
                {
                    "document_id": row["document_id"],
                    "raw_text": row["raw_text"],
                    "label": int(row["label"]),
                    "fact_check_source": row.get("fact_check_source") or "unknown",
                }
            )
    expected = {"train": 6813, "validation": 1461, "test": 1458}
    found = {name: counts.get(name, 0) for name in expected}
    if found != expected:
        raise ValueError(f"Frozen split cardinality mismatch: expected {expected}, got {found}")
    return validation, found


def _frozen_preprocessor() -> Any:
    ml_source = REPOSITORY_ROOT / "ml/src"
    if str(ml_source) not in sys.path:
        sys.path.insert(0, str(ml_source))
    from preprocessing import PreprocessingConfig, PreprocessingPipeline  # type: ignore[import-not-found]

    return PreprocessingPipeline(PreprocessingConfig.from_json_file(PREPROCESSING_CONFIG))


def _preprocess_validation(rows: list[dict[str, Any]]) -> list[str]:
    ml_source = REPOSITORY_ROOT / "ml/src"
    if str(ml_source) not in sys.path:
        sys.path.insert(0, str(ml_source))
    from preprocessing import InputDocument  # type: ignore[import-not-found]

    preprocessor = _frozen_preprocessor()
    texts = [
        preprocessor.process_document(InputDocument(document_id=row["document_id"], text=row["raw_text"])).processed_text
        for row in rows
    ]
    if any(not text.strip() for text in texts):
        raise ValueError("Frozen preprocessing produced an empty validation text")
    return texts


def _unit_score(model_key: str, score: np.ndarray) -> np.ndarray:
    """Map only the SVM margin to a bounded meta-feature, never a confidence."""

    values = np.asarray(score, dtype=float)
    if model_key != "linear_svm":
        return values
    clipped = np.clip(values, -35.0, 35.0)
    return 1.0 / (1.0 + np.exp(-clipped))


def _load_oof_scores(model_key: str) -> tuple[dict[str, tuple[int, float]], float, dict[str, Any]]:
    specification = BASE_MODELS[model_key]
    directory = OPTIMIZATION_ROOT / str(specification["optimization_id"])
    result = json.loads((directory / "optimization-result.json").read_text(encoding="utf-8"))
    score_map: dict[str, tuple[int, float]] = {}
    for line in (directory / "out-of-fold-predictions.jsonl").open(encoding="utf-8"):
        row = json.loads(line)
        document_id = str(row["document_id"])
        if document_id in score_map:
            raise ValueError(f"Duplicate OOF record for {model_key}/{document_id}")
        score_map[document_id] = (int(row["true_label"]), float(row["score"]))
    metric = float(result["tuned_cross_validation"]["aggregate_metrics"]["macro_f1"])
    resources = dict(result.get("resources", {}))
    return score_map, metric, resources


def _source_error_summary(rows: list[dict[str, Any]], predictions: np.ndarray) -> dict[str, dict[str, int]]:
    errors: dict[str, Counter[str]] = defaultdict(Counter)
    for row, prediction in zip(rows, predictions, strict=True):
        label = int(row["label"])
        if label == int(prediction):
            continue
        error_type = "false_positive" if label == 0 else "false_negative"
        errors[error_type][str(row["fact_check_source"])] += 1
    return {name: dict(sorted(values.items())) for name, values in errors.items()}


def _evaluate_variant(
    *,
    name: str,
    labels: np.ndarray,
    predictions: np.ndarray,
    scores: np.ndarray,
    rows: list[dict[str, Any]],
    components: list[str],
    score_semantics: str,
    inference_seconds: float,
) -> dict[str, Any]:
    metrics = classification_metrics(labels, predictions, scores)
    metrics["inference_seconds"] = inference_seconds
    metrics["inference_examples_per_second"] = len(labels) / inference_seconds if inference_seconds else None
    error_records = [
        {
            "document_id": row["document_id"],
            "label": row["label"],
            "prediction": int(prediction),
            "raw_text": row["raw_text"],
        }
        for row, prediction in zip(rows, predictions, strict=True)
    ]
    return {
        "name": name,
        "components": components,
        "score_semantics": score_semantics,
        "metrics": metrics,
        "error_analysis": error_slice_summary(error_records),
        "source_error_counts": _source_error_summary(rows, predictions),
    }


def _write_json(path: Path, content: dict[str, Any]) -> None:
    path.write_text(json.dumps(content, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _environment() -> dict[str, Any]:
    packages = ("scikit-learn", "numpy", "joblib", "spacy", "psutil")
    versions: dict[str, str] = {}
    for package in packages:
        try:
            versions[package] = metadata.version(package)
        except metadata.PackageNotFoundError:
            versions[package] = "not_installed"
    memory = psutil.virtual_memory()
    return {
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "logical_cpu_count": psutil.cpu_count(logical=True),
        "memory_total_bytes": memory.total,
        "memory_available_bytes": memory.available,
        "package_versions": versions,
    }


def run(output_root: Path = DEFAULT_OUTPUT_ROOT) -> Path:
    """Build classical ensembles and evaluate their frozen validation evidence."""

    protocol = EnsembleProtocol()
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    output_dir = output_root / f"P43-classical-ensemble-{stamp}"
    output_dir.mkdir(parents=True, exist_ok=False)
    try:
        process = psutil.Process(os.getpid())
        rss_before_load = process.memory_info().rss
        rows, partition_counts = _read_validation_only(DERIVATIVE_PATH)
        labels = np.asarray([row["label"] for row in rows], dtype=int)
        preprocessing_started = time.perf_counter()
        processed_text = _preprocess_validation(rows)
        preprocessing_seconds = time.perf_counter() - preprocessing_started

        pipelines: dict[str, Any] = {}
        component_scores: dict[str, np.ndarray] = {}
        component_predictions: dict[str, np.ndarray] = {}
        component_inference_seconds: dict[str, float] = {}
        component_sizes: dict[str, int] = {}
        oof_maps: dict[str, dict[str, tuple[int, float]]] = {}
        oof_macro_f1: dict[str, float] = {}
        base_resource_records: dict[str, dict[str, Any]] = {}
        for model_key, specification in BASE_MODELS.items():
            directory = OPTIMIZATION_ROOT / str(specification["optimization_id"])
            artifact = directory / "fitted-validation-candidate.joblib"
            pipeline = joblib.load(artifact)
            pipelines[model_key] = pipeline
            component_sizes[model_key] = artifact.stat().st_size
            oof_maps[model_key], oof_macro_f1[model_key], base_resource_records[model_key] = _load_oof_scores(model_key)
            component_started = time.perf_counter()
            component_predictions[model_key] = np.asarray(pipeline.predict(processed_text), dtype=int)
            if model_key == "linear_svm":
                component_scores[model_key] = np.asarray(pipeline.decision_function(processed_text), dtype=float)
            else:
                component_scores[model_key] = np.asarray(pipeline.predict_proba(processed_text)[:, 1], dtype=float)
            component_inference_seconds[model_key] = time.perf_counter() - component_started

        inference_started = time.perf_counter()
        base_variants = {
            model_key: _evaluate_variant(
                name=model_key,
                labels=labels,
                predictions=component_predictions[model_key],
                scores=component_scores[model_key],
                rows=rows,
                components=[model_key],
                score_semantics=str(BASE_MODELS[model_key]["score_type"]),
                inference_seconds=component_inference_seconds[model_key],
            )
            for model_key in BASE_MODELS
        }

        ordered = list(BASE_MODELS)
        prediction_matrix = np.column_stack([component_predictions[name] for name in ordered])
        unit_score_matrix = np.column_stack([_unit_score(name, component_scores[name]) for name in ordered])
        hard_scores = prediction_matrix.mean(axis=1)
        hard_predictions = (prediction_matrix.sum(axis=1) >= 2).astype(int)

        raw_weights = np.asarray([oof_macro_f1[name] for name in ordered], dtype=float)
        weights = raw_weights / raw_weights.sum()
        weighted_scores = prediction_matrix @ weights
        weighted_predictions = (weighted_scores >= 0.5).astype(int)

        probability_components = ["multinomial_naive_bayes", "logistic_regression"]
        soft_scores = np.column_stack([component_scores[name] for name in probability_components]).mean(axis=1)
        soft_predictions = (soft_scores >= 0.5).astype(int)

        common_oof_ids = sorted(set.intersection(*(set(score_map) for score_map in oof_maps.values())))
        if len(common_oof_ids) != 6813:
            raise ValueError(f"Expected 6813 aligned OOF records, found {len(common_oof_ids)}")
        oof_labels = np.asarray([oof_maps[ordered[0]][document_id][0] for document_id in common_oof_ids], dtype=int)
        for model_key in ordered[1:]:
            if any(oof_maps[model_key][document_id][0] != label for document_id, label in zip(common_oof_ids, oof_labels, strict=True)):
                raise ValueError("OOF labels differ between base-model artifacts")
        oof_features = np.column_stack(
            [_unit_score(model_key, np.asarray([oof_maps[model_key][document_id][1] for document_id in common_oof_ids])) for model_key in ordered]
        )
        stacking_started = time.perf_counter()
        stacker = LogisticRegression(C=1.0, solver="lbfgs", max_iter=1000, random_state=protocol.seed)
        stacker.fit(oof_features, oof_labels)
        stacking_training_seconds = time.perf_counter() - stacking_started
        stack_scores = np.asarray(stacker.predict_proba(unit_score_matrix)[:, 1], dtype=float)
        stack_predictions = (stack_scores >= 0.5).astype(int)
        inference_seconds = time.perf_counter() - inference_started

        variants = {
            **base_variants,
            "hard_voting": _evaluate_variant(
                name="hard_voting",
                labels=labels,
                predictions=hard_predictions,
                scores=hard_scores,
                rows=rows,
                components=ordered,
                score_semantics="fraction of component FAKE labels",
                inference_seconds=inference_seconds,
            ),
            "weighted_voting": _evaluate_variant(
                name="weighted_voting",
                labels=labels,
                predictions=weighted_predictions,
                scores=weighted_scores,
                rows=rows,
                components=ordered,
                score_semantics="OOF-Macro-F1-weighted fraction of component FAKE labels",
                inference_seconds=inference_seconds,
            ),
            "soft_voting": _evaluate_variant(
                name="soft_voting",
                labels=labels,
                predictions=soft_predictions,
                scores=soft_scores,
                rows=rows,
                components=probability_components,
                score_semantics="mean component FAKE probability; LinearSVC excluded",
                inference_seconds=inference_seconds,
            ),
            "stacking": _evaluate_variant(
                name="stacking",
                labels=labels,
                predictions=stack_predictions,
                scores=stack_scores,
                rows=rows,
                components=ordered,
                score_semantics="meta Logistic Regression output; not a calibrated production confidence",
                inference_seconds=inference_seconds,
            ),
        }
        stacking_path = output_dir / "stacking-meta-model.joblib"
        joblib.dump(stacker, stacking_path)
        _write_json(
            output_dir / "results.json",
            {
                "status": "evaluated_research_only_validation_only",
                "variants": variants,
                "weights": {name: float(weight) for name, weight in zip(ordered, weights, strict=True)},
                "training": {
                    "base_models": "immutable Phase 3.9 artifacts; no base retraining",
                    "stacking_meta_model_training_seconds": stacking_training_seconds,
                    "stacking_oof_record_count": len(common_oof_ids),
                },
                "resource_analysis": {
                    "component_serialized_size_bytes": component_sizes,
                    "component_resource_records": base_resource_records,
                    "stacking_meta_model_size_bytes": stacking_path.stat().st_size,
                    "process_rss_before_load_bytes": rss_before_load,
                    "process_rss_after_evaluation_bytes": process.memory_info().rss,
                    "validation_preprocessing_seconds": preprocessing_seconds,
                    "component_validation_inference_seconds": component_inference_seconds,
                    "ensemble_aggregation_and_stacking_inference_seconds": inference_seconds,
                },
                "excluded_strategies": {
                    "blending": protocol.blending_status,
                    "classical_transformer_hybrid": protocol.transformer_hybrid_status,
                },
                "protected_test_access": "none",
                "storage_policy": "No raw text, per-document predictions, or validation scores are persisted.",
            },
        )
        _write_json(
            output_dir / "run-manifest.json",
            {
                "schema_version": "1.0.0",
                "status": "evaluated_research_only_validation_only",
                "protocol": protocol_dict(),
                "data": {
                    "derivative_path": str(DERIVATIVE_PATH.resolve()),
                    "sha256": _sha256(DERIVATIVE_PATH),
                    "partition_counts": partition_counts,
                    "evaluated_partition": "validation",
                    "protected_test_access": "none",
                },
                "environment": _environment(),
                "code_revision": _git_revision(),
                "stacking_meta_model": {
                    "path": str(stacking_path.resolve()),
                    "sha256": _sha256(stacking_path),
                },
                "governance": {
                    "champion_replacement": "prohibited automatically",
                    "production_deployment": "prohibited by this benchmark",
                    "transformer_hybrid": "not evaluated because Phase 4.2 produced no transformer prediction artifact",
                },
            },
        )
        return output_dir
    except Exception as exception:
        _write_json(
            output_dir / "run-manifest.json",
            {
                "schema_version": "1.0.0",
                "status": "not_evaluated",
                "protocol": protocol_dict(),
                "failure": {"type": type(exception).__name__, "message": str(exception)},
                "protected_test_access": "none",
            },
        )
        raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    try:
        location = run(arguments.output_root)
    except Exception as error:
        print(f"Ensemble benchmark did not complete: {type(error).__name__}: {error}", file=sys.stderr)
        raise SystemExit(1) from error
    print(f"Ensemble benchmark completed: {location}")
