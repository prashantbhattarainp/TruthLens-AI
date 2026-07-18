const AppError = require('../utils/app-error');
const { sendError } = require('../utils/api-response');
const { getRequestLogger } = require('../utils/logger');

function normalizeError(error) {
  if (error instanceof AppError) {
    return {
      code: error.code,
      message: error.message,
      metadata: error.metadata,
      statusCode: error.statusCode,
    };
  }

  if (error.type === 'entity.parse.failed') {
    return {
      code: 'INVALID_JSON',
      message: 'Request body contains invalid JSON.',
      metadata: {},
      statusCode: 400,
    };
  }

  return {
    code: 'INTERNAL_SERVER_ERROR',
    message: 'An unexpected error occurred.',
    metadata: {},
    statusCode: 500,
  };
}

function errorHandler(error, request, response, _next) {
  const normalizedError = normalizeError(error);
  const logger = getRequestLogger(request);

  logger.error(
    {
      error_code: normalizedError.code,
      error_metadata: normalizedError.metadata,
      error_name: error.name,
      request_id: request.requestId,
      status_code: normalizedError.statusCode,
    },
    'request_failed',
  );

  return sendError(response, {
    code: normalizedError.code,
    message: normalizedError.message,
    requestId: request.requestId,
    statusCode: normalizedError.statusCode,
  });
}

module.exports = errorHandler;
