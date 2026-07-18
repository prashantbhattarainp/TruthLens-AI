# Multilingual Evaluation - Phase 4.4

**Status:** Complete at a bounded multilingual-compatibility evidence boundary.
**Decision authority:** [RDL-015](../../research/decision-log/RDL-015-Multilingual-Evaluation-and-Data-Boundary.md).
**Local aggregate artifact:** ignored `P44-multilingual-assessment-20260718T133030Z`, code revision `092ba06`.

## Scope and protocol

Phase 4.4 adds a separate, configurable Unicode/Hindi/Hinglish research-preprocessing layer. It does not alter `PreprocessingPipeline`, the packaged English LinearSVC, the prediction API, or the SHAP/LIME path. The new runner verifies the full derivative SHA-256, retains only validation records in memory, and records aggregate output only. It does not read, transform, label, or predict the protected test partition.

The available governed derivative remains `TL-BFNK-EN-v1.0` / `DER-20260718-r2` / `SPL-TL-BFNK-EN-v1.0` (SHA-256 `978931f41ece219a3e3e27d052cfb35dfe557af02a604d6f913d4ad8e6ca59ad`). It is an English BFNK-derived dataset, not a versioned Hindi or Hinglish fake-news corpus. No external dataset, translation, transliteration, relabelling, or split mutation was introduced.

The tracked `P44-LANGUAGE-PROBE-v1` is a manually authored, language-labelled preprocessing fixture with 12 records (4 each for English, Hindi, and Hinglish). It has no REAL/FAKE labels and is not a translation of the governed derivative. It validates preprocessing only; it contributes no classifier metric.

## Benchmark outcome

The full validation replay reproduces the incumbent evidence exactly. It is a reproducibility check, not fresh selection evidence. “English/unclassified”, “Devanagari-bearing”, and “Hinglish heuristic” are detector-defined appearance slices of the English-labelled validation derivative, not independently governed language datasets. The Hindi values below have support 9 and must not be cited as Hindi fake-news performance. Hinglish has support 2, both REAL-labelled, so the binary metric suite is not computable.

| Validation slice | Support | Accuracy | Macro precision | Macro recall | Macro F1 | Weighted F1 | ROC-AUC* | PR-AUC* | MCC | Kappa |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Full frozen validation (existing English evidence) | 1,461 | 0.5941 | 0.5563 | 0.5457 | 0.5398 | 0.5734 | 0.5576 | 0.4641 | 0.1014 | 0.0971 |
| English/unclassified appearance slice | 1,450 | 0.5938 | 0.5568 | 0.5459 | 0.5397 | 0.5728 | 0.5567 | 0.4641 | 0.1021 | 0.0976 |
| Devanagari-bearing appearance slice | 9 | 0.6667 | 0.5833 | 0.6071 | 0.5846 | 0.6872 | 0.8571 | 0.7500 | 0.1890 | 0.1818 |
| Hinglish heuristic appearance slice | 2 | — | — | — | — | — | — | — | — | — |

\* The score is the incumbent’s uncalibrated LinearSVC decision margin. ROC-AUC and PR-AUC are ranking diagnostics only, not probabilities or confidence. The 9-record Devanagari values are high-variance exploratory diagnostics, not language-wise performance evidence.

The synthetic preprocessing probe detected all 12 expected language labels (4/4 per language). This checks the small fixture only; it is not an estimate of language-identification accuracy in Indian digital media.

## Model availability

| Model | Multilingual evidence in this milestone | State |
| --- | --- | --- |
| `MDL-TL-LSVM-TFIDF-v1.1.0-rc.1` | Unicode-compatible input can be processed; only English validation evidence is governed. | No Hindi/Hinglish classification support claim; no retraining or calibration. |
| `ai4bharat/indic-bert` | None. Phase 4.2 had no authenticated model access, checkpoint, or prediction artifact. | `not_evaluated_access_limited`; no Phase 4.4 substitute result. |
| DistilBERT, BERT base, RoBERTa | None. Phase 4.2 produced no completed checkpoint or metric. | `not_evaluated_resource_limited`; not multilingual evidence. |
| Phase 4.3 ensembles | No language-specific evidence. | English validation-only challengers; no additional evaluation. |

## Interpretation and limits

The system can now inspect Unicode text, identify Devanagari, conservatively flag Roman-Hindi marker combinations, and report token/vocabulary compatibility without changing the approved architecture. It cannot establish multilingual fake-news detection quality from the available data. The only valid classifier benchmark remains the existing English validation result. A future multilingual model comparison requires a governed, rights-reviewed Hindi/Hinglish corpus with a versioned split before training, validation, or any protected-test plan.
