import { requestPrediction } from '../api/prediction-api.js';
import { PREDICTION_LOADING_STATE } from '../prediction/loading.js';
import {
  showErrorState,
  showInitialResult,
  showLoadingState,
  showPredictionResult,
} from '../prediction/result-card.js';
import {
  createPredictionState,
  PREDICTION_STATUS,
  resetPredictionState,
  setPredictionResponse,
  setPredictionStatus,
} from '../prediction/state.js';
import {
  focusFirstInvalidField,
  getPredictionElements,
  renderValidation,
  setBackendStatus,
  setFormBusy,
  showRequestError,
} from '../prediction/ui.js';
import { trimFormValues, validatePredictionForm } from '../prediction/validation.js';
import { initializeCharacterCounters } from '../prediction/character-counter.js';

function getFormInputs(elements) {
  return {
    articleInput: elements.articleInput,
    headlineInput: elements.headlineInput,
  };
}

function getRequestPayload(elements) {
  return {
    article: elements.articleInput.value,
    headline: elements.headlineInput.value,
  };
}

function getResultErrorDetails(error) {
  if (error.code === 'VALIDATION_ERROR') {
    return {
      message:
        'The backend rejected the submitted content. Review the field requirements and try again.',
      title: 'Content needs attention',
    };
  }

  if (error.code === 'REQUEST_TIMEOUT') {
    return {
      message: 'The backend did not respond before the request timeout. Please try again.',
      title: 'Request timed out',
    };
  }

  if (error.code === 'NETWORK_ERROR') {
    return {
      message: 'The TruthLens backend could not be reached. Confirm it is running and try again.',
      title: 'Backend unavailable',
    };
  }

  return {
    message: 'The backend could not complete this prediction request. Please try again.',
    title: 'Prediction unavailable',
  };
}

export function initializeDetectionInterface() {
  const form = document.querySelector('[data-detection-form]');

  if (!form) {
    return;
  }

  const elements = getPredictionElements(form);
  const state = createPredictionState();
  const updateCharacterCounters = initializeCharacterCounters([
    { counterElement: elements.headlineCounter, inputElement: elements.headlineInput },
    { counterElement: elements.articleCounter, inputElement: elements.articleInput },
  ]);

  const updateValidation = () => {
    const validation = validatePredictionForm(getFormInputs(elements));
    renderValidation(elements, validation, state.touchedFields);
    return validation;
  };

  const handleFieldInteraction = (fieldName) => {
    state.touchedFields.add(fieldName);
    updateValidation();
  };

  elements.headlineInput.addEventListener('input', () => handleFieldInteraction('headline'));
  elements.articleInput.addEventListener('input', () => handleFieldInteraction('article'));
  elements.headlineInput.addEventListener('blur', () => handleFieldInteraction('headline'));
  elements.articleInput.addEventListener('blur', () => handleFieldInteraction('article'));

  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    if (state.status === PREDICTION_STATUS.LOADING) {
      return;
    }

    trimFormValues(getFormInputs(elements));
    updateCharacterCounters();
    state.touchedFields.add('headline');
    state.touchedFields.add('article');

    const validation = updateValidation();

    if (!validation.isValid) {
      focusFirstInvalidField(elements, validation);
      return;
    }

    setPredictionStatus(state, PREDICTION_STATUS.LOADING);
    setFormBusy(elements, true);
    setBackendStatus(elements, {
      message: 'Request in progress',
      state: 'pending',
    });
    showLoadingState(elements.resultCard, PREDICTION_LOADING_STATE);

    try {
      const response = await requestPrediction(getRequestPayload(elements));

      setPredictionResponse(state, response);
      setPredictionStatus(state, PREDICTION_STATUS.COMPLETE);
      showPredictionResult(elements.resultCard, response);
      setBackendStatus(elements, {
        message: 'Prediction API connected',
        state: 'ready',
      });
    } catch (error) {
      const errorDetails = getResultErrorDetails(error);

      setPredictionStatus(state, PREDICTION_STATUS.ERROR);
      showErrorState(elements.resultCard, errorDetails);
      showRequestError(elements, error);
      setBackendStatus(elements, {
        message: 'Prediction API unavailable',
        state: 'error',
      });
    } finally {
      setFormBusy(elements, false);

      if (state.status !== PREDICTION_STATUS.ERROR) {
        updateValidation();
      }
    }
  });

  form.addEventListener('reset', () => {
    window.setTimeout(() => {
      resetPredictionState(state);
      updateCharacterCounters();
      showInitialResult(elements.resultCard);
      setBackendStatus(elements, {
        message: 'Not checked',
        state: 'pending',
      });
      updateValidation();
    }, 0);
  });

  showInitialResult(elements.resultCard);
  setBackendStatus(elements, {
    message: 'Not checked',
    state: 'pending',
  });
  updateValidation();
}
