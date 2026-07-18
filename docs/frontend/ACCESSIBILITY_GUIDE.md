# Accessibility Guide

## Scope and status

Phase 5.4 hardens the dependency-free TruthLens frontend for practical keyboard and assistive-technology use. This guide records the implemented accessibility behaviour and the checks required before a deployment. It is not a legal certification or a claim of formal WCAG conformance.

The frontend remains a research workspace. Accessibility support does not change the model's research-only, uncalibrated, English-evidence-only, or not-deployment-approved status.

## Implemented behaviour

| Area | Implementation |
| --- | --- |
| Page structure | Every route renders inside a named `main` landmark, with header, navigation, footer, and breadcrumb landmarks where appropriate. |
| Route changes | Hash-route changes scroll to the top and move focus to the main content after the new route has rendered. Loading and route-error states are announced through `aria-busy` and semantic status content. |
| Keyboard navigation | A skip link targets main content. The small-screen menu exposes its expanded state, has an explicit open/close label, closes after a navigation choice, and supports `Escape`. Visible focus indicators apply throughout the shell. |
| Forms | Headline and article controls have visible labels, descriptions, required state, character counters, `aria-invalid`, and polite field-error feedback. The disabled URL control explains that it is outside the public API contract. |
| Results and errors | Prediction loading, result, and error states use semantic regions and live status text. Error copy is actionable without exposing backend internals. |
| Notifications | Toasts use `status` or `alert` according to severity and include a keyboard-accessible dismiss button. |
| Tables | The model table has a caption, column scopes, and row headers. Its wrapper deliberately scrolls on narrow screens rather than forcing clipped content. |
| Charts and visuals | Inline SVG charts expose text equivalents; dashboard illustrations have meaningful alternative text. Charts retain nearby prose that explains evidence and research limits. |
| Motion and contrast | Focus treatment is visible, status states are not colour-only, `prefers-reduced-motion` limits animation, and forced-colors mode preserves focus visibility. |

## Authoring rules

- Use native controls before ARIA. Buttons must remain buttons, links must remain links, and status changes must be communicated in text.
- Keep labels and error explanations beside their control. Never use placeholder text as the sole label.
- Render API response values and arbitrary text with DOM text APIs. Do not introduce interpolated user or backend values into `innerHTML`.
- Give new data tables a caption and scoped headers. Give a chart a concise title/description and a nearby textual interpretation.
- Preserve explicit research boundaries in accessible names and copy: a decision margin is not confidence, and a prediction is not a factual verdict.

## Manual release checklist

1. Navigate every route using only `Tab`, `Shift+Tab`, `Enter`, and `Escape`.
2. Confirm the skip link, mobile menu state, form errors, chart controls, refresh control, toast dismissal, and links have a visible focus state.
3. Verify that focus moves to main content after a route change and to the result card after a successful prediction.
4. Check the prediction form with a screen reader in the supported browser matrix, including invalid and unavailable-service states.
5. Check browser zoom at 200% and a forced-colors/high-contrast environment; intentional table/chart scroll containers must remain operable.
6. Re-check meaningful alt text whenever an illustration or chart changes.

## Remaining validation

Automated accessibility auditing and human screen-reader testing are deployment responsibilities. Before a public release, run an accessibility scanner against the deployed build, test the supported browser/assistive-technology matrix, and retain results with release evidence.
