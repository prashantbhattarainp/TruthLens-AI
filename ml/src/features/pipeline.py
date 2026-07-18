"""Feature-extraction orchestration independent of data access and artifact writing."""

from __future__ import annotations

from collections.abc import Iterable

from features.config import FeatureConfig
from features.exceptions import FeatureExtractionError
from features.extractors.base import FeatureExtractor
from features.models import FeatureDocument, FeatureMatrix
from features.registry import FeatureExtractorRegistry, build_default_registry


class FeaturePipeline:
    """Fit or apply one registered representation method to preprocessed text only."""

    def __init__(self, config: FeatureConfig, registry: FeatureExtractorRegistry | None = None) -> None:
        self.config = config
        self._registry = registry or build_default_registry()
        self.extractor: FeatureExtractor = self._registry.create(config)

    def fit_transform(self, documents: Iterable[FeatureDocument]) -> FeatureMatrix:
        """Fit the selected method on one approved cohort and return row-aligned sparse features."""
        materialized = _materialize_documents(documents)
        matrix = self.extractor.fit_transform([document.processed_text for document in materialized])
        return FeatureMatrix(
            document_ids=tuple(document.document_id for document in materialized),
            matrix=matrix,
            feature_names=self.extractor.feature_names,
            method=self.extractor.method,
        )

    def transform(self, documents: Iterable[FeatureDocument]) -> FeatureMatrix:
        """Apply the already-fitted representation without altering its vocabulary or weights."""
        materialized = _materialize_documents(documents)
        matrix = self.extractor.transform([document.processed_text for document in materialized])
        return FeatureMatrix(
            document_ids=tuple(document.document_id for document in materialized),
            matrix=matrix,
            feature_names=self.extractor.feature_names,
            method=self.extractor.method,
        )


def _materialize_documents(documents: Iterable[FeatureDocument]) -> tuple[FeatureDocument, ...]:
    materialized = tuple(documents)
    if not materialized:
        raise FeatureExtractionError("Feature extraction requires at least one preprocessed document.")
    identifiers = [document.document_id for document in materialized]
    if len(set(identifiers)) != len(identifiers):
        raise FeatureExtractionError("Feature document IDs must be unique within one matrix.")
    return materialized
