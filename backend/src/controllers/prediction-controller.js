const { getPrediction } = require('../services/prediction-service');
const AppError = require('../utils/app-error');
const { sendSuccess } = require('../utils/api-response');
const { getRequestLogger } = require('../utils/logger');

function getMlServiceErrorStatusCode(errorCode) {
  if (errorCode === 'VALIDATION_ERROR' || errorCode === 'EMPTY_PROCESSED_INPUT') {
    return 422;
  }
  if (errorCode === 'ML_SERVICE_TIMEOUT') {
    return 504;
  }

  if (errorCode === 'ML_SERVICE_HTTP_ERROR' || errorCode === 'ML_SERVICE_INVALID_RESPONSE') {
    return 502;
  }

  return 503;
}

async function createPrediction(request, response, next) {
  try {
    const predictionResult = await getPrediction({
      article: request.validated.body.article,
      headline: request.validated.body.headline,
      requestId: request.requestId,
    });

    if (!predictionResult.ok) {
      return next(
        new AppError({
          statusCode: getMlServiceErrorStatusCode(predictionResult.error.code),
          code: predictionResult.error.code,
          message: predictionResult.error.message,
        }),
      );
    }

    getRequestLogger(request).info(
      {
        prediction: predictionResult.data.prediction,
        request_id: request.requestId,
        status_code: 200,
      },
      'prediction_response_sent',
    );

    return sendSuccess(response, {
      data: predictionResult.data,
      requestId: request.requestId,
    });
  } catch (error) {
    return next(error);
  }
}

module.exports = {
  createPrediction,
};
