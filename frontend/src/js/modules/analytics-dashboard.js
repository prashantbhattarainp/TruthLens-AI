import { getOperationalSnapshot } from '../api/system-api.js';
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
      setStatus(item, { detail: 'Contacting the service…', state: 'checking' });
    }
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
    lastUpdated.textContent = new Intl.DateTimeFormat(undefined, { dateStyle: 'medium', timeStyle: 'medium' }).format(new Date());
    notify('Service status refreshed.', { tone: 'success' });
  } catch {
    notify('Service status could not be refreshed.', { tone: 'error' });
  } finally {
    refreshButton.disabled = false;
    refreshButton.textContent = 'Refresh service status';
    root.setAttribute('aria-busy', 'false');
  }
}

export function initializeAnalyticsDashboard() {
  const root = document.querySelector('[data-analytics-dashboard]');
  if (root) {
    root.querySelector('[data-analytics-refresh]').addEventListener('click', () => refreshOperationalStatus(root));
  }
}
