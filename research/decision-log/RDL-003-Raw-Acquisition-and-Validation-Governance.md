# RDL-003: Raw Acquisition and Validation Governance

**Status:** Accepted for Phase 3.3  
**Date:** 2026-07-17  
**Related documents:** [Dataset Acquisition Report](../../docs/research/DATASET_ACQUISITION_REPORT.md), [Data Validation Report](../../docs/research/DATA_VALIDATION_REPORT.md), [Data Integrity Report](../../docs/research/DATA_INTEGRITY_REPORT.md)

## Context

Phase 3.2 selected BharatFakeNewsKosh (DSR-001) conditionally as the primary research source. The Phase 3.3 instruction authorised implementation of the approved acquisition strategy. Its current Kaggle release identifies version 1 and declares CC BY-NC 4.0. FactDrill and the COVID-19 Fake News Dataset still have no explicit licence evidence, so their acquisition gates remain closed.

## Decisions

1. Acquire BharatFakeNewsKosh version 1 once as the immutable archive `ml/data/raw/bharatfakenewskosh-v1.zip`; raw data is git-ignored and never modified or re-saved.
2. Store reproducibility evidence separately in tracked `ml/metadata/` JSON records and research reports. The archive and its inner XLSX receive SHA-256 checksums and parent identifiers.
3. Treat the acquisition as non-commercial research use under the declared CC BY-NC 4.0 licence. Source-content, translation, platform, derivative, and deployment rights remain stated limitations; raw content is not redistributed through the repository.
4. Record validation as read-only. No transformation, label conversion, cleaning, duplicate removal, split, or model action is permitted in this milestone.
5. Retain the observed raw label counts (15,913 True, 10,319 False), formula cells, and auxiliary sheets exactly as found. Their disagreement with public dataset statistics and their provenance must be resolved before a Phase 3.4 derivative or split is approved.
6. Defer DSR-002 and DSR-003. Their role selection does not become acquisition permission without explicit terms and evidence.

## Consequences

- The project has one identifiable raw research artefact but no cleaned, mapped, split, or model-ready dataset.
- Integrity checks can prove that later work used the same archive; they cannot prove label validity or source rights.
- Phase 3.4 begins with documented review of the raw-release discrepancies, not silent correction of them.
- The requested `ml/data/raw/` location is the governed raw-data root for this acquisition; it complements rather than alters the existing `ml-service/` runtime boundary.

## Architecture impact

None. The data-governance directory does not change the public API, service boundary, runtime, deployment architecture, or current mock inference flow. No ADR is created.
