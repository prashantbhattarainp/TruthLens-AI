# ADR-006 — Backend Observability and API Resilience

- Status: Accepted
- Date: 2026-07-17
- Related milestones: Phase 1 — Milestone 4

## Context

TruthLens AI uses an Express backend that communicates with an independent Python ML service. The platform needs traceable requests, safe service-to-service failure behavior, consistent API envelopes, and configuration that can move between local and production environments.

## Problem

Ad hoc console logging, route-specific error responses, and hardcoded runtime settings would make distributed debugging, deployment, and future maintenance unreliable.

## Decision

- Use Pino and pino-http for structured JSON logs written to standard output.
- Generate a UUID request ID for every inbound backend request and include it in logs, response headers, and API payloads.
- Require runtime configuration through environment variables validated at startup.
- Use one standardized success envelope and one standardized error envelope for all backend endpoints.
- Route operational errors through centralized error middleware without exposing stack traces.
- Use a dedicated ML client with per-attempt timeout, bounded retry attempts, and structured request lifecycle logging.
- Keep retry logic restricted to the idempotent ML health request in this milestone.

## Alternatives Considered

- Native console logging: rejected because it lacks structured fields and request correlation.
- Route-specific response formats: rejected because it creates inconsistent frontend and API-client behavior.
- Hardcoded development defaults: rejected because deployment configuration should be explicit and fail fast.
- Retrying inside controllers: rejected because transport reliability belongs in the ML client.

## Consequences

- Local startup requires a populated backend environment file or equivalent process environment.
- Logs are machine-readable and suitable for future container or cloud log aggregation.
- API consumers receive stable response shapes for successful and failed requests.
- Retry attempts can increase response time when the ML service is unavailable, but they reduce transient-failure sensitivity.

## Future Considerations

- Add log shipping and retention when deployment infrastructure is introduced.
- Add distributed tracing if additional services or asynchronous jobs are added.
- Revisit retry policy before introducing non-idempotent ML requests.
- Add API version-specific error documentation when public endpoints are introduced.
