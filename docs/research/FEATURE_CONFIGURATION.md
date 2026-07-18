# Feature Configuration

**Feature pipeline version:** `1.0.0`  
**Configuration strategy:** strict JSON with canonical SHA-256 identity

## Baseline configurations

| Configuration | Method | Intended future role | SHA-256 |
| --- | --- | --- | --- |
| [`count-unigram-v1.json`](../../ml/config/features/count-unigram-v1.json) | Count | Minimal count baseline, unigrams, no normalization. | `e89f516d8d6780a32d87cf4681b4754973c25adfcdd7f92be33f6722039f054b` |
| [`tfidf-unigram-bigram-v1.json`](../../ml/config/features/tfidf-unigram-bigram-v1.json) | TF-IDF | Sparse lexical baseline, unigrams and bigrams with L2 normalization. | `fdec84fd3755a6cd4be8dfc3c75689afd55d5ba2f918b90944796c71cd648938` |

Each run writes both the complete configuration snapshot and the canonical hash to its experiment record, event log, and manifest. Unknown or missing root configuration keys fail at load time.

## Baseline parameter schema

| Parameter | Type | Meaning |
| --- | --- | --- |
| `ngram_range` | `[min, max]` positive integers | Inclusive word n-gram range. |
| `max_features` | positive integer or `null` | Upper cap on fitted vocabulary size. |
| `min_df` | positive integer or proportion `(0, 1]` | Minimum document frequency required to retain a term. |
| `max_df` | positive integer or proportion `(0, 1]` | Maximum document frequency allowed for a term. |
| `binary` | boolean | Count presence rather than frequency; valid only for CountVectorizer. |
| `normalization` | `none`, `l1`, or `l2` | Applies to Count matrices after extraction and is passed to TF-IDF during extraction. |

The baseline components validate this parameter contract strictly. Other registered methods may define their own extractor-specific `parameters` schema, so new representation types do not require a change to `FeatureConfig` or `FeaturePipeline`.

## Validation settings

| Setting | Default | Purpose |
| --- | --- | --- |
| `max_empty_feature_vector_rate` | `0.0` | Fails a run if too many input documents produce all-zero rows. |
| `max_matrix_memory_mb` | `512` | Sets an explicit upper bound for the stored CSR arrays. |
| `require_nonempty_vocabulary` | `true` | Prevents an empty fitted vocabulary from being accepted. |

## Change control

- Create a new configuration file for every rationale-bearing change; never overwrite a configuration referenced by an experiment artifact.
- Change one representation decision at a time during a future comparison: n-grams, document-frequency thresholds, vocabulary cap, binary mode, or normalization.
- Keep preprocessing and feature configurations distinct. Vectorizers consume approved preprocessed text and must not lower-case, strip punctuation, or apply stop-word removal again.
- Record the source derivative, split ID, fit partition, configuration hash, code revision, dependency versions, and notes before fitting a vectorizer.
- Do not fit TF-IDF or any vocabulary-learning feature method on validation or test records.

No configuration may bypass the unresolved Phase 3.4 data-readiness, label, formula-provenance, auxiliary-sheet, duplicate/group, or temporal controls.
