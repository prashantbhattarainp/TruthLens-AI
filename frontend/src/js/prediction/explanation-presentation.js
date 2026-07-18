const DIRECTION_PRESENTATIONS = Object.freeze({
  minimal_effect: { className: 'contribution-item--minimal', label: 'Minimal effect on the classification' },
  supports_fake_margin: { className: 'contribution-item--fake', label: 'Supports the Fake classification' },
  supports_real_margin: { className: 'contribution-item--real', label: 'Supports the Real classification' },
});

export function formatContributionScore(contribution) {
  return Number.isFinite(contribution) ? `${contribution > 0 ? '+' : ''}${contribution.toFixed(3)}` : 'Unavailable';
}

export function getContributionPresentation(contribution = {}) {
  const direction = DIRECTION_PRESENTATIONS[contribution.direction] ?? DIRECTION_PRESENTATIONS.minimal_effect;
  return { className: direction.className, directionLabel: direction.label, feature: contribution.feature || 'Unnamed feature', rank: Number.isInteger(contribution.rank) ? contribution.rank : null, score: formatContributionScore(contribution.contribution) };
}

export function getExplainabilityPresentation(explainability) {
  if (!explainability) {
    return { disclaimer: 'This prediction did not include explanation details.', label: 'Unavailable', status: 'unavailable' };
  }
  const metadata = explainability.metadata ?? {};
  const isAvailable = metadata.status === 'available';
  return {
    disclaimer: metadata.disclaimer ?? (isAvailable ? 'Contributing features describe the automated classification, not factual truth or certainty.' : 'The backend could not provide explanation details for this prediction.'),
    label: isAvailable ? 'Available' : 'Unavailable',
    status: isAvailable ? 'available' : 'unavailable',
  };
}
