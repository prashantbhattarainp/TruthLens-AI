# RDL-016 - Robustness, Reliability, and Fairness Evaluation Boundary

**Date:** 2026-07-18
**Status:** Accepted
**Phase:** 4.5

## Decision

Phase 4.5 may run deterministic robustness, stability, descriptive slice, error, and inference-only ablation diagnostics against the frozen validation partition of `TL-BFNK-EN-v1.0` / `DER-20260718-r2`. The runner must verify the full derivative SHA-256 and original split counts before retaining validation rows only. It must use the integrity-checked packaged LinearSVC and frozen preprocessing; the protected test must not be read, transformed, labelled for a model, or predicted.

Allowed perturbations are fixed text stressors: typographical errors, extra punctuation, capitalization, emoji insertion, literal URL removal, stop-word variation, fixed lexical substitutions, fixed phrase rewrites, shortening, and expansion. Their inherited-label metrics are descriptive stress diagnostics only. They must not train, tune, select, promote, or deploy a model, and semantic equivalence must not be assumed for lexical/length transformations.

The LinearSVC decision margin remains uncalibrated. A fixed sigmoid margin mapping may be visualized solely to calculate explicitly labelled ECE/Brier *proxies*; no labels may fit a calibrator, and no probability/confidence/API change may result. Group slices for fact-check source, length, date appearance, topic keywords, and language appearance are descriptive only and cannot establish publisher generalization, demographic fairness, causal bias, or multilingual capability.

## Consequences

No retraining, calibration fitting, threshold change, artifact replacement, public API change, or architecture change is permitted. SHAP/LIME remains post-prediction analysis; feature-contribution overlap may be used only as a bounded explanation-stability proxy. Ensemble and transformer references remain comparison-only because no new ensemble is integrated and Phase 4.2 has no completed transformer artifact. ADR-009 and ADR-010 remain sufficient; no new ADR is required.
