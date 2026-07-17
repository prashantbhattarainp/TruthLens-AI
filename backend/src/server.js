const http = require('node:http');

const app = require('./app');
const config = require('./config/environment');
const { logger } = require('./utils/logger');

const server = http.createServer(app);
let shutdownInProgress = false;

function shutdown(signal) {
  if (shutdownInProgress) {
    return;
  }

  shutdownInProgress = true;
  logger.info(
    {
      event: 'shutdown_started',
      signal,
    },
    'Backend shutdown started',
  );

  server.close((error) => {
    if (error) {
      logger.error(
        {
          err: error,
          event: 'shutdown_failed',
        },
        'Backend shutdown failed',
      );
      process.exitCode = 1;
    } else {
      logger.info(
        {
          event: 'shutdown_completed',
          signal,
        },
        'Backend shutdown completed',
      );
    }

    process.exit();
  });

  setTimeout(() => {
    logger.error(
      {
        event: 'shutdown_timeout',
      },
      'Backend shutdown timed out',
    );
    process.exit(1);
  }, config.shutdownTimeoutMs).unref();
}

server.listen(config.port, config.host, () => {
  logger.info(
    {
      environment: config.environment,
      event: 'server_started',
      host: config.host,
      port: config.port,
      version: config.version,
    },
    'Backend server started',
  );
});

process.on('SIGINT', () => shutdown('SIGINT'));
process.on('SIGTERM', () => shutdown('SIGTERM'));
