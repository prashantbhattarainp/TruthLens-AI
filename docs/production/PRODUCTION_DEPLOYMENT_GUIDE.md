# Production Integration Deployment Guide

> **RC1 companion:** Read the controlled [release-candidate deployment guide](../deployment/RELEASE_CANDIDATE_DEPLOYMENT.md) and [known limitations](../releases/KNOWN_LIMITATIONS.md) before using this guide. Neither document authorizes public deployment.

## Status first

This guide supports running the integrated **internal candidate** service. It does not authorize external/public deployment. `TL-LSVM-TFIDF-v1.1.0-rc.1` remains `integrated_not_deployment_approved`: it was not tested after tuning, has weak absolute performance, and is restricted by data scope and licence evidence.

## Configuration

Set environment-specific values outside source control.

| Variable | Development | Testing | Production integration |
| --- | --- | --- | --- |
| `ML_SERVICE_ENV` | `development` | `testing` | `production` |
| `MODEL_PACKAGE_DIR` | Versioned candidate directory | Isolated fixture/package | Immutable approved integration path |
| `MODEL_LOADING_MODE` | `lazy` | `lazy` or `eager` | `eager` by default with readiness gate |
| `ML_SERVICE_VERSION` | Local version | Test version | Versioned release identifier |
| `ML_SERVICE_URL` (Node) | Loopback service URL | Test service URL | Private Python-service URL only |

Use the existing backend settings for CORS, timeouts, retries, request body limit, shutdown timeout, and logging. Do not put model packages, raw data, tokens, or `.env` values in Git.

Set `MODEL_STARTUP_TIMEOUT_MS` high enough for a cold integrity/spaCy package load (the example uses 60 seconds); keep `REQUEST_TIMEOUT_MS` bounded for ordinary predictions.

## Startup and verification

1. Generate the exact package once with `scripts/production/package_phase_3_10_champion.py`.
2. Verify the package manifest and filesystem permissions. Do not alter package contents after packaging.
3. Start the Python service with its `ml-service` environment and verify `/health`, then `/ready`.
4. Start the Node backend and verify `/api/health`, `/api/system/health`, `/api/model/version`, `/api/model/ready`, and `/api/model/metadata`.
5. Submit only a synthetic, non-sensitive smoke request to `POST /api/predict`; verify no request text appears in logs.
6. Block public routing if `/ready` is not ready, manifest checks fail, metadata is inconsistent, or the registry deployment status changes from the documented state without a new governance decision.

## Operations

Monitor readiness, error codes, timeout rate, latency, model version, and request IDs. Do not log text, externalize decision scores as confidence, or silently fall back to the prior mock model. A new package requires a new immutable version, manifest, registry update, reproducibility evidence, and approval gate.
