# EJ-007 — Frontend-to-Backend Prediction Integration

**Date:** 2026-07-17  
**Phase / milestone:** Phase 2 — Milestone 2.4  
**Status:** Complete

## Scope

Connected the detection interface to the Node.js mock prediction API and removed frontend-generated prediction output.

## Delivered

- A dedicated frontend API layer with timeout, network, invalid-response, and standardized-backend-error handling.
- A prediction request lifecycle that trims and validates input, prevents duplicate submissions, locks controls while pending, and renders only backend data.
- Result rendering for prediction, confidence, confidence level, risk level, model metadata, keywords, explanation, processing time, request ID, and response timestamp.
- Accessible request-error states and backend connection status indicators.
- Allowlist-based backend CORS support, configured through `CORS_ALLOWED_ORIGINS`, for independently served local frontend development.

## Deliberate boundaries

- The frontend does not manufacture a prediction or call the Python ML service.
- The backend remains the only browser-facing prediction API.
- Backend prediction data is still deterministic mock data in this phase.

## Verification focus

Verification covers a successful browser-origin request, backend validation errors, client validation, a maximum-length article, backend-offline handling, and client timeout handling.
