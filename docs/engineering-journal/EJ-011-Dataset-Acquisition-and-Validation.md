# EJ-011: Dataset Acquisition and Validation

**Phase:** 3  
**Milestone:** 3.3 - Dataset Acquisition, Validation and Data Governance  
**Date:** 2026-07-17  
**Status:** Complete

## Objective

Acquire only the approved primary source, preserve its raw release immutably, and create reproducible metadata, integrity evidence, and read-only validation records.

## Completed work

- Acquired BharatFakeNewsKosh Kaggle version 1 as `ml/data/raw/bharatfakenewskosh-v1.zip` without extraction or modification.
- Added the requested raw-data ignore rule and structured acquisition, validation, integrity, and registry metadata in `ml/metadata/`.
- Verified the outer ZIP and inner XLSX containers, UTF-8 XML encoding, source-workbook loadability, required columns, IDs, labels, text fields, empty rows, and duplicate filenames.
- Created [Dataset Acquisition Report](../research/DATASET_ACQUISITION_REPORT.md), [Data Validation Report](../research/DATA_VALIDATION_REPORT.md), and [Data Integrity Report](../research/DATA_INTEGRITY_REPORT.md), and updated the registry and provenance protocol.
- Added [RDL-003](../../research/decision-log/RDL-003-Raw-Acquisition-and-Validation-Governance.md) to record raw-data storage, immutability, and validation gates.

## Findings retained without modification

- The 26,232 raw rows contain 15,913 `True` and 10,319 `False` labels, which differs from the public description.
- The primary data sheet contains formula cells in six metadata/content columns.
- A second sheet contains 908 nonempty headerless rows and a third sheet is empty.

## Deliberately not implemented

- No extraction into a working dataset, preprocessing, cleaning, duplicate removal, label mapping, feature engineering, split generation, notebook, training, or evaluation.
- No acquisition of FactDrill or the COVID-19 Fake News Dataset because their licence gates remain unresolved.
- No changes to the mock prediction application flow.

## Architecture decision assessment

The new raw-data governance location and metadata records do not change software architecture. No ADR was created.
