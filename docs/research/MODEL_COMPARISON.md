# Phase 3.8 Model Comparison

**Comparison cohort:** `TL-BFNK-EN-v1.0` r2, same preprocessing, TF-IDF representation, seed 42, grouped five-fold CV, and frozen partitions for every model.

## Comparable baseline results

| Model | CV Macro F1 | Validation Macro F1 | CV accuracy | Validation accuracy | FAKE validation recall | Validation ROC-AUC | Model size |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Logistic Regression | 0.4976 | 0.5215 | 0.6168 | 0.6304 | 0.1948 | 0.5631 | 157.1 KiB |
| Multinomial NB | 0.4251 | 0.4358 | 0.6157 | 0.6140 | 0.0661 | 0.5697 | 625.8 KiB |
| Linear SVM | **0.5323** | **0.5274** | 0.5740 | 0.5722 | **0.3357** | 0.5530 | 157.0 KiB |

## Selection decision

The selection rule was fixed before test access: highest validation Macro F1, with lexical model-name tie break only. Linear SVM therefore won the candidate decision. Its one-time protected-test Macro F1 was 0.5486; this test result was not used to re-select or tune any candidate.

The table deliberately avoids ranking models by accuracy alone. Logistic Regression's higher accuracy coincides with substantially lower FAKE recall. Multinomial NB is fastest to train but has very low FAKE recall and is not a useful detection baseline under the primary metric.

## Resource observations

On the frozen training split, Logistic Regression, Multinomial NB, and Linear SVM took 105 ms, 9 ms, and 198 ms respectively to fit; validation inference was 1–2 ms. Model sizes were measured as serialized model objects. Those timing values are local, implementation-specific measurements rather than general hardware benchmarks.

See [the resource profile](figures/phase-3-8-resource-profile.png) and [the full evaluation report](MODEL_EVALUATION_REPORT.md).
