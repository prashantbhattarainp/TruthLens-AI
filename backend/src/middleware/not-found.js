const AppError = require('../utils/app-error');

function notFoundHandler(request, _response, next) {
  next(
    new AppError({
      statusCode: 404,
      code: 'NOT_FOUND',
      message: `No route matches ${request.method} ${request.originalUrl}.`,
    }),
  );
}

module.exports = notFoundHandler;
