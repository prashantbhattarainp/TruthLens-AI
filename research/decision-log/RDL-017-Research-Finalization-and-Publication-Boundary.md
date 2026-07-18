# RDL-017 - Research Finalization and Publication Boundary

**Date:** 2026-07-18  
**Status:** Accepted  
**Phase:** 4.6

## Decision

Phase 4.6 may consolidate the already approved Phase 3 and Phase 4 evidence into publication-oriented tables, figures index, reproducibility guidance, project summary, threats to validity, future-work plan, Model Card/Data Card updates, and registry synchronization. It may verify tracked documentation, JSON, and aggregate-figure hashes without reading governed raw data or local ignored model artifacts.

The final internal research champion remains `TL-LSVM-TFIDF-v1.1.0-rc.1` with `production_model=false` and `integrated_not_deployment_approved`. The finalization package must state that this is not a production model, a fact checker, a calibrated probability model, or a validated Hindi/Hinglish detector. It must not promote an ensemble, transformer, hybrid, or multilingual variant.

## Rationale

The completed work contains valid but heterogeneous evidence: explained LinearSVC behaviour, unevaluated transformers, validation-only ensemble trade-offs, multilingual input-compatibility diagnostics, and validation-only reliability findings. A single publication package improves traceability only when it preserves their distinct scopes and non-results.

## Consequences

No dataset/model version, split, artifact, API field, threshold, calibration, training result, deployment state, or architecture changes. The protected test remains unavailable to the tuned champion and Phase 4.6. ADR-009 and ADR-010 remain sufficient; no new ADR is required. Any new empirical work or release claim requires a new governed decision.
