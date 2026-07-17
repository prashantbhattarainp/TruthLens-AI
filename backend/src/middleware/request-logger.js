const { getRequestLogger } = require('../utils/logger');

function getLogLevel(statusCode) {
  if (statusCode >= 500) {
    return 'error';
  }

  if (statusCode >= 400) {
    return 'warn';
  }

  return 'info';
}

function requestLogger(request, response, next) {
  const startedAt = process.hrtime.bigint();

  response.on('finish', () => {
    const responseTimeMs = Number(
      (Number(process.hrtime.bigint() - startedAt) / 1_000_000).toFixed(2),
    );
    const statusCode = response.statusCode;
    const outcome = statusCode >= 400 ? 'failure' : 'success';
    const logger = getRequestLogger(request);

    logger[getLogLevel(statusCode)](
      {
        request_id: request.requestId,
        http: {
          endpoint: request.originalUrl,
          method: request.method,
          response_time_ms: responseTimeMs,
          status_code: statusCode,
        },
        outcome,
      },
      'request_completed',
    );
  });

  next();
}

module.exports = requestLogger;
