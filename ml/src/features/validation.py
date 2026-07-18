"""Validation for generated sparse feature matrices."""

from __future__ import annotations

from features.config import FeatureConfig
from features.models import FeatureMatrix, FeatureValidationReport


def validate_feature_matrix(
    feature_matrix: FeatureMatrix,
    config: FeatureConfig,
    processing_duration_ms: int,
) -> FeatureValidationReport:
    """Calculate reproducible size, sparsity, empty-row, memory, and dimensional checks."""
    matrix = feature_matrix.matrix.tocsr()
    row_count, column_count = matrix.shape
    total_cells = row_count * column_count
    nonzero_count = int(matrix.nnz)
    density = nonzero_count / total_cells if total_cells else 0.0
    empty_count = int((matrix.getnnz(axis=1) == 0).sum())
    empty_rate = empty_count / row_count if row_count else 1.0
    memory_bytes = int(matrix.data.nbytes + matrix.indices.nbytes + matrix.indptr.nbytes)
    checks = {
        "dimensions_match_document_and_vocabulary_counts": (
            row_count == len(feature_matrix.document_ids) and column_count == feature_matrix.vocabulary_size
        ),
        "vocabulary_nonempty": (feature_matrix.vocabulary_size > 0)
        if config.validation.require_nonempty_vocabulary
        else True,
        "empty_feature_vector_rate_within_limit": (
            empty_rate <= config.validation.max_empty_feature_vector_rate
        ),
        "matrix_memory_within_limit": (
            memory_bytes <= config.validation.max_matrix_memory_mb * 1024 * 1024
        ),
        "processing_duration_recorded": processing_duration_ms >= 0,
    }
    return FeatureValidationReport(
        is_valid=all(checks.values()),
        document_count=row_count,
        vocabulary_size=feature_matrix.vocabulary_size,
        feature_dimensions={"rows": row_count, "columns": column_count},
        nonzero_count=nonzero_count,
        density=round(density, 10),
        sparsity=round(1.0 - density, 10),
        empty_feature_vector_count=empty_count,
        empty_feature_vector_rate=round(empty_rate, 10),
        matrix_memory_bytes=memory_bytes,
        processing_duration_ms=processing_duration_ms,
        checks=checks,
    )
