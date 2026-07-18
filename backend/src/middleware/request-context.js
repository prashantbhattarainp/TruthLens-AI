const { randomUUID } = require('node:crypto');

function requestContext(request, response, next) {
  const requestId = randomUUID();

  request.requestId = requestId;
  response.setHeader('X-Request-Id', requestId);
  next();
}

module.exports = requestContext;
