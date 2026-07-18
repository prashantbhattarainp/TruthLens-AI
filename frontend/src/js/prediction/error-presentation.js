const ML_SERVICE_ERROR_CODES = new Set([
  'ML_SERVICE_HTTP_ERROR',
  'ML_SERVICE_INVALID_RESPONSE',
  'ML_SERVICE_NOT_CONFIGURED',
  'ML_SERVICE_UNAVAILABLE',
  'MODEL_NOT_READY',
  'MODEL_PACKAGE_UNAVAILABLE',
]);

export function getPredictionErrorPresentation(error = {}) {
  if (error.code === 'VALIDATION_ERROR' || error.code === 'EMPTY_PROCESSED_INPUT') {
    return {
      message:
        'The backend rejected the submitted content. Review the field requirements and try again.',
      title: 'Content needs attention',
    };
  }

  if (error.code === 'REQUEST_TIMEOUT' || error.code === 'ML_SERVICE_TIMEOUT') {
    return {
      message: 'The prediction service did not respond before the request timeout. Please try again.',
      title: 'Request timed out',
    };
  }

  if (error.code === 'NETWORK_ERROR') {
    return {
      message: 'The TruthLens backend could not be reached. Confirm it is running and try again.',
      title: 'Backend unavailable',
    };
  }

  if (ML_SERVICE_ERROR_CODES.has(error.code)) {
    return {
      message:
        'The model service is currently unable to complete predictions. The submitted text was not classified.',
      title: 'Model service unavailable',
    };
  }

  if (error.status >= 500) {
    return {
      message: 'The backend could not complete this prediction request. Please try again.',
      title: 'Prediction unavailable',
    };
  }

  return {
    message: 'The prediction request could not be completed. Please try again.',
    title: 'Prediction unavailable',
  };
}
