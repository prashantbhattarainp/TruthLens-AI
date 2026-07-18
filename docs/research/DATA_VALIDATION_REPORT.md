# Dataset Validation Report

**Dataset:** BharatFakeNewsKosh v1 (DSR-001)  
**Validation mode:** Read-only against `ml/data/raw/bharatfakenewskosh-v1.zip`  
**Status:** Container and required-field checks pass; findings were carried into the Phase 3.4 raw EDA and remain open before any derivative or split.

## Results

| Check | Result | Evidence |
| --- | --- | --- |
| Raw archive exists | Pass | One ZIP archive exists at the recorded raw path. |
| File count / duplicate filenames | Pass | One outer XLSX member; no duplicate names in the outer or inner ZIP containers. |
| Corruption | Pass | ZIP integrity tests passed and the XLSX loaded in read-only mode. |
| Encoding | Pass | All XML and relationship files in the XLSX container decoded as UTF-8. |
| Primary sheet | Pass | Sheet `A` has 19 declared columns and 26,232 nonempty data rows. |
| Required raw fields | Pass | `id`, `Statement`, `News Body`, `Eng_Trans_News_Body`, `Label`, `Language`, and `Fact_Check_Link` are present. |
| Missing ID / duplicate ID | Pass | 0 missing IDs and 0 duplicate IDs in sheet `A`. |
| Missing label | Pass | 0 missing labels. |
| Missing text | Pass | 0 missing values in `Statement`, `Eng_Trans_Statement`, `News Body`, `Eng_Trans_News_Body`, and `Text`. |
| Empty data rows | Pass | 0 empty rows in sheet `A`. |
| Label distribution | Review required | Raw sheet contains 15,913 `True` and 10,319 `False`, not the public record's stated 13,721 legitimate and 12,511 fraudulent items. |
| Formula-derived cells | Review required | Formula cells occur in `Region` (22,769), `Text` (180), `Video` (132), `Image` (122), `Media_Link` (47), and `News_Category` (316). |
| Auxiliary worksheets | Review required | `Sheet1` contains 908 headerless nonempty rows; `Sheet3` is empty. |

## Raw schema observed

`id`, `Author_Name`, `Fact_Check_Source`, `Source_Type`, `Statement`, `Eng_Trans_Statement`, `News Body`, `Eng_Trans_News_Body`, `Media_Link`, `Publish_Date`, `Fact_Check_Link`, `News_Category`, `Language`, `Region`, `Platform`, `Text`, `Video`, `Image`, `Label`.

## Interpretation and carried-forward gate

The checks establish that the downloaded artifact is readable and has the expected principal fields. They do **not** establish that the public statistics, labels, formula outputs, auxiliary-sheet records, or source units are scientifically ready. Phase 3.4 documented these issues without modifying the raw release; [EDA Report](EDA_REPORT.md) and [Data Quality Assessment](DATA_QUALITY_ASSESSMENT.md) carry the readiness gate forward. No preprocessing, label mapping, derivative, split, or modelling is authorised by this validation record.

Machine-readable evidence is in [bharatfakenewskosh-v1.validation.json](../../ml/metadata/bharatfakenewskosh-v1.validation.json).
