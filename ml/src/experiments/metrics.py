"""Comparable binary-classification metrics for baseline experiments."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Sequence

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    classification_report,
    cohen_kappa_score,
    confusion_matrix,
    f1_score,
    log_loss,
    matthews_corrcoef,
    precision_score,
    recall_score,
    roc_auc_score,
)

from experiments.config import MetricsSettings


@dataclass(frozen=True)
class MetricsResult:
    """Serializable Phase 3.8 metric bundle for one held-out prediction set."""

    accuracy: float
    precision: float
    recall: float
    macro_precision: float
    macro_recall: float
    macro_f1: float
    weighted_precision: float
    weighted_recall: float
    weighted_f1: float
    balanced_accuracy: float
    roc_auc: float | None
    pr_auc: float | None
    log_loss: float | None
    matthews_correlation_coefficient: float
    cohen_kappa: float
    confusion_matrix: list[list[int]]
    normalized_confusion_matrix: list[list[float]]
    classification_report: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def calculate_metrics(
    true_labels: Sequence[int],
    predicted_labels: Sequence[int],
    settings: MetricsSettings,
    scores: Sequence[float] | None = None,
    probability_scores: bool = False,
) -> MetricsResult:
    """Calculate all approved metrics, keeping macro F1 as the primary metric."""
    true_array, predicted_array = np.asarray(true_labels), np.asarray(predicted_labels)
    report = classification_report(
        true_array,
        predicted_array,
        labels=[0, 1],
        target_names=["REAL", "FAKE"],
        output_dict=True,
        zero_division=settings.zero_division,
    )
    roc_auc: float | None = None
    pr_auc: float | None = None
    cross_entropy: float | None = None
    if scores is not None and len(np.unique(true_array)) == 2:
        score_array = np.asarray(scores)
        roc_auc = round(float(roc_auc_score(true_array, score_array)), 10)
        pr_auc = round(float(average_precision_score(true_array, score_array)), 10)
        if probability_scores:
            cross_entropy = round(float(log_loss(true_array, score_array, labels=[0, 1])), 10)
    raw_confusion = confusion_matrix(true_array, predicted_array, labels=[0, 1])
    normalized_confusion = confusion_matrix(true_array, predicted_array, labels=[0, 1], normalize="true")
    return MetricsResult(
        accuracy=_round(accuracy_score(true_array, predicted_array)),
        precision=_round(
            precision_score(
                true_array, predicted_array, pos_label=settings.positive_label, zero_division=settings.zero_division
            )
        ),
        recall=_round(
            recall_score(
                true_array, predicted_array, pos_label=settings.positive_label, zero_division=settings.zero_division
            )
        ),
        macro_precision=_round(
            precision_score(true_array, predicted_array, average="macro", zero_division=settings.zero_division)
        ),
        macro_recall=_round(
            recall_score(true_array, predicted_array, average="macro", zero_division=settings.zero_division)
        ),
        macro_f1=_round(f1_score(true_array, predicted_array, average="macro", zero_division=settings.zero_division)),
        weighted_precision=_round(
            precision_score(true_array, predicted_array, average="weighted", zero_division=settings.zero_division)
        ),
        weighted_recall=_round(
            recall_score(true_array, predicted_array, average="weighted", zero_division=settings.zero_division)
        ),
        weighted_f1=_round(
            f1_score(true_array, predicted_array, average="weighted", zero_division=settings.zero_division)
        ),
        balanced_accuracy=_round(balanced_accuracy_score(true_array, predicted_array)),
        roc_auc=roc_auc,
        pr_auc=pr_auc,
        log_loss=cross_entropy,
        matthews_correlation_coefficient=_round(matthews_corrcoef(true_array, predicted_array)),
        cohen_kappa=_round(cohen_kappa_score(true_array, predicted_array)),
        confusion_matrix=raw_confusion.astype(int).tolist(),
        normalized_confusion_matrix=np.round(normalized_confusion.astype(float), 10).tolist(),
        classification_report=_json_safe(report),
    )


def _round(value: float) -> float:
    return round(float(value), 10)


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, np.generic):
        return value.item()
    return value
