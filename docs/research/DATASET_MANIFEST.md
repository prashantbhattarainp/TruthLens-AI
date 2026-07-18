# Dataset Manifest: TL-BFNK-EN-v1.0

**Manifest type:** Governance and experiment-readiness manifest; no derivative file is created by this document.  
**Status:** Frozen for future Phase 3 materialization and experiments.  
**Machine-readable counterpart:** [`ml/metadata/truthlens-bfnk-en-v1.0.manifest.json`](../../ml/metadata/truthlens-bfnk-en-v1.0.manifest.json)

## Identity and provenance

| Field | Frozen value |
| --- | --- |
| Research dataset ID / version | `TL-BFNK-EN-v1.0` |
| Registry ID / role | `DSR-001` / sole Phase 3 primary experimental source |
| Parent acquisition ID | `indian-digital-media-2026.07.17-r1` |
| Source release | BharatFakeNewsKosh, Kaggle version 1 (Initial release) |
| Raw archive | `ml/data/raw/bharatfakenewskosh-v1.zip` |
| Raw archive SHA-256 | `330feb9b24b48f49c4113ca6de87695f1bd0821d29361a86e2b27ab35a77c69c` |
| Inner workbook SHA-256 | `6b3435a29eba8df3d7ac5d027808277e4d1a67189beea052aea2298eb8a61fb8` |
| Official source | [Kaggle data card](https://www.kaggle.com/datasets/man2191989/bharatfakenewskosh) |
| Source publication | [Singh et al., SmartCom 2023](https://doi.org/10.1007/978-981-99-0838-7_24) |
| Licence | CC BY-NC 4.0; research-only boundary and third-party-content limitations retained |

## Cohort and field contract

| Contract element | Frozen rule |
| --- | --- |
| Population | Worksheet `A` only; raw `Language == "English"` exactly. |
| Text unit | One fact-checked news item represented by source `Statement` and `News Body`; neither field is asserted to be a full original article. |
| Permitted source text | Native source `Statement` and `News Body` only. Translation fields are excluded. |
| Labels | `LMAP-BFNK-v1.0`: `True -> REAL (0)` and `False -> FAKE (1)`. |
| Excluded raw workbooks/sheets | All `Sheet1` and `Sheet3` content; no header/label contract supports their inclusion. |
| Exact conflict exclusion | Exclude every exact `Statement` + `News Body` cluster containing both mapped labels. |
| Duplicate grouping | `DUP-BFNK-v1.0`; clusters cannot cross partitions. |
| Source / time | Audit fields only; never model features. |

## Release statistics

| Population | Rows | REAL / raw `True` | FAKE / raw `False` | Notes |
| --- | ---: | ---: | ---: | --- |
| Immutable primary sheet `A` | 26,232 | 15,913 (60.66%) | 10,319 (39.34%) | Release-specific raw counts; differ from public landing-page totals. |
| English eligibility population | 10,010 | 6,046 (60.40%) | 3,964 (39.60%) | Exact raw language value `English`; 16 fact-check sources. |
| Prospective Phase 3 cohort | 9,732 | 5,907 | 3,825 | English population less 278 rows in 139 exact text-pair clusters with conflicting labels. This count is a frozen eligibility rule, not a materialized file. |

The prospective class counts follow directly from the conflict-cluster rule: each of the 139 exact-pair conflicts has one `True` and one `False` row. A future materialization must reconcile its included/excluded counts to this manifest before preprocessing.

## Quality and leakage statistics retained in the manifest

| Measure | Frozen evidence and disposition |
| --- | --- |
| Exact pair duplicates, English population | 671 clusters / 671 extra rows; retain only within one duplicate group. |
| Repeated English bodies | 734 clusters / 1,562 extra rows; largest cluster 821; group, do not treat as independent across partitions. |
| Exact text-pair conflicts, English population | 139 clusters / 278 rows; exclude from `TL-BFNK-EN-v1.0`. |
| English sources | 16; India Today is largest with 2,312 rows. Source is audited and balanced where feasible, never a model feature. |
| Formula exposure | None of the selected identity, text, label, source, or date fields are formula-backed. |
| Date usability | Raw date values retained; no temporal split because a large portion is ambiguous/unparsed by the existing conservative audit. |

## Frozen split configuration

| Field | Value |
| --- | --- |
| Split identifier | `SPL-TL-BFNK-EN-v1.0` |
| Ratios | Train 70%, validation 15%, test 15% by included row count, subject to indivisible duplicate clusters. |
| Seed | `42` |
| Allocation | Deterministic grouped-stratified three-way allocation over `duplicate_cluster_id`, stratified on canonical binary label. Cluster assignments are atomic. |
| Source constraint | No source-based allocation constraint; report source/class counts in every partition. Do not use source as a model feature or claim unseen-source generalisation. |
| Temporal constraint | None; raw dates are audit-only and no chronological claim is permitted. |
| Test-access policy | Test partition is created once, checksummed, and inaccessible to preprocessing choice, feature choice, CV, hyperparameter selection, thresholding, or model selection. |
| CV policy | Five-fold `stratified_group_kfold`, seed 42, on the frozen training partition only. Validation supports selection; test is used once after selection is frozen. |

Phase 3.8 materialized the derived r2 split beneath `ml/data/derived/TL-BFNK-EN-v1.0/DER-20260718-r2/`. Its `split-documents.jsonl` SHA-256 is `978931f41ece219a3e3e27d052cfb35dfe557af02a604d6f913d4ad8e6ca59ad`; it contains IDs, duplicate-group IDs, labels, partitions, source/date audit fields, and no group crossing. Its parent remains this frozen manifest and it must not be overwritten.

## Frozen pipeline identities

| Stage | Version/configuration | Canonical SHA-256 |
| --- | --- | --- |
| Label mapping | `LMAP-BFNK-v1.0` | Defined in this manifest and [Dataset Governance](DATASET_GOVERNANCE.md). |
| Duplicate policy | `DUP-BFNK-v1.0` | Defined in [Dataset Governance](DATASET_GOVERNANCE.md). |
| Preprocessing | `conservative-en-v1.json`, pipeline `1.0.0` | `52ce7a78fa4892adf302e3c4dcc0633aebc9dfb55ca4347647f1d1cd87d3976f` |
| Baseline feature representation | `tfidf-unigram-bigram-v1.json`, pipeline `1.0.0` | `fdec84fd3755a6cd4be8dfc3c75689afd55d5ba2f918b90944796c71cd648938` |
| Cross-validation experiment config | One new `*-bfnk-en-v1.json` grouped-CV config per approved baseline | LR `b66fde370a7a0619ca4309bfd4d23524d1b836bca0b578de4b7393c6f8ab1288`; MNB `e847864d3f71f192eead03287c21d1233cdac7dc41a47a86c443a16363d24137`; Linear SVM `6de45ac063452b408b7fb42cbaec42a53d1d2ac3a56f5df9f27bbf9e33503653`. |

## Release boundary

FactDrill (DSR-002) and the COVID-19 Fake News Dataset (DSR-003) remain deferred and are not part of `TL-BFNK-EN-v1.0`. This manifest is not a licence grant for deployment, a trained model, an experiment result, or external evaluation evidence.
