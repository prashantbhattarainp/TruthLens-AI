# Data Card - TruthLens Transformer Benchmark Input

**Scope:** Phase 4.2 input record for the already frozen research derivative.  
**Status:** No new dataset, collection, relabelling, split, or preprocessing derivative was created.

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

## Limitations

The source, language, temporal, template, duplicate, and label limitations recorded during Phase 3 still apply. A public transformer repository’s pretraining language coverage does not make the derivative multilingual, repair label noise, or remove source/template sensitivity. Any data-scope expansion requires a new dataset/model version and governed decision.
