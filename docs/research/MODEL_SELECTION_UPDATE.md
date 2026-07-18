# Model Selection Update - Phase 4.2

## Decision status

**No champion replacement is approved.** `TL-LSVM-TFIDF-v1.1.0-rc.1` remains the current internal research champion with `production_model=false` and `integrated_not_deployment_approved`. Phase 4.2 creates transformer challengers only; it does not modify the FastAPI service, public API, or current candidate package.

## Champion-challenger strategy

1. Freeze the shared data derivative, labels, split, protocol, and outcome metrics before reviewing a challenger.
2. Select a transformer checkpoint only by validation Macro F1 within its fixed one-epoch schedule.
3. Perform at most one protected-test evaluation for a completed challenger and use it only as descriptive non-selection evidence.
4. Preserve the tuned LinearSVC’s protected-test restriction. Compare its frozen validation evidence, not its historical pre-tuning test result.
5. Require a separate decision before any promotion. That decision must consider repeatability, error patterns, data rights, calibration, robustness/fairness, operational resource cost, release-package integrity, monitoring, incident response, and human-review controls.

A model cannot be promoted just because a single metric is greater than 0.5398. The incumbent’s absolute validation performance is limited, and the new challengers inherit the same dataset/source/template, language, and factual-verdict limitations.

## Current challenger disposition

| Candidate | Registry disposition | Promotion eligibility |
| --- | --- | --- |
| IndicBERT | `not_evaluated_access_limited` | No; no trained/evaluated artifact |
| DistilBERT | `not_evaluated_resource_limited` | No; stopped before checkpoint/validation/test evidence |
| BERT base | `not_evaluated_resource_limited` | No; not started after lower-cost CPU limitation |
| RoBERTa base | `not_evaluated_resource_limited` | No; not started after lower-cost CPU limitation |

The next decision remains pending until completed candidate artifacts can be reviewed on suitable compute. That review is explicitly outside automatic benchmark execution.
