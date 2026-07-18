"""Configurable, provenance-aware text preprocessing for TruthLens AI."""

from preprocessing.config import PreprocessingConfig
from preprocessing.models import InputDocument, ProcessedDocument
from preprocessing.pipeline import PreprocessingPipeline
from preprocessing.runner import PreprocessingRunner

__all__ = [
    "InputDocument",
    "PreprocessingConfig",
    "PreprocessingPipeline",
    "PreprocessingRunner",
    "ProcessedDocument",
]
