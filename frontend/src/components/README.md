# Frontend Component Contracts

TruthLens uses small vanilla-JavaScript renderers plus a CSS component layer. Page modules compose the components; they do not fetch data directly or embed repeated navigation/footer markup.

| Component | Location | Contract |
| --- | --- | --- |
| Navigation | `js/components/navigation.js` | Renders hash-route navigation, active state, mobile disclosure, and Escape-to-close behaviour. |
| Footer | `js/components/footer.js` | Renders shared research-use footer links. |
| Breadcrumbs | `js/components/breadcrumbs.js` | Adds semantic route context to non-home views. |
| Icon | `js/components/icon.js` | Supplies consistent inline SVG icons without an icon dependency. |
| Modal | `js/components/modal.js` | Creates an accessible native-dialog shell with backdrop and close controls. |
| Toast | `js/components/toast.js` | Adds short non-blocking messages to the polite live region. |
| Prediction interface | `js/modules/detection-interface.js` | Coordinates validation, API state, loading, error, reset, and result rendering. |

The reusable visual primitives live in `css/components.css`: buttons, cards, badges, alerts, form fields, tables, empty states, loading panels, dialogs, toasts, and footer/navigation. Prediction-specific visual patterns are in `css/pages.css`.

No component may treat `decision_score` as confidence or display a calibrated-confidence badge. The public API boundary remains `js/api/api.js`; `js/api/prediction-api.js` is the prediction-specific adapter.
