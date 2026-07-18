# Data Provenance Protocol

**Scope:** Data-source and derivative traceability design
**Status:** Approved protocol with recorded DSR-001 acquisition and read-only EDA events; no data derivative exists
**Related documents:** [Dataset registry](DATASET_REGISTRY.md), [Data dictionary](DATA_DICTIONARY.md)

## Purpose

Data provenance establishes where every permitted record came from, how it was received, which version produced it, and which transformations or exclusions produced each later derivative. It allows a reviewer to trace a model result backward to an approved source without treating source identity as a model feature.

## Required provenance chain

Each dataset lineage must be traceable through the following ordered artefacts:

1. Candidate registry record and review evidence.
2. Approved source release, access method, licence/terms snapshot, and acquisition event.
3. Immutable raw-data manifest with source checksums and row-count evidence.
4. Quality-audit report, including missingness, schema, label, duplicate, language, source, and time findings.
5. Derived data versions for any permitted cleaning, deduplication, or label mapping, each with parent identifiers and configuration hashes.
6. Split manifest, including group and partition assignments.
7. Experiment, model, evaluation, and explanation records that reference exact data and split identifiers.

No derivative may omit its parent dataset ID, transformation configuration ID, creation time, creator/process, or checksum.

## Identifiers and immutable records

| Artefact | Planned identifier form | Must record |
| --- | --- | --- |
| Candidate | DSR-### | Registry decision, review evidence, and source release. |
| Dataset release | indian-digital-media-YYYY.MM.DD-rN | Source release, licence snapshot, acquisition event, schema version, row count, checksum. |
| Data derivative | Dataset ID plus stage suffix | Parent ID, stage, configuration hash, inclusion/exclusion counts, checksum. |
| Duplicate cluster | DCL-<dataset-version>-<number> | Method/version, members, review outcome, and partition restriction. |
| Split | SPL-<dataset-version>-<rule-version> | Parent data ID, group rule, seed, partition assignments, class counts, checksum. |
| Experiment | EXP-YYYYMMDD-### | Dataset/split IDs, configuration, code/environment, results, and report. |
| Model | MDL-<algorithm>-<version> | Experiment ID, artefact checksums, model card, and approval state. |

The final identifier syntax may be automated later, but identifiers are immutable once published in a manifest or report.

## Acquisition-event record

Every permitted acquisition must record:

- registry ID, approved source release/version, access URL or method, and date/time in ISO 8601;
- actor or service that performed the acquisition;
- licence and terms snapshot reference, including access and retention restrictions;
- source-file names or stable source identifiers, byte sizes, and SHA-256 checksums;
- content type and whether full text, metadata, identifiers, or approved excerpts were retained;
- known access limitations, exclusions, and errors; and
- an immutable raw-manifest location.

Secrets, account credentials, tokens, and personal information about reviewers must never be included in a public manifest.

## Transformation and exclusion evidence

Each transformation is reproducible only if it records its input version, output version, configuration hash, code revision, seed where applicable, tool/environment version, row counts before and after, and a reason for every exclusion category. Manual reviews require a rule, reviewer role, date, and outcome. Original allowed raw content remains the authoritative source; processed text never replaces it.

## Integrity and retention

SHA-256 checksums protect artefact identity; they do not prove a source is truthful. The project retains evidence only for the period and purpose allowed by the source terms. If a source must be removed, the provenance log retains the removal event and reason while respecting legal deletion requirements. Downstream artefacts that cannot be reproduced after removal are marked accordingly rather than silently retained as valid.

## Prohibited practices

- Do not add an unrecorded source or manually edit a dataset without creating a new derivative version.
- Do not overwrite a manifest, split file, audit report, or checksum after an experiment references it.
- Do not use publisher, URL, verdict, filename, source-record ID, or post-publication correction fields as model input unless a future approved study explicitly evaluates that feature and its leakage implications.
- Do not claim provenance for content whose licence, source release, or acquisition event cannot be demonstrated.

## Recorded acquisition event: DSR-001

| Field | Recorded value |
| --- | --- |
| Registry / dataset / acquisition ID | DSR-001 / `indian-digital-media-2026.07.17-r1` / `ACQ-2026-07-17-DSR-001-R1` |
| Source release | BharatFakeNewsKosh, Kaggle `man2191989/bharatfakenewskosh`, version 1, Initial release |
| Acquisition time | 2026-07-17T23:09:33.932666+05:30 |
| Raw artefact | `ml/data/raw/bharatfakenewskosh-v1.zip` |
| Container member | `bharatfakenewskosh (3).xlsx` |
| Licence evidence | CC BY-NC 4.0 recorded from the public release; non-commercial research scope only |
| Immutable evidence | Archive and inner-workbook SHA-256 checksums in [Integrity Report](DATA_INTEGRITY_REPORT.md) |
| Metadata records | `ml/metadata/bharatfakenewskosh-v1.acquisition.json`, `validation.json`, and `integrity.json` |
| Validation state | Readable and structurally valid; semantic findings require resolution before any derivative is created |

The raw archive was retained without extraction or modification. It is the root parent for any future allowed derivative. DSR-002 and DSR-003 have no acquisition event because their explicit licence gates remain unresolved.

## Recorded read-only EDA event: EDA-2026-07-17-DSR-001-R1

| Field | Recorded value |
| --- | --- |
| Parent dataset / analysis ID | `indian-digital-media-2026.07.17-r1` / `EDA-2026-07-17-DSR-001-R1` |
| Parent artefact | Unchanged `ml/data/raw/bharatfakenewskosh-v1.zip` |
| Procedure | `scripts/research/run_phase_3_4_eda.py`, read-only in-memory workbook inspection |
| Outputs | Aggregate `ml/metadata/bharatfakenewskosh-v1.eda.json` and `docs/research/figures/*.svg` |
| Integrity evidence | Raw archive checksum was identical before and after analysis; no raw extract or derivative was created. |
| Constraints carried forward | Label-count reconciliation, formula provenance, auxiliary-sheet purpose, duplicate clustering, task-unit, source, and time decisions remain open. |

The EDA event is evidence about the raw parent, not a processed-data version. It does not create an inclusion list, label mapping, duplicate cluster, split, or model input.
