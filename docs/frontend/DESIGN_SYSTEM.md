# TruthLens Design System

## Foundations

The token source is [`frontend/src/css/tokens.css`](../../frontend/src/css/tokens.css). It defines semantic colors, typography, spacing, radii, shadows, and content dimensions. Components consume tokens rather than literal values where practical.

| Token group | Intent |
| --- | --- |
| Ink / soft ink | Primary and supporting text with strong contrast on light surfaces |
| Brand teal | Primary actions, active navigation, research identity |
| Amber | Caution and interpretation-boundary emphasis only |
| Success / danger | Explicit completed/error state with accompanying text |
| `--space-1` through `--space-8` | 4px-based spacing scale for compact to section-level rhythm |
| `--radius-sm` through `--radius-xl` | Consistent controls, cards, and panel corners |
| `--content-width` / `--reading-width` | Wide application canvas with readable copy measure |

## Typography

The system uses a platform-first Inter/system sans stack to avoid external font loading. Headings use tighter letter spacing and responsive `clamp()` sizing; body text remains at 16px with a 1.6 line height. Small metadata is never the only place essential model limitations appear.

## Core primitives

| Primitive | Classes | Use |
| --- | --- | --- |
| Buttons | `.button--primary`, `.button--secondary`, `.button--ghost` | One primary task action; secondary or low-emphasis navigation |
| Cards | `.card`, `.card--elevated` | Group related information without over-framing every line |
| Badges | `.badge--research`, `.badge--warning`, `.badge--success`, `.badge--muted` | Concise textual status, never color only |
| Alerts | `.alert--info`, `.alert--warning`, `.alert--danger` | Persistent context, limitations, or recoverable failure |
| Forms | `.form-field`, `.input`, `.textarea`, `.field-error` | Labelled controls with hints, counters, and live validation |
| Tables | `.table-wrap`, `.table` | Scrollable on narrow screens instead of clipping data |
| States | `.empty-state`, `.loading-panel`, `.result-card__error` | Intentional empty, waiting, and error experiences |

## Prediction-specific rules

`.result-label` is a classification-result label, not a quality or truth indicator. `.confidence-progress[data-status="unavailable"]` uses a neutral pattern rather than a filled bar so “not calibrated” cannot be mistaken for zero confidence. The result card surfaces trace metadata and explanation text returned from the existing API.

## Iconography

`frontend/src/js/components/icon.js` provides a small line-icon set: spark, shield, layers, activity, message, book, check, arrow, and menu. Icons support labels when meaningful; decorative icons are hidden from assistive technology.
