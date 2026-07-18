# Architecture Decision Records Index

| ID      | Title                                    | Status   |
| ------- | ---------------------------------------- | -------- |
| ADR-006 | Backend Observability and API Resilience | Accepted |
| ADR-007 | Frontend-to-Backend API Boundary         | Accepted |
| ADR-008 | Backend-to-ML Prediction Delegation      | Accepted |
| ADR-009 | Internal Model Package and Safe Inference Boundary | Accepted |
| ADR-010 | Explainability Service and Compatible Prediction Metadata | Accepted |

## Phase 4.6 review

Research finalization adds documentation and verification only. It does not change the frontend -> Node.js -> Python trust boundary, model package, API contract, or explainability service. ADR-009 and ADR-010 remain sufficient; no Phase 4.6 ADR is required.

## Phase 5.1 review

The UI foundation adds a static frontend shell and hash routing only. It preserves the browser -> Node.js public API boundary and does not modify the backend, ML service, model package, API contract, or explainability semantics. ADR-009 and ADR-010 remain sufficient; no Phase 5.1 ADR is required.

## Phase 5.2 review

The prediction dashboard consumes the existing public prediction envelope and optional explainability extension only. It preserves the browser -> Node.js -> Python boundary, request/response contract, model package, and Phase 4.1 explainability semantics. ADR-007, ADR-009, and ADR-010 remain sufficient; no Phase 5.2 ADR is required.
