# Chart Guidelines

## Evidence-first charting

TruthLens charts must identify their evidence class before visual polish:

1. **Frozen evidence:** name the data partition, metric, and documented source.
2. **Live operational state:** name the public endpoint and refresh behaviour.
3. **Illustrative placeholder:** use a visible label and state what data is unavailable.
4. **Not implemented:** present a clear empty state instead of a synthetic chart.

No chart may turn an uncalibrated margin into confidence, imply a factual verdict, promote a research challenger, imply a language benchmark, or treat a validation-only result as production monitoring.

## Current chart contracts

| Chart | Data class | Rule |
| --- | --- | --- |
| Candidate comparison | Frozen validation | Preserve candidate labels and practical-tie context. |
| Dataset composition | Frozen derivative | Display aggregate class counts only. |
| Aggregate SHAP features | Train-only global reference | Explain model-margin behaviour only. |
| Prediction distribution | Illustrative placeholder | Keep the illustrative badge until governed aggregate retention exists. |

## Accessible implementation

- Use `<figure>`/caption semantics or an equivalent labelled card for every visual.
- Give SVGs a title/description or a complete nearby text alternative.
- Do not use colour as the only category or status signal.
- Preserve readable value labels, especially for exact research metrics.
- Keep control labels explicit; buttons must expose `aria-pressed` when they select a chart metric.
- Respect reduced-motion preferences; Phase 5.3 uses no chart animation.

## Maintainability

The frozen dashboard values live in `frontend/src/js/analytics/dashboard-data.js`. Reusable rendering lives in `chart-renderer.js`; page markup does not contain duplicated metric arrays. Any future data change requires its governed research source, a documentation update, and tests for the visible evidence boundary.
