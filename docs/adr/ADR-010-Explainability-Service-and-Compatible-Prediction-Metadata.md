# ADR-010 - Explainability Service and Compatible Prediction Metadata

**Status:** Accepted
**Date:** 2026-07-18

## Context

The integrated Phase 3 champion is a sparse TF-IDF and LinearSVC pipeline. It exposes an uncalibrated decision margin, not a probability. Phase 4.1 requires local SHAP and LIME explanations for every successful prediction and publication-oriented global analysis without replacing the model, duplicating preprocessing, or changing the frontend → Node → Python trust boundary.

## Decision

- Add an in-process `explainability` module to the Python ML service. It receives the same in-memory processed text and TF-IDF row used for the successful prediction.
- Use `shap.LinearExplainer` with a documented all-zero TF-IDF reference for additive local contributions to the Fake-class margin.
- Use `LimeTextExplainer` as a deterministic local surrogate over a two-column signed-margin adapter (`-margin`, `margin`), never a probability adapter.
- Extend the successful prediction payload with an optional `explainability` object. Existing fields, including `confidence: null`, retain their Phase 3 meanings.
- Generate global figures only from a deterministic, balanced reference cohort in the frozen training partition. Do not read the validation or protected-test partitions.

## Consequences

The public request route and service topology are unchanged, while clients that accept additive response fields can consume SHAP/LIME metadata immediately. Explanation generation increases inference latency and must be monitored. Contributions describe model behaviour only; they do not establish truth, causality, confidence, or deployment readiness.
