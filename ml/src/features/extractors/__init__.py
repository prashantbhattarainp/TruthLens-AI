"""Feature-extractor implementations registered by the composition root."""

from features.extractors.base import FeatureExtractor
from features.extractors.count import CountFeatureExtractor
from features.extractors.tfidf import TfidfFeatureExtractor

__all__ = ["CountFeatureExtractor", "FeatureExtractor", "TfidfFeatureExtractor"]
