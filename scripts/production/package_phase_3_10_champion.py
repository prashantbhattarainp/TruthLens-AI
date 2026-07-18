"""Create an immutable, versioned internal-service package for the Phase 3.9 champion.

This is a packaging operation only: it neither reads raw data nor trains, evaluates, or
reselects a model. The package is intentionally marked as integration-only because the
candidate has not received a post-tuning protected-test evaluation.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import joblib


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_VERSION = "TL-LSVM-TFIDF-v1.1.0-rc.1"
DATASET_VERSION = "TL-BFNK-EN-v1.0"
OPTIMIZATION_ID = "OPT-20260718-linear-svm-faafafe15e"
SOURCE_ROOT = PROJECT_ROOT / "ml" / "data" / "optimization" / DATASET_VERSION / "phase-3-9-r1" / OPTIMIZATION_ID
PACKAGE_DIRECTORY = PROJECT_ROOT / "ml-service" / "artifacts" / "candidate" / MODEL_VERSION


def main() -> None:
    if PACKAGE_DIRECTORY.exists():
        raise FileExistsError(f"Refusing to overwrite existing model package: {PACKAGE_DIRECTORY}")
    optimization = _read_json(SOURCE_ROOT / "optimization-result.json")
    pipeline = joblib.load(SOURCE_ROOT / "fitted-validation-candidate.joblib")
    if set(pipeline.named_steps) != {"tfidf", "classifier"}:
        raise ValueError("Champion artifact does not contain the expected TF-IDF and classifier steps.")

    PACKAGE_DIRECTORY.mkdir(parents=True)
    pipeline_path = PACKAGE_DIRECTORY / "model-pipeline.joblib"
    vectorizer_path = PACKAGE_DIRECTORY / "vectorizer.joblib"
    classifier_path = PACKAGE_DIRECTORY / "classifier.joblib"
    joblib.dump(pipeline, pipeline_path)
    joblib.dump(pipeline.named_steps["tfidf"], vectorizer_path)
    joblib.dump(pipeline.named_steps["classifier"], classifier_path)

    _write_json(PACKAGE_DIRECTORY / "label-mapping.json", {
        "mapping_id": "LMAP-BFNK-v1.0",
        "labels": {"0": "REAL", "1": "FAKE"},
        "positive_class": "FAKE",
        "label_encoder": "not_applicable; fixed binary mapping",
    })
    _copy_json(PROJECT_ROOT / "ml" / "config" / "features" / "tfidf-unigram-bigram-v1.json", PACKAGE_DIRECTORY / "feature-configuration.json")
    _copy_json(PROJECT_ROOT / "ml" / "config" / "preprocessing" / "conservative-en-v1.json", PACKAGE_DIRECTORY / "preprocessing-configuration.json")

    metrics = optimization["baseline_comparison"]["tuned_validation_metrics"]
    metadata = {
        "artifact_type": "truthlens_internal_model_package",
        "package_version": "1.0.0",
        "model_name": "TruthLens Linear SVM conditional research champion",
        "model_version": MODEL_VERSION,
        "deployment_status": "integrated_not_deployment_approved",
        "dataset_version": optimization["dataset_version"],
        "dataset_hash": optimization["dataset_hash"],
        "derivative_release": "DER-20260718-r2",
        "split_id": optimization["split_id"],
        "feature_engineering_version": optimization["feature_engineering_version"],
        "feature_configuration_sha256": optimization["feature_configuration_sha256"],
        "preprocessing_version": optimization["preprocessing_version"],
        "preprocessing_configuration_sha256": optimization["preprocessing_configuration_sha256"],
        "training_timestamp": optimization["completed_at"],
        "experiment_id": optimization["baseline_comparison"]["baseline_experiment_id"],
        "optimization_id": optimization["optimization_id"],
        "source_artifact_sha256": _sha256(SOURCE_ROOT / "fitted-validation-candidate.joblib"),
        "metrics_summary": {
            "validation_macro_f1": metrics["macro_f1"],
            "validation_mcc": metrics["matthews_correlation_coefficient"],
            "validation_fake_recall": metrics["recall"],
        },
        "prediction_contract": {
            "input_text_composition": "headline + \\n\\n + article",
            "confidence": "unavailable; LinearSVC decision scores are not calibrated probabilities",
            "label_mapping": "0=REAL, 1=FAKE",
        },
        "limitations": [
            "Untested after tuning; no protected-test evidence may be reused.",
            "Not approved for deployment, fact checking, factual verdicts, or calibrated confidence claims.",
            "English BFNK-derived research scope only; source/template sensitivity remains a material risk.",
            "Underlying dataset is CC BY-NC 4.0; licence and downstream content-rights boundaries apply.",
        ],
        "packaged_at": datetime.now(timezone.utc).isoformat(),
    }
    _write_json(PACKAGE_DIRECTORY / "model-metadata.json", metadata)
    package_files = [
        pipeline_path,
        vectorizer_path,
        classifier_path,
        PACKAGE_DIRECTORY / "label-mapping.json",
        PACKAGE_DIRECTORY / "feature-configuration.json",
        PACKAGE_DIRECTORY / "preprocessing-configuration.json",
        PACKAGE_DIRECTORY / "model-metadata.json",
    ]
    _write_json(PACKAGE_DIRECTORY / "manifest.json", {
        "artifact_type": "truthlens_internal_model_package_manifest",
        "model_version": MODEL_VERSION,
        "deployment_status": "integrated_not_deployment_approved",
        "files": {path.name: _sha256(path) for path in package_files},
    })
    print(PACKAGE_DIRECTORY)


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _copy_json(source: Path, target: Path) -> None:
    _write_json(target, _read_json(source))


def _write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    main()
