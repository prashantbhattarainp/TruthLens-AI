"""Generate governed, training-only Phase 4.1 XAI figures and an artifact manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ML_SERVICE_ROOT = PROJECT_ROOT / 'ml-service'
sys.path.insert(0, str(ML_SERVICE_ROOT))

from explainability.configuration import ExplainabilityConfiguration
from explainability.feature_importance import calculate_global_feature_importance
from explainability.service import ExplanationService
from explainability.visualizations import (
    save_absolute_importance_plot,
    save_contribution_bar_plot,
    save_waterfall_plot,
)
from inference.production_model_service import ProductionModelService


DEFAULT_DATASET = PROJECT_ROOT / 'ml' / 'data' / 'derived' / 'TL-BFNK-EN-v1.0' / 'DER-20260718-r2' / 'split-documents.jsonl'
DEFAULT_PACKAGE = ML_SERVICE_ROOT / 'artifacts' / 'candidate' / 'TL-LSVM-TFIDF-v1.1.0-rc.1'
DEFAULT_FIGURES = PROJECT_ROOT / 'docs' / 'research' / 'figures'
DEFAULT_REPORT = PROJECT_ROOT / 'docs' / 'research' / 'XAI_ARTIFACT_MANIFEST.json'
DEFAULT_GLOBAL_REPORT = PROJECT_ROOT / 'docs' / 'research' / 'XAI_FEATURE_IMPORTANCE.json'
SYNTHETIC_HEADLINE = 'Synthetic explanation example'
SYNTHETIC_ARTICLE = (
    'This deliberately synthetic article is used only to illustrate how the existing classifier exposes '
    'feature contributions. It is not a news claim, a fact check, or a dataset record, and it contains '
    'no governed evaluation text.'
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset', type=Path, default=DEFAULT_DATASET)
    parser.add_argument('--package', type=Path, default=DEFAULT_PACKAGE)
    parser.add_argument('--figures-directory', type=Path, default=DEFAULT_FIGURES)
    parser.add_argument('--report-path', type=Path, default=DEFAULT_REPORT)
    parser.add_argument('--global-report-path', type=Path, default=DEFAULT_GLOBAL_REPORT)
    parser.add_argument('--max-documents', type=int, default=512)
    parser.add_argument('--top-features', type=int, default=10)
    parser.add_argument('--lime-samples', type=int, default=1000)
    parser.add_argument('--seed', type=int, default=42)
    return parser.parse_args()


def select_train_texts(path: Path, max_documents: int) -> list[str]:
    if max_documents < 2:
        raise ValueError('max-documents must be at least 2.')
    per_label_limit = max_documents // 2
    grouped: dict[int, list[str]] = {0: [], 1: []}
    with path.open(encoding='utf-8') as handle:
        for line in handle:
            record = json.loads(line)
            label = record.get('label')
            text = record.get('raw_text')
            if record.get('partition') != 'train' or label not in grouped or not isinstance(text, str):
                continue
            if len(grouped[label]) < per_label_limit:
                grouped[label].append(text)
            if all(len(values) >= per_label_limit for values in grouped.values()):
                break
    texts = [*grouped[0], *grouped[1]]
    if len(texts) < 2:
        raise RuntimeError('The governed derivative does not contain enough training text for XAI aggregation.')
    return texts


def to_jsonable(contributions):
    return [contribution.model_dump() for contribution in contributions]


def main() -> None:
    args = parse_args()
    if not args.dataset.is_file():
        raise FileNotFoundError(f'Governed derivative not found: {args.dataset}')
    args.figures_directory.mkdir(parents=True, exist_ok=True)
    args.report_path.parent.mkdir(parents=True, exist_ok=True)
    args.global_report_path.parent.mkdir(parents=True, exist_ok=True)

    model_service = ProductionModelService(args.package.resolve())
    model_service.ensure_loaded()
    vectorizer, classifier = model_service.explainability_components()
    selected_texts = select_train_texts(args.dataset, args.max_documents)
    processed_texts = [
        model_service.preprocess_text(document_id=f'xai-reference-{index}', text=text)
        for index, text in enumerate(selected_texts)
    ]
    feature_matrix = vectorizer.transform(processed_texts)
    importance = calculate_global_feature_importance(
        classifier=classifier,
        feature_names=vectorizer.get_feature_names_out(),
        feature_matrix=feature_matrix,
        top_feature_count=args.top_features,
    )

    configuration = ExplainabilityConfiguration(
        top_feature_count=args.top_features,
        lime_sample_count=args.lime_samples,
        lime_random_seed=args.seed,
    )
    explanation_service = ExplanationService(model_service, configuration)
    local_example = explanation_service.predict_and_explain(
        headline=SYNTHETIC_HEADLINE,
        article=SYNTHETIC_ARTICLE,
    )
    if local_example.explainability.shap is None or local_example.explainability.lime is None:
        raise RuntimeError('Local explanation generation failed; no figures were created.')

    save_absolute_importance_plot(
        args.figures_directory / 'shap-global-summary.png',
        title='Global SHAP Feature Importance (Train-only Reference Cohort)',
        contributions=importance.mean_absolute_shap,
    )
    save_contribution_bar_plot(
        args.figures_directory / 'shap-feature-importance.png',
        title='Global SHAP Directional Feature Contributions',
        contributions=importance.mean_absolute_shap,
        x_label='Mean signed SHAP contribution (margin units)',
    )
    save_contribution_bar_plot(
        args.figures_directory / 'top-feature-rankings.png',
        title='LinearSVC Global Coefficient Rankings',
        contributions=importance.coefficient_top,
        x_label='LinearSVC coefficient (Fake-class margin direction)',
    )
    save_contribution_bar_plot(
        args.figures_directory / 'lime-local-example.png',
        title='LIME Local Margin-Surrogate Example (Synthetic Input)',
        contributions=[
            *local_example.explainability.lime.top_positive_features,
            *local_example.explainability.lime.top_negative_features,
        ],
        x_label='LIME surrogate contribution to Fake-class margin',
    )
    save_waterfall_plot(
        args.figures_directory / 'shap-local-waterfall-example.png',
        title='SHAP Local Waterfall Example (Synthetic Input)',
        base_value=local_example.explainability.shap.base_value,
        contributions=local_example.explainability.top_influential_features,
    )

    metadata = model_service.metadata(load=True)
    global_report = {
        'artifact_type': 'phase_4_1_global_feature_importance',
        'model_version': metadata['model_version'],
        'dataset_version': metadata['dataset_version'],
        'dataset_partition': 'train_only',
        'reference_document_count': len(selected_texts),
        'coefficient_top_features': to_jsonable(importance.coefficient_top),
        'mean_absolute_shap_top_features': to_jsonable(importance.mean_absolute_shap),
    }
    args.global_report_path.write_text(json.dumps(global_report, indent=2) + '\n', encoding='utf-8')
    manifest = {
        'artifact_type': 'phase_4_1_xai_report',
        'model_version': metadata['model_version'],
        'dataset_version': metadata['dataset_version'],
        'dataset_partition': 'train_only',
        'reference_document_count': len(selected_texts),
        'reference_selection': 'first deterministic class-balanced records in frozen train partition',
        'protected_test_access': 'none',
        'validation_partition_access': 'none',
        'shap_method': 'LinearExplainer with zero TF-IDF reference',
        'lime_method': 'LimeTextExplainer over the uncalibrated Fake-class margin',
        'lime_sample_count': args.lime_samples,
        'lime_random_seed': args.seed,
        'synthetic_local_example_only': True,
        'figures': sorted(path.name for path in args.figures_directory.glob('*.png')),
        'global_feature_report': args.global_report_path.name,
        'source_derivative_sha256': hashlib.sha256(args.dataset.read_bytes()).hexdigest(),
        'limitations': [
            'Feature contributions explain the model margin, not factual truth or calibrated confidence.',
            'The candidate remains integrated_not_deployment_approved and untested after tuning.',
            'No raw document text, document identifiers, or protected-test content is emitted in the report.',
        ],
    }
    args.report_path.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
