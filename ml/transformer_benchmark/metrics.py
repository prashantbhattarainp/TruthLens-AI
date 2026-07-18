"""Metrics and pre-specified error slices for Phase 4.2."""

from __future__ import annotations

from collections import defaultdict
from typing import Iterable

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    cohen_kappa_score,
    confusion_matrix,
    matthews_corrcoef,
    precision_recall_fscore_support,
    roc_auc_score,
)


def classification_metrics(labels: Iterable[int], predictions: Iterable[int], scores: Iterable[float]) -> dict:
    """Compute the fixed binary-classification metric suite without rounding."""

    y_true = np.asarray(list(labels), dtype=int)
    y_pred = np.asarray(list(predictions), dtype=int)
    y_score = np.asarray(list(scores), dtype=float)
    macro = precision_recall_fscore_support(y_true, y_pred, average="macro", zero_division=0)
    weighted = precision_recall_fscore_support(y_true, y_pred, average="weighted", zero_division=0)
    fake = precision_recall_fscore_support(y_true, y_pred, average="binary", pos_label=1, zero_division=0)
    return {
        "support": int(len(y_true)),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision_macro": float(macro[0]),
        "recall_macro": float(macro[1]),
        "macro_f1": float(macro[2]),
        "precision_weighted": float(weighted[0]),
        "recall_weighted": float(weighted[1]),
        "weighted_f1": float(weighted[2]),
        "fake_precision": float(fake[0]),
        "fake_recall": float(fake[1]),
        "fake_f1": float(fake[2]),
        "roc_auc": float(roc_auc_score(y_true, y_score)),
        "pr_auc": float(average_precision_score(y_true, y_score)),
        "mcc": float(matthews_corrcoef(y_true, y_pred)),
        "cohen_kappa": float(cohen_kappa_score(y_true, y_pred)),
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=[0, 1]).tolist(),
        "confusion_matrix_labels": ["REAL", "FAKE"],
    }


COHORT_KEYWORDS = {
    "political": ("election", "government", "minister", "prime minister", "bjp", "congress", "parliament", "vote", "president"),
    "health": ("health", "covid", "vaccine", "doctor", "disease", "hospital", "medical", "virus"),
    "breaking": ("breaking", "urgent", "alert", "just in"),
    "ambiguous": ("claim", "alleged", "reportedly", "rumour", "rumor", "unverified", "unclear", "misleading"),
}


def cohorts_for_text(text: str) -> list[str]:
    """Return documented, overlapping heuristic cohorts; never used in training."""

    folded = text.casefold()
    cohorts = [name for name, terms in COHORT_KEYWORDS.items() if any(term in folded for term in terms)]
    if len(text) <= 150:
        cohorts.append("short")
    if len(text) >= 400:
        cohorts.append("long")
    return cohorts


def error_slice_summary(records: Iterable[dict]) -> dict:
    """Summarise false positives/negatives by fixed error type and text cohorts.

    Input rows may contain text, but the returned object holds only counts and
    identifiers; raw article text must never be written into benchmark reports.
    """

    summary: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    examples: dict[str, list[str]] = defaultdict(list)
    for row in records:
        actual, prediction = int(row["label"]), int(row["prediction"])
        if actual == prediction:
            continue
        error_type = "false_positive" if actual == 0 and prediction == 1 else "false_negative"
        summary[error_type]["all"] += 1
        examples[error_type].append(str(row["document_id"]))
        for cohort in cohorts_for_text(str(row["raw_text"])):
            summary[error_type][cohort] += 1
    return {
        "cohort_definitions": {
            "political": list(COHORT_KEYWORDS["political"]),
            "health": list(COHORT_KEYWORDS["health"]),
            "breaking": list(COHORT_KEYWORDS["breaking"]),
            "ambiguous": list(COHORT_KEYWORDS["ambiguous"]),
            "short": "raw_text length <= 150 characters",
            "long": "raw_text length >= 400 characters",
        },
        "error_counts": {kind: dict(counts) for kind, counts in summary.items()},
        "error_document_ids": dict(examples),
        "limitations": "Cohorts overlap and use text-keyword heuristics; they are descriptive only, not topic labels.",
    }
