import { renderBreadcrumbs } from '../components/breadcrumbs.js';

const pageModules = {
  dashboard: {
    exportName: 'renderAnalyticsDashboardPage',
    load: () => import('./analytics-dashboard-page.js'),
  },
  home: {
    exportName: 'renderHomePage',
    load: () => import('./home-page.js'),
  },
  models: {
    exportName: 'renderModelsPage',
    load: () => import('./models-page.js'),
  },
  notFound: {
    exportName: 'renderNotFoundPage',
    load: () => import('./not-found-page.js'),
  },
  placeholder: {
    exportName: 'renderPlaceholderPage',
    load: () => import('./placeholder-page.js'),
  },
  predict: {
    exportName: 'renderPredictPage',
    load: () => import('./predict-page.js'),
  },
  research: {
    exportName: 'renderResearchPage',
    load: () => import('./research-page.js'),
  },
};

function getPageModule(routeId) {
  return pageModules[routeId] ?? pageModules.placeholder;
}

export function renderPageSkeleton(root, route) {
  root.innerHTML = `${renderBreadcrumbs(route)}
    <section class="page-section" aria-label="Loading ${route.label}">
      <div class="container"><div class="page-skeleton" role="status"><span class="sr-only">Loading ${route.label}</span><span class="page-skeleton__eyebrow"></span><span class="page-skeleton__title"></span><span class="page-skeleton__copy"></span><span class="page-skeleton__copy page-skeleton__copy--short"></span></div></div>
    </section>`;
}

export function renderPageError(root, route) {
  root.innerHTML = `${renderBreadcrumbs(route)}
    <section class="page-section">
      <div class="container"><div class="empty-state empty-state--error" role="alert"><h1>That workspace could not load.</h1><p>Refresh the page or return to the research home to continue. No prediction or research data was changed.</p><a class="button button--secondary" href="#/">Return home</a></div></div>
    </section>`;
}

export async function renderPage(root, route) {
  const page = getPageModule(route.id);
  const pageModule = await page.load();
  const render = pageModule[page.exportName];
  const content = page === pageModules.placeholder ? render(route) : render();

  root.innerHTML = `${renderBreadcrumbs(route)}${content}`;
}
