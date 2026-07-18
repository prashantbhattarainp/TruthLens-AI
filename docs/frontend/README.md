# Frontend Guide

The frontend is a static, dependency-light SPA.

- src/js/routing/ defines hash routes.
- src/js/pages/ renders pages.
- src/js/components/ provides shared navigation, footer, icons, notifications, and breadcrumbs.
- src/js/api/ contains the public API client.
- src/js/modules/ coordinates page behavior.
- src/css/ contains tokens, layout, component, page, and dashboard styles.

The frontend calls only the Node.js backend. It must not call the ML service directly or expose runtime-package information.
