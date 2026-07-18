const express = require('express');

const {
  getModelMetadata,
  getModelReady,
  getModelVersion,
} = require('../controllers/model-controller');

const router = express.Router();

router.get('/ready', getModelReady);
router.get('/metadata', getModelMetadata);
router.get('/version', getModelVersion);

module.exports = router;
