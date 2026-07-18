import {
  DASHBOARD_EVIDENCE,
  PERFORMANCE_METRICS,
  PERFORMANCE_SERIES,
} from './dashboard-data.js';

function formatMetricValue(value) {
  return value.toFixed(4);
}

export function getPerformanceMetric(metricId) {
  return PERFORMANCE_METRICS[metricId] ?? PERFORMANCE_METRICS.macroF1;
}

export function renderPerformanceChart(metricId = 'macroF1') {
  const metric = getPerformanceMetric(metricId);
  const rows = PERFORMANCE_SERIES.map((series, index) => {
    const value = series[metricId] ?? series.macroF1;
    const y = 34 + index * 37;
    const width = Math.round((value / metric.maximum) * 270);
    const tone = series.label === 'LinearSVC' ? 'chart-bar--champion' : 'chart-bar--comparison';

    return `
      <text class="chart-svg__label" x="0" y="${y + 13}">${series.label}</text>
      <rect class="chart-svg__track" x="125" y="${y}" width="270" height="18" rx="4"></rect>
      <rect class="chart-svg__bar ${tone}" x="125" y="${y}" width="${width}" height="18" rx="4"></rect>
      <text class="chart-svg__value" x="405" y="${y + 13}">${formatMetricValue(value)}</text>
    `;
  }).join('');

  return `
    <svg class="chart-svg" viewBox="0 0 470 205" role="img" aria-labelledby="performance-chart-title performance-chart-description">
      <title id="performance-chart-title">${metric.label} comparison across evaluated validation candidates</title>
      <desc id="performance-chart-description">${metric.sourceLabel} values for the internal LinearSVC champion and three evaluated research challengers. This comparison does not promote a production model.</desc>
      ${rows}
      <line class="chart-svg__axis" x1="125" y1="190" x2="395" y2="190"></line>
      <text class="chart-svg__axis-label" x="125" y="203">0</text>
      <text class="chart-svg__axis-label" x="365" y="203">${metric.maximum.toFixed(2)}</text>
    </svg>
  `;
}

export function renderDatasetCompositionChart() {
  const { fakeRecords, realRecords } = DASHBOARD_EVIDENCE.dataset;
  const total = fakeRecords + realRecords;
  const realPercent = (realRecords / total) * 100;
  const fakePercent = 100 - realPercent;

  return `
    <div class="donut-chart" role="img" aria-label="Frozen dataset composition: ${realRecords.toLocaleString()} REAL records and ${fakeRecords.toLocaleString()} FAKE records.">
      <svg viewBox="0 0 120 120" aria-hidden="true">
        <circle class="donut-chart__track" cx="60" cy="60" r="42"></circle>
        <circle class="donut-chart__real" cx="60" cy="60" r="42" pathLength="100" stroke-dasharray="${realPercent} ${fakePercent}"></circle>
        <circle class="donut-chart__fake" cx="60" cy="60" r="42" pathLength="100" stroke-dasharray="${fakePercent} ${realPercent}" stroke-dashoffset="-${realPercent}"></circle>
      </svg>
      <div class="donut-chart__center"><strong>${total.toLocaleString()}</strong><span>records</span></div>
    </div>
    <ul class="chart-legend" aria-label="Dataset composition legend">
      <li><span class="chart-legend__swatch chart-legend__swatch--real"></span>REAL <strong>${realRecords.toLocaleString()}</strong></li>
      <li><span class="chart-legend__swatch chart-legend__swatch--fake"></span>FAKE <strong>${fakeRecords.toLocaleString()}</strong></li>
    </ul>
  `;
}

export function renderPredictionDistributionChart() {
  const { fake, real } = DASHBOARD_EVIDENCE.predictionDistribution;

  return `
    <div class="distribution-chart" role="img" aria-label="Illustrative placeholder prediction distribution: ${real}% Real and ${fake}% Fake. No prediction history is retained.">
      <div class="distribution-chart__bar"><span class="distribution-chart__real" style="width: ${real}%"></span><span class="distribution-chart__fake" style="width: ${fake}%"></span></div>
      <div class="distribution-chart__labels"><span>Real <strong>${real}%</strong></span><span>Fake <strong>${fake}%</strong></span></div>
    </div>
  `;
}

export function renderFeatureImportanceChart() {
  const maximum = DASHBOARD_EVIDENCE.xaiFeatures[0].value;
  const rows = DASHBOARD_EVIDENCE.xaiFeatures.map(({ feature, value }) => `
    <li class="feature-chart__row"><span>${feature}</span><span class="feature-chart__track"><i style="width: ${(value / maximum) * 100}%"></i></span><strong>${value.toFixed(4)}</strong></li>
  `).join('');

  return `<ol class="feature-chart" aria-label="Top mean absolute SHAP features from the train-only reference cohort">${rows}</ol>`;
}
