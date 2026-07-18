import test from 'node:test';
import assert from 'node:assert/strict';

import { getPredictionErrorPresentation } from '../src/js/prediction/error-presentation.js';
import { formatContributionScore, getContributionPresentation, getExplainabilityPresentation } from '../src/js/prediction/explanation-presentation.js';

test('formats contribution directions without assigning factual meaning', () => {
  assert.equal(formatContributionScore(0.125), '+0.125');
  assert.deepEqual(getContributionPresentation({ contribution: -0.42, direction: 'supports_real_margin', feature: 'verified', rank: 2 }), {
    className: 'contribution-item--real', directionLabel: 'Supports the Real classification', feature: 'verified', rank: 2, score: '-0.420',
  });
});

test('distinguishes unavailable explainability and service errors', () => {
  assert.equal(getExplainabilityPresentation().label, 'Unavailable');
  assert.equal(getPredictionErrorPresentation({ code: 'ML_SERVICE_UNAVAILABLE' }).title, 'Model service unavailable');
  assert.equal(getPredictionErrorPresentation({ code: 'ML_SERVICE_TIMEOUT' }).title, 'Request timed out');
  assert.equal(getPredictionErrorPresentation({ code: 'INVALID_RESPONSE' }).title, 'Unexpected service response');
  assert.equal(getPredictionErrorPresentation({ status: 404 }).title, 'Service endpoint unavailable');
});
