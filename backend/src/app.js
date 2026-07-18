const express = require('express');

const config = require('./config/environment');
const healthRoutes = require('./routes/health-routes');
const predictionRoutes = require('./routes/prediction-routes');
const systemHealthRoutes = require('./routes/system-health-routes');
const cors = require('./middleware/cors');
const errorHandler = require('./middleware/error-handler');
const notFoundHandler = require('./middleware/not-found');
const requestContext = require('./middleware/request-context');
const requestLogger = require('./middleware/request-logger');
const { createHttpLogger } = require('./utils/logger');

const app = express();
app.disable('x-powered-by');
app.use(requestContext);
app.use(createHttpLogger());
app.use(requestLogger);
app.use(cors);
app.use(express.json({ limit: config.requestBodyLimit }));
app.use(express.urlencoded({ extended: false, limit: config.requestBodyLimit }));
app.use('/api/health', healthRoutes);
app.use('/api/predict', predictionRoutes);
app.use('/api/system/health', systemHealthRoutes);
app.use(notFoundHandler);
app.use(errorHandler);

module.exports = app;
