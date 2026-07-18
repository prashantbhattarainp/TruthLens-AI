# Exploratory Data Analysis Report

**Phase:** 3 - Milestone 3.4  
**Dataset:** BharatFakeNewsKosh v1 (`DSR-001`)  
**Dataset ID:** `indian-digital-media-2026.07.17-r1`  
**Analysis ID:** `EDA-2026-07-17-DSR-001-R1`  
**Status:** Complete as a read-only raw-data assessment; no derivative, label mapping, split, preprocessing, or model is approved.

## Scope and reproducibility

The analysis read `ml/data/raw/bharatfakenewskosh-v1.zip` in memory from its sole XLSX member. The archive SHA-256 was identical before and after the run: `330feb9b24b48f49c4113ca6de87695f1bd0821d29361a86e2b27ab35a77c69c`. The workbook member SHA-256 remains `6b3435a29eba8df3d7ac5d027808277e4d1a67189beea052aea2298eb8a61fb8`.

The reproducible, read-only procedure is [run_phase_3_4_eda.py](../../scripts/research/run_phase_3_4_eda.py). It records aggregate results only in [bharatfakenewskosh-v1.eda.json](../../ml/metadata/bharatfakenewskosh-v1.eda.json) and emits vector SVG figures. It does not extract, save, filter, normalise, decode, deduplicate, or modify raw records.

### Analytical population

| Raw workbook area | Observed content | Treatment in this report |
| --- | ---: | --- |
| Sheet `A` | 1 header + 26,232 nonempty data rows | Descriptive primary population only. |
| `Sheet1` | 908 nonempty, headerless rows | Retained as undocumented auxiliary content; not treated as data records. |
| `Sheet3` | 0 nonempty rows | Retained as an empty source worksheet. |

This definition does not exclude, alter, or approve records. It is a transparent reporting boundary for a worksheet that is the only one with declared fields and raw labels.

### Measurement rules

- Text statistics use the source fields `News Body` and `Statement` exactly as stored.
- A word-like token is a case-preserving Unicode match of `[^\W_]+(?:['’][^\W_]+)*`. No lowercasing, stop-word removal, stemming, lemmatisation, translation, filtering, or text rewrite occurred.
- Formula locations are counted from the raw formula workbook. Descriptive values use cached displayed values only; formulas were not recalculated.
- Missingness means a blank cell or an exact empty string. Whitespace-only nonempty strings are reported separately; none occurred.
- Duplicate analysis is exact raw equality only. It does not claim to find semantic or near duplicates and no row is removed.
- Date analysis accepts typed Excel dates and unambiguous ISO-like values. Ambiguous or other nonblank strings remain unparsed instead of being guessed.

## EDA summary

| Finding | Evidence | Research interpretation |
| --- | --- | --- |
| Class distribution | 15,913 raw `True` (60.66%) and 10,319 raw `False` (39.34%); ratio 1.54:1 | Moderate raw imbalance. The values are syntactically clean but still have no approved semantic mapping to REAL/FAKE. |
| Public-statistic discrepancy | Raw counts differ from the public description of 13,721 legitimate and 12,511 fraudulent items | `VAL-001` remains a high-severity reconciliation gate before any label mapping, split, or modelling. |
| Text coverage | All 26,232 primary rows have literal values in both text fields | Presence is strong, but `News Body` is compact (median 62 raw tokens; maximum 264), so it must not automatically be described as a full original article. |
| Language coverage | Nine source-provided values; English is 10,010 rows (38.16%) | The corpus is multilingual. A future English-first derivative must establish native-English eligibility and must not silently substitute translated fields. |
| Exact duplicates | 0 duplicate IDs and complete rows; 1,872 extra duplicate `News Body` rows and 858 extra duplicate `Statement`+`News Body` rows | Text repetition is material even though record IDs are unique. It is a leakage risk requiring a future documented cluster/group rule. |
| Source concentration | 19 fact-check sources; Factcrescendo.com supplies 10,903 rows (41.56%); HHI = 0.21 | Source bias is plausible. Future evaluation must preserve source-aware reporting and prevent group leakage. |
| Temporal usability | 13,728 dates (52.33%) are typed or unambiguous; 12,504 nonblank dates remain unparsed | Raw date presence is not equivalent to an auditable time variable. A format policy is required before a temporal split or trend claim. |
| Raw categorical consistency | 83 exact `News_Category` values and visibly separate platform spellings/cases | Raw categories are informative but not a controlled vocabulary. Any later canonicalisation needs a versioned mapping that retains the raw value. |
| Formula-derived content | Formula cells occur in six columns, especially `Region` (22,769; 86.80%) | Cached values may be used only after formula provenance and the permitted representation are documented. |
| Text representation | XLSX XML is UTF-8-decodable; the diagnostic signature appears in one `News Body` and one `Eng_Trans_News_Body` record (0.004% each) | There is no evidence of a corpus-wide transcoding failure. The isolated indicator remains a small review item; no decoding was applied. |

## Figures

The [figures directory](figures/README.md) contains 14 accessible, editable SVG figures. The required visualisations cover labels, workbook composition, text length, word and character distributions, missingness, exact duplicates, source, raw tokens, language, category, publication year, and the encoding diagnostic.

## Research observations

1. The raw `True`/`False` field is complete and has no unexpected value, but it cannot yet be interpreted as the project's REAL/FAKE target. The unreconciled release-statistic discrepancy prevents that inference.
2. `News Body` is consistently populated but relatively short. Its observed length supports the more cautious description “source body field” rather than an unverified claim of full-article availability.
3. Exact duplicate full rows are absent, which is positive for record identity, but repeated body fields are common and one raw body cluster contains 873 rows. A row-level random split would therefore be unsafe.
4. English is the largest individual language cohort but not a majority. The multilingual raw corpus remains valuable for profiling, while the planned primary claim remains limited to a later verified native-English derivative.
5. Source, category, platform, and time fields expose plausible selection bias. They are audit and split-control variables, not default model features.
6. The structural container and literal-missingness checks are strong. Scientific readiness remains constrained by label provenance, formula provenance, auxiliary-sheet purpose, text-unit fit, duplicate leakage, source concentration, and date representation.

## Conclusion

The raw release is structurally readable, complete in the primary declared fields, and now descriptively profiled. It is **conditionally usable for continued governance work, not yet model-ready**. The next work must resolve the open findings through an approved, versioned derivative protocol; this milestone intentionally creates neither that derivative nor a split.

Related reports: [Data Profile](DATA_PROFILE.md), [Dataset Statistics](DATASET_STATISTICS.md), [Data Quality Assessment](DATA_QUALITY_ASSESSMENT.md), and [Preprocessing Recommendations](PREPROCESSING_RECOMMENDATIONS.md).
