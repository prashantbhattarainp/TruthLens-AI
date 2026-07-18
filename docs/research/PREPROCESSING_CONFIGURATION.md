# Preprocessing Configuration

**Default configuration:** [`conservative-en-v1.json`](../../ml/config/preprocessing/conservative-en-v1.json)  
**Configuration SHA-256:** `52ce7a78fa4892adf302e3c4dcc0633aebc9dfb55ca4347647f1d1cd87d3976f`

## Strategy

Configurations are JSON documents validated by `PreprocessingConfig`. Unknown, missing, incorrectly typed, or incompatible options fail at load time. Every successful run persists both the full configuration snapshot and its canonical SHA-256 hash, so a later feature or experiment record can name the exact transformation policy.

The default is deliberately conservative: it removes HTML, URLs, emails, and excess whitespace, uses NFC Unicode normalisation and spaCy tokenisation, but preserves case, numbers, punctuation, symbols, stop words, and surface forms. That policy reflects the Phase 3.4 finding that names, negation, numbers, URLs, original scripts, and multilingual content require explicit evaluation rather than implicit deletion.

## Configuration surface

| Section | Options | Default | Behaviour when enabled |
| --- | --- | --- | --- |
| `spacy` | `model_name`, `allow_blank_fallback`, `batch_size` | `en_core_web_sm`, `true`, `128` | Loads a named model; records a blank-language fallback only when permitted. |
| `unicode_normalization` | `enabled`, `form` | `true`, `NFC` | Supports NFC, NFD, NFKC, and NFKD. |
| `html_removal` | `enabled` | `true` | Removes markup using an HTML parser while retaining text nodes. |
| `url_removal` | `enabled` | `true` | Replaces HTTP(S)/`www` URL spans with whitespace. |
| `email_removal` | `enabled` | `true` | Replaces email-address spans with whitespace. |
| `whitespace_normalization` | `enabled` | `true` | Collapses whitespace and trims the result. |
| `lowercasing` | `enabled` | `false` | Applies Unicode-aware lowercasing before spaCy tokenisation. |
| `special_character_handling` | `enabled`, `mode` | `false`, `preserve` | Handles Unicode symbol-category characters. |
| `number_handling` | `enabled`, `mode` | `false`, `preserve` | Handles Unicode digit sequences. |
| `punctuation_handling` | `enabled`, `mode` | `false`, `preserve` | Handles Unicode punctuation-category characters. |
| `tokenization` | `enabled` | `true` | Uses spaCy tokens. Disabling it also requires stop-word removal and lemmatisation to be disabled. |
| `stopword_removal` | `enabled`, `preserve_negations` | `false`, `true` | Uses spaCy stop-word flags while preserving `no`, `not`, `never`, and related negations when requested. |
| `lemmatization` | `enabled` | `false` | Uses spaCy lemmas only when the selected model has a lemmatiser. |
| `validation` | `max_empty_document_rate`, `max_failures` | `0.0`, `0` | Defines run-level acceptance thresholds. |

`special_character_handling`, `number_handling`, and `punctuation_handling` each accept `preserve`, `remove`, `replace_with_space`, or `replace_with_token`. A mode is inert unless its operation is enabled.

## Safe configuration changes

- Create a new configuration file rather than overwriting one referenced by a run.
- Change one rationale-bearing choice at a time, particularly lowercasing, stop-word removal, lemmatisation, number, punctuation, and multilingual handling.
- Retain negation by default. Any alternative needs explicit evaluation evidence.
- Treat language as a declared cohort property, not an inference from text. The English default does not authorise the use of translation-derived text in the primary study.
- Enable lemmatisation only with a recorded spaCy model version and a language-appropriate quality review.

No configuration choice may bypass the Phase 3.4 label, text-unit, formula, auxiliary-sheet, duplicate, source, or temporal gates.
