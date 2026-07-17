const { getSystemHealth } = require('../services/system-health-service');
const AppError = require('../utils/app-error');
const { sendSuccess } = require('../utils/api-response');

async function getSystemHealthStatus(request, response, next) {
  try {
    const systemHealth = await getSystemHealth({
      requestId: request.requestId,
    });

    if (!systemHealth.ok) {
      return next(
        new AppError({
          statusCode: 503,
          code: systemHealth.error.code,
          message: systemHealth.error.message,
        }),
      );
    }

    return sendSuccess(response, {
      data: {
        backend: systemHealth.backend,
        ml_service: systemHealth.mlService,
      },
      requestId: request.requestId,
    });
  } catch (error) {
    return next(error);
  }
}

module.exports = {
  getSystemHealthStatus,
};
