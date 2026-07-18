# ADR-010 — Explainability Service and Prediction Metadata

**Status:** Accepted  
**Date:** 2026-07-18

## Context

Users need context for an automated classification without treating an explanation as proof of factual truth.

## Decision

- Provide optional local feature-contribution details with successful predictions.
- Keep explanation generation inside the ML service.
- Preserve the frontend → Node.js → Python service boundary.
- Render explanations as contributing signals and display a clear independent-verification reminder.
- Omit runtime-package identifiers from the public prediction response.

## Consequences

The interface can present inspectable classification context while keeping the public API focused on product behavior and safe interpretation.
