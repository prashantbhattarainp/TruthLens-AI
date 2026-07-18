"""TF-IDF Vectorizer representation component."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer

from features.config import FeatureConfig, VectorizerParameters
from features.exceptions import FeatureConfigurationError, FeatureExtractionError
from features.extractors.base import FeatureExtractor


class TfidfFeatureExtractor(FeatureExtractor):
    """Word n-gram TF-IDF features that preserve the upstream token surface form."""

    method = "tfidf"

    def __init__(self, config: FeatureConfig) -> None:
        self._parameters = VectorizerParameters.from_mapping(config.parameters)
        if self._parameters.binary:
            raise FeatureConfigurationError("binary mode is supported by CountVectorizer only, not TF-IDF.")
        norm = None if self._parameters.normalization == "none" else self._parameters.normalization
        self._vectorizer = TfidfVectorizer(
            analyzer="word",
            tokenizer=str.split,
            token_pattern=None,
            preprocessor=None,
            lowercase=False,
            ngram_range=self._parameters.ngram_range,
            max_features=self._parameters.max_features,
            min_df=self._parameters.min_df,
            max_df=self._parameters.max_df,
            norm=norm,
            dtype=np.float32,
        )
        self._fitted = False

    def fit_transform(self, documents: Sequence[str]) -> csr_matrix:
        try:
            matrix = self._vectorizer.fit_transform(documents)
        except ValueError as error:
            raise FeatureExtractionError(f"TF-IDF Vectorizer could not fit the supplied documents: {error}") from error
        self._fitted = True
        return matrix.tocsr()

    def transform(self, documents: Sequence[str]) -> csr_matrix:
        self._require_fitted()
        return self._vectorizer.transform(documents).tocsr()

    @property
    def feature_names(self) -> tuple[str, ...]:
        self._require_fitted()
        return tuple(self._vectorizer.get_feature_names_out().tolist())

    def _require_fitted(self) -> None:
        if not self._fitted:
            raise FeatureExtractionError("TF-IDF Vectorizer has not been fitted yet.")
