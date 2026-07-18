# System Architecture

## Overview

TruthLens AI separates browser concerns, public API concerns, and analysis concerns.

    Browser SPA → Node.js API → FastAPI ML service

The browser never calls the ML service directly. The backend validates incoming data, assigns a request identifier, applies safe error handling, and returns a stable response envelope.

## Components

| Component | Responsibility |
| --- | --- |
| Frontend | Product UI, client validation, accessible result states, and on-demand health display. |
| Backend | Public API, CORS, request validation, request correlation, upstream timeout handling, and response envelopes. |
| ML service | Automated classification and optional feature-contribution details. |
| Shared contracts | JSON schemas that document the public prediction request and response payloads. |

## Data flow

1. A user enters a headline and article in the frontend.
2. The frontend sends the request to POST /api/predict.
3. The backend validates the request and forwards it to the private ML service.
4. The ML service returns a classification and optional explanation details.
5. The backend validates the upstream response and returns it in the public envelope.
6. The frontend presents the result with a reminder to independently verify important claims.

## Security and privacy boundaries

- The backend is the only public API boundary.
- The ML service should remain on a private network.
- Runtime packages and .env files are not tracked.
- v1.0.0 does not persist submitted text, user profiles, or prediction history.
- CORS must list only approved frontend origins.

## Availability

The frontend calls GET /api/health and GET /api/system/health only when the user asks to refresh service status. The product does not create a telemetry store or imply continuous monitoring.
