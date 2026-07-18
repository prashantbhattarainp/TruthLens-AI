"""Produce deterministic paired baseline-versus-tuned comparisons for Phase 3.9."""

from __future__ import annotations

import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "ml" / "src"))

from evaluation.statistics import bootstrap_macro_f1_ci, mcnemar_test, paired_fold_comparison


DATASET_VERSION = "TL-BFNK-EN-v1.0"
BASELINE_IDS = {
    "linear_svm": "EXP-20260717-linear-svm-177d71e9c9",
    "logistic_regression": "EXP-20260717-logistic-regression-e7612c6153",
    "multinomial_naive_bayes": "EXP-20260717-multinomial-naive-bayes-7869d12afd",
}


def main() -> None:
    optimization_root = PROJECT_ROOT / "ml" / "data" / "optimization" / DATASET_VERSION / "phase-3-9-r1"
    baseline_root = PROJECT_ROOT / "ml" / "data" / "experiments" / DATASET_VERSION / "phase-3-8-r2"
    results: dict[str, object] = {
        "artifact_type": "phase_3_9_paired_optimization_comparison",
        "dataset_version": DATASET_VERSION,
        "partition": "train out-of-fold predictions only",
        "test_access": "none",
        "bootstrap": {"resamples": 1000, "seed": 42},
        "comparisons": {},
    }
    for optimization_path in sorted(optimization_root.glob("OPT-*/optimization-result.json")):
        optimized = _read_json(optimization_path)
        model = optimized["model"]
        baseline_id = BASELINE_IDS[model]
        baseline_directory = baseline_root / baseline_id
        baseline_oof = _read_jsonl(baseline_directory / "out-of-fold-predictions.jsonl")
        tuned_oof = _read_jsonl(optimization_path.parent / "out-of-fold-predictions.jsonl")
        baseline_by_id = {row["document_id"]: row for row in baseline_oof}
        tuned_by_id = {row["document_id"]: row for row in tuned_oof}
        if set(baseline_by_id) != set(tuned_by_id):
            raise ValueError(f"OOF document mismatch for {model}.")
        identifiers = sorted(tuned_by_id)
        labels = [int(tuned_by_id[item]["true_label"]) for item in identifiers]
        baseline_predictions = [int(baseline_by_id[item]["predicted_label"]) for item in identifiers]
        tuned_predictions = [int(tuned_by_id[item]["predicted_label"]) for item in identifiers]
        baseline_folds = _read_json(baseline_directory / "cross-validation-results.json")["fold_results"]
        tuned_folds = optimized["tuned_cross_validation"]["fold_metrics"]
        results["comparisons"][model] = {
            "baseline_experiment_id": baseline_id,
            "optimization_id": optimized["optimization_id"],
            "bootstrap_macro_f1_ci": {
                "baseline": bootstrap_macro_f1_ci(labels, baseline_predictions),
                "tuned": bootstrap_macro_f1_ci(labels, tuned_predictions),
            },
            "paired_fold_macro_f1": paired_fold_comparison(
                [float(row["metrics"]["macro_f1"]) for row in tuned_folds],
                [float(row["metrics"]["macro_f1"]) for row in baseline_folds],
            ),
            "mcnemar_accuracy": mcnemar_test(labels, tuned_predictions, baseline_predictions),
        }
    output = optimization_root / "statistical-comparison.json"
    output.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


if __name__ == "__main__":
    main()
