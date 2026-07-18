"""Publication-ready, aggregate-only visualisations for Phase 3.8."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import precision_recall_curve, roc_curve


MODEL_LABELS = {
    "logistic_regression": "Logistic Regression",
    "multinomial_naive_bayes": "Multinomial NB",
    "linear_svm": "Linear SVM",
}
MODEL_COLORS = {
    "logistic_regression": "#4C78A8",
    "multinomial_naive_bayes": "#F58518",
    "linear_svm": "#54A24B",
}


def generate_phase_3_8_figures(
    result: dict[str, Any], statistics: dict[str, Any], cv_records: dict[str, dict[str, Any]], output_directory: Path
) -> tuple[Path, ...]:
    """Write all Phase 3.8 PNG figures from aggregate predictions and metadata."""
    output_directory.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 10, "axes.titlesize": 12, "axes.labelsize": 10})
    paths = (
        _validation_macro_f1(result, statistics, output_directory / "phase-3-8-validation-macro-f1.png"),
        _roc_curves(result, output_directory / "phase-3-8-validation-roc-curves.png"),
        _pr_curves(result, output_directory / "phase-3-8-validation-pr-curves.png"),
        _cv_distribution(cv_records, output_directory / "phase-3-8-cv-macro-f1-distribution.png"),
        _test_confusion(result, output_directory / "phase-3-8-selected-test-confusion.png"),
        _feature_importance(result, output_directory / "phase-3-8-feature-importance.png"),
        _error_analysis(result, output_directory / "phase-3-8-selected-test-error-analysis.png"),
        _resources(result, output_directory / "phase-3-8-resource-profile.png"),
    )
    return paths


def _validation_macro_f1(result: dict[str, Any], statistics: dict[str, Any], path: Path) -> Path:
    models = list(result["validation_results"])
    values = [result["validation_results"][name]["metrics"]["macro_f1"] for name in models]
    figure, axis = plt.subplots(figsize=(8, 4.8))
    bars = axis.bar(
        [MODEL_LABELS[name] for name in models], values, color=[MODEL_COLORS[name] for name in models],
    )
    axis.set_ylim(0, 0.7)
    axis.set_ylabel("Macro F1")
    axis.set_title("Validation macro F1 used for candidate selection")
    axis.grid(axis="y", alpha=0.25)
    for bar, value in zip(bars, values):
        axis.text(bar.get_x() + bar.get_width() / 2, value + 0.015, f"{value:.3f}", ha="center")
    figure.tight_layout()
    figure.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(figure)
    return path


def _roc_curves(result: dict[str, Any], path: Path) -> Path:
    figure, axis = plt.subplots(figsize=(6.6, 5.4))
    for model, curve in result["validation_curve_data"].items():
        fpr, tpr, _ = roc_curve(curve["true_labels"], curve["scores"])
        auc = result["validation_results"][model]["metrics"]["roc_auc"]
        axis.plot(fpr, tpr, label=f"{MODEL_LABELS[model]} (AUC {auc:.3f})", color=MODEL_COLORS[model], linewidth=2)
    axis.plot([0, 1], [0, 1], color="#666666", linestyle="--", linewidth=1, label="Chance")
    axis.set(xlim=(0, 1), ylim=(0, 1), xlabel="False positive rate", ylabel="True positive rate", title="Validation ROC curves")
    axis.legend(loc="lower right", frameon=False)
    axis.grid(alpha=0.2)
    figure.tight_layout()
    figure.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(figure)
    return path


def _pr_curves(result: dict[str, Any], path: Path) -> Path:
    figure, axis = plt.subplots(figsize=(6.6, 5.4))
    for model, curve in result["validation_curve_data"].items():
        precision, recall, _ = precision_recall_curve(curve["true_labels"], curve["scores"])
        auc = result["validation_results"][model]["metrics"]["pr_auc"]
        axis.plot(recall, precision, label=f"{MODEL_LABELS[model]} (AP {auc:.3f})", color=MODEL_COLORS[model], linewidth=2)
    prevalence = np.mean(next(iter(result["validation_curve_data"].values()))["true_labels"])
    axis.axhline(prevalence, color="#666666", linestyle="--", linewidth=1, label=f"Prevalence ({prevalence:.3f})")
    axis.set(xlim=(0, 1), ylim=(0, 1), xlabel="Recall", ylabel="Precision", title="Validation precision–recall curves")
    axis.legend(loc="lower left", frameon=False)
    axis.grid(alpha=0.2)
    figure.tight_layout()
    figure.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(figure)
    return path


def _cv_distribution(records: dict[str, dict[str, Any]], path: Path) -> Path:
    models = list(records)
    values = [[fold["metrics"]["macro_f1"] for fold in records[name]["fold_results"]] for name in models]
    figure, axis = plt.subplots(figsize=(8, 4.8))
    boxplot = axis.boxplot(values, tick_labels=[MODEL_LABELS[name] for name in models], patch_artist=True)
    for patch, name in zip(boxplot["boxes"], models):
        patch.set_facecolor(MODEL_COLORS[name])
        patch.set_alpha(0.7)
    for index, series in enumerate(values, start=1):
        axis.scatter(np.full(len(series), index), series, color="#222222", s=20, zorder=3)
    axis.set_ylabel("Fold Macro F1")
    axis.set_title("Grouped five-fold cross-validation variability (training partition only)")
    axis.grid(axis="y", alpha=0.25)
    figure.tight_layout()
    figure.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(figure)
    return path


def _test_confusion(result: dict[str, Any], path: Path) -> Path:
    metrics = result["selected_model"]["test_result"]["metrics"]
    matrices = (metrics["confusion_matrix"], metrics["normalized_confusion_matrix"])
    titles = ("Raw counts", "Row-normalized")
    figure, axes = plt.subplots(1, 2, figsize=(8, 3.8))
    for axis, matrix, title in zip(axes, matrices, titles):
        values = np.asarray(matrix)
        image = axis.imshow(values, cmap="Blues")
        axis.set(title=title, xticks=[0, 1], yticks=[0, 1], xticklabels=["REAL", "FAKE"], yticklabels=["REAL", "FAKE"], xlabel="Predicted", ylabel="Actual")
        for row in range(2):
            for column in range(2):
                text = f"{values[row, column]:.3f}" if title != "Raw counts" else str(int(values[row, column]))
                axis.text(column, row, text, ha="center", va="center", color="white" if values[row, column] > values.max() / 2 else "black")
        figure.colorbar(image, ax=axis, fraction=0.046, pad=0.04)
    figure.suptitle("Selected Linear SVM: one-time protected test evaluation")
    figure.tight_layout()
    figure.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(figure)
    return path


def _feature_importance(result: dict[str, Any], path: Path) -> Path:
    importance = result["feature_importance"]
    figure, axes = plt.subplots(2, 2, figsize=(11, 11))
    for row, model in enumerate(("logistic_regression", "linear_svm")):
        for column, (key, title) in enumerate((("real_indicative", "REAL-indicative"), ("fake_indicative", "FAKE-indicative"))):
            items = importance[model][key][:12]
            axis = axes[row, column]
            weights = [item["weight"] for item in items][::-1]
            names = [item["feature"] for item in items][::-1]
            axis.barh(names, weights, color=MODEL_COLORS[model])
            axis.axvline(0, color="#444444", linewidth=0.8)
            axis.set_title(f"{MODEL_LABELS[model]} — {title}")
            axis.set_xlabel("Model coefficient")
    figure.suptitle("Training-partition TF-IDF feature coefficients (interpretive, not causal)")
    figure.tight_layout()
    figure.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(figure)
    return path


def _error_analysis(result: dict[str, Any], path: Path) -> Path:
    rates = result["error_analysis"]["error_rates"]
    class_items = [(key.split(":", 1)[1], value["error_rate"]) for key, value in rates.items() if key.startswith("class:")]
    source_items = sorted(
        ((key.split(":", 1)[1], value["error_rate"], value["count"]) for key, value in rates.items() if key.startswith("source:")),
        key=lambda item: (-item[2], item[0]),
    )[:8]
    figure, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    axes[0].bar([item[0] for item in class_items], [item[1] for item in class_items], color="#54A24B")
    axes[0].set(title="Protected-test error rate by true class", ylabel="Error rate", ylim=(0, 1))
    axes[0].grid(axis="y", alpha=0.25)
    axes[1].barh([item[0] for item in source_items][::-1], [item[1] for item in source_items][::-1], color="#54A24B")
    axes[1].set(title="Error rate by eight largest test sources", xlabel="Error rate", xlim=(0, 1))
    axes[1].grid(axis="x", alpha=0.25)
    figure.tight_layout()
    figure.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(figure)
    return path


def _resources(result: dict[str, Any], path: Path) -> Path:
    rows = result["validation_results"]
    models = list(rows)
    figure, axes = plt.subplots(1, 2, figsize=(9, 4.5))
    axes[0].bar([MODEL_LABELS[name] for name in models], [rows[name]["training_time_ms"] for name in models], color=[MODEL_COLORS[name] for name in models])
    axes[0].set(title="Training time on frozen train split", ylabel="Milliseconds")
    axes[0].tick_params(axis="x", rotation=20)
    axes[1].bar([MODEL_LABELS[name] for name in models], [rows[name]["model_size_bytes"] / 1024 for name in models], color=[MODEL_COLORS[name] for name in models])
    axes[1].set(title="Serialized model size", ylabel="KiB")
    axes[1].tick_params(axis="x", rotation=20)
    for axis in axes:
        axis.grid(axis="y", alpha=0.25)
    figure.tight_layout()
    figure.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(figure)
    return path
