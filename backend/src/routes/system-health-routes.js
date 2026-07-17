const express = require('express');

const { getSystemHealthStatus } = require('../controllers/system-health-controller');

const router = express.Router();

router.get('/', getSystemHealthStatus);

module.exports = router;
