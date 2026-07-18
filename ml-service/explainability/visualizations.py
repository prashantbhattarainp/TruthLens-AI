"""Publication-oriented figure helpers that expose only aggregate feature terms and scores."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'truthlens-matplotlib'))

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt

from schemas.explainability import FeatureContribution


def save_contribution_bar_plot(
    path: Path,
    *,
    title: str,
    contributions: list[FeatureContribution],
    x_label: str,
) -> None:
    ordered = list(reversed(contributions))
    labels = [item.feature for item in ordered]
    values = [item.contribution for item in ordered]
    colors = ['#b44d4d' if value > 0 else '#2f6f9f' for value in values]
    figure, axis = plt.subplots(figsize=(9, max(4, len(ordered) * 0.38 + 1.6)), constrained_layout=True)
    axis.barh(labels, values, color=colors)
    axis.axvline(0, color='#3f3f3f', linewidth=0.8)
    axis.set_title(title, fontweight='bold')
    axis.set_xlabel(x_label)
    axis.grid(axis='x', alpha=0.2)
    figure.savefig(path, dpi=300, bbox_inches='tight')
    plt.close(figure)


def save_absolute_importance_plot(
    path: Path,
    *,
    title: str,
    contributions: list[FeatureContribution],
) -> None:
    ordered = list(reversed(contributions))
    labels = [item.feature for item in ordered]
    values = [abs(item.contribution) for item in ordered]
    figure, axis = plt.subplots(figsize=(9, max(4, len(ordered) * 0.38 + 1.6)), constrained_layout=True)
    axis.barh(labels, values, color='#5d8f62')
    axis.set_title(title, fontweight='bold')
    axis.set_xlabel('Mean absolute SHAP value (LinearSVC margin units)')
    axis.grid(axis='x', alpha=0.2)
    figure.savefig(path, dpi=300, bbox_inches='tight')
    plt.close(figure)


def save_waterfall_plot(
    path: Path,
    *,
    title: str,
    base_value: float,
    contributions: list[FeatureContribution],
) -> None:
    ordered = sorted(contributions, key=lambda item: abs(item.contribution), reverse=True)
    labels = ['Base margin', *[item.feature for item in ordered]]
    values = [base_value, *[item.contribution for item in ordered]]
    running = 0.0
    starts: list[float] = []
    heights: list[float] = []
    for value in values:
        next_value = running + value
        starts.append(min(running, next_value))
        heights.append(abs(value))
        running = next_value
    colors = ['#6e6e6e', *['#b44d4d' if value > 0 else '#2f6f9f' for value in values[1:]]]
    figure, axis = plt.subplots(figsize=(11, 5.5), constrained_layout=True)
    axis.bar(range(len(values)), heights, bottom=starts, color=colors)
    axis.axhline(0, color='#3f3f3f', linewidth=0.8)
    axis.set_xticks(range(len(labels)), labels, rotation=38, ha='right')
    axis.set_ylabel('LinearSVC Fake-class margin')
    axis.set_title(title, fontweight='bold')
    axis.grid(axis='y', alpha=0.2)
    figure.savefig(path, dpi=300, bbox_inches='tight')
    plt.close(figure)
