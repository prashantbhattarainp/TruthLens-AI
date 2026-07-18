# TruthLens UI Guidelines

## Purpose

The interface should feel like a calm research workspace: clear hierarchy, deliberate space, visible provenance, and no visual language that overstates model certainty.

## Content principles

- Lead with the task and the research boundary. Describe the output as a classification signal, not a factual verdict.
- Use plain language for status: “Confidence unavailable,” “Not deployment approved,” and “Human review required.”
- Keep labels short, specific, and sentence-cased. Use one primary action per view.
- Do not use red/green labels alone to communicate prediction, status, or an error. Pair color with text and an icon or pattern.
- Avoid celebratory language for a model result. The current LinearSVC has limited validation evidence and no post-tuning protected-test result.

## Interaction and accessibility

- Use native buttons, links, inputs, labels, and dialog elements before ARIA roles.
- Provide visible `:focus-visible` rings and a “Skip to main content” link.
- Keep keyboard order aligned with the visual order. Mobile navigation closes on Escape.
- Use polite live regions for validation, result, and toast updates; do not move focus for routine field validation.
- Move focus to the result card after a completed response or request error, so screen-reader and keyboard users receive the state change.
- Respect `prefers-reduced-motion`; loading movement is limited to the spinner.

## Research-status presentation

| Information | Approved UI language | Prohibited shorthand |
| --- | --- | --- |
| `confidence: null` | “Confidence unavailable” or “Not calibrated” | Percentage confidence, probability, or certainty gauge |
| `decision_score` | “Uncalibrated decision margin” | Risk score, trust score, or likelihood of truth |
| Prediction label | “Research classification result” | Fact check, verdict, confirmed fake/real |
| Explainability | “Model behaviour only” | Why the claim is true/false |
| Language scope | “Hindi/Hinglish not validated” | Multilingual fake-news detection |

## Visual tone

Use the dark ink/teal research palette, warm amber only for cautions, and soft surfaces with restrained shadows. Animations should communicate loading only; navigation, cards, and results do not need decorative motion.
