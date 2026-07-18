# Migration Guide — Phase 5.4 to v1.0.0-RC1

## Scope

RC1 is a packaging, validation, and documentation increment. It contains no database migration, model migration, training migration, frontend framework migration, API breaking change, or change to the prediction request/response contract.

## Required configuration review

1. Replace local frontend `apiBaseUrl` with the deployed HTTPS Node API URL.
2. Replace local `CORS_ALLOWED_ORIGINS` with exact deployed frontend origins.
3. Keep the ML service private and set its production loading mode to `eager` with an immutable package path.
4. Set service version labels according to the controlled deployment manifest; do not claim that an RC label approves the model for production.
5. Run `scripts/release/verify_release_candidate.py` after startup and before enabling the internal RC audience.

## Compatibility statement

The browser still calls only Node `POST /api/predict`; Node still calls only private FastAPI `/predict`. The same field limits, standard envelope, `request_id`, unavailable confidence, non-assessed risk, and optional explainability extension apply. Existing Phase 5.4 frontend deployments require no content/data migration.

## Rollback

If readiness or the synthetic verifier fails, remove traffic from the RC deployment and restore the preceding approved immutable internal integration. Do not overwrite the candidate package, silently enable a mock response, or retain failed-request text for diagnosis.
