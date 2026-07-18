# Data Quality Assessment

**Dataset:** BharatFakeNewsKosh v1 (`DSR-001`)  
**Assessment status:** Historical raw assessment. RDL-008 resolves its listed governance decisions for `TL-BFNK-EN-v1.0`; corrected r2 materialization and Phase 3.8 baseline evidence now exist. This raw assessment remains the source-quality baseline.

## Assessment matrix

| Dimension | Result | Evidence | Required disposition |
| --- | --- | --- | --- |
| File/container integrity | Pass | Archive and inner-workbook hashes reconcile; ZIP and XML checks passed in Phase 3.3. | Retain immutable archive; verify hash before later use. |
| Primary-field completeness | Pass | 0 literal missing/exact-empty cells and 0 whitespace-only values across all 19 declared fields. | Do not equate nonblank values with semantic validity. |
| Label syntax | Pass | Only raw `True` and `False`; 0 missing or unexpected values. | Preserve raw values. |
| Label semantics and count reconciliation | High risk | 15,913/10,319 raw counts conflict with public 13,721/12,511 description. | Resolve `VAL-001` before canonical mapping, split, or model use. |
| Record identity | Pass | 0 missing or duplicate IDs; 0 exact duplicate full rows. | Preserve IDs unchanged. |
| Text repetition and leakage risk | High risk | 1,872 extra exact `News Body` rows; 858 extra exact text-pair rows; one body cluster has 873 rows. | Create approved exact/near-duplicate clusters and group controls before a split; do not delete raw rows. |
| Text-unit fitness | Review required | Body median is 62 raw tokens and maximum 264; field name alone cannot prove full-article content. | Define approved task text unit and report the limitation. |
| Encoding | Pass with isolated review item | XML is UTF-8-decodable; one possible UTF-8-as-Latin-1-like diagnostic indicator in each body field. | Preserve source text; inspect isolated cases only in a future governed derivative. |
| Formula provenance | Medium risk | Formula cells populate six columns, including `Region` for 86.80% of rows. | Document formula meaning and cached-value policy before use. |
| Auxiliary sheets | Medium risk | `Sheet1` has 908 headerless rows; `Sheet3` is empty. | Establish source purpose before expanding the analytical population. |
| Language coverage | Review required | Nine languages; English is 38.16% of raw rows. | Keep language cohorts separate; verify native-English criterion for the initial study. |
| Source bias | Medium-high risk | Top fact-check source is 41.56%; HHI = 0.21. | Use source-aware cohort reporting and leakage controls. |
| Category/platform consistency | Medium risk | 83 exact category values and raw casing/spelling variants in platform/category fields. | Version a future canonical mapping while retaining raw values. |
| Temporal usability | High risk | 47.67% of nonblank dates are unparsed by the conservative date rule. | Establish source-date formats and missing/ambiguous-date policy before temporal analysis or splitting. |
| Class balance | Moderate risk | Raw label ratio is 1.54:1. | Use stratified reporting after semantic mapping is approved; do not rely on accuracy alone. |

## Overall quality judgement

The acquisition has strong structural integrity and unusually complete declared primary cells. That foundation is offset by unresolved research-validity issues: release-statistic/label reconciliation, formula and auxiliary-sheet provenance, repeated text, source concentration, category/platform inconsistency, and incomplete temporal usability.

Accordingly, the release is **not research-ready for a model pipeline**. It is suitable only for the completed raw EDA and for the next governance decisions that create an explicitly versioned derivative. This judgement is intentionally conservative: a complete cell is not automatically a valid label, independent observation, full article, or usable timestamp.

## Risks and mitigations

| Risk | Mitigation before downstream use |
| --- | --- |
| Incorrect label interpretation | Reconcile source release evidence and approve a raw-label mapping register with reviewer, evidence, and exclusions. |
| Train/test leakage through repeated content | Assign exact and near-duplicate clusters; group every cluster into one partition only after the method is approved. |
| Source shortcut learning | Treat source as an audit/group variable, not a default feature; report source cohorts and source-held-out sensitivity where support permits. |
| Overstated English/full-article claim | Select only reviewed native-English records for the planned primary cohort and identify the text unit precisely. |
| Unreliable temporal claims | Preserve raw date values, document parsers/ambiguity treatment, and defer temporal splitting until coverage is sufficient. |
| Loss of provenance | Keep the raw archive immutable; attach all future derivatives to the recorded parent hash, configuration, and row-accounting manifest. |
