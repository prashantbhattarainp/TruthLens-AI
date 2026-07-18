const { z } = require('zod');

const modelReadySchema = z
  .object({
    status: z.literal('ready'),
    model_loaded: z.literal(true),
    model_version: z.string(),
    deployment_status: z.string(),
  })
  .strict();

const modelMetadataSchema = z
  .object({
    model_name: z.string(),
    model_version: z.string(),
    deployment_status: z.string(),
    dataset_version: z.string(),
    feature_engineering_version: z.string(),
    preprocessing_version: z.string(),
    training_timestamp: z.string(),
    experiment_id: z.string(),
    optimization_id: z.string(),
    metrics_summary: z.record(z.number().nullable()),
    limitations: z.array(z.string()),
  })
  .strict();

const modelVersionSchema = z
  .object({
    service: z.string(),
    service_version: z.string(),
    environment: z.string(),
    model_status: z.enum(['not_loaded', 'ready', 'failed']),
    model_version: z.string().nullable(),
    deployment_status: z.string(),
  })
  .strict();

module.exports = {
  modelMetadataSchema,
  modelReadySchema,
  modelVersionSchema,
};
