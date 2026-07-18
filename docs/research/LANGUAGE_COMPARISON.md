# Language Comparison - Phase 4.4

## What is being compared

The comparison separates processing compatibility from classifier validity. The detector-defined slices below are all drawn from the English-labelled frozen validation derivative and must not be presented as balanced English/Hindi/Hinglish benchmark cohorts.

| Appearance slice | Records | Mean raw characters | Mean multilingual tokens | Unique frozen tokens | In-champion-vocabulary tokens | Unique-token coverage | Mean active TF-IDF features | Zero-feature inputs |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| English/unclassified | 1,450 | 244.52 | 40.90 | 8,507 | 4,697 | 55.21% | 57.58 | 0 |
| Devanagari-bearing | 9 | 251.44 | 43.33 | 269 | 192 | 71.38% | 51.56 | 0 |
| Hinglish heuristic | 2 | 405.50 | 66.00 | 114 | 105 | 92.11% | 90.00 | 0 |

The apparently higher token coverage for the two small multilingual slices does not show better Hindi or Hinglish support. A record can be routed by one Devanagari character or two Roman-Hindi markers while most of its text remains English. Sparse samples magnify that effect. The key implementation finding is only that the frozen pipeline accepted every audited input; the key research finding is that acceptance is not language validity.

## Tokenization and terminology

The new modular preprocessor tokenizes Devanagari and Latin runs without depending on an English spaCy model. It preserves Devanagari tokens, lowercases Latin tokens, and applies the Roman-Hindi normalization map only to Hinglish-routed text. It also records the routing reason in memory for audit use.

The frozen champion still applies its original English preprocessing and English-trained TF-IDF vocabulary for prediction. Consequently, terms in Hindi script, transliterated variants, Indian political names, health claims, local locations, and social-media style can be underrepresented, mis-segmented, or spuriously represented by nearby English vocabulary. This audit does not alter the model vocabulary or vectorizer.

## Comparative conclusion

The current evidence supports a three-language processing extension and a repeatable audit harness. It does not support a claim that English, Hindi, and Hinglish have been fairly compared. A future study should use language-labelled, source-balanced, class-balanced datasets; register per-language corpus versions; pre-specify split and metric aggregation; and report confidence intervals appropriate to each language cohort.
