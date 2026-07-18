# ADR-009 — Runtime Package and Safe Inference Boundary

**Status:** Accepted  
**Date:** 2026-07-18

## Context

The public product needs a reliable way to load its configured runtime package without exposing that package through the browser or public API.

## Decision

- Store runtime packages outside source control in a private, versioned directory.
- Let FastAPI load and validate the configured package before serving analysis requests.
- Keep Node.js as the public API boundary.
- Return product-facing prediction data only: classification, explanation, keywords, and processing time.
- Report package-load failures through safe service-health and prediction errors.

## Consequences

The browser receives a stable product response without runtime-package identifiers. Deployment operators control the private package mount and can detect failures through health checks.
