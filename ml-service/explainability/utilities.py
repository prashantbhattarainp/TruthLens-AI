"""Shared feature-ranking helpers with explicit LinearSVC margin semantics."""

from __future__ import annotations

from collections.abc import Iterable

from schemas.explainability import FeatureContribution


def rank_signed_features(
    feature_names: Iterable[str],
    values: Iterable[float],
    *,
    limit: int,
) -> tuple[list[FeatureContribution], list[FeatureContribution], list[FeatureContribution]]:
    entries = [
        (str(feature).strip(), float(value))
        for feature, value in zip(feature_names, values, strict=True)
        if value and str(feature).strip() and str(feature).strip()[0].isalnum()
    ]
    positive = sorted((entry for entry in entries if entry[1] > 0), key=lambda entry: entry[1], reverse=True)
    negative = sorted((entry for entry in entries if entry[1] < 0), key=lambda entry: entry[1])
    least = sorted(entries, key=lambda entry: (abs(entry[1]), entry[0]))[:limit]
    return (
        _contributions(positive[:limit], direction='supports_fake_margin'),
        _contributions(negative[:limit], direction='supports_real_margin'),
        _contributions(least, direction='minimal_effect'),
    )


def merge_top_features(
    positive: list[FeatureContribution],
    negative: list[FeatureContribution],
    *,
    limit: int,
) -> list[FeatureContribution]:
    ranked = sorted(
        [*positive, *negative],
        key=lambda contribution: (-abs(contribution.contribution), contribution.feature),
    )
    return [
        FeatureContribution(
            feature=contribution.feature,
            contribution=contribution.contribution,
            direction=contribution.direction,
            rank=index,
        )
        for index, contribution in enumerate(ranked[:limit], start=1)
    ]


def _contributions(
    entries: list[tuple[str, float]],
    *,
    direction: str,
) -> list[FeatureContribution]:
    return [
        FeatureContribution(feature=feature, contribution=value, direction=direction, rank=index)
        for index, (feature, value) in enumerate(entries, start=1)
    ]
