import {
  renderDatasetCompositionChart,
  renderFeatureImportanceChart,
  renderPredictionDistributionChart,
} from '../analytics/chart-renderer.js';
import { icon } from '../components/icon.js';
import { getRouteHref } from '../routing/routes.js';
import { DASHBOARD_EVIDENCE } from '../analytics/dashboard-data.js';

const dashboard = DASHBOARD_EVIDENCE;

function monitoringItem({ detail, iconName, label, service, state = 'pending', status = 'Not checked' }) {
  return `
    <li class="monitoring-item" data-monitoring-service="${service}" data-state="${state}">
      <span class="monitoring-item__icon">${icon(iconName)}</span>
      <span class="monitoring-item__content"><strong>${label}</strong><span data-monitoring-detail>${detail}</span></span>
      <span class="status-pill" data-monitoring-status>${status}</span>
    </li>
  `;
}

export function renderAnalyticsDashboardPage() {
  const totalRecords = dashboard.dataset.fakeRecords + dashboard.dataset.realRecords;

  return `
    <div data-analytics-dashboard>
      <header class="dashboard-hero">
        <div class="container dashboard-hero__grid">
          <div>
            <p class="eyebrow">Analytics and research operations</p>
            <h1>Evidence, operations, and limits in one workspace.</h1>
            <p>Explore frozen research evidence alongside on-demand public service checks. This dashboard never turns research metrics into a deployment or factual-verdict claim.</p>
            <div class="dashboard-hero__actions">
              <button class="button button--primary" type="button" data-analytics-refresh>${icon('refresh')} Refresh operational status</button>
              <a class="button button--secondary" href="${getRouteHref('predict')}">Open prediction workspace ${icon('arrowRight')}</a>
            </div>
            <p class="dashboard-hero__timestamp">Operational status: <span data-analytics-last-updated>not checked</span></p>
          </div>
          <div class="dashboard-visual card--elevated">
            <img src="assets/images/analytics-research-flow.svg" width="520" height="280" alt="Abstract visual showing research evidence flowing through model, explanation, and review stages." />
            <div class="dashboard-visual__caption"><span class="status-pill status-pill--research">Research only</span><span>Frozen evidence + on-demand health</span></div>
          </div>
        </div>
      </header>

      <section class="page-section dashboard-section">
        <div class="container">
          <div class="dashboard-section__header"><div><p class="eyebrow">Project overview</p><h2>Current research state</h2></div><p>Governed static evidence from the final Phase 4 package.</p></div>
          <div class="dashboard-kpis">
            <article class="dashboard-kpi"><span>Current candidate</span><strong>LinearSVC</strong><small>Internal research champion</small></article>
            <article class="dashboard-kpi"><span>Validation Macro F1</span><strong>0.5398</strong><small>Frozen validation only</small></article>
            <article class="dashboard-kpi"><span>Validation cohort</span><strong>${dashboard.dataset.validationRecords.toLocaleString()}</strong><small>Records; post-tuning test unavailable</small></article>
            <article class="dashboard-kpi dashboard-kpi--warning"><span>Deployment</span><strong>Not approved</strong><small>production_model=false</small></article>
          </div>
        </div>
      </section>

      <section class="page-section page-section--surface dashboard-section">
        <div class="container dashboard-grid dashboard-grid--operations">
          <article class="dashboard-card dashboard-card--monitoring" aria-labelledby="system-status-title">
            <div class="dashboard-card__header"><div><p class="eyebrow">System health</p><h2 id="system-status-title">Operational status</h2></div><span class="badge badge--muted">On demand</span></div>
            <p class="dashboard-card__intro">Checks use existing public health and model endpoints only. No monitoring database or telemetry retention is implied.</p>
            <ul class="monitoring-list" aria-live="polite">
              ${monitoringItem({ detail: 'Use refresh to check /api/health.', iconName: 'server', label: 'Backend API connectivity', service: 'api' })}
              ${monitoringItem({ detail: 'Use refresh to check /api/system/health.', iconName: 'activity', label: 'ML service', service: 'ml-service' })}
              ${monitoringItem({ detail: 'Use refresh to check /api/model/ready.', iconName: 'brain', label: 'Model package', service: 'model' })}
              ${monitoringItem({ detail: 'No database status endpoint is implemented.', iconName: 'database', label: 'Database', service: 'database', state: 'not-instrumented', status: 'Not instrumented' })}
            </ul>
          </article>
          <article class="dashboard-card dashboard-card--model" aria-labelledby="model-trace-title">
            <div class="dashboard-card__header"><div><p class="eyebrow">Model trace</p><h2 id="model-trace-title">Integrated research candidate</h2></div>${icon('shield')}</div>
            <dl class="dashboard-trace">
              <dt>Model</dt><dd>${dashboard.model.name}</dd>
              <dt>Version</dt><dd data-dashboard-model-version>${dashboard.model.version}</dd>
              <dt>Dataset</dt><dd>${dashboard.dataset.identifier}</dd>
              <dt>Production model</dt><dd>None approved</dd>
              <dt>Deployment</dt><dd data-dashboard-deployment>${dashboard.model.deploymentStatus}</dd>
              <dt>Confidence</dt><dd>Unavailable; margin is uncalibrated</dd>
            </dl>
            <p class="research-callout">The current model is not a production model, fact checker, or calibrated confidence system.</p>
          </article>
        </div>
      </section>

      <section class="page-section dashboard-section">
        <div class="container">
          <div class="dashboard-section__header"><div><p class="eyebrow">Model performance</p><h2>Validation evidence, not a leaderboard.</h2></div><p>All candidate comparisons use the frozen validation partition; no post-tuning protected-test result exists.</p></div>
          <div class="dashboard-grid dashboard-grid--performance">
            <article class="dashboard-card dashboard-card--chart" aria-labelledby="performance-title">
              <div class="dashboard-card__header"><div><h3 id="performance-title">Candidate comparison</h3><p>LinearSVC is retained for integration despite near-tied ensemble metrics.</p></div><span class="badge badge--research">Frozen validation</span></div>
              <div class="chart-controls" role="group" aria-label="Select a validation comparison metric">
                <button type="button" class="chart-control" data-chart-metric="macroF1" aria-pressed="true">Macro F1</button>
                <button type="button" class="chart-control" data-chart-metric="accuracy" aria-pressed="false">Accuracy</button>
                <button type="button" class="chart-control" data-chart-metric="fakeRecall" aria-pressed="false">FAKE recall</button>
                <button type="button" class="chart-control" data-chart-metric="rocAuc" aria-pressed="false">ROC-AUC</button>
              </div>
              <div class="chart-frame" data-performance-chart aria-live="polite"></div>
              <p class="chart-note">Hard voting reaches Macro F1 0.5447, within the 0.005 practical-tie tolerance; it is a research challenger, not a promotion.</p>
            </article>
            <article class="dashboard-card dashboard-card--distribution" aria-labelledby="prediction-distribution-title">
              <div class="dashboard-card__header"><div><h3 id="prediction-distribution-title">Prediction distribution</h3><p>Visual placeholder while aggregate prediction retention is unavailable.</p></div><span class="badge badge--warning">Illustrative</span></div>
              ${renderPredictionDistributionChart()}
              <p class="chart-note">${dashboard.predictionDistribution.note}</p>
            </article>
          </div>
        </div>
      </section>

      <section class="page-section page-section--surface dashboard-section">
        <div class="container dashboard-grid dashboard-grid--research">
          <article class="dashboard-card" aria-labelledby="dataset-title">
            <div class="dashboard-card__header"><div><p class="eyebrow">Dataset information</p><h2 id="dataset-title">Frozen composition</h2></div>${icon('database')}</div>
            <div class="dataset-composition">${renderDatasetCompositionChart()}</div>
            <p class="chart-note">${totalRecords.toLocaleString()} English BFNK-derived records. Devanagari/Hinglish appearances are insufficient for language-wise performance claims.</p>
          </article>
          <article class="dashboard-card" aria-labelledby="xai-summary-title">
            <div class="dashboard-card__header"><div><p class="eyebrow">Explainability summary</p><h2 id="xai-summary-title">Aggregate feature importance</h2></div>${icon('spark')}</div>
            <p class="dashboard-card__intro">Mean absolute SHAP terms from the train-only 512-document reference cohort.</p>
            ${renderFeatureImportanceChart()}
            <p class="chart-note">Terms describe model-margin behaviour only; they do not establish factual truth, causality, or confidence.</p>
          </article>
        </div>
      </section>

      <section class="page-section dashboard-section">
        <div class="container">
          <div class="dashboard-section__header"><div><p class="eyebrow">Research insights</p><h2>Evidence inventory at a glance</h2></div><p>Counts and status labels point to the documented research package rather than live analytics.</p></div>
          <div class="research-insights-grid">
            <article class="insight-card"><span>Tracked Phase 4 records</span><strong>${dashboard.research.trackedRecords}</strong><p>Registry records, including non-results and documentation consolidation.</p></article>
            <article class="insight-card"><span>Champion model</span><strong>1</strong><p>LinearSVC research candidate; deployment is not approved.</p></article>
            <article class="insight-card"><span>Explainability methods</span><strong>2</strong><p>${dashboard.research.explainabilityMethods}</p></article>
            <article class="insight-card"><span>Language scope</span><strong>1</strong><p>${dashboard.research.supportedLanguages}</p></article>
          </div>
          <div class="dashboard-grid dashboard-grid--activity section-offset">
            <article class="dashboard-card" aria-labelledby="activity-title"><div class="dashboard-card__header"><div><h3 id="activity-title">Latest evidence activity</h3><p>Milestone timeline, not runtime telemetry.</p></div>${icon('clock')}</div><ol class="activity-timeline"><li><span>Phase 5.3</span><p>Analytics dashboard added over existing static evidence and on-demand health endpoints.</p></li><li><span>Phase 5.2</span><p>Prediction and explainability workflow completed without changing the public contract.</p></li><li><span>Phase 4.6</span><p>Publication package, registries, and limitations consolidated; no model or data update.</p></li></ol></article>
            <article class="dashboard-card" aria-labelledby="recent-predictions-title"><div class="dashboard-card__header"><div><h3 id="recent-predictions-title">Recent predictions</h3><p>Privacy and retention boundary.</p></div>${icon('clock')}</div><div class="dashboard-empty"><span class="badge badge--muted">No retained records</span><h4>Prediction history is not implemented.</h4><p>Individual requests remain in the current prediction workflow only. This dashboard does not invent a history, user analytics, or a confidence distribution.</p><a class="button button--secondary" href="${getRouteHref('predict')}">Run a research prediction ${icon('arrowRight')}</a></div></article>
          </div>
        </div>
      </section>
    </div>
  `;
}
