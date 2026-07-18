# Responsive Design

## Strategy

TruthLens is mobile-first. A route remains a single semantic reading order at every width; grids enhance progressively rather than hiding essential content.

| Range | Behaviour |
| --- | --- |
| Under 48rem | One-column content grids, full-width readable cards, scrollable tables, compact page margins |
| 48rem and above | Two/three/four-column generic grids where content permits |
| 52rem and above | Four metric cells fit in the prediction result row |
| 56rem and above | Desktop navigation replaces the mobile menu disclosure |
| 64rem and above | Home hero becomes two columns; prediction result sidebar becomes sticky; architecture nodes align in a row |

## Mobile details

- The navigation menu is a labelled disclosure, not an off-screen hover menu.
- Controls maintain a 44px minimum height through the button/nav patterns.
- Form labels, hints, counters, and errors stay adjacent to their inputs.
- Tables retain all columns in a horizontal scroll container instead of shrinking text below legibility.
- The result card follows the form in document order and becomes a side panel only on large screens.

## Accessibility checks

Visual QA covers keyboard-visible focus, menu open/close behaviour, page focus after navigation, contrast-safe status copy, and reduced-motion fallback. Responsive implementation is CSS-only; no viewport-dependent JavaScript content is needed.
