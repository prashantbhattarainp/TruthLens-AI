# Prediction Dashboard

## Purpose and boundary

The `/predict` hash route is the core research-prediction workspace. It sends a validated headline and article only to the existing public Node endpoint, then presents the returned classification, model trace, and optional explainability metadata.

It is not a fact-checking workflow. The displayed `decision_score` is an uncalibrated LinearSVC margin; `confidence` remains unavailable, and `risk_level` remains not assessed.

## Input workflow

1. Enter a headline (1-300 characters) and article text (100-15,000 characters).
2. Read inline validation and character counters before the Run prediction control becomes available.
3. Submit once; the form locks and the result card announces the loading state.
4. Review the returned prediction, trace metadata, and any available explanation details.
5. Use Clear input to reset both the form and result state.

The disabled Article URL field is an explicit placeholder. The public API currently accepts `headline` and `article` only, so the field is neither validated nor sent.

## Result states

| State | User-facing behaviour |
| --- | --- |
| Initial | Explains the input needed for a prediction. |
| Validation | Shows field-specific guidance and moves focus to the first invalid field on submit. |
| Loading | Locks form controls and announces an in-progress request. |
| Success | Moves focus to the result card, shows the backend response, and adds a polite notification. |
| Failure | Preserves the input, focuses the error card, and explains whether content, network, timeout, backend, or model-service handling failed. |

## Displayed response fields

The dashboard uses only fields returned inside `POST /api/predict`'s public success envelope: prediction, confidence status, decision score, risk level, processing time, explanation summary/reasons, keywords, model/version/dataset trace, response timestamp, request ID, and optional `explainability` metadata.

The confidence badge intentionally displays **Unavailable** for the current model. A patterned progress track and the label **Not calibrated** reinforce that the decision margin is not a percentage, probability, or reliability estimate.

## Accessibility and responsive behaviour

- All form controls have labels, descriptions, native constraints, counters, and inline live validation.
- Loading, success, and error states are announced without using colour as their only signal.
- Result and error transitions move keyboard focus to the relevant card.
- Contribution direction is communicated in text as well as colour.
- The dashboard is single-column on narrow screens; XAI panels become a compact grid at wider widths.
