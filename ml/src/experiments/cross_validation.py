"""Deterministic stratified cross-validation planning for binary baseline experiments."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
from sklearn.model_selection import StratifiedGroupKFold, StratifiedKFold

from experiments.config import CrossValidationSettings
from experiments.exceptions import ExperimentInputError


@dataclass(frozen=True)
class CrossValidationFold:
    """One immutable pair of train and validation row positions."""

    fold_index: int
    train_indices: tuple[int, ...]
    validation_indices: tuple[int, ...]


def build_cross_validation_folds(
    labels: Sequence[int],
    settings: CrossValidationSettings,
    seed: int,
    groups: Sequence[str] | None = None,
) -> tuple[CrossValidationFold, ...]:
    """Build the configured stratified folds without fitting data-dependent components."""
    label_array = np.asarray(labels)
    _validate_labels(label_array, settings.n_splits)
    indices = np.arange(len(label_array))
    try:
        if settings.strategy == "stratified_kfold":
            splitter = StratifiedKFold(
                n_splits=settings.n_splits,
                shuffle=settings.shuffle,
                random_state=seed if settings.shuffle else None,
            )
            pairs = splitter.split(indices, label_array)
        else:
            if groups is None or len(groups) != len(label_array):
                raise ExperimentInputError(
                    "stratified_group_kfold requires one nonempty group value for every document."
                )
            group_array = np.asarray(groups)
            if any(not isinstance(group, str) or not group.strip() for group in group_array):
                raise ExperimentInputError("Cross-validation groups must be nonempty strings.")
            splitter = StratifiedGroupKFold(
                n_splits=settings.n_splits,
                shuffle=settings.shuffle,
                random_state=seed if settings.shuffle else None,
            )
            pairs = splitter.split(indices, label_array, group_array)
        return tuple(
            CrossValidationFold(
                fold_index=fold_index,
                train_indices=tuple(int(index) for index in train_indices),
                validation_indices=tuple(int(index) for index in validation_indices),
            )
            for fold_index, (train_indices, validation_indices) in enumerate(pairs, start=1)
        )
    except ValueError as error:
        raise ExperimentInputError(f"Unable to create cross-validation folds: {error}") from error


def _validate_labels(labels: np.ndarray, n_splits: int) -> None:
    if labels.ndim != 1 or len(labels) < n_splits * 2:
        raise ExperimentInputError("Insufficient rows for binary stratified cross-validation.")
    unique, counts = np.unique(labels, return_counts=True)
    if tuple(unique.tolist()) != (0, 1):
        raise ExperimentInputError("Baseline experiments require exactly binary labels 0 and 1.")
    if int(counts.min()) < n_splits:
        raise ExperimentInputError(
            "The smallest binary class must contain at least as many rows as cross-validation folds."
        )
