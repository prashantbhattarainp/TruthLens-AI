const express = require('express');

const { createPrediction } = require('../controllers/prediction-controller');
const logPredictionRequest = require('../middleware/prediction-request-logger');
const predictionRequestSchema = require('../validators/schemas/prediction-request-schema');
const validateRequest = require('../validators/validate-request');

const router = express.Router();

router.post(
  '/',
  logPredictionRequest,
  validateRequest(predictionRequestSchema, 'body', {
    schemaName: 'prediction_request',
  }),
  createPrediction,
);

module.exports = router;
