# EJ-022 - Hybrid and Ensemble Learning

**Date:** 2026-07-18  
**Milestone:** Phase 4.3

## Completed work

- Added a standalone Phase 4.3 ensemble harness that verifies the derivative SHA-256 and split counts, applies the frozen preprocessing, and invokes only the three immutable Phase 3.9 classical pipelines.
- Implemented hard voting, OOF-Macro-F1-weighted hard voting, probability-only soft voting, and an OOF-trained Logistic Regression stacker.
- Evaluated validation evidence with accuracy, macro precision/recall/F1, weighted F1, ROC-AUC, PR-AUC, MCC, Cohen's kappa, confusion matrices, bounded error cohorts, source-level error aggregates, model sizes, timings, and process RSS observations.
- Stored the stacking meta-model and aggregate result manifest only in an ignored local artifact bundle. No raw text, per-document scores, or protected-test outputs are persisted in tracked files.
- Added Phase 4.3 research reports, RDL-014, registry records, Model Card/Data Card updates, and Champion-Challenger documentation.

## Findings

Hard and weighted voting both reached validation Macro F1 0.5447, a small +0.0049 over the LinearSVC's 0.5398, but with lower accuracy, weighted F1, MCC, and FAKE precision trade-offs. Probability-only soft voting reached Macro F1 0.5443 and the strongest ranking metrics (ROC-AUC 0.5688; PR-AUC 0.4769). The OOF stacker failed the recall safety check: it predicted only 10 of 575 FAKE validation examples correctly, with Macro F1 0.3944.

No transformer candidate completed in Phase 4.2, so a classical-transformer hybrid has no valid score. Blending was intentionally excluded to preserve the frozen protocol. The current champion, service, and API are unchanged.

## Verification

The harness unit suite passed, Python compilation passed, the final validation-only bundle completed from code revision `c8a9733`, and no protected-test prediction path was invoked. The Phase 4.3 test suite is rerun before branch handoff.
