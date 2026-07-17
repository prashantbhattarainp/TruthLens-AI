# EJ-009: Machine Learning Research Methodology

**Phase:** 3  
**Milestone:** 3.1 - Machine Learning Research Methodology  
**Date:** 2026-07-17  
**Status:** Complete

## Objective

Define the research protocol for TruthLens AI before any dataset acquisition, preprocessing, training, or inference work begins.

## Completed work

- Authored the [research methodology](../../research/Research-Methodology.md) covering scope, objectives, research questions, dataset governance, split design, leakage prevention, imbalance handling, preprocessing strategy, baselines, evaluation, explainability, reproducibility, and experiment tracking.
- Added [RDL-001](../../research/decision-log/RDL-001-Research-Methodology-and-Reproducibility.md) to record the accepted methodological decisions.
- Added a phased [research roadmap](../architecture/Research-Roadmap.md) with gated follow-on milestones.

## Deliberately not implemented

- Dataset discovery, download, acquisition, or processing.
- spaCy or any NLP preprocessing implementation.
- Feature extraction, model training, evaluation, explainability algorithms, or model loading.
- Database schema changes and experiment records.
- Changes to the existing distributed mock-prediction application flow.

## Architecture decision assessment

No service boundary, runtime, protocol, or deployment decision changed. The methodology introduces future requirements only, so no ADR was created.

## Verification

- Confirmed the documentation records all required Phase 3.1 planning topics.
- Confirmed the milestone contains documentation changes only and does not introduce ML implementation artefacts.
