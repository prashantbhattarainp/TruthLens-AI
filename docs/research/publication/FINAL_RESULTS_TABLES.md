# Final Results Tables

**Phase:** 4.6 research finalization  
**Evidence boundary:** frozen validation evidence unless stated otherwise. `—` means that no valid measurement exists; it is not a zero result.

## Evidence scope

All evaluated classical and ensemble rows use the same `TL-BFNK-EN-v1.0` / `DER-20260718-r2` validation partition (`n=1,461`). The tuned LinearSVC and every ensemble have **no post-tuning protected-test result**. Transformer candidates produced no completed checkpoint or metric. See [the experiment summary](FINAL_EXPERIMENT_SUMMARY.md) for protocol and status.

## Model-performance comparison

| Candidate | Accuracy | Macro F1 | MCC | ROC-AUC | PR-AUC | FAKE recall | Evidence and disposition |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| LinearSVC incumbent | 0.5941 | 0.5398 | **0.1014** | 0.5576 | 0.4641 | 0.3183 | Integrated internal research champion; validation only |
| MultinomialNB | 0.5647 | 0.5399 | 0.0802 | 0.5652 | 0.4672 | 0.4226 | Classical challenger; validation only |
| Logistic Regression | 0.5585 | 0.5371 | 0.0743 | 0.5599 | 0.4620 | 0.4365 | Classical challenger; validation only |
| Hard vote | 0.5825 | **0.5447** | 0.0962 | 0.5513 | 0.4353 | 0.3739 | Research challenger; +32 FN and +49 FP trade-off versus incumbent |
| Weighted hard vote | 0.5825 | **0.5447** | 0.0962 | 0.5509 | 0.4384 | 0.3739 | Same validation labels as hard vote; research challenger |
| Soft vote | 0.5674 | 0.5443 | 0.0888 | **0.5688** | **0.4769** | 0.4348 | Research challenger; +67 FN reduction but +106 FP versus incumbent |
| OOF stacker | **0.6092** | 0.3944 | 0.0498 | 0.5659 | 0.4722 | 0.0174 | Rejected: only 10 of 575 FAKE records detected |
| IndicBERT | — | — | — | — | — | — | `not_evaluated_access_limited`; gated upstream access failed before data use |
| DistilBERT | — | — | — | — | — | — | `not_evaluated_resource_limited`; stopped after more than 86 CPU minutes |
| BERT base / RoBERTa base | — | — | — | — | — | — | Not started after the CPU limitation; no result exists |

The 0.0049 Macro-F1 improvement of hard/weighted voting is inside the Phase 3.9 practical-tie tolerance of 0.005. It therefore does not supersede the simpler, integrated LinearSVC.

## Reliability and robustness diagnostics for the incumbent

The following are deterministic inherited-label stress diagnostics, not independently labelled robustness benchmarks or selection evidence.

| Stressor | Inputs changed | Prediction flips | Macro F1 | Accuracy |
| --- | ---: | ---: | ---: | ---: |
| Frozen baseline | — | — | 0.5398 | 0.5941 |
| Typographical errors | 30.2% | 1.1% | 0.5429 | 0.5969 |
| Extra punctuation | 100.0% | 3.6% | 0.5360 | 0.5804 |
| Capitalization changes | 100.0% | **29.0%** | **0.4520** | 0.5975 |
| Emoji insertion | 100.0% | 0.0% | 0.5398 | 0.5941 |
| URL removal | 0.3% | 0.0% | 0.5398 | 0.5941 |
| Stop-word variation | 100.0% | 11.6% | 0.5284 | 0.5880 |
| Synonym replacement | 62.4% | 4.0% | 0.5353 | 0.5852 |
| Light headline paraphrase | 3.8% | 0.2% | 0.5388 | 0.5934 |
| Shortened headline | 98.2% | 14.4% | 0.5383 | 0.5955 |
| Expanded headline | 100.0% | **27.0%** | 0.5334 | **0.5359** |

The uncalibrated LinearSVC margin has a non-fitted sigmoid diagnostic only: ECE proxy 0.0620 and Brier proxy 0.2395. These values are not calibrated confidence or probability metrics.

## Language-appearance and slice evidence

| Slice | Support | Macro F1 | Valid conclusion |
| --- | ---: | ---: | --- |
| Full frozen validation | 1,461 | 0.5398 | Existing English-derived validation evidence |
| English/unclassified appearance | 1,450 | 0.5397 | Descriptive majority slice only |
| Devanagari-bearing appearance | 9 | 0.5846 | Too small and not language-labelled; not Hindi performance |
| Hinglish heuristic appearance | 2 | Not computable | Both records are REAL; not a Hinglish benchmark |

The 12-record synthetic language-processing fixture routed 4 English, 4 Hindi, and 4 Hinglish examples as expected. It has no REAL/FAKE labels and supplies no classifier-performance claim.

## Final model-selection statement

There is **no production-approved model**. The final Phase 4 selection is the packaged internal research champion `TL-LSVM-TFIDF-v1.1.0-rc.1` (TF-IDF unigram/bigram + LinearSVC). It is retained because it is reproducibly packaged, already integrated, bounded by SHAP/LIME explanations, and not materially outperformed by an evaluated alternative under the frozen protocol. It remains uncalibrated, English-evidence-only, untested after tuning, `production_model=false`, and `integrated_not_deployment_approved`.
