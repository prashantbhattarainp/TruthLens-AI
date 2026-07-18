"""Frozen text-preprocessing contract used by the packaged TruthLens candidate."""

from .config import PreprocessingConfig
from .models import InputDocument, ProcessedDocument
from .pipeline import PreprocessingPipeline

__all__ = [
    'InputDocument',
    'ProcessedDocument',
    'PreprocessingConfig',
    'PreprocessingPipeline',
]
