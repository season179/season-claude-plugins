#!/usr/bin/env python3
"""
Validate datasets for Ragas evaluation.

This script validates dataset structure and checks compatibility with
selected metrics before running expensive evaluations.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Set

# Metric requirements (field dependencies)
METRIC_REQUIREMENTS = {
    'Faithfulness': {'user_input', 'retrieved_contexts', 'response'},
    'AnswerRelevancy': {'user_input', 'response'},
    'ContextPrecision': {'user_input', 'retrieved_contexts', 'reference'},
    'ContextRecall': {'user_input', 'retrieved_contexts', 'reference'},
    'AnswerCorrectness': {'user_input', 'response', 'reference'},
    'AnswerSimilarity': {'user_input', 'response', 'reference'},
    'ContextRelevancy': {'user_input', 'retrieved_contexts'},
    'ContextEntityRecall': {'user_input', 'retrieved_contexts', 'reference'},
    'AgentGoalAccuracyWithoutReference': {'user_input', 'response'},
    'ToolCallAccuracy': {'user_input', 'response'},
}


def load_dataset(input_path: Path) -> List[Dict[str, Any]]:
    """Load dataset from JSON file."""
    print(f"📂 Loading dataset from: {input_path}")

    if not input_path.exists():
        raise FileNotFoundError(f"File not found: {input_path}")

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Dataset must be a list of dictionaries")

    print(f"✓ Loaded {len(data)} samples\n")
    return data


def validate_structure(dataset: List[Dict[str, Any]]) -> tuple:
    """Validate basic dataset structure."""
    print("🔍 Validating Dataset Structure")
    print("=" * 50)

    errors = []
    warnings = []

    # Check if dataset is empty
    if len(dataset) == 0:
        errors.append("Dataset is empty")
        return errors, warnings

    # Check each sample
    for i, sample in enumerate(dataset):
        # Must be a dictionary
        if not isinstance(sample, dict):
            errors.append(f"Sample {i}: Not a dictionary (type: {type(sample).__name__})")
            continue

        # Check for common fields
        available_fields = set(sample.keys())

        # Check user_input
        if 'user_input' not in sample:
            errors.append(f"Sample {i}: Missing 'user_input' field")
        elif not isinstance(sample['user_input'], str):
            errors.append(f"Sample {i}: 'user_input' must be string")
        elif not sample['user_input'].strip():
            warnings.append(f"Sample {i}: Empty 'user_input'")

        # Check retrieved_contexts if present
        if 'retrieved_contexts' in sample:
            contexts = sample['retrieved_contexts']
            if not isinstance(contexts, list):
                errors.append(f"Sample {i}: 'retrieved_contexts' must be a list")
            elif len(contexts) == 0:
                warnings.append(f"Sample {i}: Empty 'retrieved_contexts' list")
            else:
                for j, ctx in enumerate(contexts):
                    if not isinstance(ctx, str):
                        errors.append(f"Sample {i}: Context {j} must be string")

        # Check response if present
        if 'response' in sample:
            if not isinstance(sample['response'], str):
                errors.append(f"Sample {i}: 'response' must be string")
            elif not sample['response'].strip():
                warnings.append(f"Sample {i}: Empty 'response'")

        # Check reference if present
        if 'reference' in sample:
            if not isinstance(sample['reference'], str):
                errors.append(f"Sample {i}: 'reference' must be string")
            elif not sample['reference'].strip():
                warnings.append(f"Sample {i}: Empty 'reference'")

    # Summary
    if errors:
        print(f"❌ Found {len(errors)} errors:")
        for error in errors[:10]:  # Show first 10
            print(f"   - {error}")
        if len(errors) > 10:
            print(f"   ... and {len(errors) - 10} more")
    else:
        print("✅ No structural errors found")

    if warnings:
        print(f"\n⚠️  Found {len(warnings)} warnings:")
        for warning in warnings[:10]:  # Show first 10
            print(f"   - {warning}")
        if len(warnings) > 10:
            print(f"   ... and {len(warnings) - 10} more")

    print()
    return errors, warnings


def check_metric_compatibility(dataset: List[Dict[str, Any]], metrics: List[str]) -> dict:
    """Check if dataset is compatible with specified metrics."""
    print("🎯 Checking Metric Compatibility")
    print("=" * 50)

    if not metrics:
        print("No metrics specified, skipping compatibility check\n")
        return {}

    # Analyze available fields across dataset
    all_fields = set()
    field_coverage = {}

    for sample in dataset:
        for field in sample.keys():
            all_fields.add(field)
            field_coverage[field] = field_coverage.get(field, 0) + 1

    print(f"Available fields in dataset:")
    for field in sorted(all_fields):
        coverage = field_coverage[field] / len(dataset) * 100
        print(f"  - {field}: {field_coverage[field]}/{len(dataset)} samples ({coverage:.1f}%)")

    print()

    # Check each metric
    results = {}
    for metric in metrics:
        if metric not in METRIC_REQUIREMENTS:
            print(f"⚠️  Unknown metric: {metric} (skipping)")
            continue

        required_fields = METRIC_REQUIREMENTS[metric]
        missing_fields = required_fields - all_fields

        # Count samples with all required fields
        compatible_samples = 0
        for sample in dataset:
            if all(field in sample and sample[field] for field in required_fields):
                compatible_samples += 1

        compatible_pct = compatible_samples / len(dataset) * 100 if dataset else 0

        results[metric] = {
            'required_fields': list(required_fields),
            'missing_fields': list(missing_fields),
            'compatible_samples': compatible_samples,
            'compatible_percentage': compatible_pct,
            'status': 'compatible' if compatible_samples == len(dataset) else
                     'partial' if compatible_samples > 0 else 'incompatible'
        }

        # Print result
        if results[metric]['status'] == 'compatible':
            print(f"✅ {metric}: Compatible ({compatible_samples}/{len(dataset)} samples)")
        elif results[metric]['status'] == 'partial':
            print(f"⚠️  {metric}: Partially compatible ({compatible_samples}/{len(dataset)} samples)")
            print(f"   Missing fields in some samples: {', '.join(required_fields)}")
        else:
            print(f"❌ {metric}: Incompatible (0/{len(dataset)} samples)")
            print(f"   Missing required fields: {', '.join(missing_fields)}")

    print()
    return results


def suggest_metrics(dataset: List[Dict[str, Any]]) -> List[str]:
    """Suggest compatible metrics based on available fields."""
    print("💡 Suggested Metrics")
    print("=" * 50)

    # Analyze available fields
    all_fields = set()
    for sample in dataset:
        all_fields.update(sample.keys())

    suggested = []
    for metric, required_fields in METRIC_REQUIREMENTS.items():
        if required_fields.issubset(all_fields):
            # Check if fields are non-empty
            compatible_count = 0
            for sample in dataset:
                if all(field in sample and sample[field] for field in required_fields):
                    compatible_count += 1

            if compatible_count > 0:
                pct = compatible_count / len(dataset) * 100
                suggested.append((metric, pct))

    if suggested:
        print("Based on your dataset, you can use:")
        for metric, pct in sorted(suggested, key=lambda x: x[1], reverse=True):
            print(f"  ✓ {metric} ({pct:.0f}% of samples)")
    else:
        print("⚠️  No metrics are fully compatible with this dataset")
        print("\nYour dataset might be missing key fields. Common requirements:")
        print("  - user_input: The question/query (required by all metrics)")
        print("  - retrieved_contexts: Retrieved passages (required by context metrics)")
        print("  - response: Generated answer (required by answer metrics)")
        print("  - reference: Ground truth answer (required by some metrics)")

    print()
    return [m for m, _ in suggested]


def generate_report(
    structure_errors: List[str],
    structure_warnings: List[str],
    compatibility_results: dict,
    suggested_metrics: List[str],
    output_path: Path
):
    """Generate validation report."""
    report = {
        'structure': {
            'errors': structure_errors,
            'warnings': structure_warnings,
            'valid': len(structure_errors) == 0
        },
        'compatibility': compatibility_results,
        'suggested_metrics': suggested_metrics
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"📄 Detailed report saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Validate datasets for Ragas evaluation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate dataset structure
  python validate_dataset.py testset.json

  # Check compatibility with specific metrics
  python validate_dataset.py testset.json --metrics Faithfulness AnswerRelevancy

  # Generate detailed report
  python validate_dataset.py testset.json --report validation_report.json

  # Validate and get metric suggestions
  python validate_dataset.py testset.json --suggest
        """
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Input dataset (JSON file)"
    )

    parser.add_argument(
        "--metrics",
        nargs='+',
        help="Metrics to check compatibility for"
    )

    parser.add_argument(
        "--suggest",
        action="store_true",
        help="Suggest compatible metrics"
    )

    parser.add_argument(
        "--report",
        type=Path,
        help="Save validation report to JSON file"
    )

    args = parser.parse_args()

    try:
        # Load dataset
        dataset = load_dataset(args.input)

        # Validate structure
        errors, warnings = validate_structure(dataset)

        # Check metric compatibility
        compatibility = {}
        if args.metrics:
            compatibility = check_metric_compatibility(dataset, args.metrics)

        # Suggest metrics
        suggested = []
        if args.suggest or not args.metrics:
            suggested = suggest_metrics(dataset)

        # Generate report if requested
        if args.report:
            generate_report(errors, warnings, compatibility, suggested, args.report)

        # Exit with appropriate code
        if errors:
            print("❌ Validation failed with errors")
            sys.exit(1)
        elif warnings:
            print("⚠️  Validation passed with warnings")
        else:
            print("✅ Validation passed successfully!")

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
