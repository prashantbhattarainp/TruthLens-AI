# Dataset Versioning Policy

**Current frozen version:** `TL-BFNK-EN-v1.0`  
**Status:** Effective for all future Phase 3 experiments.

## Version identity

A TruthLens research dataset version identifies a reproducible experimental population, not merely a downloaded file. Its identity binds the raw parent hash, source release, cohort rules, label mapping, exclusions, duplicate policy, split configuration, and permitted pipeline configurations.

`TL-BFNK-EN-v1.0` is derived only by specification from the immutable DSR-001 archive. Its raw archive is never changed. The version becomes a materialized derivative only when a later authorised run produces a checksummed record-level manifest that reconciles to [Dataset Manifest](DATASET_MANIFEST.md).

## Immutable fields

The following fields are frozen for `TL-BFNK-EN-v1.0`:

- the two raw archive/workbook SHA-256 values and Kaggle version 1 release;
- use of worksheet `A`, exact raw `Language == "English"`, `Statement`, and `News Body`;
- exclusion of translated fields and the two auxiliary worksheets;
- `LMAP-BFNK-v1.0`, including FAKE = 1 and REAL = 0;
- exact-conflict exclusion and `DUP-BFNK-v1.0` grouping rules;
- `SPL-TL-BFNK-EN-v1.0`, including ratios, seed, grouped stratification, source balance checks, and test-access rule;
- the declared preprocessing and baseline TF-IDF configuration identities; and
- the research-only CC BY-NC 4.0 use boundary.

No experiment may patch an immutable field locally, silently substitute a field, rerun a split with altered inputs, or overwrite an existing artifact directory.

## When a new version is required

Create a new version before any change to source release/hash, included languages, text unit, mapping, label correction, row inclusion/exclusion, duplicate threshold or handling, group definition, source/time policy, split ratios/seed/assignment, licence interpretation, or preprocessing/feature configuration that changes the data representation.

Use a new semantic version suffix and retain the old manifest, split, artifacts, and rationale. For example, `TL-BFNK-EN-v1.1` may correct a documented source-label issue; `TL-BFNK-EN-v2.0` may change cohort scope or the duplicate policy. No result across versions is directly comparable unless the changed field is explicitly analysed.

## Required derivative and split records

Before data-bearing execution, the materialization workflow must write new, immutable records containing:

1. parent manifest/version and archive hash;
2. input and output record counts, class counts, inclusion/exclusion reasons, and SHA-256 checksums;
3. raw-to-derivative `record_id` lineage without copying raw text into metadata;
4. duplicate cluster ID, method/configuration identity, and conflict disposition;
5. the split ID, partition assignment, label/source/date audit summaries, seed, algorithm/configuration hash, and split checksum; and
6. the preprocessing, feature, and experiment artifact identifiers that consume the frozen partition.

An invalidated derivative or split is retained with status and reason; it is never replaced in place.
