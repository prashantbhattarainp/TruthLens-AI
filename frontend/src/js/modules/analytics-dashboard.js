import { getOperationalSnapshot } from '../api/system-api.js';
import { renderPerformanceChart } from '../analytics/chart-renderer.js';
import { notify } from '../components/toast.js';

function setStatus(item, { detail, state }) {
  const status = item.querySelector('[data-monitoring-status]');
  const description = item.querySelector('[data-monitoring-detail]');

  item.dataset.state = state;
  status.textContent = { checking: 'Checking', healthy: 'Healthy', unavailable: 'Unavailable' }[state] ?? 'Unavailable';
  description.textContent = detail ?? 'No status detail returned.';
}

function setCheckingStatus(root) {
  root.querySelectorAll('[data-monitoring-service]').forEach((item) => {
    if (item.dataset.monitoringService !== 'database') {
      setStatus(item, { detail: 'Contacting the existing public endpoint…', state: 'checking' });
    }
  });
}

function setMetricSelection(root, metricId) {
  const chart = root.querySelector('[data-performance-chart]');
  const metricButtons = root.querySelectorAll('[data-chart-metric]');

  chart.innerHTML = renderPerformanceChart(metricId);
  metricButtons.forEach((button) => {
    button.setAttribute('aria-pressed', String(button.dataset.chartMetric === metricId));
  });
}

async function refreshOperationalStatus(root) {
  const refreshButton = root.querySelector('[data-analytics-refresh]');
  const lastUpdated = root.querySelector('[data-analytics-last-updated]');

  refreshButton.disabled = true;
  refreshButton.textContent = 'Checking services...';
  root.setAttribute('aria-busy', 'true');
  setCheckingStatus(root);

  try {
    const snapshot = await getOperationalSnapshot();

    setStatus(root.querySelector('[data-monitoring-service="api"]'), snapshot.api);
    setStatus(root.querySelector('[data-monitoring-service="ml-service"]'), snapshot.mlService);
    setStatus(root.querySelector('[data-monitoring-service="model"]'), snapshot.model);
    if (snapshot.model.version) {
      root.querySelector('[data-dashboard-model-version]').textContent = snapshot.model.version;
    }
    if (snapshot.model.deploymentStatus) {
      root.querySelector('[data-dashboard-deployment]').textContent = snapshot.model.deploymentStatus.replaceAll('_', ' ');
    }
    lastUpdated.textContent = new Intl.DateTimeFormat(undefined, {
      dateStyle: 'medium',
      timeStyle: 'medium',
    }).format(new Date());
    notify('Operational status refreshed from the public API.', { tone: 'success' });
  } catch {
    notify('Operational status could not be refreshed. The existing research evidence is still available.', { tone: 'error' });
  } finally {
    refreshButton.disabled = false;
    refreshButton.textContent = 'Refresh operational status';
    root.setAttribute('aria-busy', 'false');
  }
}

export function initializeAnalyticsDashboard() {
  const root = document.querySelector('[data-analytics-dashboard]');

  if (!root) {
    return;
  }

  root.querySelectorAll('[data-chart-metric]').forEach((button) => {
    button.addEventListener('click', () => setMetricSelection(root, button.dataset.chartMetric));
  });
  root.querySelector('[data-analytics-refresh]').addEventListener('click', () => refreshOperationalStatus(root));
  setMetricSelection(root, 'macroF1');
}
