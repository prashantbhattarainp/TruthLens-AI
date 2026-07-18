import test from 'node:test';
import assert from 'node:assert/strict';

import { getConfidencePresentation } from '../src/js/prediction/confidence-badge.js';
import { getPredictionErrorPresentation } from '../src/js/prediction/error-presentation.js';
import {
  formatContributionScore,
  getContributionPresentation,
  getExplainabilityPresentation,
} from '../src/js/prediction/explanation-presentation.js';

test('keeps unavailable LinearSVC confidence distinct from a percentage', () => {
  assert.deepEqual(getConfidencePresentation(null), {
    ariaValueNow: 0,
    ariaValueText: 'Confidence unavailable. The decision margin is not a probability.',
    badgeLabel: 'Unavailable',
    displayValue: 'Unavailable',
    label: 'Not calibrated',
    progress: '0%',
    status: 'unavailable',
  });
});

test('formats bounded contribution directions without assigning factual meaning', () => {
  assert.equal(formatContributionScore(0.125), '+0.125');
  assert.deepEqual(
    getContributionPresentation({
      contribution: -0.42,
      direction: 'supports_real_margin',
      feature: 'verified',
      rank: 2,
    }),
    {
      className: 'contribution-item--real',
      directionLabel: 'Supports the Real-class margin',
      feature: 'verified',
      rank: 2,
      score: '-0.420',
    },
  );
});

test('distinguishes unavailable explainability and model-service errors', () => {
  assert.equal(getExplainabilityPresentation().label, 'Unavailable');
  assert.equal(
    getPredictionErrorPresentation({ code: 'ML_SERVICE_UNAVAILABLE' }).title,
    'Model service unavailable',
  );
  assert.equal(
    getPredictionErrorPresentation({ code: 'ML_SERVICE_TIMEOUT' }).title,
    'Request timed out',
  );
});
