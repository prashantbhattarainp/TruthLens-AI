# TruthLens AI v1.0.0-RC1 — Release Notes

**Release type:** Controlled integration release candidate
**Status:** Ready for internal RC validation; not approved for public deployment
**Date:** 2026-07-18

## Purpose

RC1 packages the completed Phase 5 frontend, API integration, explainability UI, industrial research dashboard, accessibility/performance hardening, verification evidence, deployment guidance, and release documentation. It introduces no new model, data, training, database, retention layer, public API contract, or production approval.

## Included

- Dependency-free, responsive SPA with prediction, research, models, analytics dashboard, explicit empty states, not-found handling, accessible form/error feedback, and on-demand service status.
- Node public API validation, safe envelopes, request IDs, bounded ML-service timeout/retry behaviour, CORS configuration, privacy-safe logs, and model endpoint proxies.
- Private FastAPI inference with integrity-checked package loading and optional bounded SHAP/LIME model-margin explanation metadata.
- Release-candidate HTTP verifier, deployment guide, QA report, architecture/workflow diagrams, and browser-captured local UI evidence.

## RC validation evidence

The local RC run passed `GET /api/health`, `/api/system/health`, `/api/model/ready`, `/api/model/version`, `/api/model/metadata`, and a synthetic `POST /api/predict`. The prediction preserved `confidence: null`, `confidence_status: unavailable`, `risk_level: not_assessed`, and `TL-LSVM-TFIDF-v1.1.0-rc.1` model identity. The dashboard reported Backend API, ML service, and model package as healthy; database status remained correctly `Not instrumented`.

## Explicitly excluded

- Public deployment, production model approval, factual verification, calibrated confidence, external/generalized performance claims, Hindi/Hinglish validation, authentication, database integration, prediction retention, telemetry, and rate limiting.
- Backend, ML-service, model package, frozen results, model registry candidate, or API-contract redesign.

See [known limitations](KNOWN_LIMITATIONS.md) and [the final QA report](FINAL_QA_REPORT.md) before any controlled deployment decision.
