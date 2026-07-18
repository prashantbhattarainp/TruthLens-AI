# Dataset Integrity Report

**Dataset:** BharatFakeNewsKosh v1 (DSR-001)  
**Scope:** File identity, container health, and read-only loadability  
**Status:** Pass with semantic-validation findings retained separately.

## Integrity evidence

| Artefact | Format | Size | SHA-256 |
| --- | --- | ---: | --- |
| `ml/data/raw/bharatfakenewskosh-v1.zip` | ZIP | 10,735,967 bytes | `330feb9b24b48f49c4113ca6de87695f1bd0821d29361a86e2b27ab35a77c69c` |
| `bharatfakenewskosh (3).xlsx` inside archive | XLSX | 11,463,031 bytes | `6b3435a29eba8df3d7ac5d027808277e4d1a67189beea052aea2298eb8a61fb8` |

- The outer ZIP passed its integrity test and contains one workbook member with no duplicate filename.
- The XLSX is itself a valid ZIP container with 536 members, no duplicate filenames, UTF-8-decodable XML/relationship members, and successful read-only workbook loading.
- The raw archive is never edited or re-saved. Integrity metadata is stored separately so later stages can verify identity before using any derivative.

Cryptographic integrity does not prove that labels are valid, source rights are complete, formulas are appropriate for research use, or the dataset is free of duplicates. Those separate concerns remain in [Data Validation Report](DATA_VALIDATION_REPORT.md) and the Phase 3.4 gate.

Machine-readable evidence is in [bharatfakenewskosh-v1.integrity.json](../../ml/metadata/bharatfakenewskosh-v1.integrity.json).
