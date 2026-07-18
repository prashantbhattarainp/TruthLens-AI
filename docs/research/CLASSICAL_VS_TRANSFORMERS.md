# Classical vs Transformers - Phase 4.2

**Purpose:** A governed comparison view, not a release decision.  
**Champion policy:** The LinearSVC remains the internal champion unless a separate review satisfies the gates in [MODEL_SELECTION_UPDATE.md](MODEL_SELECTION_UPDATE.md).

## Evidence comparison

| Model | Family | Validation Macro F1 | Validation MCC | Protected-test evidence in Phase 4.2 | Research status |
| --- | --- | ---: | ---: | --- | --- |
| `TL-LSVM-TFIDF-v1.1.0-rc.1` | TF-IDF unigram/bigram + LinearSVC | 0.5398 | 0.1014 | Prohibited after Phase 3.9 tuning | Internal champion; not deployment-approved |
| IndicBERT | Multilingual ALBERT | — | — | Not accessed | Access-limited; not evaluated |
| DistilBERT base uncased | Distilled English transformer | — | — | Not accessed | Resource-limited; stopped before checkpoint |
| BERT base uncased | English transformer | — | — | Not accessed | Not started after lower-cost candidate exceeded CPU window |
| RoBERTa base | English transformer | — | — | Not accessed | Not started after lower-cost candidate exceeded CPU window |

The LinearSVC test result from Phase 3.8 is deliberately absent: it was measured before the Phase 3.9 tuning that created the current candidate and cannot be reused for a post-tuning comparison. No transformer candidate may fill a result cell until its immutable local run manifest and `results.json` are both complete.

## Methodological comparability

All candidates retain the same derivative, labels, and partition membership. The classical candidate consumes its frozen sparse-preprocessing/TF-IDF representation; transformers consume the identical frozen `raw_text` with their own tokenizers. This is an algorithm-level input-representation difference, not a change to dataset version, preprocessing derivative, label semantics, or evaluation method.

Completed transformer tables must compare validation and test results separately. Test results are descriptive, with no hyperparameter, epoch, threshold, feature, or deployment selection based on them. Differences must be interpreted alongside error slices, timing, memory constraints, source/template sensitivity, language limits, and uncertainty—not as a claim that one model can determine factual truth.
