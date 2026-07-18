# Dataset Registry

**Scope:** Candidate and approved data-source register
**Status:** DSR-001 is materialized and evaluated as `TL-BFNK-EN-v1.0` r2; all other candidates remain deferred or rejected.
**Owner:** Research governance
**Related documents:** [Dataset selection strategy](DATASET_SELECTION_STRATEGY.md), [Data provenance](DATA_PROVENANCE.md)

## Purpose

This registry makes dataset selection decisions reviewable. It records candidates before acquisition and links an approved candidate to its later dataset card, manifest, and provenance evidence. It is not a data catalogue, download list, or licence substitute.

## Status vocabulary

| Status | Meaning |
| --- | --- |
| Proposed | Candidate recorded; no substantive review or acquisition is authorised. |
| Under review | Mandatory-gate evidence is being assessed. |
| Approved for acquisition | Every gate passed for the stated version and scope; acquisition may begin. |
| Acquired and manifested | Permitted content was acquired and an immutable raw manifest exists. |
| Deferred | Evidence is incomplete or a decision is pending. |
| Rejected | Candidate failed one or more gates; reason is retained. |
| Superseded | A later source version or candidate replaces this entry; historical record remains. |

## Required fields for every candidate

| Field | Description |
| --- | --- |
| Registry ID | Stable identifier, for example DSR-001; never reused. |
| Candidate name and release | Creator-provided name and exact release/version/date if available. |
| Candidate status | One status from the registry vocabulary. |
| Candidate URL or citation | Stable landing page, DOI, repository, or publication citation. |
| Creator/custodian | Organisation or people responsible for the source release. |
| Indian-media relevance evidence | Documented basis for inclusion and known geographic or media gaps. |
| Intended task fit | Text unit, proposed target, and known mismatch with TruthLens AI's research scope. |
| Label provenance summary | Raw labels, verifier or annotator process, ambiguity treatment, and corrections policy. |
| Content and metadata summary | Availability of text, URL, publisher, time, language, topic, and source IDs. |
| Licence and terms evidence | Licence identifier/text, terms snapshot reference, attribution, retention, derivative, and redistribution conditions. |
| Copyright/privacy review | Full-text rights, personal-data/sensitive-content assessment, and handling restrictions. |
| Coverage and quality assessment | Counts if published, class balance, source/language/topic/time coverage, and duplicate risk. |
| Reproducibility assessment | Source-release stability, access method, and ability to create an immutable manifest. |
| Decision and rationale | Approved, deferred, or rejected outcome with evidence-based reasoning. |
| Reviewer and review date | Person or role responsible and ISO 8601 date. |
| Evidence locations | Links to snapshots, notes, dataset card, licence review, and later manifest. |

## Current entries

The following entries use publicly available descriptive evidence only. They do not constitute a dataset card, licence approval, acquisition event, raw manifest, or permission to use data.

| Registry ID | Candidate / release | Status | Intended role or outcome | Licence / terms outcome | Decision rationale | Reviewed on |
| --- | --- | --- | --- | --- | --- | --- |
| DSR-001 | BharatFakeNewsKosh Kaggle v1 | Acquired, governed derivative r2, and baseline-evaluated | `TL-BFNK-EN-v1.0` sole primary Phase 3 source | CC BY-NC 4.0 recorded; source-content and translation rights remain limitations | RDL-008/009 govern the English mapping, duplicate/leakage policy, split, and r2 execution. r1 is invalidated for a missing-cell rendering defect; r2 is the sole result-bearing release. | 2026-07-18 |
| DSR-002 | FactDrill public catalogue release | Deferred | Conditional Indian-context dataset | No explicit reuse licence located | Not acquired: binary mapping, task fit, and rights remain unresolved. | 2026-07-17 |
| DSR-003 | COVID-19 Fake News shared-task release | Deferred | Conditional external evaluation dataset | No explicit dataset licence located | Not acquired: shared-task terms and data rights remain unresolved. | 2026-07-17 |
| DSR-004 | FakeNewsIndia v1 | Deferred | False-only Indian contextual analysis only | No explicit reuse licence located | Lacks a matched TRUE class, so cannot support the binary study | 2026-07-17 |
| DSR-005 | IFND public disclosure | Rejected | Not selected | No explicit archival licence verified | Synthetic fake augmentation and source-class shortcuts conflict with the label/leakage protocol | 2026-07-17 |
| DSR-006 | Multilingual Fake News Detection Dataset, Zenodo v1 | Deferred | Future Indic-language candidate | Explicit reuse licence not located on the record | Promising language coverage but incomplete provenance/label evidence and inconsistent public descriptions | 2026-07-17 |
| DSR-007 | FakeNewsNet current public release | Rejected | Not selected | Complete corpus is explicitly non-distributable | Not Indian; full reproducible corpus is restricted by publisher copyright and Twitter privacy policy | 2026-07-17 |

Evidence links, strengths, weaknesses, score contributions, and the role-separated recommendation are in [Dataset Comparison Matrix](DATASET_COMPARISON_MATRIX.md), [Dataset Scoring](DATASET_SCORING.md), [Dataset Licences](DATASET_LICENSES.md), and [Final Dataset Selection](FINAL_DATASET_SELECTION.md).

## Entry template

| Registry ID | Candidate name/release | Status | Indian-media evidence | Label evidence | Licence/terms outcome | Review outcome | Reviewed on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| To be assigned | To be recorded after candidate discovery | Proposed | Pending | Pending | Pending | Pending | Pending |

The template row is illustrative and is not a dataset candidate.
