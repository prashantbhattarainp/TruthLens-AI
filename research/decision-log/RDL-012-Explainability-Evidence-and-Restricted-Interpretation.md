# RDL-012 - Explainability Evidence and Restricted Interpretation

**Date:** 2026-07-18
**Status:** Accepted
**Phase:** 4.1

## Decision

Phase 4.1 may analyse `TL-LSVM-TFIDF-v1.1.0-rc.1` with SHAP and LIME without retraining, calibration, threshold selection, feature changes, model changes, validation access, or protected-test access.

Local requests are explained in memory after inference using the exact frozen preprocessing and TF-IDF representation. SHAP contributions use the zero TF-IDF reference and sum with the classifier intercept to the LinearSVC decision margin. LIME uses a fixed seed and sample count to approximate that same signed margin; its fidelity is recorded as surrogate quality, not prediction confidence.

Global figures use the first deterministic class-balanced 512-document cohort from the frozen training partition. They emit only aggregate feature terms and scores. Raw text, document identifiers, submitted requests, validation records, and protected-test records are excluded from XAI artifacts and logs.

## Consequences

The candidate retains `integrated_not_deployment_approved` status and `confidence_status: unavailable`. XAI findings can support transparent model-behaviour reporting, but cannot support factual-verdict, causality, fairness, calibration, or broad Indian-media reliability claims.
