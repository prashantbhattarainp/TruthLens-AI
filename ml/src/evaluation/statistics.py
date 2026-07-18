"""Uncertainty intervals and paired baseline-comparison tests."""

from __future__ import annotations

from typing import Sequence

import numpy as np
from scipy import stats
from sklearn.metrics import f1_score


def bootstrap_macro_f1_ci(
    labels: Sequence[int], predictions: Sequence[int], *, seed: int = 42, samples: int = 1000
) -> dict[str, float | int]:
    """Deterministic percentile confidence interval for Macro F1."""
    y_true, y_pred = np.asarray(labels), np.asarray(predictions)
    rng = np.random.default_rng(seed)
    values = np.empty(samples)
    for index in range(samples):
        sample = rng.integers(0, len(y_true), len(y_true))
        values[index] = f1_score(y_true[sample], y_pred[sample], average="macro", zero_division=0)
    return {
        "estimate": round(float(f1_score(y_true, y_pred, average="macro", zero_division=0)), 8),
        "lower_95": round(float(np.percentile(values, 2.5)), 8),
        "upper_95": round(float(np.percentile(values, 97.5)), 8),
        "resamples": samples,
        "seed": seed,
    }


def paired_fold_comparison(left: Sequence[float], right: Sequence[float]) -> dict[str, float | int | None]:
    """Paired t-test, Wilcoxon test, CI, and Cohen dz for aligned CV folds."""
    left_values, right_values = np.asarray(left, dtype=float), np.asarray(right, dtype=float)
    difference = left_values - right_values
    standard_deviation = float(np.std(difference, ddof=1))
    standard_error = standard_deviation / np.sqrt(len(difference)) if standard_deviation else 0.0
    critical = float(stats.t.ppf(0.975, len(difference) - 1)) if len(difference) > 1 else 0.0
    t_result = stats.ttest_rel(left_values, right_values)
    nonzero = difference[difference != 0]
    wilcoxon_p = float(stats.wilcoxon(nonzero, alternative="two-sided").pvalue) if len(nonzero) else 1.0
    return {
        "folds": len(difference),
        "mean_difference": round(float(np.mean(difference)), 8),
        "ci_lower_95": round(float(np.mean(difference) - critical * standard_error), 8),
        "ci_upper_95": round(float(np.mean(difference) + critical * standard_error), 8),
        "paired_t_statistic": round(float(t_result.statistic), 8) if np.isfinite(t_result.statistic) else None,
        "paired_t_p_value": round(float(t_result.pvalue), 8) if np.isfinite(t_result.pvalue) else None,
        "wilcoxon_p_value": round(wilcoxon_p, 8),
        "cohen_dz": round(float(np.mean(difference) / standard_deviation), 8) if standard_deviation else None,
    }


def mcnemar_test(
    labels: Sequence[int], left_predictions: Sequence[int], right_predictions: Sequence[int]
) -> dict[str, float | int | str]:
    """Exact binomial McNemar test for two aligned classifier prediction sets."""
    y_true, left, right = np.asarray(labels), np.asarray(left_predictions), np.asarray(right_predictions)
    left_correct, right_correct = left == y_true, right == y_true
    left_only = int(np.sum(left_correct & ~right_correct))
    right_only = int(np.sum(~left_correct & right_correct))
    discordant = left_only + right_only
    p_value = float(stats.binomtest(min(left_only, right_only), discordant, 0.5).pvalue) if discordant else 1.0
    rendered_p_value: float | str = "<1e-8" if p_value < 0.5e-8 else round(p_value, 8)
    return {
        "left_only_correct": left_only,
        "right_only_correct": right_only,
        "discordant_pairs": discordant,
        "method": "exact_binomial",
        "p_value": rendered_p_value,
    }
