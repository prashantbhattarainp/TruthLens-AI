# Generalization Study - Phase 4.5

## Available evidence

The frozen validation derivative has 16 `fact_check_source` values but no publisher field. It therefore cannot evaluate previously unseen publishers. Phase 4.5 reports source-stratified validation behaviour only; it does not retrain leave-one-source-out models because that would violate the frozen candidate boundary.

`publish_date` is absent. `publish_date_raw` supports descriptive year buckets, but it includes missing/unparseable values and cannot support a properly separated temporal train/test split.

| Temporal appearance slice | Support | Macro F1 | MCC |
| --- | ---: | ---: | ---: |
| Missing or unparseable date | 289 | 0.4585 | -0.0460 |
| Through 2020 | 432 | 0.5117 | 0.0489 |
| 2021 | 304 | 0.5824 | 0.1888 |
| 2022 or later | 436 | 0.5781 | 0.1649 |

Length and language-appearance results are recorded in [BIAS_AND_FAIRNESS.md](BIAS_AND_FAIRNESS.md). The existing source, temporal, and topic variations show that validation performance is inconsistent across observed cohorts. They are not external generalization estimates because they reuse one frozen validation set and its source/template limitations.

## Required future study

An external generalization claim needs publisher identity, publication time, source-balanced new data, a preregistered temporal or leave-source-out protocol, and a new release decision. The current champion must not reuse its protected test for that purpose.
