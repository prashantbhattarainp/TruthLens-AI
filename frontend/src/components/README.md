# Frontend Component Contracts

TruthLens uses small vanilla-JavaScript renderers plus a CSS component layer. Page modules compose the components; they do not fetch data directly or duplicate shared navigation and footer markup.

| Component | Location | Contract |
| --- | --- | --- |
| Navigation | js/components/navigation.js | Renders product navigation, active state, mobile disclosure, and Escape-to-close behavior. |
| Footer | js/components/footer.js | Renders shared product links and version text. |
| Breadcrumbs | js/components/breadcrumbs.js | Adds semantic route context to non-home views. |
| Icon | js/components/icon.js | Supplies consistent inline SVG icons without an icon dependency. |
| Modal | js/components/modal.js | Creates an accessible native-dialog shell with backdrop and close controls. |
| Toast | js/components/toast.js | Adds short non-blocking messages to the polite live region. |
| Prediction interface | js/modules/detection-interface.js | Coordinates validation, API state, loading, error, reset, and result rendering. |

The public API boundary remains js/api/api.js; js/api/prediction-api.js is the prediction-specific adapter.
