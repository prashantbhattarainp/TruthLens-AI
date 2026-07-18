# Dataset Governance: Phase 3 Experiment Freeze

**Milestone:** Phase 3.7.5 - Research Dataset Finalization and Experiment Readiness  
**Decision date:** 2026-07-18  
**Frozen research-dataset version:** `TL-BFNK-EN-v1.0`  
**Parent acquisition:** `indian-digital-media-2026.07.17-r1` / DSR-001

## Scope and evidence

`TL-BFNK-EN-v1.0` is the governance specification for the first Phase 3 experimental cohort. Its only source is the immutable BharatFakeNewsKosh Kaggle version 1 archive. It does not create, extract, clean, preprocess, deduplicate, split, vectorize, train, or evaluate data.

The source [Kaggle data card](https://www.kaggle.com/datasets/man2191989/bharatfakenewskosh) describes 26,232 Indian fact-checked news samples, a CC BY-NC 4.0 licence, and legitimate/fraudulent classes. The source [publication](https://doi.org/10.1007/978-981-99-0838-7_24) defines the `Label` field as the annotator judgement true, false, or partially true. The acquired release contains only `True` and `False` values. The archive hash and release-specific raw counts, not a changing landing-page summary, are the identity and statistical authority for this version.

The English-first cohort is specified, not materialized, as:

- source worksheet: `A` only;
- original raw `Language` exactly `English`;
- permitted textual fields: `Statement` and `News Body`, retaining their raw provenance separately before the existing conservative preprocessing pipeline is run;
- raw label included only under the mapping below; and
- all rows from `Sheet1` and `Sheet3` excluded from the experimental population.

The `Eng_Trans_Statement` and `Eng_Trans_News_Body` fields are not eligible input text for this version. This prevents translated text from being presented as native-English content.

## Final semantic label mapping

**Mapping identifier:** `LMAP-BFNK-v1.0`  
**Canonical positive class:** `FAKE = 1`

| Raw source value | Source-defined meaning | Canonical label | Numeric label | Treatment |
| --- | --- | --- | ---: | --- |
| `True` | Annotator true/legitimate judgement | REAL | 0 | Included, subject to all cohort and duplicate rules. |
| `False` | Annotator false/fraudulent judgement | FAKE | 1 | Included, subject to all cohort and duplicate rules. |
| `Partially True` or any equivalent | Source publication describes it as a possible annotation class, but it is absent from this archive | None | None | Excluded if encountered in another release; it requires a new mapping/version decision. |
| Missing, unknown, or changed label | Not present in the acquired archive | None | None | Excluded and recorded; never inferred. |

The source-documentation count (13,721 legitimate and 12,511 fraudulent) differs from the immutable archive's release-specific `True`/`False` count. This is a metadata discrepancy, not evidence that the observed label tokens reverse their documented semantics. `TL-BFNK-EN-v1.0` therefore maps the documented token meanings above and records the archive's observed counts separately. It does not restate the public counts as the count of this release.

## Formula and auxiliary-sheet resolution

The selected experimental fields (`id`, `Statement`, `News Body`, `Label`, `Language`, `Fact_Check_Source`, `Fact_Check_Link`, and `Publish_Date`) contain no formula cells in the raw workbook. Formula cells occur only in non-feature metadata/support fields: `Region`, `News_Category`, `Text`, `Video`, `Image`, and `Media_Link`.

Those formula-backed fields are retained in the immutable archive but are excluded from model input, label mapping, eligibility, and split assignment. They may be copied later only as audit metadata with their raw/cached representation and a new versioned decision; they are not needed to materialize this version.

`Sheet1` has 908 nonempty headerless rows and no mapped label field. It contains 901 fact-check links matching the primary sheet's 901 unique dfrac.org links, so it is treated as unlabelled auxiliary source material rather than an independent population. `Sheet3` is empty. Neither sheet contributes records, labels, or text to `TL-BFNK-EN-v1.0`.

## Duplicate policy

**Policy identifier:** `DUP-BFNK-v1.0`  
**Purpose:** prevent train/validation/test leakage while preserving raw provenance.

| Duplicate category | Detection rule | Required treatment |
| --- | --- | --- |
| Exact text-pair duplicate | Exact raw equality of the ordered pair (`Statement`, `News Body`) after no textual transformation. | Assign one `duplicate_cluster_id`; a cluster must never cross a partition. If the same exact pair has both mapped labels, exclude every row in that cluster from this version and retain an exclusion reason. |
| Exact single-field repeat | Exact raw equality of `News Body` or `Statement` alone. | Retain the rows because a single field can legitimately accompany a different claim/context; cluster them with the pair rule and the near-duplicate rule so related records cannot leak across partitions. |
| Near duplicate | Future deterministic audit over the pair representation using Unicode NFKC, case-folding, HTML-entity decoding, and whitespace collapse for matching only; no stop-word removal, stemming, translation, or training preprocessing. Candidate pairs use 5-character shingles, 128-permutation MinHash with seed `42`, and are confirmed when exact shingle Jaccard similarity is at least `0.90`. Connected components define clusters. | Retain records and assign the component as one group; do not silently delete semantically similar records. Record cross-label components as a data-quality finding and keep the full component in one partition. Any later decision to exclude/relabel a near-duplicate component creates a new dataset version. |
| Cross-dataset duplicate | Apply the same matching protocol to a future separately acquired dataset against this version before it is used. | DSR-002 and DSR-003 are not part of this version and must not be merged. A future external-test overlap is reported and excluded from that external evaluation; adding another source requires a new dataset version. |

Read-only audit evidence for the specified English cohort shows 671 exact text-pair duplicate clusters (671 extra rows) and 139 such clusters with conflicting raw labels. The latter are the only deterministic exclusion category in this version: 278 rows are prospectively excluded when the governed derivative is materialized. No duplicate is removed from the raw archive.

## Source-leakage policy

`Fact_Check_Source`, `Source_Type`, author, URLs, region, platform, category, media flags, and dates are provenance/audit fields only. They must not be concatenated into text, vectorized, used as labels, or used for model feature selection.

Duplicate-cluster membership is the mandatory partition group. Source is a balance and reporting variable, not a source-held-out group for the primary split: the English cohort has only 16 represented fact-check sources and is concentrated (India Today contributes 2,312 rows). A hard source-held-out primary split would make the 70/15/15 cohort unstable and would answer a different unseen-source question.

The split manifest must report source counts and class counts for every partition, but source membership is not an allocation constraint. This keeps the frozen allocation deterministic and avoids pretending that the 16 uneven source groups support a valid source-held-out primary design. No report from this version may claim generalisation to unseen fact-check sources. A source-held-out study is a separate, versioned robustness protocol.

## Temporal-leakage policy

`Publish_Date` is neither a feature nor a split key for this version. Only 13,728 of 26,232 raw dates are typed or conservatively unambiguous; the remaining nonblank values include ambiguous and other strings. A temporal split would therefore create an undocumented selection mechanism.

The future split manifest preserves the raw date value and its parse-status audit field but uses no date-derived value. Results are not evidence of forward-in-time generalisation. A chronological experiment requires a new dataset version with an approved date parser, ambiguity policy, coverage threshold, and time-held-out protocol.

## Licence and use boundary

The dataset card declares CC BY-NC 4.0. This freeze permits non-commercial research processing of the acquired archive within the documented project boundary. It does not resolve third-party publisher, platform, translation, redistribution, deployment, or commercial-use rights. The raw archive remains git-ignored and is never copied into documentation, experiment artifacts, or the public API.

## Freeze rule

The mapping, cohort definition, raw parent hash, duplicate policy, source/temporal policies, and split configuration in [Dataset Manifest](DATASET_MANIFEST.md) are frozen as `TL-BFNK-EN-v1.0`. No Phase 3 experiment may change them. A change to any of them requires a new dataset version under [Dataset Versioning](DATASET_VERSIONING.md).
