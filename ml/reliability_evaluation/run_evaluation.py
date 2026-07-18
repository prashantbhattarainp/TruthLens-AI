"""Run the governed Phase 4.5 robustness and reliability assessment.

The runner uses the integrity-checked packaged English LinearSVC and its frozen
preprocessing. It performs deterministic validation-only diagnostics; it never
fits a calibrator, retrains a model, changes a threshold, or accesses the
protected test partition.

Usage from the repository root::

    .\\ml-service\\.venv\\Scripts\\python.exe -m ml.reliability_evaluation.run_evaluation
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable

import numpy as np
from sklearn.metrics import confusion_matrix

from ml.transformer_benchmark.metrics import classification_metrics

from .figures import generate_figures
from .perturbations import Perturbation, perturbations
from .protocol import DATASET_SHA256, ReliabilityProtocol, protocol_dict


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
ML_SERVICE_ROOT = REPOSITORY_ROOT / "ml-service"
DERIVATIVE_PATH = REPOSITORY_ROOT / "ml/data/derived/TL-BFNK-EN-v1.0/DER-20260718-r2/split-documents.jsonl"
MODEL_PACKAGE = REPOSITORY_ROOT / "ml-service/artifacts/candidate/TL-LSVM-TFIDF-v1.1.0-rc.1"
DEFAULT_OUTPUT_ROOT = REPOSITORY_ROOT / "ml/data/reliability-evaluations"
FIGURE_DIRECTORY = REPOSITORY_ROOT / "docs/research/figures"
FIGURE_MANIFEST_PATH = REPOSITORY_ROOT / "docs/research/PHASE_4_5_ARTIFACT_MANIFEST.json"

TOPIC_TERMS: dict[str, tuple[str, ...]] = {
    "political": ("election", "government", "minister", "parliament", "bjp", "congress", "vote", "president"),
    "health": ("health", "covid", "vaccine", "doctor", "hospital", "medical", "virus", "disease"),
    "financial": ("finance", "financial", "bank", "economy", "economic", "rupee", "stock", "investment", "tax"),
    "entertainment": ("film", "movie", "actor", "actress", "celebrity", "bollywood", "song"),
    "sports": ("cricket", "football", "match", "player", "tournament", "olympic", "sports"),
    "satire": ("satire", "satirical", "parody", "joke", "humour", "humor"),
    "opinion": ("opinion", "editorial", "column", "viewpoint", "commentary"),
    "ambiguous": ("claim", "alleged", "reportedly", "rumour", "rumor", "unverified", "unclear", "misleading"),
}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _git_revision() -> str | None:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=REPOSITORY_ROOT, text=True, capture_output=True, check=False
    )
    return completed.stdout.strip() if completed.returncode == 0 else None


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _load_model_service() -> Any:
    if str(ML_SERVICE_ROOT) not in sys.path:
        sys.path.insert(0, str(ML_SERVICE_ROOT))
    from inference.production_model_service import ProductionModelService  # type: ignore[import-not-found]

    service = ProductionModelService(MODEL_PACKAGE)
    service.ensure_loaded()
    return service


def _load_multilingual_preprocessor() -> Any:
    source_root = REPOSITORY_ROOT / "ml/src"
    if str(source_root) not in sys.path:
        sys.path.insert(0, str(source_root))
    from preprocessing.multilingual import MultilingualPreprocessor  # type: ignore[import-not-found]

    return MultilingualPreprocessor()


def _read_validation_only(path: Path) -> tuple[list[dict[str, Any]], dict[str, int]]:
    """Verify full lineage while retaining only validation records in memory."""

    actual_hash = _sha256(path)
    if actual_hash != DATASET_SHA256:
        raise ValueError(f"Frozen derivative hash mismatch: expected {DATASET_SHA256}, got {actual_hash}")
    rows: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            record = json.loads(line)
            partition = str(record.get("partition"))
            counts[partition] += 1
            if partition == "validation":
                rows.append(
                    {
                        "document_id": str(record["document_id"]),
                        "raw_text": str(record["raw_text"]),
                        "label": int(record["label"]),
                        "fact_check_source": str(record.get("fact_check_source") or "unknown"),
                        "publish_date_raw": record.get("publish_date_raw"),
                    }
                )
    expected = {"train": 6813, "validation": 1461, "test": 1458}
    found = {name: counts.get(name, 0) for name in expected}
    if found != expected:
        raise ValueError(f"Frozen split cardinality mismatch: expected {expected}, got {found}")
    return rows, found


def _score_processed_text(vectorizer: Any, classifier: Any, texts: list[str]) -> tuple[Any, np.ndarray, np.ndarray]:
    matrix = vectorizer.transform(texts)
    margins = np.asarray(classifier.decision_function(matrix), dtype=float)
    predictions = np.asarray(classifier.predict(matrix), dtype=int)
    return matrix, margins, predictions


def _safe_metrics(labels: Iterable[int], predictions: Iterable[int], margins: Iterable[float]) -> dict[str, Any]:
    """Return the established metric suite when a slice contains both labels."""

    y_true = np.asarray(list(labels), dtype=int)
    y_pred = np.asarray(list(predictions), dtype=int)
    y_margin = np.asarray(list(margins), dtype=float)
    base = {
        "support": int(len(y_true)),
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=[0, 1]).tolist(),
        "confusion_matrix_labels": ["REAL", "FAKE"],
        "score_semantics": "uncalibrated LinearSVC decision margin; not probability or confidence",
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
        "status": "computed_descriptive_validation_only",
        "metrics": {**classification_metrics(y_true, y_pred, y_margin), "score_semantics": base["score_semantics"]},
    }


def _margin_proxy(margins: np.ndarray) -> np.ndarray:
    """Map a margin monotonically for a diagnostic chart without fitting calibration."""

    clipped = np.clip(np.asarray(margins, dtype=float), -35.0, 35.0)
    return 1.0 / (1.0 + np.exp(-clipped))


def calibration_diagnostic(labels: Iterable[int], margins: Iterable[float], bins: int = 10) -> dict[str, Any]:
    """Calculate non-fitted margin-proxy reliability diagnostics.

    This is intentionally not calibration: the model exposes an uncalibrated
    margin and no fitted mapping is learned from the validation labels.
    """

    y_true = np.asarray(list(labels), dtype=int)
    proxy = _margin_proxy(np.asarray(list(margins), dtype=float))
    boundaries = np.linspace(0.0, 1.0, bins + 1)
    records: list[dict[str, Any]] = []
    ece = 0.0
    for index in range(bins):
        lower, upper = float(boundaries[index]), float(boundaries[index + 1])
        selected = (proxy >= lower) & (proxy < upper if index < bins - 1 else proxy <= upper)
        count = int(selected.sum())
        if count:
            mean_proxy = float(proxy[selected].mean())
            observed = float(y_true[selected].mean())
            ece += count / len(y_true) * abs(mean_proxy - observed)
        else:
            mean_proxy = 0.0
            observed = 0.0
        records.append(
            {
                "label": f"{lower:.1f}-{upper:.1f}",
                "lower": lower,
                "upper": upper,
                "count": count,
                "mean_margin_proxy": mean_proxy,
                "observed_fake_rate": observed,
            }
        )
    return {
        "status": "diagnostic_not_fitted_calibration",
        "mapping": "sigmoid-clipped LinearSVC decision margin; no learned calibration mapping",
        "expected_calibration_error_proxy": float(ece),
        "brier_score_proxy": float(np.mean((proxy - y_true) ** 2)),
        "bins": records,
        "limitation": "Neither metric is a calibrated-confidence claim, probability validation, or API output because the LinearSVC margin remains uncalibrated.",
    }


def _topic_tags(text: str) -> set[str]:
    folded = text.casefold()
    return {name for name, terms in TOPIC_TERMS.items() if any(term in folded for term in terms)}


def _length_band(text: str) -> str:
    if len(text) <= 150:
        return "short_0_150"
    if len(text) >= 400:
        return "long_400_plus"
    return "medium_151_399"


def _time_band(value: Any) -> str:
    matched = re.match(r"^(\d{4})-", str(value or ""))
    if not matched:
        return "missing_or_unparseable"
    year = int(matched.group(1))
    if year <= 2020:
        return "through_2020"
    if year == 2021:
        return "year_2021"
    return "year_2022_or_later"


def _slice_result(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return _safe_metrics(
        (int(row["label"]) for row in rows),
        (int(row["prediction"]) for row in rows),
        (float(row["margin"]) for row in rows),
    )


def _group_results(rows: list[dict[str, Any]], grouping) -> dict[str, dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        values = grouping(row)
        for value in values if isinstance(values, set) else {values}:
            groups[str(value)].append(row)
    return {name: _slice_result(group) for name, group in sorted(groups.items())}


def _top_feature_sets(matrix: Any, coefficients: np.ndarray, feature_names: np.ndarray, limit: int = 10) -> list[set[str]]:
    output: list[set[str]] = []
    for index in range(matrix.shape[0]):
        row = matrix.getrow(index)
        if not row.nnz:
            output.append(set())
            continue
        contributions = np.abs(row.data * coefficients[row.indices])
        selected = np.argsort(contributions)[-limit:]
        output.append({str(feature_names[row.indices[position]]) for position in selected})
    return output


def _mean_jaccard(left: list[set[str]], right: list[set[str]]) -> float:
    values: list[float] = []
    for first, second in zip(left, right, strict=True):
        union = first | second
        values.append(len(first & second) / len(union) if union else 1.0)
    return float(np.mean(values)) if values else 0.0


def _error_themes(rows: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    themes: dict[str, Counter[str]] = {name: Counter() for name in (*TOPIC_TERMS, "unclassified")}
    for row in rows:
        if int(row["label"]) == int(row["prediction"]):
            continue
        error = "false_positive" if int(row["label"]) == 0 else "false_negative"
        tags = _topic_tags(str(row["raw_text"])) or {"unclassified"}
        for tag in tags:
            themes[tag][error] += 1
    return {
        name: {"false_positive": int(counts["false_positive"]), "false_negative": int(counts["false_negative"])}
        for name, counts in themes.items()
    }


def _ablation(vectorizer: Any, classifier: Any, rows: list[dict[str, Any]], baseline_matrix: Any) -> dict[str, Any]:
    labels = np.asarray([int(row["label"]) for row in rows], dtype=int)
    raw_matrix = vectorizer.transform([str(row["raw_text"]) for row in rows])
    raw_margins = np.asarray(classifier.decision_function(raw_matrix), dtype=float)
    raw_predictions = np.asarray(classifier.predict(raw_matrix), dtype=int)

    feature_names = np.asarray(vectorizer.get_feature_names_out())
    coefficients = np.asarray(classifier.coef_[0], dtype=float)
    unigram_only_coefficients = coefficients.copy()
    unigram_only_coefficients[np.char.find(feature_names.astype(str), " ") >= 0] = 0.0
    unigram_margins = np.asarray(baseline_matrix.dot(unigram_only_coefficients)).ravel() + float(classifier.intercept_[0])
    unigram_predictions = (unigram_margins >= 0.0).astype(int)

    return {
        "variants": {
            "frozen_baseline": {
                "metrics": _safe_metrics(labels, (int(row["prediction"]) for row in rows), (float(row["margin"]) for row in rows))["metrics"],
                "interpretation": "Approved frozen preprocessing plus full unigram/bigram TF-IDF pipeline.",
            },
            "raw_text_no_preprocessing": {
                "metrics": _safe_metrics(labels, raw_predictions, raw_margins)["metrics"],
                "interpretation": "Inference-contract stressor only; raw input is fed to the existing vectorizer without frozen preprocessing, not a retrained model.",
            },
            "bigram_weights_zeroed": {
                "metrics": _safe_metrics(labels, unigram_predictions, unigram_margins)["metrics"],
                "interpretation": "Inference-only diagnostic that zeroes existing bigram coefficients; no feature fitting or classifier retraining.",
            },
        },
        "explainability_module": {
            "status": "analysis_only_not_ablated",
            "finding": "SHAP/LIME consume an already prepared prediction and cannot alter its margin or label by architecture.",
        },
        "ensemble_strategy": {
            "status": "comparison_only",
            "finding": "Phase 4.3 hard/weighted voting Macro F1 0.5447 and soft voting 0.5443 are English validation-only challengers; no ensemble is integrated here.",
        },
        "transformer_models": {
            "status": "not_evaluated",
            "finding": "Phase 4.2 produced no completed transformer checkpoint or prediction artifact, so no transformer ablation/comparison is valid.",
        },
    }


def _figure_manifest(paths: list[Path], artifact_id: str) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "phase": "4.5",
        "artifact_id": artifact_id,
        "code_revision": _git_revision(),
        "figures": [{"path": str(path.relative_to(REPOSITORY_ROOT)).replace("\\", "/"), "sha256": _sha256(path)} for path in paths],
        "content_policy": "Aggregate-only figures; no raw article text, document identifier, per-record prediction, or margin is shown.",
    }


def run(output_root: Path = DEFAULT_OUTPUT_ROOT) -> Path:
    """Execute the full Phase 4.5 descriptive assessment."""

    protocol = ReliabilityProtocol()
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    artifact_id = f"P45-reliability-assessment-{stamp}"
    output_dir = output_root / artifact_id
    output_dir.mkdir(parents=True, exist_ok=False)
    try:
        rows, partition_counts = _read_validation_only(DERIVATIVE_PATH)
        service = _load_model_service()
        vectorizer, classifier = service.explainability_components()
        multilingual = _load_multilingual_preprocessor()
        processed_texts = [service.preprocess_text(document_id=row["document_id"], text=row["raw_text"]) for row in rows]
        if any(not text.strip() for text in processed_texts):
            raise ValueError("Frozen preprocessing produced an empty validation text")
        baseline_matrix, baseline_margins, baseline_predictions = _score_processed_text(vectorizer, classifier, processed_texts)
        feature_names = np.asarray(vectorizer.get_feature_names_out())
        coefficients = np.asarray(classifier.coef_[0], dtype=float)
        baseline_features = _top_feature_sets(baseline_matrix, coefficients, feature_names)
        for index, row in enumerate(rows):
            language = multilingual.process_document(document_id=row["document_id"], text=row["raw_text"]).language
            row.update(
                {
                    "processed_text": processed_texts[index],
                    "margin": float(baseline_margins[index]),
                    "prediction": int(baseline_predictions[index]),
                    "language": language,
                    "length_band": _length_band(row["raw_text"]),
                    "time_band": _time_band(row.get("publish_date_raw")),
                }
            )

        baseline = _safe_metrics((row["label"] for row in rows), baseline_predictions, baseline_margins)
        perturbation_results: list[dict[str, Any]] = []
        explanation_stability: list[dict[str, Any]] = []
        for perturbation in perturbations():
            transformed = [perturbation.transform(str(row["raw_text"])) for row in rows]
            variant_raw = [item[0] for item in transformed]
            touched = np.asarray([item[1] for item in transformed], dtype=bool)
            variant_processed = [
                service.preprocess_text(document_id=f"{row['document_id']}-{perturbation.key}", text=text)
                for row, text in zip(rows, variant_raw, strict=True)
            ]
            if any(not text.strip() for text in variant_processed):
                raise ValueError(f"Perturbation {perturbation.key} produced an empty frozen-preprocessed input")
            matrix, margins, predictions = _score_processed_text(vectorizer, classifier, variant_processed)
            top_features = _top_feature_sets(matrix, coefficients, feature_names)
            flip_rate = float(np.mean(predictions != baseline_predictions))
            stability = _mean_jaccard(baseline_features, top_features)
            perturbation_results.append(
                {
                    "key": perturbation.key,
                    "display_name": perturbation.display_name,
                    "coverage_count": int(touched.sum()),
                    "coverage_rate": float(touched.mean()),
                    "prediction_flip_rate": flip_rate,
                    "mean_absolute_margin_delta": float(np.mean(np.abs(margins - baseline_margins))),
                    "metrics": _safe_metrics((row["label"] for row in rows), predictions, margins)["metrics"],
                    "interpretation": perturbation.interpretation,
                    "label_preservation": perturbation.label_preservation,
                }
            )
            explanation_stability.append(
                {
                    "key": perturbation.key,
                    "display_name": perturbation.display_name,
                    "mean_top_feature_jaccard": stability,
                    "interpretation": "Top absolute linear-contribution overlap; a proxy for sparse explanation stability, not a LIME equivalence test.",
                }
            )

        source_results = _group_results(rows, lambda row: str(row["fact_check_source"]))
        length_results = _group_results(rows, lambda row: str(row["length_band"]))
        temporal_results = _group_results(rows, lambda row: str(row["time_band"]))
        language_results = _group_results(rows, lambda row: str(row["language"]))
        topic_results = _group_results(rows, lambda row: _topic_tags(str(row["raw_text"])) or {"unclassified"})
        eligible_source_f1 = [
            value["metrics"]["macro_f1"]
            for value in source_results.values()
            if value["metrics"]["support"] >= 20 and value["metrics"].get("macro_f1") is not None
        ]
        bias_and_fairness = {
            "status": "descriptive_group_performance_not_demographic_fairness",
            "source_proxy": source_results,
            "length": length_results,
            "topic": topic_results,
            "language_appearance": language_results,
            "source_macro_f1_range_support_20_plus": (
                {"minimum": float(min(eligible_source_f1)), "maximum": float(max(eligible_source_f1)), "range": float(max(eligible_source_f1) - min(eligible_source_f1))}
                if eligible_source_f1
                else None
            ),
            "limitations": "Fact-check source is not publisher identity; topic/language labels are overlapping heuristics; no demographic attributes or causal fairness evidence exists.",
        }
        results: dict[str, Any] = {
            "status": "completed_research_only_reliability_assessment",
            "baseline": baseline,
            "robustness": {
                "perturbations": perturbation_results,
                "limitations": "Synthetic variants are stress tests. Metrics use inherited labels only as diagnostics and do not validate semantic invariance or select a model.",
            },
            "calibration": calibration_diagnostic((row["label"] for row in rows), baseline_margins),
            "generalization": {
                "source_proxy": source_results,
                "length": length_results,
                "temporal_slice": temporal_results,
                "language_appearance": language_results,
                "publisher_evaluation": "not available: derivative has fact_check_source but no publisher identity",
                "time_split": "not performed: publish_date is absent; publish_date_raw supports descriptive temporal slices only",
                "limitations": "All slices reuse the frozen validation set and are descriptive, not external or unseen-publisher generalization estimates.",
            },
            "bias_and_fairness": bias_and_fairness,
            "error_analysis": {
                "themes": _error_themes(rows),
                "cohort_policy": "English keyword heuristics; themes overlap and are neither factual nor demographic labels.",
            },
            "ablation": _ablation(vectorizer, classifier, rows, baseline_matrix),
            "stability": {
                "perturbation_explanation_stability": explanation_stability,
                "prediction_stability": "Measured as prediction-flip rate under each synthetic perturbation.",
                "limitation": "No human semantic-similarity annotation is available; synthetic variants are only a proxy for semantically similar inputs.",
            },
            "limitations": {
                "champion": "The LinearSVC remains immutable, uncalibrated, English-only research evidence, untested after tuning, and not deployment-approved.",
                "protected_test": "No protected-test text, label, feature, or prediction was accessed.",
                "transformers": "No completed Phase 4.2 transformer artifact exists for a reliability comparison.",
                "deployment": "This assessment does not satisfy the remaining rights, calibration, robustness, fairness, monitoring, human-review, or release gates.",
            },
        }
        _write_json(output_dir / "results.json", results)
        figure_paths = generate_figures(results, FIGURE_DIRECTORY)
        figure_manifest = _figure_manifest(figure_paths, artifact_id)
        _write_json(FIGURE_MANIFEST_PATH, figure_manifest)
        _write_json(
            output_dir / "run-manifest.json",
            {
                "schema_version": "1.0.0",
                "status": "completed_research_only_reliability_assessment",
                "protocol": protocol_dict(),
                "data": {
                    "derivative_path": str(DERIVATIVE_PATH.resolve()),
                    "sha256": _sha256(DERIVATIVE_PATH),
                    "partition_counts": partition_counts,
                    "evaluated_partition": "validation",
                    "protected_test_access": "none",
                },
                "model": {
                    "package_path": str(MODEL_PACKAGE.resolve()),
                    "package_manifest_sha256": _sha256(MODEL_PACKAGE / "manifest.json"),
                    "decision_margin": "uncalibrated; confidence remains unavailable",
                },
                "figures": figure_manifest["figures"],
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
        print(f"Reliability assessment did not complete: {type(error).__name__}: {error}", file=sys.stderr)
        raise SystemExit(1) from error
    print(f"Reliability assessment completed: {location}")
