"""CountVectorizer representation component."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize

from features.config import FeatureConfig, VectorizerParameters
from features.exceptions import FeatureExtractionError
from features.extractors.base import FeatureExtractor


class CountFeatureExtractor(FeatureExtractor):
    """Word n-gram count features with optional binary and matrix normalization modes."""

    method = "count"

    def __init__(self, config: FeatureConfig) -> None:
        self._parameters = VectorizerParameters.from_mapping(config.parameters)
        self._vectorizer = CountVectorizer(
            analyzer="word",
            tokenizer=str.split,
            token_pattern=None,
            preprocessor=None,
            lowercase=False,
            ngram_range=self._parameters.ngram_range,
            max_features=self._parameters.max_features,
            min_df=self._parameters.min_df,
            max_df=self._parameters.max_df,
            binary=self._parameters.binary,
            dtype=np.int64,
        )
        self._fitted = False

    def fit_transform(self, documents: Sequence[str]) -> csr_matrix:
        try:
            matrix = self._vectorizer.fit_transform(documents)
        except ValueError as error:
            raise FeatureExtractionError(f"CountVectorizer could not fit the supplied documents: {error}") from error
        self._fitted = True
        return self._normalize(matrix)

    def transform(self, documents: Sequence[str]) -> csr_matrix:
        self._require_fitted()
        return self._normalize(self._vectorizer.transform(documents))

    @property
    def feature_names(self) -> tuple[str, ...]:
        self._require_fitted()
        return tuple(self._vectorizer.get_feature_names_out().tolist())

    def _normalize(self, matrix: csr_matrix) -> csr_matrix:
        if self._parameters.normalization == "none":
            return matrix.tocsr()
        return normalize(matrix, norm=self._parameters.normalization, copy=True).tocsr()

    def _require_fitted(self) -> None:
        if not self._fitted:
            raise FeatureExtractionError("CountVectorizer has not been fitted yet.")
