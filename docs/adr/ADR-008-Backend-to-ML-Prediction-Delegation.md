# ADR-008 - Backend-to-ML Prediction Delegation

**Status:** Accepted  
**Date:** 2026-07-17

## Context

The public Node.js prediction endpoint previously returned deterministic mock data internally. The project requires the same public API contract while validating the distributed backend-to-Python service architecture before real ML implementation begins.

## Decision

- The Node.js Prediction Service delegates validated requests to `POST /predict` on the Python ML service through `MlServiceClient`.
- The ML client applies the existing configurable URL, timeout, and retry settings and forwards `X-Request-Id` for trace correlation.
- The Python ML service returns the raw prediction data payload; the Node.js backend validates it and owns the public standardized API envelope.
- Upstream unavailability, timeout, HTTP failure, and contract-validation failure are mapped to safe, standardized public errors.
- Both services return deterministic mock data only until the approved ML pipeline replaces the Python mock inference component.

## Consequences

- The frontend contract remains unchanged while the ML implementation can evolve behind the backend boundary.
- Node.js can reject malformed or incomplete upstream output before it reaches users.
- Runtime availability now depends on the Python ML service; operational errors are explicit and traceable through shared request IDs.
