# Industrial Analytics and Research Dashboard

## Scope

Phase 5.3 turns `#/dashboard` into the TruthLens analytics workspace. It combines governed Phase 4 research evidence with an on-demand view of the existing public health/model endpoints. It does not add a backend route, database, telemetry store, prediction history, user analytics, model change, or deployment claim.

## Information classes

| Class | Dashboard treatment | Source |
| --- | --- | --- |
| Frozen research evidence | Displayed as documented validation or train-only evidence. | Phase 4 publication tables, data card, model registry, XAI feature artifact |
| Live operational state | Fetched only after **Refresh operational status** is selected. | `GET /api/health`, `/api/system/health`, `/api/model/ready`, `/api/model/version` |
| Not implemented | Clearly marked rather than simulated. | Prediction history, database health, telemetry, and runtime analytics |
| Illustrative placeholder | Visually distinct and labelled. | Prediction distribution while aggregate retention is unavailable |

## Dashboard sections

- **Project overview:** candidate, frozen validation Macro F1, validation cohort size, and deployment boundary.
- **System health:** on-demand Node API, ML-service, and model-package checks; database status is explicitly not instrumented.
- **Model trace:** candidate version, dataset lineage, deployment status, and uncalibrated-confidence boundary.
- **Model performance:** selectable validation comparisons for Macro F1, accuracy, FAKE recall, and ROC-AUC.
- **Dataset and XAI:** frozen dataset composition plus train-only aggregate mean-absolute-SHAP terms.
- **Research insights:** registry count, champion status, explainability methods, language limit, evidence timeline, and no-retention recent-predictions state.

## Interactions

The comparison controls swap a semantic SVG bar chart without leaving the route. The status refresh button uses the existing frontend fetch boundary and preserves a readable unavailable state if a service cannot be reached. It does not automatically poll, create a monitoring claim, or store returned status data.

## Interpretation boundaries

- Performance values are frozen validation evidence, not live quality metrics.
- The LinearSVC remains an internal research candidate; `production_model=false` and deployment is not approved.
- SHAP features describe the uncalibrated model margin, not factual truth or confidence.
- The distribution chart is illustrative because prediction retention is not implemented.
- English-derived evidence does not establish Hindi or Hinglish fake-news performance.

## Accessibility and responsive design

Every chart has a text label and accessible description. Metric controls are keyboard-operable buttons with pressed state. Service labels communicate state in text and colour. The dashboard is one column on small screens, moves to two columns for cards at medium widths, and uses four compact overview cards on wide screens. Wide chart SVGs remain readable through contained horizontal overflow rather than forcing page overflow.
