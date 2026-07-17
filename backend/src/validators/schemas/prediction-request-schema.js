const { z } = require('zod');

const predictionRequestSchema = z
  .object({
    headline: z.string().trim().min(1).max(300),
    article: z.string().trim().min(100).max(15000),
  })
  .strict();

module.exports = predictionRequestSchema;
