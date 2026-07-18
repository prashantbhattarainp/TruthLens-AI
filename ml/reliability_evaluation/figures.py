"""Publication-oriented aggregate figures for Phase 4.5.

Every figure is generated from aggregate result dictionaries. No raw text,
document identifier, score, or per-record prediction is written to a figure.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Any

MPL_CONFIG_DIRECTORY = Path(tempfile.gettempdir()) / "truthlens-matplotlib"
MPL_CONFIG_DIRECTORY.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CONFIG_DIRECTORY))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


DPI = 300
BLUE = "#1f77b4"
ORANGE = "#ff7f0e"
GREEN = "#2ca02c"
RED = "#d62728"
GRAY = "#6b7280"


def _save(figure: plt.Figure, path: Path) -> Path:
    figure.tight_layout()
    figure.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(figure)
    return path


def _metric(value: Any) -> float:
    return float(value) if value is not None else float("nan")


def generate_figures(results: dict[str, Any], figure_directory: Path) -> list[Path]:
    """Render the fixed Phase 4.5 figure set and return generated paths."""

    figure_directory.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []

    calibration = results["calibration"]
    bins = calibration["bins"]
    observed = [item["observed_fake_rate"] for item in bins if item["count"]]
    expected = [item["mean_margin_proxy"] for item in bins if item["count"]]
    fig, axis = plt.subplots(figsize=(6.8, 5.0))
    axis.plot([0, 1], [0, 1], linestyle="--", color=GRAY, label="Ideal reliability")
    axis.plot(expected, observed, marker="o", color=BLUE, label="Sigmoid-margin diagnostic")
    axis.set(xlim=(0, 1), ylim=(0, 1), xlabel="Mean sigmoid-mapped decision margin", ylabel="Observed FAKE-label frequency", title="Calibration curve (diagnostic only)")
    axis.legend(frameon=False)
    axis.grid(alpha=0.2)
    paths.append(_save(fig, figure_directory / "phase-4-5-calibration-curve.png"))

    fig, (bar_axis, hist_axis) = plt.subplots(1, 2, figsize=(10.0, 4.6), gridspec_kw={"width_ratios": [1.25, 1]})
    x = np.arange(len(bins))
    bar_axis.bar(x - 0.18, [item["mean_margin_proxy"] for item in bins], width=0.36, label="Proxy", color=BLUE)
    bar_axis.bar(x + 0.18, [item["observed_fake_rate"] for item in bins], width=0.36, label="Observed", color=ORANGE)
    bar_axis.set(xticks=x, xticklabels=[item["label"] for item in bins], ylim=(0, 1), ylabel="Rate", title="Reliability diagram")
    bar_axis.tick_params(axis="x", rotation=45)
    bar_axis.legend(frameon=False, fontsize=8)
    hist_axis.bar(x, [item["count"] for item in bins], color=GREEN)
    hist_axis.set(xticks=x, xticklabels=[item["label"] for item in bins], ylabel="Validation records", title="Margin-proxy histogram")
    hist_axis.tick_params(axis="x", rotation=45)
    paths.append(_save(fig, figure_directory / "phase-4-5-reliability-diagram.png"))

    perturbations = results["robustness"]["perturbations"]
    names = [item["display_name"] for item in perturbations]
    flips = [100 * item["prediction_flip_rate"] for item in perturbations]
    touched = [100 * item["coverage_rate"] for item in perturbations]
    fig, axis = plt.subplots(figsize=(9.2, 5.6))
    y = np.arange(len(names))
    axis.barh(y - 0.18, flips, height=0.36, color=RED, label="Prediction flips")
    axis.barh(y + 0.18, touched, height=0.36, color=BLUE, label="Inputs changed")
    axis.set(yticks=y, yticklabels=names, xlabel="Validation records (%)", title="Robustness stressor coverage and prediction flips")
    axis.invert_yaxis()
    axis.legend(frameon=False)
    axis.grid(axis="x", alpha=0.2)
    paths.append(_save(fig, figure_directory / "phase-4-5-robustness-comparison.png"))

    baseline = results["baseline"]["metrics"]
    labels = ["Baseline", *names]
    accuracy = [_metric(baseline["accuracy"]), *[_metric(item["metrics"]["accuracy"]) for item in perturbations]]
    macro_f1 = [_metric(baseline["macro_f1"]), *[_metric(item["metrics"]["macro_f1"]) for item in perturbations]]
    fig, axis = plt.subplots(figsize=(10.0, 5.2))
    x = np.arange(len(labels))
    axis.plot(x, accuracy, marker="o", color=BLUE, label="Accuracy")
    axis.plot(x, macro_f1, marker="s", color=ORANGE, label="Macro F1")
    axis.set(xticks=x, xticklabels=labels, ylim=(0, 1), ylabel="Metric", title="Perturbation performance (synthetic stress labels)")
    axis.tick_params(axis="x", rotation=52)
    axis.legend(frameon=False)
    axis.grid(axis="y", alpha=0.2)
    paths.append(_save(fig, figure_directory / "phase-4-5-perturbation-performance.png"))

    themes = results["error_analysis"]["themes"]
    categories = list(themes)
    false_positive = [themes[name]["false_positive"] for name in categories]
    false_negative = [themes[name]["false_negative"] for name in categories]
    fig, axis = plt.subplots(figsize=(9.2, 4.8))
    x = np.arange(len(categories))
    axis.bar(x, false_positive, color=ORANGE, label="False positive")
    axis.bar(x, false_negative, bottom=false_positive, color=RED, label="False negative")
    axis.set(xticks=x, xticklabels=categories, ylabel="Errors (overlapping cohorts)", title="Error distribution by descriptive theme")
    axis.tick_params(axis="x", rotation=42)
    axis.legend(frameon=False)
    paths.append(_save(fig, figure_directory / "phase-4-5-error-distribution.png"))

    bias = results["bias_and_fairness"]
    length = bias["length"]
    topic = bias["topic"]
    fig, (length_axis, topic_axis) = plt.subplots(1, 2, figsize=(10.0, 4.6))
    length_names = list(length)
    length_axis.bar(length_names, [_metric(length[name]["metrics"].get("macro_f1")) for name in length_names], color=BLUE)
    length_axis.set(ylim=(0, 1), ylabel="Macro F1", title="Length-slice diagnostic")
    topic_names = [name for name, value in topic.items() if value["metrics"].get("macro_f1") is not None]
    topic_axis.bar(topic_names, [_metric(topic[name]["metrics"]["macro_f1"]) for name in topic_names], color=GREEN)
    topic_axis.set(ylim=(0, 1), ylabel="Macro F1", title="Topic-keyword diagnostic")
    topic_axis.tick_params(axis="x", rotation=45)
    paths.append(_save(fig, figure_directory / "phase-4-5-bias-analysis.png"))

    ablation = results["ablation"]
    names = list(ablation["variants"])
    values = [_metric(ablation["variants"][name]["metrics"].get("macro_f1")) for name in names]
    fig, axis = plt.subplots(figsize=(8.4, 4.8))
    bars = axis.bar(names, values, color=[BLUE, ORANGE, GREEN])
    axis.set(ylim=(0, 1), ylabel="Macro F1", title="Inference-only ablation diagnostics")
    axis.tick_params(axis="x", rotation=24)
    for bar, value in zip(bars, values, strict=True):
        if not np.isnan(value):
            axis.text(bar.get_x() + bar.get_width() / 2, value + 0.015, f"{value:.3f}", ha="center", va="bottom", fontsize=8)
    paths.append(_save(fig, figure_directory / "phase-4-5-ablation-study.png"))

    stability = results["stability"]
    names = [item["display_name"] for item in stability["perturbation_explanation_stability"]]
    overlaps = [item["mean_top_feature_jaccard"] for item in stability["perturbation_explanation_stability"]]
    fig, axis = plt.subplots(figsize=(9.2, 4.8))
    axis.barh(np.arange(len(names)), overlaps, color=GREEN)
    axis.set(yticks=np.arange(len(names)), yticklabels=names, xlim=(0, 1), xlabel="Mean top-feature Jaccard overlap", title="Prediction-explanation stability proxy")
    axis.invert_yaxis()
    axis.grid(axis="x", alpha=0.2)
    paths.append(_save(fig, figure_directory / "phase-4-5-explanation-stability.png"))

    return paths
