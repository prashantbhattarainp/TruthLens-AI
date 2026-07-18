# EJ-023 - Multilingual Evaluation

**Date:** 2026-07-18
**Milestone:** Phase 4.4

## Completed work

- Reviewed the Phase 3/4 governance, model, data, XAI, transformer, and ensemble evidence before adding code.
- Added a standalone `ml/multilingual_benchmark/` protocol and runner plus a separate `preprocessing.multilingual` module. The frozen English preprocessing import surface and production service path remain unchanged.
- Implemented Unicode NFC normalization, HTML/URL/email and zero-width cleanup, Devanagari-aware token extraction, conservative Roman-Hindi marker routing, case-safe acronym handling, and bounded Hinglish spelling normalization.
- Added a tracked 12-record synthetic language-processing fixture with explicit no-label/no-training/no-translation restrictions.
- Ran the validation-only audit against the immutable derivative. It verified the existing SHA-256 and 6,813 / 1,461 / 1,458 split before retaining the validation partition only; it generated aggregate ignored evidence at `P44-multilingual-assessment-20260718T133030Z`.
- Added the required multilingual research reports, RDL-015, registry/model-card/data-card updates, and README status update.

## Findings and verification

The full validation replay reproduced the LinearSVC’s existing Macro F1 0.5398 and MCC 0.1014. The derivative yielded only 9 Devanagari-bearing validation records and 2 conservative Hinglish-heuristic records, so no Hindi/Hinglish performance claim is valid. The synthetic fixture routed 12/12 expected language examples correctly; this is a fixture check, not a real-world language-ID benchmark. IndicBERT remained access-limited with no checkpoint or metric.

All 15 ML-service unit tests passed (2 production-model, 3 explainability, 2 transformer-protocol, 3 ensemble-protocol, and 5 multilingual checks), along with targeted Python compilation and JSON validation. No protected-test access, retraining, calibration, model-package replacement, API change, or architecture change occurred.
