const MlServiceClient = require('../clients/ml-service-client');
const config = require('../config/environment');
const { logger } = require('../utils/logger');
const predictionResponseSchema = require('../validators/schemas/prediction-response-schema');

const mlServiceClient = new MlServiceClient({
  baseUrl: config.mlServiceUrl,
  retryAttempts: config.mlServiceRetryAttempts,
  retryDelayMs: config.mlServiceRetryDelayMs,
  timeoutMs: config.requestTimeoutMs,
});

function createInvalidResponseResult(requestId, issues) {
  logger.warn(
    {
      request_id: requestId,
      validation_issues: issues.map((issue) => ({
        code: issue.code,
        path: issue.path.join('.'),
      })),
    },
    'ml_prediction_response_invalid',
  );

  return {
    error: {
      code: 'ML_SERVICE_INVALID_RESPONSE',
      message: 'ML service returned an invalid prediction response.',
    },
    ok: false,
  };
}

async function getPrediction({ article, headline, requestId }) {
  const mlPrediction = await mlServiceClient.predict({
    article,
    headline,
    requestId,
  });

  if (!mlPrediction.ok) {
    return {
      error: mlPrediction.error,
      ok: false,
    };
  }

  const validationResult = predictionResponseSchema.safeParse(mlPrediction.data);

  if (!validationResult.success) {
    return createInvalidResponseResult(requestId, validationResult.error.issues);
  }

  logger.info(
    {
      ml_service_response_time_ms: mlPrediction.responseTimeMs,
      request_id: requestId,
    },
    'prediction_service_completed',
  );

  return {
    data: validationResult.data,
    ok: true,
  };
}

module.exports = {
  getPrediction,
};
