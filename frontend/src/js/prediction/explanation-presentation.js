const DIRECTION_PRESENTATIONS = Object.freeze({
  minimal_effect: {
    className: 'contribution-item--minimal',
    label: 'Minimal effect on the model margin',
  },
  supports_fake_margin: {
    className: 'contribution-item--fake',
    label: 'Supports the Fake-class margin',
  },
  supports_real_margin: {
    className: 'contribution-item--real',
    label: 'Supports the Real-class margin',
  },
});

export function formatContributionScore(contribution) {
  if (!Number.isFinite(contribution)) {
    return 'Unavailable';
  }

  return `${contribution > 0 ? '+' : ''}${contribution.toFixed(3)}`;
}

export function getContributionPresentation(contribution = {}) {
  const direction = DIRECTION_PRESENTATIONS[contribution.direction] ??
    DIRECTION_PRESENTATIONS.minimal_effect;

  return {
    className: direction.className,
    directionLabel: direction.label,
    feature: contribution.feature || 'Unnamed feature',
    rank: Number.isInteger(contribution.rank) ? contribution.rank : null,
    score: formatContributionScore(contribution.contribution),
  };
}

export function getExplainabilityPresentation(explainability) {
  if (!explainability) {
    return {
      disclaimer: 'This prediction did not include explanation metadata.',
      label: 'Unavailable',
      status: 'unavailable',
    };
  }

  const metadata = explainability.metadata ?? {};
  const isAvailable = metadata.status === 'available';

  return {
    disclaimer:
      metadata.disclaimer ??
      (isAvailable
        ? 'Feature contributions describe the model margin, not factual truth or confidence.'
        : 'The backend could not provide explanation metadata for this prediction.'),
    label: isAvailable ? 'Available' : 'Unavailable',
    status: isAvailable ? 'available' : 'unavailable',
  };
}
