# EJ-027: Prediction and Explainability Dashboard

**Milestone:** Phase 5.2  
**Status:** Complete  
**Scope:** Frontend-only prediction workflow and bounded explainability visualization

## Objective

Deliver the core browser experience for the existing `POST /api/predict` contract without changing the Node backend, Python service, model package, experiment results, explainability computation, or research claims.

## Implemented work

- Extended `/predict` with validated headline/article submission, character counters, loading state, reset, focus management, and an explicit disabled URL placeholder.
- Added reusable confidence, backend-error, explanation-presentation, and explanation-panel helpers.
- Rendered prediction, processing time, decision margin, risk status, model/version/dataset trace, response timestamp, and request ID from the existing public response envelope.
- Preserved the existing unavailable confidence semantics: the UI does not calculate a probability from the LinearSVC margin.
- Rendered optional top feature contributions plus SHAP and LIME-equivalent metadata, including clear unavailable states for absent or null response data.
- Added success/error notifications and explicit mappings for validation, network, timeout, backend, and ML-service failures.
- Added frontend integration, prediction-page, and XAI UI documentation.

## Contract and governance boundary

The browser still calls the public Node endpoint only. The request remains `{ headline, article }`; no URL, API, response-schema, backend, ML, model, experiment-registry, model-registry, RDL, or ADR decision is changed. XAI panels describe the model margin, never factual truth or calibrated confidence.

## Verification

- Node built-in frontend tests cover routes, shell landmarks, and pure prediction presentation helpers.
- JavaScript syntax checks cover all frontend source modules.
- Static-file preview checks confirm the dashboard assets are served together.
- Existing model and Phase 4 verification commands remain unchanged and are rerun as regression checks.

## Outcome

Phase 5.2 makes the current governed research candidate inspectable through the web UI without broadening its capability claims. Phase 5.3 remains subject to approval.
