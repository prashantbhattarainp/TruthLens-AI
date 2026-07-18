import {
  getContributionPresentation,
  getExplainabilityPresentation,
} from './explanation-presentation.js';

function setText(element, value) {
  if (element) {
    element.textContent = value;
  }
}

function formatNumber(value) {
  return Number.isFinite(value) ? value.toFixed(3) : 'Unavailable';
}

function renderMetadata(element, entries) {
  setText(
    element,
    entries
      .filter(([, value]) => value !== undefined && value !== null)
      .map(([label, value]) => `${label}: ${value}`)
      .join('; '),
  );
}

export function renderContributionList(listElement, contributions, emptyMessage) {
  if (!listElement) {
    return;
  }

  if (!Array.isArray(contributions) || contributions.length === 0) {
    const emptyItem = document.createElement('li');
    emptyItem.className = 'xai-empty';
    emptyItem.textContent = emptyMessage;
    listElement.replaceChildren(emptyItem);
    return;
  }

  listElement.replaceChildren(
    ...contributions.map((contribution) => {
      const presentation = getContributionPresentation(contribution);
      const item = document.createElement('li');
      item.className = `contribution-item ${presentation.className}`;

      const feature = document.createElement('span');
      feature.className = 'contribution-item__feature';
      feature.textContent = presentation.rank ? `${presentation.rank}. ${presentation.feature}` : presentation.feature;

      const direction = document.createElement('span');
      direction.className = 'contribution-item__direction';
      direction.textContent = presentation.directionLabel;

      const score = document.createElement('strong');
      score.className = 'contribution-item__score';
      score.textContent = presentation.score;

      item.append(feature, direction, score);
      return item;
    }),
  );
}

export function renderExplanationDashboard(resultCard, explainability) {
  const presentation = getExplainabilityPresentation(explainability);
  const elements = {
    disclaimer: resultCard.querySelector('[data-explainability-disclaimer]'),
    limeDetails: resultCard.querySelector('[data-lime-details]'),
    limeNegative: resultCard.querySelector('[data-lime-negative-list]'),
    limePositive: resultCard.querySelector('[data-lime-positive-list]'),
    limeStatus: resultCard.querySelector('[data-lime-status]'),
    shapDetails: resultCard.querySelector('[data-shap-details]'),
    shapNegative: resultCard.querySelector('[data-shap-negative-list]'),
    shapPositive: resultCard.querySelector('[data-shap-positive-list]'),
    shapStatus: resultCard.querySelector('[data-shap-status]'),
    status: resultCard.querySelector('[data-explainability-status]'),
    topFeatures: resultCard.querySelector('[data-top-feature-list]'),
  };
  const unavailableMessage = 'No contribution details were returned for this prediction.';

  setText(elements.status, presentation.label);
  setText(elements.disclaimer, presentation.disclaimer);
  renderContributionList(elements.topFeatures, explainability?.top_influential_features, unavailableMessage);

  const shap = presentation.status === 'available' ? explainability?.shap : null;
  setText(elements.shapStatus, shap ? 'Available' : 'Unavailable');
  renderMetadata(
    elements.shapDetails,
    shap
      ? [
          ['Method', shap.method],
          ['Baseline', shap.baseline],
          ['Base value', formatNumber(shap.base_value)],
          ['Additivity residual', formatNumber(shap.additive_residual)],
        ]
      : [['Status', unavailableMessage]],
  );
  renderContributionList(elements.shapPositive, shap?.top_positive_features, unavailableMessage);
  renderContributionList(elements.shapNegative, shap?.top_negative_features, unavailableMessage);

  const lime = presentation.status === 'available' ? explainability?.lime : null;
  setText(elements.limeStatus, lime ? 'Available' : 'Unavailable');
  renderMetadata(
    elements.limeDetails,
    lime
      ? [
          ['Method', lime.method],
          ['Target', lime.target],
          ['Local fidelity', formatNumber(lime.local_fidelity)],
          ['Samples', lime.sample_count],
          ['Seed', lime.random_seed],
        ]
      : [['Status', unavailableMessage]],
  );
  renderContributionList(elements.limePositive, lime?.top_positive_features, unavailableMessage);
  renderContributionList(elements.limeNegative, lime?.top_negative_features, unavailableMessage);
}
