# ADR-009 - Internal Model Package and Safe Inference Boundary

**Status:** Accepted  
**Date:** 2026-07-18

## Context

Phase 3.9 selected `TL-LSVM-TFIDF-v1.1.0-rc.1` as a conditional champion, but RDL-009/RDL-010 prohibit reuse of the protected test after tuning and prohibit deployment or factual-verdict claims. The prior Python service intentionally exposed mock inference only. The existing public architecture must now support governed internal integration without silently converting a research candidate into a release-approved model.

## Decision

- Package the immutable candidate under a versioned, Git-ignored internal artifact directory with model pipeline, vectorizer, classifier, label mapping, frozen configurations, metadata, and a SHA-256 manifest.
- Let FastAPI lazy-load the package, validate every required artifact/hash, and expose `/health`, `/ready`, `/metadata`, `/version`, and `/predict`.
- Keep Node.js as the public API boundary and add validated proxies for model readiness, metadata, and version state.
- Return `confidence: null`, `confidence_status: "unavailable"`, an uncalibrated `decision_score`, and `risk_level: "not_assessed"`. No decision score may be interpreted as probability or factual confidence.
- Mark package and registry status `integrated_not_deployment_approved`. Failure to load a package is explicit readiness failure; there is no mock/fallback inference path.

## Consequences

The application gains reproducible internal inference integration, startup/readiness observability, and safe version/lineage introspection while preserving the established frontend → Node → Python boundary. The public API response schema changes semantically to prevent a misleading confidence display; frontend and backend validators were updated together. Public deployment remains outside this decision and requires new governed evidence.
