# ADR-007 — Frontend-to-Backend API Boundary

**Status:** Accepted  
**Date:** 2026-07-17

## Context

The static frontend and Node.js backend can run independently in local development. The browser must submit prediction requests only to the Node.js backend, while the Python ML service remains private to the backend.

## Decision

- The frontend has one HTTP boundary: `frontend/src/js/api/api.js`.
- Prediction-specific requests are exposed through `frontend/src/js/api/prediction-api.js`.
- `frontend/public/config.js` supplies the backend base URL and timeout at runtime; UI modules do not contain URLs or `fetch` calls.
- The backend enables browser access only for origins configured in `CORS_ALLOWED_ORIGINS`.
- The frontend renders only standardized backend responses and never constructs prediction data locally.

## Consequences

- The frontend can be served separately during development without bypassing browser-origin protections.
- Frontend-to-backend calls remain replaceable and testable through a small API layer.
- Production deployment requires an explicit CORS allowlist and runtime API URL.
- The ML service remains inaccessible from the browser, preserving the service boundary.
