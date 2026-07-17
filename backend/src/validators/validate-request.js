const AppError = require('../utils/app-error');
const { getRequestLogger } = require('../utils/logger');

function validateRequest(schema, source = 'body', { schemaName = 'request' } = {}) {
  return (request, _response, next) => {
    const result = schema.safeParse(request[source]);
    const logger = getRequestLogger(request);

    if (!result.success) {
      const issues = result.error.issues.map((issue) => ({
        code: issue.code,
        path: issue.path.join('.'),
      }));

      logger.warn(
        {
          request_id: request.requestId,
          validation_issues: issues,
          validation_schema: schemaName,
          validation_source: source,
        },
        'request_validation_failed',
      );

      return next(
        new AppError({
          statusCode: 400,
          code: 'VALIDATION_ERROR',
          message: 'Request validation failed.',
          metadata: {
            issues,
          },
        }),
      );
    }

    request.validated = {
      ...request.validated,
      [source]: result.data,
    };

    logger.info(
      {
        request_id: request.requestId,
        validation_schema: schemaName,
        validation_source: source,
      },
      'request_validation_succeeded',
    );

    return next();
  };
}

module.exports = validateRequest;
