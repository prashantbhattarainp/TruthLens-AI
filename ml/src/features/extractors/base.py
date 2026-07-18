"""Common interface for independently implemented feature extractors."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence

from scipy.sparse import csr_matrix


class FeatureExtractor(ABC):
    """A fitted representation method that maps preprocessed text to sparse features."""

    method: str

    @abstractmethod
    def fit_transform(self, documents: Sequence[str]) -> csr_matrix:
        """Fit only on the supplied text cohort, then return its matrix."""

    @abstractmethod
    def transform(self, documents: Sequence[str]) -> csr_matrix:
        """Transform new documents using the frozen fitted representation."""

    @property
    @abstractmethod
    def feature_names(self) -> tuple[str, ...]:
        """Return the fitted feature names in exact matrix-column order."""
