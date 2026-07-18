# Future Work

This roadmap records remaining research and release gates. It does not start Phase 5.

## Highest-priority evidence gaps

1. Acquire rights-reviewed, language-labelled Hindi and Hinglish corpora with source, time, duplicate, and split governance; do not reinterpret the English derivative as multilingual data.
2. Create a new versioned data/model scope for external, publisher-held-out, and temporal evaluation. Add normalized publication time and publisher identity where rights allow.
3. Conduct a separately governed calibration study using an appropriate calibration partition and a release-oriented probability contract. Do not retrofit the current margin as confidence.
4. Address and remeasure capitalization, added-context, shortening, and stop-word sensitivity using independently labelled robustness data and error review.
5. Design adequately powered fairness research with valid attributes/annotations, rather than inferring demographic fairness from source/topic proxies.

## Model and compute studies

- Re-run the fixed transformer protocol on suitable compute after resolving authorized IndicBERT access. Record resolved revisions, resource use, checkpoints, validation selection, and one permitted non-selection test evaluation.
- Compare future models on the same newly governed multilingual and external evaluation protocol; do not mix historical validation metrics with new test metrics.
- Evaluate ensembles or hybrids only with a separate development partition, composite explainability plan, calibration evidence, resource tests, and a release review.

## Operational research gates

- Establish a new model-release decision with data-rights review, independent post-tuning evaluation, monitoring/incident policy, human-review workflow, abuse analysis, and rollback controls.
- Add measured end-to-end latency, throughput, memory, and failure-mode testing on intended serving hardware.
- Define user communication that makes the research signal, uncertainty, limitations, and escalation path understandable without suggesting a factual verdict.

## Publication follow-up

- Obtain independent methodological review of the evidence boundaries and statistical design.
- Reconcile or restore the unavailable primary Phase 1-3 Markdown records before a historical-methods appendix relies on them.
- Add authorship, data-rights, citation, ethics, and venue-specific formatting review before external submission.
