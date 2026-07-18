const { z } = require('zod');

const featureContributionSchema = z.object({
  feature: z.string().min(1), contribution: z.number().finite(), direction: z.enum(['supports_fake_margin', 'supports_real_margin', 'minimal_effect']), rank: z.number().int().positive(),
}).strict();

const explainabilitySchema = z.object({
  metadata: z.object({
    status: z.enum(['available', 'unavailable']), prediction_confidence_status: z.literal('unavailable'), decision_score_interpretation: z.literal('uncalibrated_linear_svm_margin'), preprocessing_reused: z.boolean(), feature_engineering_reused: z.boolean(), disclaimer: z.string(),
  }).strict(),
  top_influential_features: z.array(featureContributionSchema),
  shap: z.object({ method: z.literal('linear_shap'), baseline: z.literal('zero_tfidf_reference'), base_value: z.number().finite(), additive_residual: z.number().finite(), top_positive_features: z.array(featureContributionSchema), top_negative_features: z.array(featureContributionSchema), least_influential_features: z.array(featureContributionSchema) }).strict().nullable(),
  lime: z.object({ method: z.literal('lime_text_margin_surrogate'), target: z.literal('fake_margin'), local_fidelity: z.number().finite(), random_seed: z.number().int().nonnegative(), sample_count: z.number().int().positive(), top_positive_features: z.array(featureContributionSchema), top_negative_features: z.array(featureContributionSchema) }).strict().nullable(),
}).strict();

module.exports = z.object({
  prediction: z.enum(['Real', 'Fake']),
  explanation: z.object({ summary: z.string(), reasons: z.array(z.string()) }).strict(),
  keywords: z.array(z.string()),
  processing_time_ms: z.number().int().nonnegative(),
  explainability: explainabilitySchema.optional(),
}).strict();
