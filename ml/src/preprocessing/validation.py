"""Aggregate, non-destructive validation of preprocessing results."""

from __future__ import annotations

import re
from collections import Counter
from statistics import fmean, median

from preprocessing.components import EMAIL_PATTERN, URL_PATTERN
from preprocessing.config import PreprocessingConfig
from preprocessing.models import ProcessingResult, ValidationReport


def validate_processing_result(
    result: ProcessingResult,
    config: PreprocessingConfig,
) -> ValidationReport:
    """Calculate required quality checks without changing processed documents."""
    documents = result.documents
    token_counts = [len(document.tokens) for document in documents]
    empty_count = sum(not document.processed_text.strip() for document in documents)
    unexpected = {
        "empty_token_values": sum(
            any(not token.strip() for token in document.tokens) for document in documents
        ),
        "urls_remaining_after_enabled_removal": _remaining_matches(
            documents, URL_PATTERN, config.url_removal.enabled
        ),
        "emails_remaining_after_enabled_removal": _remaining_matches(
            documents, EMAIL_PATTERN, config.email_removal.enabled
        ),
        "repeated_whitespace_after_enabled_normalization": sum(
            bool(re.search(r"\s{2,}", document.processed_text))
            for document in documents
        )
        if config.whitespace_normalization.enabled
        else 0,
    }
    failure_summaries = dict(sorted(Counter(failure.error_type for failure in result.failures).items()))
    empty_rate = empty_count / len(documents) if documents else 1.0
    is_valid = (
        len(result.failures) <= config.validation.max_failures
        and empty_rate <= config.validation.max_empty_document_rate
        and not any(unexpected.values())
    )
    return ValidationReport(
        is_valid=is_valid,
        processed_document_count=len(documents),
        failure_count=len(result.failures),
        empty_processed_document_count=empty_count,
        token_statistics=_token_statistics(token_counts),
        vocabulary_size=len({token for document in documents for token in document.tokens}),
        unexpected_output_counts=unexpected,
        failure_summaries=failure_summaries,
    )


def _remaining_matches(documents: tuple, pattern: re.Pattern[str], enabled: bool) -> int:
    if not enabled:
        return 0
    return sum(bool(pattern.search(document.processed_text)) for document in documents)


def _token_statistics(token_counts: list[int]) -> dict[str, int | float]:
    if not token_counts:
        return {"count": 0, "min": 0, "median": 0, "mean": 0, "max": 0}
    return {
        "count": len(token_counts),
        "min": min(token_counts),
        "median": median(token_counts),
        "mean": round(fmean(token_counts), 4),
        "max": max(token_counts),
    }
