# Hinglish Analysis - Phase 4.4

## Detection and normalization design

Hinglish is represented as Roman-script Hindi, often mixed with English. Phase 4.4 uses a transparent conservative heuristic rather than a statistical language-ID model:

- Devanagari characters route text to the Hindi path.
- Otherwise, at least two distinct Roman-Hindi markers are required for the Hinglish path.
- Fully uppercase tokens are treated as acronyms/named entities for marker detection, avoiding a common false signal from the political-party acronym `AAP`.
- Unicode NFC normalization, HTML/URL/email removal, zero-width-character removal, and whitespace normalization run before language routing.
- Common Roman-Hindi variants such as `kyu`→`kyun` and `nahi`/`nhi`→`nahin` are normalized only after a record is routed to Hinglish. This is spelling consolidation, not translation.

The 12-record synthetic language-processing fixture correctly routed all four Hinglish examples. A dedicated unit check also verifies two explicit normalization replacements. The fixture itself did not contain a replacement variant, so its aggregate normalization count is zero. Neither result measures real-world language-ID accuracy or fake-news detection.

## Available data and evaluation limit

The governed validation derivative produced only two Hinglish-heuristic candidates. Both carry the REAL label, so accuracy, precision, recall, Macro F1, weighted F1, ROC-AUC, PR-AUC, MCC, and Cohen’s kappa are deliberately reported as not computable. The one observed false positive is an exploratory diagnostic only.

The slice had 92.11% unique frozen-token vocabulary overlap and 90 mean active TF-IDF features. This unexpectedly high overlap should not be interpreted as Roman-Hindi support: the heuristic candidates contain substantial English/model-vocabulary material and may expose code-mixing or marker ambiguity. It illustrates why vocabulary coverage is an input-compatibility diagnostic rather than a multilingual quality metric.

## Code-mixing risks

- Roman spellings vary by region, author, keyboard habit, and emphasis; a small normalization map cannot resolve them safely.
- Markers can collide with English tokens, names, and political acronyms. The two-marker and uppercase safeguards reduce, but do not remove, that risk.
- Named entities, hashtags, abbreviations, English health terminology, and social-media conventions can dominate the TF-IDF representation even when the author uses Roman Hindi grammar.
- A label from an English fact-check derivative does not establish that a Hinglish message has the same claim, source context, or intended meaning.

Future Hinglish work needs a rights-reviewed corpus with documented Romanization/code-mixing policy, language annotation, class balance, source/time lineage, and a pre-specified split. A multilingual transformer may be a useful future candidate, but it needs accessible weights and an independently governed benchmark; Phase 4.2’s IndicBERT run remains access-limited.
