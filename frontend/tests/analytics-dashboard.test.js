import test from 'node:test';
import assert from 'node:assert/strict';

import { DASHBOARD_EVIDENCE, PERFORMANCE_SERIES } from '../src/js/analytics/dashboard-data.js';
import {
  getPerformanceMetric,
  renderDatasetCompositionChart,
  renderPerformanceChart,
} from '../src/js/analytics/chart-renderer.js';
import { renderAnalyticsDashboardPage } from '../src/js/pages/analytics-dashboard-page.js';

test('analytics evidence retains the governed model and dataset boundaries', () => {
  assert.equal(DASHBOARD_EVIDENCE.model.version, 'TL-LSVM-TFIDF-v1.1.0-rc.1');
  assert.equal(DASHBOARD_EVIDENCE.dataset.validationRecords, 1461);
  assert.equal(DASHBOARD_EVIDENCE.predictionDistribution.note.includes('Illustrative placeholder'), true);
  assert.equal(PERFORMANCE_SERIES.find(({ label }) => label === 'LinearSVC').macroF1, 0.5398);
});

test('chart renderers expose accessible frozen-evidence descriptions', () => {
  assert.equal(getPerformanceMetric('missing').label, 'Macro F1');
  assert.match(renderPerformanceChart('fakeRecall'), /FAKE recall comparison/);
  assert.match(renderDatasetCompositionChart(), /Frozen dataset composition/);
});

test('dashboard page exposes status checks and retention boundaries', () => {
  const page = renderAnalyticsDashboardPage();

  assert.match(page, /data-analytics-refresh/);
  assert.match(page, /No database status endpoint is implemented/);
  assert.match(page, /Prediction history is not implemented/);
  assert.match(page, /data-performance-chart/);
});
