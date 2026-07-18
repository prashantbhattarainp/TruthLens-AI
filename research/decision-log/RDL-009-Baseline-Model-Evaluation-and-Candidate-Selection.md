# RDL-009: Baseline Model Evaluation and Candidate Selection

**Status:** Accepted for Phase 3.8  
**Date:** 2026-07-18  
**Related documents:** [Model evaluation report](../../docs/research/MODEL_EVALUATION_REPORT.md), [model comparison](../../docs/research/MODEL_COMPARISON.md), [statistical analysis](../../docs/research/STATISTICAL_ANALYSIS.md), [error analysis](../../docs/research/ERROR_ANALYSIS.md)

## Context

RDL-008 authorised a single frozen experimental cohort and split. Phase 3.8 executed only that protocol using the three previously approved baseline algorithms and no optimisation or deployment work.

The initial derivative r1 was found to convert missing spreadsheet cells to literal `nan` tokens. It is retained as invalidated audit evidence. Corrected r2 renders absent source text as empty text; it preserves cohort membership, `LMAP-BFNK-v1.0`, duplicate policy, split policy, seed, and dataset version. Only r2 supports the decisions below.

## Decisions

1. Retain Linear SVM v1.0.0 as the sole **evaluated research candidate** for this baseline comparison. It achieved the highest validation Macro F1 (0.5274) after grouped CV and was then tested once after a train+validation refit (test Macro F1 0.5486).
2. Keep Macro F1 as the selection metric. Logistic Regression and Multinomial NB have higher accuracy but markedly lower FAKE recall, so they are not selected for the binary detection objective.
3. Record the candidate and all three immutable CV experiments in the local registries with r2 lineage, artifacts, configuration hashes, and invalidated-r1 boundary.
4. Do not promote the Linear SVM beyond research-candidate status. Protected-test FAKE recall is 0.3805, MCC is 0.1037, source/template features are prominent, and source/length slices show material validity risks.
5. Preserve the protected-test result. It must not be reused for tuning, threshold selection, or another candidate decision. Any substantive data, representation, hyperparameter, or evaluation-protocol change requires a new registered experiment and, where governed fields change, a new dataset version.

## Consequences

- Phase 3.8 establishes a reproducible baseline reference and a narrow selected candidate for future research comparison.
- It does not establish generalisation to unseen fact-check sources, Indian languages beyond English, full news articles, time-forward data, or external datasets.
- No ADR is required: this is a research-evaluation and registry decision with no public API, service-boundary, deployment, or runtime architecture change.
