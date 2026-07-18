import { getConfidencePresentation } from './confidence-badge.js';
import { renderExplanationDashboard } from './explanation-panel.js';

function getResultElements(resultCard) {
  return {
    confidenceBadge: resultCard.querySelector('[data-confidence-badge]'),
    confidenceLabel: resultCard.querySelector('[data-confidence-label]'),
    confidenceProgress: resultCard.querySelector('[data-confidence-progress]'),
    confidenceProgressFill: resultCard.querySelector('[data-confidence-progress-fill]'),
    datasetVersion: resultCard.querySelector('[data-dataset-version]'),
    decisionScore: resultCard.querySelector('[data-decision-score]'),
    error: resultCard.querySelector('[data-result-error]'),
    errorMessage: resultCard.querySelector('[data-result-error-message]'),
    errorTitle: resultCard.querySelector('[data-result-error-title]'),
    explanationList: resultCard.querySelector('[data-explanation-list]'),
    explanationSummary: resultCard.querySelector('[data-explanation-summary]'),
    initial: resultCard.querySelector('[data-result-initial]'),
    keywordList: resultCard.querySelector('[data-keyword-list]'),
    loadingDescription: resultCard.querySelector('[data-loading-description]'),
    loadingPanel: resultCard.querySelector('[data-loading-panel]'),
    loadingTitle: resultCard.querySelector('[data-loading-title]'),
    modelName: resultCard.querySelector('[data-model-name]'),
    modelVersion: resultCard.querySelector('[data-model-version]'),
    requestId: resultCard.querySelector('[data-request-id]'),
    responseTimestamp: resultCard.querySelector('[data-response-timestamp]'),
    resultConfidence: resultCard.querySelector('[data-result-confidence]'),
    resultContent: resultCard.querySelector('[data-result-content]'),
    resultHeading: resultCard.querySelector('[data-result-heading]'),
    resultPrediction: resultCard.querySelector('[data-result-prediction]'),
    resultRisk: resultCard.querySelector('[data-result-risk]'),
    resultStatus: resultCard.querySelector('[data-result-status]'),
    resultStatusDot: resultCard.querySelector('[data-result-status-dot]'),
    resultTime: resultCard.querySelector('[data-result-time]'),
  };
}

function renderList(listElement, items, className, itemElementName = 'li') {
  listElement.replaceChildren(
    ...items.map((item) => {
      const listItem = document.createElement(itemElementName);
      listItem.className = className;
      listItem.textContent = item;
      return listItem;
    }),
  );
}

function formatRiskLevel(riskLevel) {
  return `${riskLevel.charAt(0).toUpperCase()}${riskLevel.slice(1)}`.replaceAll('_', ' ');
}

function formatTimestamp(timestamp) {
  const date = new Date(timestamp);

  if (Number.isNaN(date.getTime())) {
    return 'Not provided';
  }

  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'medium',
  }).format(date);
}

function formatDecisionScore(score) {
  return Number.isFinite(score) ? score.toFixed(3) : 'Unavailable';
}

function setResultStatus(elements, message, state = 'pending') {
  elements.resultStatus.textContent = message;
  elements.resultStatusDot?.classList.toggle('status-dot--success', state === 'success');
}

function hideAllResultStates(elements) {
  elements.error.hidden = true;
  elements.initial.hidden = true;
  elements.loadingPanel.hidden = true;
  elements.resultContent.hidden = true;
}

export function showInitialResult(resultCard) {
  const elements = getResultElements(resultCard);

  hideAllResultStates(elements);
  elements.initial.hidden = false;
  resultCard.setAttribute('aria-busy', 'false');
  resultCard.setAttribute('aria-labelledby', 'result-title');
  resultCard.removeAttribute('aria-label');
  setResultStatus(elements, 'Waiting for input');
}

export function showLoadingState(resultCard, loadingState) {
  const elements = getResultElements(resultCard);

  hideAllResultStates(elements);
  elements.loadingPanel.hidden = false;
  elements.loadingTitle.textContent = loadingState.title;
  elements.loadingDescription.textContent = loadingState.description;
  resultCard.setAttribute('aria-busy', 'true');
  resultCard.setAttribute('aria-label', loadingState.title);
  resultCard.removeAttribute('aria-labelledby');
  setResultStatus(elements, 'Request in progress');
}

export function showPredictionResult(resultCard, response) {
  const elements = getResultElements(resultCard);
  const { data } = response;
  const confidence = getConfidencePresentation(data.confidence);

  hideAllResultStates(elements);
  elements.resultContent.hidden = false;
  elements.resultHeading.textContent = `Prediction: ${data.prediction}`;
  elements.resultPrediction.textContent = data.prediction;
  elements.resultConfidence.textContent = confidence.displayValue;
  elements.resultRisk.textContent = formatRiskLevel(data.risk_level);
  elements.decisionScore.textContent = formatDecisionScore(data.decision_score);
  elements.resultTime.textContent = `${data.processing_time_ms} ms`;
  elements.confidenceBadge.textContent = confidence.badgeLabel;
  elements.confidenceLabel.textContent = confidence.label;
  elements.confidenceProgress.setAttribute('aria-valuenow', String(confidence.ariaValueNow));
  elements.confidenceProgress.setAttribute('aria-valuetext', confidence.ariaValueText);
  elements.confidenceProgress.dataset.status = confidence.status;
  elements.confidenceProgressFill.style.setProperty(
    '--confidence-progress',
    confidence.progress,
  );
  setResultStatus(elements, 'Response received from backend', 'success');
  elements.explanationSummary.textContent = data.explanation?.summary ?? 'Explanation metadata was unavailable.';
  elements.modelName.textContent = data.model;
  elements.modelVersion.textContent = data.model_version;
  elements.datasetVersion.textContent = data.dataset_version;
  elements.responseTimestamp.textContent = formatTimestamp(response.timestamp);
  elements.requestId.textContent = response.requestId ?? 'Not provided';
  renderList(elements.explanationList, data.explanation?.reasons ?? [], 'explanation-list__item');
  renderList(elements.keywordList, data.keywords ?? [], 'keyword-list__item', 'span');
  renderExplanationDashboard(resultCard, data.explainability);
  resultCard.setAttribute('aria-busy', 'false');
  resultCard.setAttribute('aria-labelledby', 'result-title-complete');
  resultCard.removeAttribute('aria-label');
  resultCard.focus();
}

export function showErrorState(resultCard, { message, title }) {
  const elements = getResultElements(resultCard);

  hideAllResultStates(elements);
  elements.error.hidden = false;
  elements.errorTitle.textContent = title;
  elements.errorMessage.textContent = message;
  resultCard.setAttribute('aria-busy', 'false');
  resultCard.setAttribute('aria-labelledby', 'result-error-title');
  resultCard.removeAttribute('aria-label');
  setResultStatus(elements, 'Prediction unavailable');
  resultCard.focus();
}
