# Data Profile

**Dataset:** BharatFakeNewsKosh v1 (`DSR-001`)  
**Profile basis:** Immutable raw archive, read-only EDA `EDA-2026-07-17-DSR-001-R1`  
**Primary analytical population:** 26,232 declared rows in workbook sheet `A`

## Dataset identity and scope

| Field | Profile |
| --- | --- |
| Raw artefact | `ml/data/raw/bharatfakenewskosh-v1.zip` (one XLSX member) |
| Raw release | Kaggle `man2191989/bharatfakenewskosh`, version 1 / Initial release |
| Licence scope | CC BY-NC 4.0 recorded for non-commercial research; source-content and downstream rights remain constrained. |
| Text unit observed | `Statement` and `News Body` fields; whether either represents a full original article remains unverified. |
| Raw labels | Exact values `True` and `False`; no canonical mapping is approved. |
| Source languages | Nine source-provided language values. |
| Auxiliary content | `Sheet1` has 908 headerless rows; `Sheet3` is empty. |

## Declared primary schema

The sheet has 19 columns: `id`, `Author_Name`, `Fact_Check_Source`, `Source_Type`, `Statement`, `Eng_Trans_Statement`, `News Body`, `Eng_Trans_News_Body`, `Media_Link`, `Publish_Date`, `Fact_Check_Link`, `News_Category`, `Language`, `Region`, `Platform`, `Text`, `Video`, `Image`, and `Label`.

Fields are profiled as raw source fields. They are not renamed into the planned unified schema and none is an approved model feature.

## Text profile

| Measure | `News Body` | `Statement` |
| --- | ---: | ---: |
| Literal missing | 0 | 0 |
| Character count: median / mean / maximum | 198 / 270.75 / 836 | 79 / 81.59 / 230 |
| Raw token count: median / mean / maximum | 62 / 83.43 / 264 | 24 / 24.02 / 89 |
| 95th percentile raw tokens | 197 | 41 |
| IQR high-outlier rows | 0 | 65 |
| Case-preserving vocabulary size | 37,169 | 24,284 |

The combined case-preserving raw vocabulary is 43,929 forms. These are descriptive lexical measurements, not a tokenised training corpus.

## Labels, language, and sources

| Dimension | Raw profile |
| --- | --- |
| Label | `True`: 15,913 (60.66%); `False`: 10,319 (39.34%); unexpected values: 0 |
| Language | English 10,010; Tamil 4,757; Hindi 4,192; Malayalam 2,723; Gujarati 2,205; Odia 1,268; Bangla 584; Assamese 409; Telugu 84 |
| Fact-check source | 19 distinct values; largest, Factcrescendo.com, has 10,903 rows (41.56%) |
| Source type | `IFCN`: 23,826 (90.83%); `Non_IFCN`: 2,406 (9.17%) |
| Categories | 83 exact raw values; Politics 10,436, Fact Check 4,807, and Society 4,565 account for 75.51% together |
| Platform | Eight exact values, including case/spelling variants such as `Twitter`/`twitter` and `Facebook`/`facbook`/`Facbook` |

## Time and formula profile

| Topic | Raw profile | Limitation |
| --- | --- | --- |
| `Publish_Date` | 13,728 typed or unambiguous ISO-like dates, spanning 2012-09-10 to 2022-12-07 | 12,504 nonblank values are not parsed by the conservative rule: 590 ambiguous numeric strings and 11,914 other strings. |
| Formula cells | `Region` 22,769; `News_Category` 316; `Text` 180; `Video` 132; `Image` 122; `Media_Link` 47 | Formula semantics and cached-value provenance require review before a derivative uses them. |
| Text representation | XML/relationship members pass UTF-8 decoding; isolated diagnostic indicator in one row of each body field | Native non-ASCII characters are expected. The diagnostic is not a decoding action or proof of a global defect. |

## Profile constraints

- The profile does not infer a label's truth meaning, a publisher's identity, or a record's language from text.
- It keeps original-language and English-translation fields distinct.
- It does not represent `Sheet1` as unused or invalid; its relationship to sheet `A` is simply undocumented.
- All findings remain attached to the raw archive through [EDA metadata](../../ml/metadata/bharatfakenewskosh-v1.eda.json), not to a cleaned dataset.
