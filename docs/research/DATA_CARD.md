# Data Card - TruthLens Frozen Research Derivative

**Scope:** Final Phase 4 record for the already frozen research derivative.
**Status:** No new dataset, collection, relabelling, split, translation, or preprocessing derivative was created in Phase 4.

## Dataset identity

| Field | Value |
| --- | --- |
| Dataset version | `TL-BFNK-EN-v1.0` |
| Derivative | `DER-20260718-r2` |
| Split | `SPL-TL-BFNK-EN-v1.0` |
| Derivative SHA-256 | `978931f41ece219a3e3e27d052cfb35dfe557af02a604d6f913d4ad8e6ca59ad` |
| Records | 9,732: train 6,813; validation 1,461; protected test 1,458 |
| Labels | `REAL=0` (5,907), `FAKE=1` (3,825) |
| Model input | Frozen `raw_text`; the selected transformer tokenizer performs only model-native tokenization |

The benchmark runner rejects a derivative hash or partition-count mismatch before it downloads or trains a model. Existing data lineage, duplicate controls, source fields, and label-mapping governance remain in the Phase 3 research records; this card does not replace them.

## Intended and unsuitable uses

This derivative supports bounded internal research into a binary classification signal. It does not establish factual truth, a real-world reliability score, user intent, demographic attributes, political orientation, or comprehensive Indian-media coverage. It must not be used as a fact-checking corpus or as evidence that a text is true or false outside the recorded research protocol.

## Phase 4.2 handling and safeguards

The current transformer experiment reads the existing train, validation, and protected-test partitions without changing membership. Token budgets can truncate model input but never rewrite the stored text. Error cohorts use overlapping keyword/length heuristics only after prediction; they neither alter labels nor train a model. Raw text is not copied into tracked reports; ignored artifacts retain only the minimum run evidence, aggregate counts, and local identifiers necessary for audit.

## Phase 4.3 handling

Phase 4.3 reused only the frozen validation records for ensemble evaluation. Existing Phase 3.9 component pipelines received the same frozen preprocessing; the stacker learned only from their aligned train-only OOF scores. Test records were excluded from model transformation, prediction, label use, and selection. Ensemble error analysis retains aggregate source/cohort counts only. No data version, labels, split membership, or text derivative changed.

## Phase 4.4 multilingual handling

Phase 4.4 does not create a Hindi or Hinglish dataset. The existing English derivative was scanned in memory for script/marker appearance and only the frozen validation partition was passed to the unchanged champion for descriptive compatibility slices. The runner verifies the full derivative hash and counts all partitions for integrity, but does not retain, transform, label, or predict train/test records. The derivative contains 59 Devanagari-bearing records overall (40 train, 9 validation, 10 protected test) and only 2 conservative Hinglish-heuristic validation records; neither is a language-labelled benchmark cohort.

`ml/fixtures/multilingual/phase-4-4-language-probe.json` is a manually authored 12-record language-processing fixture. It contains expected language labels only; it has no REAL/FAKE target, no translated derivative text, and no role in training, model scoring, or selection. Ignored Phase 4.4 artifacts retain aggregate counts/metrics and checksums only. No external multilingual source, synthetic fake-news translation/transliteration, label change, or split change occurred.

## Phase 4.5 robustness/reliability handling

Phase 4.5 reuses the frozen validation partition only. The runner verifies the full derivative SHA-256 and split cardinality, then applies the integrity-checked packaged candidate and frozen preprocessing to original and deterministic in-memory stress variants. It records aggregate metrics, group counts, and figure hashes only; raw text, document identifiers, per-record scores, and per-record predictions are excluded from tracked reports and figures. Training/test rows are counted only for split integrity and never retained, transformed, labelled for a model, or predicted.

Date analysis uses `publish_date_raw` descriptive buckets because normalized `publish_date` is absent. Fact-check source is not publisher identity. Topic, language, and length slices are non-training descriptive heuristics. No data source, label, derivative, split, translation, or model training change occurred.

## Limitations

## Phase 4.6 finalization

Phase 4.6 only consolidates the Phase 4 evidence into publication documentation. It does not read the derivative, alter a row, create a release, expose raw text, or change the controls above. The final package continues to describe this dataset as English BFNK-derived and treats the 9 Devanagari-bearing and 2 Hinglish-heuristic validation records as insufficient descriptive appearance slices, never as a multilingual benchmark. See [the reproducibility guide](publication/REPRODUCIBILITY_GUIDE.md) and [threats to validity](publication/THREATS_TO_VALIDITY.md).

The source, language, temporal, template, duplicate, and label limitations recorded during Phase 3 still apply. A public transformer repository’s pretraining language coverage does not make the derivative multilingual, repair label noise, or remove source/template sensitivity. Any data-scope expansion requires a new dataset/model version and governed decision.
