const { getRequestLogger } = require('../utils/logger');

function getFieldLength(value) {
  return typeof value === 'string' ? value.length : null;
}

function logPredictionRequest(request, _response, next) {
  const logger = getRequestLogger(request);

  logger.info(
    {
      article_length: getFieldLength(request.body?.article),
      headline_length: getFieldLength(request.body?.headline),
      request_id: request.requestId,
    },
    'prediction_request_received',
  );

  return next();
}

module.exports = logPredictionRequest;
