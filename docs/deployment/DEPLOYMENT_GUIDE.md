# Deployment Guide

## Deployment topology

Deploy three services:

1. **Frontend** — static HTML, CSS, JavaScript, and public/config.js.
2. **Backend** — the only public API service; it receives browser calls under /api.
3. **ML service** — a private FastAPI service reachable only from the backend.

v1.0.0 is stateless. A database is not required and no database connection string should be configured for this release.

## Frontend

Publish the contents of frontend/ through a static host or reverse proxy. Before publishing, set the production backend URL in frontend/public/config.js.

    window.TruthLensConfig = {
      apiBaseUrl: "https://api.example.com",
      apiTimeoutMs: 12000,
    };

Serve the app over HTTPS. Hash routing in v1.0.0 works on any static host.

## Node.js backend

Install production dependencies and start the service.

    Set-Location backend
    pnpm install --prod --ignore-scripts
    $env:NODE_ENV = "production"
    pnpm start

Set these environment variables in the deployment platform:

| Variable | Required | Notes |
| --- | --- | --- |
| NODE_ENV | Yes | Set to production. |
| SERVICE_VERSION | Yes | Set to 1.0.0. |
| HOST / PORT | Yes | Bind to the platform interface and port. |
| CORS_ALLOWED_ORIGINS | Yes | Exact comma-separated frontend origins. |
| ML_SERVICE_URL | Yes | Private ML-service URL. Never expose it to the browser. |
| REQUEST_TIMEOUT_MS | Yes | Upstream request timeout. |
| MODEL_STARTUP_TIMEOUT_MS | Yes | Readiness timeout for ML startup. |
| LOG_LEVEL | No | Defaults to info. |

Place a TLS-terminating reverse proxy or managed gateway in front of the backend. Allow only the frontend origin through CORS.

## Python ML service

Install dependencies in an isolated environment and start FastAPI.

    Set-Location ml-service
    python -m pip install -r requirements.txt
    $env:ML_SERVICE_ENV = "production"
    $env:ML_SERVICE_VERSION = "1.0.0"
    python -m uvicorn main:app --host 0.0.0.0 --port 8000

Set MODEL_PACKAGE_DIR to the private mounted runtime package and make the package read-only for the service identity. Do not publish that package as a static asset or include it in a public source repository. Set MODEL_LOADING_MODE=eager for deployment checks so configuration errors surface during startup.

Keep the ML service on a private subnet, internal container network, or equivalent. Only the backend needs network access to it.

## Database

No database is used in v1.0.0. Do not add a placeholder database, retention store, or tracking service merely for deployment. If a future version introduces persistence, use a managed database, encrypted connections, least-privilege credentials, migrations, backups, and an explicit data-retention policy.

## Environment and secrets

- Start from backend/.env.example and ml-service/.env.example.
- Store production values in the deployment platform's secret manager.
- Never commit .env files, runtime packages, access keys, or submitted content.
- Rotate any secret immediately if it is exposed.

## Health checks

Configure the public platform health check against GET /api/health and GET /api/system/health.

A successful system health response confirms that the backend can reach the ML service. Monitor response failures and latency at the platform layer without recording submitted article text.

## Release checklist

1. Set frontend API URL and exact backend CORS origin.
2. Set backend and ML-service versions to 1.0.0.
3. Mount the ML runtime package privately and verify read access.
4. Start the ML service, then the backend, then publish the frontend.
5. Check both health endpoints.
6. Submit a synthetic, non-sensitive prediction through the deployed frontend.
7. Confirm HTTPS, CORS, logs, and error pages behave as expected.
