const config = require('../config/environment');

function cors(request, response, next) {
  const origin = request.get('origin');

  if (!origin || !config.corsAllowedOrigins.includes(origin)) {
    return next();
  }

  response.setHeader('Access-Control-Allow-Origin', origin);
  response.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  response.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-Request-Id');
  response.setHeader('Access-Control-Expose-Headers', 'X-Request-Id');
  response.setHeader('Vary', 'Origin');

  if (request.method === 'OPTIONS') {
    return response.sendStatus(204);
  }

  return next();
}

module.exports = cors;
