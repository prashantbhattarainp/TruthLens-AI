# Administrator Guide

## Services

Operate the frontend, backend, and ML service as separate services. The backend is public; the ML service remains private.

## Configuration

- Use the supplied .env.example files as templates.
- Keep secrets in the deployment platform's secret manager.
- Set exact frontend origins in CORS_ALLOWED_ORIGINS.
- Set the ML runtime package location through MODEL_PACKAGE_DIR.
- Use MODEL_LOADING_MODE=eager in production to detect package issues at startup.

## Operational checks

- Backend health: GET /api/health
- System health: GET /api/system/health
- End-to-end check: submit a synthetic, non-sensitive prediction through the frontend.

## Incident response

If a secret is exposed, rotate it immediately. If the ML service is unavailable, the backend returns a safe error and the frontend preserves the user's input. Do not log or retain submitted article text when diagnosing an incident.
