const config = require('../config/environment');
const { sendSuccess } = require('../utils/api-response');

function getHealth(request, response) {
  return sendSuccess(response, {
    data: {
      service: config.serviceName,
      status: 'healthy',
      version: config.version,
    },
    requestId: request.requestId,
  });
}

module.exports = {
  getHealth,
};
