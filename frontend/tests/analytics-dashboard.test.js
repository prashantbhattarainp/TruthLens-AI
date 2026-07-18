import test from 'node:test';
import assert from 'node:assert/strict';

import { renderAnalyticsDashboardPage } from '../src/js/pages/analytics-dashboard-page.js';

test('dashboard exposes on-demand service checks and privacy boundaries', () => {
  const page = renderAnalyticsDashboardPage();
  assert.match(page, /data-analytics-refresh/);
  assert.match(page, /This version is stateless; no database is configured/);
  assert.match(page, /No activity history/);
  assert.match(page, /data-monitoring-service="ml-service"/);
});
