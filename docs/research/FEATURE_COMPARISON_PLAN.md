# Feature Comparison Plan

**Status:** Design only. No dataset feature matrix, model, metric, or feature-method comparison has been run.

## Aim

When the Phase 3.4 governance gate is resolved, compare sparse lexical representations fairly before introducing learned embeddings or transformer representations. The comparison informs a later, separately approved baseline-model study; it is not a model evaluation result.

## Planned comparison cohort

| Candidate | Frozen configuration | Expected value | Primary caution |
| --- | --- | --- | --- |
| Count unigrams | `count-unigram-v1.json` | Transparent raw lexical frequency baseline. | Common words may dominate without normalization or frequency controls. |
| TF-IDF unigrams and bigrams | `tfidf-unigram-bigram-v1.json` | Downweights ubiquitous terms while retaining short phrase signals. | Vocabulary/IDF must be fitted on training data only. |
| Count or TF-IDF variants | New versioned configuration only | Isolates the impact of one controlled parameter change. | Not directly comparable if data, split, preprocessing, or task definition changes. |

Word2Vec, FastText, GloVe, Doc2Vec, BERT, and IndicBERT remain future extension candidates. They are excluded from the initial sparse-baseline comparison because they require separate language coverage, licensing, compute, and representation-quality decisions.

## Fair-comparison protocol

1. Approve a derivative, label mapping, text-unit/language rule, duplicate clusters, and source/time grouping policy.
2. Freeze one split manifest and identify the training partition.
3. Freeze one preprocessing configuration and use the same processed input representation for every candidate.
4. Fit each vocabulary or IDF representation only on the training partition; preserve its fitted artifact.
5. Transform held-out partitions with that same artifact without extending its vocabulary or recomputing IDF.
6. Record feature configuration, dataset/split identifiers, source-manifest hash, dependency versions, row/column dimensions, sparsity, empty-vector rate, memory, duration, and validation outcome.
7. Only in a later approved milestone, pair comparable feature artifacts with the same model protocol and report results without mixing cohorts.

## Non-comparability conditions

Feature artifacts must be treated as distinct cohorts—not winners or losers—if any of the following changes: source derivative, label mapping, inclusion rule, preprocessing policy, split/grouping rule, fit partition, feature configuration, or metric/model protocol.

## Decision rule

No representation is selected in Phase 3.6. A future selection must balance validation acceptance, resource use, sparse dimensionality, leakage controls, model evidence, error analysis, and Indian-language/task coverage. Raw vocabulary size or a single held-out metric alone is insufficient.
