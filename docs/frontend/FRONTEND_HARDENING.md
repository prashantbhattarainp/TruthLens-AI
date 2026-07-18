# Frontend Hardening

## Boundary preserved

Phase 5.4 changes only the static frontend. The browser continues to call the existing Node.js public API; it never calls the Python ML service directly. No backend, ML service, model package, API contract, architecture decision, or research result was changed.

## Security and resilience controls

| Area | Control |
| --- | --- |
| Input handling | The existing client validation gives immediate feedback; the backend remains the authoritative validator. The unsupported URL control stays disabled and is excluded from the request payload. |
| Safe rendering | Dynamic prediction/explanation content is rendered with DOM text APIs. The reusable modal builder now constructs heading/content/actions with DOM nodes rather than interpolating strings. |
| API use | The shared request boundary accepts JSON, applies an abort timeout, uses same-origin credentials, prevents stale cache reads, and maps unreadable responses to a bounded application error. |
| Error exposure | UI messages distinguish network, timeout, ML-service, invalid-response, 404, and 5xx conditions without displaying raw server messages, stack traces, or request content. |
| Sensitive data | `public/config.js` is public runtime configuration only and must not contain credentials, tokens, model secrets, or user data. The frontend stores no prediction history. |
| Supply chain | The UI uses no external fonts, scripts, images, icon libraries, chart packages, or analytics SDKs. The dashboard SVG is local/original. |

## Code-quality cleanup

- Route-level imports replace eager page imports, and only active route controllers initialize.
- The previously unused prediction backend-status reference now has a visible, announced status badge.
- An unknown route has a dedicated not-found state rather than an ambiguous home fallback.
- Toast presentation has one reusable severity/dismissal contract.
- Shared status badges, loading skeletons, and responsive patterns are centralized in CSS instead of copied per page.

## Deployment responsibilities

Frontend hardening cannot replace server controls. A deployment should enforce HTTPS, a reviewed Content Security Policy, security headers, dependency review, access control/session handling where applicable, server-side rate limits, validation, logging policy, and incident response. Any authentication, telemetry, persistence, or data-retention change requires separate approval and architecture review.
