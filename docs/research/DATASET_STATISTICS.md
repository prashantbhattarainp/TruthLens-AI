# Dataset Statistics

**Dataset:** BharatFakeNewsKosh v1 (`DSR-001`)  
**Mode:** Read-only aggregation of raw sheet `A`; no rows were added, removed, or altered.

## Sample and label statistics

| Statistic | Value |
| --- | ---: |
| Primary samples | 26,232 |
| Raw `True` labels | 15,913 (60.66%) |
| Raw `False` labels | 10,319 (39.34%) |
| `True`:`False` ratio | 1.54:1 |
| Unexpected raw label values | 0 |
| Dataset-wise distribution | One acquired dataset: 26,232 primary rows |

The raw labels have not been mapped to the canonical REAL/FAKE convention. The distribution differs from the public release description and remains subject to `VAL-001` reconciliation.

## Text measurements

| Field | Count | Min | Q1 | Median | Mean | Q3 | P95 | P99 | Max |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `News Body` characters | 26,232 | 2 | 144 | 198 | 270.75 | 388 | 549 | 603 | 836 |
| `Statement` characters | 26,232 | 18 | 68 | 79 | 81.59 | 92 | 119 | 143 | 230 |
| `News Body` raw tokens | 26,232 | 1 | 28 | 62 | 83.43 | 134 | 197 | 220 | 264 |
| `Statement` raw tokens | 26,232 | 2 | 14 | 24 | 24.02 | 32 | 41 | 52 | 89 |

Vocabulary sizes are 37,169 raw forms for `News Body`, 24,284 for `Statement`, and 43,929 combined. Tokens preserve original case and forms; high-frequency-token results have no stop-word removal.

## Missingness and formula cells

Every one of the 19 declared primary columns has 0 blank/exact-empty cells and 0 whitespace-only nonempty strings. This includes identifiers, labels, the five text-related fields, URLs, date, source, language, category, region, platform, and media fields.

| Formula-bearing raw column | Formula cells | Share of primary rows |
| --- | ---: | ---: |
| `Region` | 22,769 | 86.80% |
| `News_Category` | 316 | 1.20% |
| `Text` | 180 | 0.69% |
| `Video` | 132 | 0.50% |
| `Image` | 122 | 0.47% |
| `Media_Link` | 47 | 0.18% |

## Exact duplicate statistics

| Exact raw comparison | Distinct values/clusters | Extra duplicate rows | Largest cluster |
| --- | ---: | ---: | ---: |
| `id` | 26,232 values | 0 | 0 |
| Complete 19-field row | 26,232 values | 0 | 0 |
| `Statement` | 1,233 duplicate clusters | 1,237 (4.72%) | 3 |
| `News Body` | 929 duplicate clusters | 1,872 (7.14%) | 873 |
| `Statement` + `News Body` pair | 858 duplicate clusters | 858 (3.27%) | 2 |

These are exact stored-value counts only. They do not assess near duplicates, translations, or semantic equivalence.

## Source, language, and category statistics

| Fact-check source (top five) | Rows |
| --- | ---: |
| Factcrescendo.com | 10,903 |
| Alt News | 3,343 |
| India Today | 2,495 |
| Boomlive.in | 2,272 |
| Youturn.in | 1,903 |

There are 19 exact `Fact_Check_Source` values. The top source accounts for 41.56% of the primary population; the raw-source HHI is 0.21.

| Language | Rows | Share |
| --- | ---: | ---: |
| English | 10,010 | 38.16% |
| Tamil | 4,757 | 18.13% |
| Hindi | 4,192 | 15.98% |
| Malayalam | 2,723 | 10.38% |
| Gujarati | 2,205 | 8.41% |
| Odia | 1,268 | 4.83% |
| Bangla | 584 | 2.23% |
| Assamese | 409 | 1.56% |
| Telugu | 84 | 0.32% |

| Top raw news category | Rows |
| --- | ---: |
| Politics | 10,436 |
| Fact Check | 4,807 |
| Society | 4,565 |
| Society Viral | 953 |
| Religion | 778 |
| national | 453 |
| Coronavirus | 429 |
| Health | 414 |
| International | 386 |
| Social Viral | 380 |

## Temporal statistics

| Date profile | Rows |
| --- | ---: |
| Typed Excel date/time | 13,728 (52.33%) |
| Ambiguous numeric date string | 590 (2.25%) |
| Other nonblank date string | 11,914 (45.42%) |
| Literal missing date | 0 |

The parseable subset spans 2012-09-10 through 2022-12-07. Its largest observed years are 2022 (4,225), 2020 (3,533), 2021 (3,249), and 2019 (2,290). This is not a complete temporal distribution until the unparsed representations are governed.

The complete aggregate record is [bharatfakenewskosh-v1.eda.json](../../ml/metadata/bharatfakenewskosh-v1.eda.json).
