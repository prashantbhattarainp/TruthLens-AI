import { icon } from '../components/icon.js';
import { getRouteHref } from '../routing/routes.js';

function monitoringItem({ detail, iconName, label, service, state = 'pending', status = 'Not checked' }) {
  return `<li class="monitoring-item" data-monitoring-service="${service}" data-state="${state}"><span class="monitoring-item__icon">${icon(iconName)}</span><span class="monitoring-item__content"><strong>${label}</strong><span data-monitoring-detail>${detail}</span></span><span class="status-pill" data-monitoring-status>${status}</span></li>`;
}

export function renderAnalyticsDashboardPage() {
  return `
    <div data-analytics-dashboard>
      <header class="dashboard-hero">
        <div class="container dashboard-hero__grid">
          <div>
            <p class="eyebrow">Product dashboard</p>
            <h1>Service status and responsible use, in one place.</h1>
            <p>Check the availability of the public API and analysis service, then use the prediction workflow with independent verification in mind.</p>
            <div class="dashboard-hero__actions"><button class="button button--primary" type="button" data-analytics-refresh>${icon('refresh')} Refresh service status</button><a class="button button--secondary" href="${getRouteHref('predict')}">Open prediction ${icon('arrowRight')}</a></div>
            <p class="dashboard-hero__timestamp">Last checked: <span data-analytics-last-updated>not checked</span></p>
          </div>
          <div class="dashboard-visual card--elevated">
            <div class="dashboard-empty"><span class="badge badge--success">Privacy-aware</span><h2>Session-based workflow</h2><p>TruthLens does not show a prediction history or claim to retain submitted articles in the dashboard.</p></div>
          </div>
        </div>
      </header>

      <section class="page-section dashboard-section">
        <div class="container dashboard-grid dashboard-grid--operations">
          <article class="dashboard-card dashboard-card--monitoring" aria-labelledby="system-status-title">
            <div class="dashboard-card__header"><div><p class="eyebrow">System health</p><h2 id="system-status-title">Operational status</h2></div><span class="badge badge--muted">On demand</span></div>
            <p class="dashboard-card__intro">Checks run only when you select refresh. No dashboard telemetry or account activity is implied.</p>
            <ul class="monitoring-list" aria-live="polite">
              ${monitoringItem({ detail: 'Use refresh to check the public API.', iconName: 'server', label: 'Backend API', service: 'api' })}
              ${monitoringItem({ detail: 'Use refresh to check the analysis service.', iconName: 'activity', label: 'ML service', service: 'ml-service' })}
              ${monitoringItem({ detail: 'This version is stateless; no database is configured.', iconName: 'database', label: 'Database', service: 'database', state: 'not-instrumented', status: 'Not configured' })}
            </ul>
          </article>
          <article class="dashboard-card" aria-labelledby="dashboard-use-title">
            <div class="dashboard-card__header"><div><p class="eyebrow">How to use results</p><h2 id="dashboard-use-title">A practical review loop</h2></div>${icon('shield')}</div>
            <ol class="activity-timeline"><li><span>1</span><p>Read the text and consider the source context before submitting it.</p></li><li><span>2</span><p>Use the classification and contributing words as a prompt for further review.</p></li><li><span>3</span><p>Verify important claims using credible, independent sources.</p></li></ol>
          </article>
        </div>
      </section>

      <section class="page-section page-section--surface dashboard-section">
        <div class="container">
          <div class="dashboard-section__header"><div><p class="eyebrow">Analytics</p><h2>What the dashboard does—and does not—track.</h2></div><p>Designed for transparent use without inventing activity metrics.</p></div>
          <div class="grid grid--three">
            <article class="card"><div class="card__icon">${icon('activity')}</div><h3 class="card__title">Live availability</h3><p class="card__copy">On-demand checks show whether the backend and analysis service can be reached.</p></article>
            <article class="card"><div class="card__icon card__icon--accent">${icon('spark')}</div><h3 class="card__title">Explainability</h3><p class="card__copy">Individual prediction results can show the text features that influenced an outcome.</p></article>
            <article class="card"><div class="card__icon card__icon--success">${icon('shield')}</div><h3 class="card__title">No activity history</h3><p class="card__copy">This release does not present user analytics, prediction history, or a fabricated accuracy dashboard.</p></article>
          </div>
        </div>
      </section>
    </div>
  `;
}
