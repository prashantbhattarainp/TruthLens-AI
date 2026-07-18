# EJ-010: Dataset Landscape and Conditional Selection

**Phase:** 3  
**Milestone:** 3.2 - Dataset Landscape Analysis and Final Dataset Selection  
**Date:** 2026-07-17  
**Status:** Complete

## Objective

Evaluate publicly described fake-news dataset candidates against the Phase 3.1 methodology and define a research-grade selection strategy without acquiring or processing any data.

## Completed work

- Reviewed seven candidate resources using public source papers, institutional/repository pages, and licence metadata only.
- Added the [dataset landscape report](../research/DATASET_SELECTION_REPORT.md), [comparison matrix](../research/DATASET_COMPARISON_MATRIX.md), [weighted scoring record](../research/DATASET_SCORING.md), [licence assessment](../research/DATASET_LICENSES.md), and [final conditional selection](../research/FINAL_DATASET_SELECTION.md).
- Registered candidates DSR-001 through DSR-007 in the [Dataset Registry](../research/DATASET_REGISTRY.md), retaining deferred and rejected candidates with their rationale.
- Chose a role-separated conditional strategy: BharatFakeNewsKosh for primary-source review, FactDrill for Indian-context review, and the COVID-19 Fake News Dataset for external-evaluation review.
- Added [RDL-002](../../research/decision-log/RDL-002-Dataset-Landscape-and-Conditional-Selection.md) to preserve the decision and its non-compensatory approval gates.

## Deliberately not implemented

- No dataset download, registration, scraping, access request, or file inspection.
- No preprocessing, schema implementation, label conversion, duplicate detection, data split, notebook, model, or evaluation.
- No change to the existing mock prediction application flow.

## Architecture decision assessment

No software architecture, public API, service boundary, runtime, storage, or deployment decision changed. Dataset roles are research governance only; no ADR was created.

## Verification

- Confirmed every selected role has an explicitly documented intended use and prohibition against pooled training/evaluation.
- Confirmed no candidate is marked approved for acquisition and that missing licence evidence blocks acquisition.
- Confirmed the documentation contains no local dataset, preprocessing, or ML implementation artefact.
