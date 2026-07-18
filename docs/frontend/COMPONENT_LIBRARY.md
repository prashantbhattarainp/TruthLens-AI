# TruthLens Component Library

## Application components

| Component | Reuse point | Accessibility behaviour |
| --- | --- | --- |
| Navigation | All routes | `aria-current`, mobile disclosure state, Escape closes menu |
| Breadcrumbs | Non-home routes | Semantic `<nav aria-label="Breadcrumb">` |
| Footer | All routes | Secondary semantic navigation |
| Prediction form | `/predict` | Labels, hints, counters, native constraints, inline errors, busy state |
| Confidence badge | Result card | Displays unavailable calibration distinctly from a percentage |
| Result card | `/predict` | Live result state, focus on result/error, governed prediction/model trace |
| Explainability dashboard | Result card | Textual and colour-coded bounded feature directions; unavailable states stay explicit |
| Analytics dashboard | `/dashboard` | Evidence-aware research and operational overview; does not imply live analytics |
| Status pill and monitoring item | Analytics dashboard | Textual healthy/unavailable/not-instrumented status, updated only on user refresh |
| Evidence chart | Analytics dashboard | Accessible frozen/illustrative chart with explicit data-class label |
| Modal | Future actions | Native `<dialog>`, labelled title, backdrop close |
| Toast | Future acknowledgements | Polite live-region update |
| Empty state | Planned routes | Explains scope rather than presenting a broken screen |

## Result-card API contract

The result card is deliberately a presentation layer for the public Node envelope. It reads `response.data.prediction`, `confidence`, `confidence_status`, `decision_score`, `risk_level`, `explanation`, `keywords`, `processing_time_ms`, model/dataset metadata, and optional `explainability` metadata. `confidence-badge.js`, `error-presentation.js`, and `explanation-panel.js` are reusable presentation helpers. They do not derive a probability, assign a risk level, rerun XAI, or call the Python service directly.

## Adding a component

1. Add semantic markup and reusable styles before creating a JavaScript renderer.
2. Put generic renderers in `src/js/components/`; page orchestration belongs in `src/js/pages/`.
3. Keep network requests in `src/js/api/` and stateful prediction behaviour in `src/js/prediction/` or `src/js/modules/`.
4. Provide keyboard, focus, empty, loading, error, and reduced-motion behaviour where relevant.
5. Document any API field that becomes visible in the UI, especially its interpretation boundary.

The initial library intentionally avoids a third-party component framework. Phase 5.1 prioritizes a small, auditable surface that can evolve without disrupting the current API architecture.

Phase 5.3 retains that approach: the analytics dashboard uses local SVG/CSS charts and a small public-status client rather than a charting or monitoring dependency. See [Analytics UI Component Reference](UI_COMPONENT_REFERENCE.md).
