# Threats to Validity

## Construct validity

- A binary `REAL`/`FAKE` derivative label is a bounded research target, not factual truth, source credibility, author intent, or risk.
- The LinearSVC decision margin is not a probability. The sigmoid ECE/Brier values are non-fitted diagnostics only.
- Keyword topic, fact-check-source, date-appearance, language-appearance, and length groups are descriptive proxies. They are not demographic attributes, publisher labels, controlled topics, or causal variables.
- Synthetic perturbations can change meaning. Their inherited-label scores are stress diagnostics rather than real-world robustness estimates.

## Internal validity

- The tuned incumbent has no post-tuning protected-test result; the earlier Phase 3.8 test result cannot be reused.
- Results come from one frozen validation partition. Repeated selection, retraining, threshold tuning, and calibration fitting were deliberately excluded.
- The stacker uses train-only OOF scores, but ensemble results still require an independent, governed release study before operational use.
- Phase 4.5 ablations are inference-only. They do not estimate the effects of retraining without preprocessing or bigrams.

## External validity

- `TL-BFNK-EN-v1.0` is an English BFNK-derived corpus and does not represent all Indian languages, publishers, regions, platforms, or time periods.
- Nine Devanagari-bearing and two Hinglish-heuristic validation records cannot establish language-wise quality.
- `fact_check_source` is not publisher identity, and missing normalized publication dates prevent unseen-publisher or proper temporal generalization studies.
- Source/template patterns, duplicated formats, and class composition can be learned as shortcuts by sparse text models.

## Sampling, labels, and fairness

- Source availability, collection policy, fact-check workflow, language representation, label noise, and historical coverage may bias the corpus.
- Small, overlapping slices make observed variation unstable. The financial, source, and language-appearance results indicate review priorities, not parity or discrimination findings.
- No protected demographic attributes or causal exposure data are available, so a demographic fairness conclusion is unsupported.

## Reproducibility and reporting

- Data and versioned model packages are intentionally not tracked because of governance and content controls. A reproduction requires authorized local artifacts and hash verification.
- The current checkout lacks the primary Markdown files linked as historical Phase 1-3 records in older indexes; Phase 4.6 corrects those indexes and does not recreate unavailable evidence.
- Transformer exact package revisions are retained in ignored run manifests; the current service environment is not a substitute for the temporary Phase 4.2 benchmark environment.

These threats mean the package supports transparent bounded research reporting, not deployment or a general fake-news-detection claim.
