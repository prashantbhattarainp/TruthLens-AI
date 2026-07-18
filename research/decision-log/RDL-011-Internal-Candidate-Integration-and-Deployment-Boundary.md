# RDL-011 - Internal Candidate Integration and Deployment Boundary

**Date:** 2026-07-18  
**Status:** Accepted  
**Phase:** 3.10

## Decision

`TL-LSVM-TFIDF-v1.1.0-rc.1` may be packaged and integrated into the project’s private Python ML service as an immutable internal candidate. The package uses its frozen preprocessing and TF-IDF configuration, fixed label mapping, Phase 3.9 optimization identity, and integrity manifest. It must be recorded as `integrated_not_deployment_approved`, not as a deployed/approved production model.

No raw data, retraining, calibration, threshold selection, feature changes, model changes, or protected-test reuse is permitted. The response must mark confidence unavailable and risk not assessed because the Linear SVM margin is uncalibrated. The candidate must not make factual-verdict, fact-checking, or general Indian-media reliability claims.

## Rationale

This permits maintainable end-to-end integration and API validation while preserving the exact Phase 3.9 governance boundary. The required release gates—fresh protected-test plan, calibration, robustness/fairness evidence, licence/deployment review, monitoring, and human-review controls—remain unsatisfied.

## Consequences

Phase 3 implementation work is complete at the integration-ready boundary. Any public deployment, retraining, or scope expansion requires a new dataset/model version and an explicit new decision.
