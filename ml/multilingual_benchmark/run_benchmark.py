"""Run the governed Phase 4.4 multilingual compatibility assessment.

The runner never trains a model and deliberately excludes the protected test
partition.  It evaluates only the frozen LinearSVC on language-appearance
slices of the existing English validation derivative, and separately validates
the multilingual preprocessing layer with a synthetic language-labelled probe.

Usage from repository root::

    .\\ml-service\\.venv\\Scripts\\python.exe -m ml.multilingual_benchmark.run_benchmark
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable

import joblib
import numpy as np
from sklearn.metrics import confusion_matrix

from ml.transformer_benchmark.metrics import classification_metrics

from .protocol import DATASET_SHA256, MultilingualProtocol, protocol_dict


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DERIVATIVE_PATH = REPOSITORY_ROOT / "ml/data/derived/TL-BFNK-EN-v1.0/DER-20260718-r2/split-documents.jsonl"
MODEL_ARTIFACT = (
    REPOSITORY_ROOT
    / "ml/data/optimization/TL-BFNK-EN-v1.0/phase-3-9-r1/OPT-20260718-linear-svm-faafafe15e/fitted-validation-candidate.joblib"
)
PREPROCESSING_CONFIG = (
    REPOSITORY_ROOT
    / "ml-service/artifacts/candidate/TL-LSVM-TFIDF-v1.1.0-rc.1/preprocessing-configuration.json"
)
SYNTHETIC_PROBE_PATH = REPOSITORY_ROOT / "ml/fixtures/multilingual/phase-4-4-language-probe.json"
DEFAULT_OUTPUT_ROOT = REPOSITORY_ROOT / "ml/data/multilingual-benchmarks"


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


def _load_multilingual_preprocessor() -> Any:
    source_root = REPOSITORY_ROOT / "ml/src"
    if str(source_root) not in sys.path:
        sys.path.insert(0, str(source_root))
    from preprocessing.multilingual import MultilingualPreprocessor  # type: ignore[import-not-found]

    return MultilingualPreprocessor()


def _load_frozen_preprocessor() -> Any:
    source_root = REPOSITORY_ROOT / "ml/src"
    if str(source_root) not in sys.path:
        sys.path.insert(0, str(source_root))
    from preprocessing import PreprocessingConfig, PreprocessingPipeline  # type: ignore[import-not-found]

    return PreprocessingPipeline(PreprocessingConfig.from_json_file(PREPROCESSING_CONFIG))


def _read_validation_only(path: Path) -> tuple[list[dict[str, Any]], dict[str, int]]:
    """Hash the derivative and retain validation rows only in memory.

    Training and protected-test rows are counted only to verify the immutable
    split contract; their text and labels are not retained or evaluated.
    """

    actual_hash = _sha256(path)
    if actual_hash != DATASET_SHA256:
        raise ValueError(f"Frozen derivative hash mismatch: expected {DATASET_SHA256}, got {actual_hash}")
    rows: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            partition = str(row.get("partition"))
            counts[partition] += 1
            if partition == "validation":
                rows.append(
                    {
                        "document_id": str(row["document_id"]),
                        "raw_text": str(row["raw_text"]),
                        "label": int(row["label"]),
                    }
                )
    expected = {"train": 6813, "validation": 1461, "test": 1458}
    found = {name: counts.get(name, 0) for name in expected}
    if found != expected:
        raise ValueError(f"Frozen split cardinality mismatch: expected {expected}, got {found}")
    return rows, found


def _read_synthetic_probe(path: Path) -> list[dict[str, str]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("status") != "synthetic_preprocessing_fixture_only":
        raise ValueError("Synthetic language probe status is invalid")
    records = payload.get("records")
    if not isinstance(records, list) or not records:
        raise ValueError("Synthetic language probe records are missing")
    checked: list[dict[str, str]] = []
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Synthetic language probe record is invalid")
        if "label" in record or "fake" in record or "real" in record:
            raise ValueError("Synthetic language probe must not carry a fake-news label")
        language = record.get("expected_language")
        if language not in {"english", "hindi", "hinglish"}:
            raise ValueError("Synthetic language probe has an unsupported expected language")
        checked.append(
            {
                "record_id": str(record["record_id"]),
                "expected_language": str(language),
                "scenario": str(record["scenario"]),
                "text": str(record["text"]),
            }
        )
    return checked


def _safe_metrics(labels: Iterable[int], predictions: Iterable[int], margins: Iterable[float]) -> dict[str, Any]:
    """Compute the standard suite when both binary classes are represented."""

    y_true = np.asarray(list(labels), dtype=int)
    y_pred = np.asarray(list(predictions), dtype=int)
    y_margin = np.asarray(list(margins), dtype=float)
    base = {
        "support": int(len(y_true)),
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=[0, 1]).tolist(),
        "confusion_matrix_labels": ["REAL", "FAKE"],
        "score_semantics": "uncalibrated LinearSVC decision margin; ranking only, not probability or confidence",
    }
    if len(y_true) == 0 or set(y_true) != {0, 1}:
        return {
            "status": "not_computable_both_labels_not_present",
            "metrics": {
                **base,
                "accuracy": None,
                "precision_macro": None,
                "recall_macro": None,
                "macro_f1": None,
                "weighted_f1": None,
                "roc_auc": None,
                "pr_auc": None,
                "mcc": None,
                "cohen_kappa": None,
            },
        }
    return {
        "status": "computed_exploratory_slice_only",
        "metrics": {**classification_metrics(y_true, y_pred, y_margin), "score_semantics": base["score_semantics"]},
    }


def _cohorts(text: str, language: str) -> set[str]:
    """Return overlapping descriptive cohorts without retaining text in output."""

    folded = text.casefold()
    cohorts: set[str] = set()
    keyword_sets = {
        "political": ("election", "government", "minister", "bjp", "congress", "चुनाव", "सरकार", "चुनाव", "chunav", "sarkar"),
        "health": ("health", "covid", "vaccine", "doctor", "hospital", "स्वास्थ्य", "टीका", "डॉक्टर", "covid", "vaccine"),
        "social_media": ("social media", "whatsapp", "facebook", "instagram", "youtube", "ट्विटर", "व्हाट्सऐप", "post", "viral"),
    }
    for name, terms in keyword_sets.items():
        if any(term in folded for term in terms):
            cohorts.add(name)
    if len(text) <= 150:
        cohorts.add("short")
    if len(text) >= 400:
        cohorts.add("long")
    if language == "hindi":
        cohorts.add("devanagari")
    if language == "hinglish":
        cohorts.add("transliterated")
    if any(token.isupper() and len(token) > 1 for token in text.split()):
        cohorts.add("named_entity_or_acronym")
    return cohorts


def _error_summary(rows: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    summary: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        actual = int(row["label"])
        prediction = int(row["prediction"])
        if actual == prediction:
            continue
        error_type = "false_positive" if actual == 0 else "false_negative"
        summary[error_type]["all"] += 1
        for cohort in _cohorts(str(row["raw_text"]), str(row["language"])):
            summary[error_type][cohort] += 1
    return {kind: dict(sorted(counts.items())) for kind, counts in sorted(summary.items())}


def _vocabulary_summary(rows: list[dict[str, Any]], vocabulary: set[str]) -> dict[str, Any]:
    all_tokens = [token for row in rows for token in row["frozen_tokens"]]
    unique_tokens = set(all_tokens)
    covered = unique_tokens & vocabulary
    nonzero_counts = [int(value) for row in rows for value in row["feature_nonzero"]]
    return {
        "documents": len(rows),
        "mean_raw_characters": round(sum(int(row["raw_length"]) for row in rows) / len(rows), 4) if rows else 0.0,
        "mean_multilingual_tokens": round(sum(int(row["language_token_count"]) for row in rows) / len(rows), 4) if rows else 0.0,
        "unique_frozen_tokens": len(unique_tokens),
        "unique_tokens_in_champion_vocabulary": len(covered),
        "unique_token_vocabulary_coverage": round(len(covered) / len(unique_tokens), 6) if unique_tokens else 0.0,
        "documents_with_zero_tfidf_features": sum(value == 0 for value in nonzero_counts),
        "mean_active_tfidf_features": round(sum(nonzero_counts) / len(nonzero_counts), 4) if nonzero_counts else 0.0,
        "hinglish_normalization_replacements": sum(int(row["hinglish_normalization_count"]) for row in rows),
    }


def _probe_summary(records: list[dict[str, str]], preprocessor: Any) -> dict[str, Any]:
    outcomes: list[dict[str, Any]] = []
    for record in records:
        processed = preprocessor.process_document(document_id=record["record_id"], text=record["text"])
        outcomes.append(
            {
                "expected_language": record["expected_language"],
                "detected_language": processed.language,
                "language_token_count": len(processed.tokens),
                "hinglish_normalization_count": processed.hinglish_normalization_count,
            }
        )
    by_language: dict[str, dict[str, int]] = {}
    for language in ("english", "hindi", "hinglish"):
        subset = [item for item in outcomes if item["expected_language"] == language]
        by_language[language] = {
            "support": len(subset),
            "correct_language_detections": sum(item["expected_language"] == item["detected_language"] for item in subset),
            "total_tokens": sum(int(item["language_token_count"]) for item in subset),
            "hinglish_normalization_replacements": sum(int(item["hinglish_normalization_count"]) for item in subset),
        }
    return {
        "fixture_status": "synthetic_preprocessing_fixture_only",
        "records": len(outcomes),
        "correct_language_detections": sum(item["expected_language"] == item["detected_language"] for item in outcomes),
        "language_detection_accuracy": round(
            sum(item["expected_language"] == item["detected_language"] for item in outcomes) / len(outcomes), 6
        ),
        "by_expected_language": by_language,
        "limitations": "This validates a hand-authored fixture only. It is not a fake-news dataset, translation corpus, or general language-identification accuracy estimate.",
    }


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run(output_root: Path = DEFAULT_OUTPUT_ROOT) -> Path:
    """Produce ignored aggregate evidence for the Phase 4.4 research reports."""

    protocol = MultilingualProtocol()
    output_dir = output_root / f"P44-multilingual-assessment-{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}"
    output_dir.mkdir(parents=True, exist_ok=False)
    try:
        validation_rows, partition_counts = _read_validation_only(DERIVATIVE_PATH)
        multilingual = _load_multilingual_preprocessor()
        frozen = _load_frozen_preprocessor()
        pipeline = joblib.load(MODEL_ARTIFACT)
        vectorizer = pipeline.named_steps["tfidf"]
        vocabulary = set(vectorizer.vocabulary_)

        assessed: list[dict[str, Any]] = []
        for row in validation_rows:
            language_document = multilingual.process_document(document_id=row["document_id"], text=row["raw_text"])
            from preprocessing import InputDocument  # type: ignore[import-not-found]

            frozen_document = frozen.process_document(InputDocument(document_id=row["document_id"], text=row["raw_text"]))
            assessed.append(
                {
                    **row,
                    "language": language_document.language,
                    "raw_length": len(row["raw_text"]),
                    "language_token_count": len(language_document.tokens),
                    "hinglish_normalization_count": language_document.hinglish_normalization_count,
                    "frozen_text": frozen_document.processed_text,
                    "frozen_tokens": frozen_document.tokens,
                }
            )
        frozen_texts = [str(row["frozen_text"]) for row in assessed]
        transformed = vectorizer.transform(frozen_texts)
        predictions = pipeline.predict(frozen_texts).astype(int)
        margins = pipeline.decision_function(frozen_texts).astype(float)
        for index, row in enumerate(assessed):
            row["prediction"] = int(predictions[index])
            row["margin"] = float(margins[index])
            row["feature_nonzero"] = [int(transformed[index].nnz)]

        language_summaries: dict[str, Any] = {}
        for language in ("english", "hindi", "hinglish"):
            subset = [row for row in assessed if row["language"] == language]
            language_summaries[language] = {
                "classification_slice": _safe_metrics(
                    (int(row["label"]) for row in subset),
                    (int(row["prediction"]) for row in subset),
                    (float(row["margin"]) for row in subset),
                ),
                "input_compatibility": _vocabulary_summary(subset, vocabulary),
                "error_summary": _error_summary(subset),
                "interpretation": (
                    "Exploratory language-appearance slice of the English-labelled derivative; not a governed Hindi/Hinglish benchmark."
                    if language != "english"
                    else "Majority English/unclassified slice of an English-labelled derivative; still validation-only evidence."
                ),
            }

        all_validation = _safe_metrics(
            (int(row["label"]) for row in assessed),
            (int(row["prediction"]) for row in assessed),
            (float(row["margin"]) for row in assessed),
        )
        probe = _probe_summary(_read_synthetic_probe(SYNTHETIC_PROBE_PATH), multilingual)
        _write_json(
            output_dir / "results.json",
            {
                "status": "completed_research_only_multilingual_compatibility_assessment",
                "all_validation": all_validation,
                "language_appearance_slices": language_summaries,
                "synthetic_preprocessing_probe": probe,
                "limitations": {
                    "dataset": "No governed labelled Hindi or Hinglish fake-news dataset was acquired or created.",
                    "metrics": "Slice metrics are descriptive only and are not valid language-wise performance claims or selection evidence.",
                    "champion": "The frozen English LinearSVC was neither retrained nor recalibrated; its decision margin is not confidence.",
                    "transformer": "IndicBERT remains not evaluated because no authenticated upstream access or completed checkpoint exists.",
                    "protected_test": "No protected-test text, label, feature, or prediction was accessed.",
                },
            },
        )
        _write_json(
            output_dir / "run-manifest.json",
            {
                "schema_version": "1.0.0",
                "status": "completed_research_only_multilingual_compatibility_assessment",
                "protocol": protocol_dict(),
                "data": {
                    "derivative_path": str(DERIVATIVE_PATH.resolve()),
                    "sha256": _sha256(DERIVATIVE_PATH),
                    "partition_counts": partition_counts,
                    "evaluated_partition": "validation",
                    "protected_test_access": "none",
                },
                "model": {
                    "artifact": str(MODEL_ARTIFACT.resolve()),
                    "sha256": _sha256(MODEL_ARTIFACT),
                    "preprocessing_configuration": str(PREPROCESSING_CONFIG.resolve()),
                    "decision_margin": "uncalibrated; not confidence",
                },
                "synthetic_probe": {
                    "path": str(SYNTHETIC_PROBE_PATH.resolve()),
                    "sha256": _sha256(SYNTHETIC_PROBE_PATH),
                    "purpose": protocol.synthetic_probe_policy,
                },
                "code_revision": _git_revision(),
                "artifact_policy": protocol.artifact_policy,
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
        print(f"Multilingual assessment did not complete: {type(error).__name__}: {error}", file=sys.stderr)
        raise SystemExit(1) from error
    print(f"Multilingual assessment completed: {location}")
