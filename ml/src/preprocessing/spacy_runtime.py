"""spaCy loading with an explicit, auditable blank-pipeline fallback."""

from __future__ import annotations

from dataclasses import dataclass

import spacy
from spacy.language import Language

from preprocessing.config import PreprocessingConfig
from preprocessing.exceptions import ModelCapabilityError


@dataclass(frozen=True)
class SpacyRuntime:
    nlp: Language
    model_identifier: str
    fallback_used: bool

    @property
    def has_lemmatizer(self) -> bool:
        return self.nlp.has_pipe("lemmatizer")


def load_spacy_runtime(config: PreprocessingConfig) -> SpacyRuntime:
    """Load the configured model, falling back only when the configuration permits it."""
    try:
        nlp = spacy.load(config.spacy.model_name)
        return SpacyRuntime(nlp=nlp, model_identifier=config.spacy.model_name, fallback_used=False)
    except OSError as error:
        if not config.spacy.allow_blank_fallback:
            raise ModelCapabilityError(
                f"Configured spaCy model {config.spacy.model_name!r} is unavailable."
            ) from error
        if config.lemmatization.enabled:
            raise ModelCapabilityError(
                "Lemmatization cannot use the blank spaCy fallback. Install the configured language "
                "model or disable lemmatization."
            ) from error
        nlp = spacy.blank(config.language)
        return SpacyRuntime(
            nlp=nlp,
            model_identifier=f"blank:{config.language}",
            fallback_used=True,
        )
