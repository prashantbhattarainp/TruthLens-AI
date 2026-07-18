# IndicBERT Evaluation

**Model:** `ai4bharat/indic-bert`  
**Status:** `not_evaluated_access_limited`  
**Protected test:** Not accessed

IndicBERT was selected because its upstream card describes an ALBERT multilingual model covering 12 Indian languages, including English. It is a relevant challenger for the Indian-news context, but relevance is not evidence of better performance on the frozen English BFNK derivative.

The Phase 4.2 runner attempted to load the model before frozen-split tokenization. Hugging Face rejected access because this repository requires acceptance of gated-model conditions and authenticated access. The resulting ignored run manifest is `P42-indicbert-20260718T115636Z/run-manifest.json`; it records the 401 failure and confirms `protected_test_access: none`.

No accuracy, F1, AUC, timing, confusion matrix, error analysis, or model-ranking conclusion is available. A future run must first obtain access through the model owner’s normal conditions, then use the unchanged Phase 4.2 protocol as a new evidence artifact. It must not use this access failure to alter labels, the split, or the incumbent model.
