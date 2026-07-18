# RDL-006: Feature Engineering Framework

**Status:** Accepted for Phase 3.6  
**Date:** 2026-07-18  
**Related documents:** [Feature Engineering](../../docs/research/FEATURE_ENGINEERING.md), [Feature Configuration](../../docs/research/FEATURE_CONFIGURATION.md), [Feature Comparison Plan](../../docs/research/FEATURE_COMPARISON_PLAN.md), [Feature Validation Report](../../docs/research/FEATURE_VALIDATION_REPORT.md)

## Context

Phase 3.5 supplied a configurable preprocessing implementation but did not create a BharatFakeNewsKosh derivative because the Phase 3.4 data-readiness gate remains open. Phase 3.6 needs a reproducible representation framework without fitting a vocabulary or TF-IDF weights to an unapproved cohort.

## Decisions

1. Implement feature extraction under `ml/src/features/` with an independent `FeatureExtractor` interface and an open registry. Future representation methods may be added by registering a factory rather than changing baseline pipeline code.
2. Provide CountVectorizer and TF-IDF as the only implemented baseline methods. Their versioned JSON configurations define n-grams, vocabulary cap, document-frequency limits, binary behavior, normalization, and validation limits.
3. Treat input as already-preprocessed whitespace-delimited text. Disable vectorizer lowercasing and default token-pattern processing so feature extraction does not silently apply an additional text-cleaning policy.
4. Require a data-bearing feature run to declare an experiment ID, dataset version, split ID, fit partition, configuration snapshot/hash, source-manifest hash, timestamp, and notes. Fit vocabulary/IDF only on the declared training partition; retain the fitted extractor for held-out transformation.
5. Validate every generated matrix for vocabulary size, dimensions, sparsity, empty rows, CSR memory use, and processing duration. Store the matrix, vocabulary, record-order IDs, fitted extractor, validation report, structured log, and checksummed manifest in a new feature-output directory.
6. Keep Phase 3.6 fixture-only until the RDL-004 data gate is resolved. No raw archive, processed BFNK derivative, label mapping, split, feature matrix, model, metric, or comparison is authorised by this decision.

## Consequences

- The project has a testable sparse-feature framework but no research feature artifact.
- Count and TF-IDF configurations can be reproduced exactly through persisted hashes and fitted artifacts.
- Training-only fitting is an explicit leakage control, not an optional implementation detail.
- Future embedding and transformer methods have a defined extension route but need their own research and resource decisions.

## Architecture impact

None. The framework remains below the existing ML-service boundary and changes no public API, deployment, model-serving, or mock-inference contract; no ADR is created.
