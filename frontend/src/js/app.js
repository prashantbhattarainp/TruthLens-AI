import { renderFooter } from './components/footer.js';
import { renderNavigation } from './components/navigation.js';
import { initializeDetectionInterface } from './modules/detection-interface.js';
import { initializeAnalyticsDashboard } from './modules/analytics-dashboard.js';
import { renderPage, renderPageError, renderPageSkeleton } from './pages/page-renderer.js';
import { getRouteFromHash } from './routing/routes.js';

const appRoot = document.querySelector('[data-app-root]');
let renderSequence = 0;

async function renderApplication({ moveFocus = false } = {}) {
  if (!appRoot) {
    return;
  }

  const sequence = ++renderSequence;
  const route = getRouteFromHash(window.location.hash);
  document.body.dataset.page = route.id;
  document.title = route.title;
  renderNavigation(route.id);
  renderFooter();
  appRoot.setAttribute('aria-busy', 'true');
  renderPageSkeleton(appRoot, route);

  if (moveFocus) {
    window.scrollTo(0, 0);
  }

  try {
    await renderPage(appRoot, route);
  } catch {
    if (sequence === renderSequence) {
      renderPageError(appRoot, route);
    }
  }

  if (sequence !== renderSequence) {
    return;
  }

  appRoot.setAttribute('aria-busy', 'false');

  if (route.id === 'predict') {
    initializeDetectionInterface();
  }
  if (route.id === 'dashboard') {
    initializeAnalyticsDashboard();
  }

  if (moveFocus) {
    appRoot.focus({ preventScroll: true });
  }
}

window.addEventListener('hashchange', () => renderApplication({ moveFocus: true }));
void renderApplication();
