# Hindi Dataset Analysis - Phase 4.4

## Dataset finding

No governed Hindi fake-news dataset is present in the repository. The reused `TL-BFNK-EN-v1.0` derivative is English BFNK-derived and must remain described that way. A Unicode scan found 59 Devanagari-bearing records among 9,732 records (0.61%): 40 train, 9 validation, and 10 protected test. Only the 9 validation records were included in the Phase 4.4 descriptive audit; the protected-test records were not retained, transformed, labelled for a model, or predicted.

“Devanagari-bearing” is intentionally narrower and more honest than “Hindi dataset.” A record can contain a Devanagari name, quotation, social-media fragment, or copied text while otherwise being English. The source does not provide a verified per-record Hindi language label, Hindi collection method, Hindi fact-check provenance, or a Hindi-specific train/validation/test design.

## Exploratory validation slice

The 9-record Devanagari-bearing validation slice contains 7 REAL and 2 FAKE labels. The frozen English LinearSVC produced confusion matrix `[5, 2; 1, 1]` (`[REAL→REAL, REAL→FAKE; FAKE→REAL, FAKE→FAKE]`), with Macro F1 0.5846 and MCC 0.1890. These figures are included for audit completeness only. With nine non-language-labelled examples, they are not a Hindi evaluation, cannot compare models, and cannot influence the champion.

The Phase 4.4 compatibility check produced no empty model inputs for these records. Its 71.38% unique-token vocabulary overlap and 51.56 mean active TF-IDF features are not evidence of Hindi lexical support: the slice may include substantial Latin/English content, while the detector needs only one Devanagari character to route a record to this slice.

## Data governance decision

No external Hindi source was acquired, downloaded, or synthesized. No translations or transliterations of TruthLens examples were created. The only synthetic artifact is a small language-processing fixture with no fake-news label, documented in [MULTILINGUAL_EVALUATION.md](MULTILINGUAL_EVALUATION.md).

Before a genuine Hindi benchmark, the project must register a new source and licence/content-rights evidence; version raw and derivative data; preserve source and label lineage; define a Hindi-aware duplicate/leakage policy; pre-specify stratified train/validation/test membership; and keep the current tuned champion’s protected-test restriction intact. This is a new data/model scope and needs a new governed decision rather than reuse of the English derivative.
