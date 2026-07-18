const { z } = require('zod');

const predictionResponseSchema = z
  .object({
    prediction: z.enum(['Real', 'Fake']),
    confidence: z.null(),
    confidence_status: z.literal('unavailable'),
    decision_score: z.number().finite(),
    risk_level: z.literal('not_assessed'),
    explanation: z
      .object({
        summary: z.string(),
        reasons: z.array(z.string()),
      })
      .strict(),
    keywords: z.array(z.string()),
    processing_time_ms: z.number().int().nonnegative(),
    model: z.string(),
    model_version: z.string(),
    dataset_version: z.string(),
  })
  .strict();

module.exports = predictionResponseSchema;
