import { renderFooter } from './components/footer.js';
import { renderNavigation } from './components/navigation.js';
import { initializeDetectionInterface } from './modules/detection-interface.js';
import { renderPage } from './pages/page-renderer.js';
import { getRouteFromHash } from './routing/routes.js';

const appRoot = document.querySelector('[data-app-root]');

function renderApplication({ moveFocus = false } = {}) {
  if (!appRoot) {
    return;
  }

  const route = getRouteFromHash(window.location.hash);
  document.body.dataset.page = route.id;
  document.title = route.title;
  renderNavigation(route.id);
  renderPage(appRoot, route);
  renderFooter();
  initializeDetectionInterface();

  if (moveFocus) {
    window.scrollTo(0, 0);
    appRoot.focus({ preventScroll: true });
  }
}

window.addEventListener('hashchange', () => renderApplication({ moveFocus: true }));
renderApplication();
