function getConfidenceLabel(confidence) {
  if (confidence >= 0.8) {
    return 'High confidence';
  }

  if (confidence >= 0.6) {
    return 'Moderate confidence';
  }

  return 'Low confidence';
}

export function getConfidencePresentation(confidence) {
  if (!Number.isFinite(confidence)) {
    return {
      ariaValueNow: 0,
      ariaValueText: 'Confidence unavailable. The decision margin is not a probability.',
      badgeLabel: 'Unavailable',
      displayValue: 'Unavailable',
      label: 'Not calibrated',
      progress: '0%',
      status: 'unavailable',
    };
  }

  const percent = Math.round(confidence * 100);
  const label = getConfidenceLabel(confidence);

  return {
    ariaValueNow: percent,
    ariaValueText: `${percent}% - ${label}`,
    badgeLabel: `${percent}%`,
    displayValue: `${percent}%`,
    label,
    progress: `${percent}%`,
    status: 'available',
  };
}
