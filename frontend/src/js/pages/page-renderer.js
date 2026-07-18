import { renderHomePage } from './home-page.js';
import { renderModelsPage } from './models-page.js';
import { renderPlaceholderPage } from './placeholder-page.js';
import { renderPredictPage } from './predict-page.js';
import { renderResearchPage } from './research-page.js';
import { renderBreadcrumbs } from '../components/breadcrumbs.js';

export function renderPage(root, route) {
  const pages = {
    dashboard: renderAnalyticsDashboardPage,
    home: renderHomePage,
    models: renderModelsPage,
    predict: renderPredictPage,
    research: renderResearchPage,
  };
  const render = pages[route.id] ?? (() => renderPlaceholderPage(route));

  root.innerHTML = `${renderBreadcrumbs(route)}${render()}`;
}
import { renderAnalyticsDashboardPage } from './analytics-dashboard-page.js';
