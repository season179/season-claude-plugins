#!/usr/bin/env python3
"""
Evaluate RAG systems using Ragas metrics.

This script provides a simple CLI to run evaluations on test datasets
with progress tracking, error handling, and multiple output formats.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

try:
    from ragas import evaluate
    from ragas.metrics import (
        Faithfulness, AnswerRelevancy, ContextPrecision, ContextRecall,
        AnswerCorrectness, AnswerSimilarity, ContextRelevancy
    )
    from ragas.llms import llm_factory
    from tqdm import tqdm
except ImportError as e:
    print(f"Error: Missing required dependencies. Run: pip install -r requirements.txt")
    print(f"Details: {e}")
    sys.exit(1)


AVAILABLE_METRICS = {
    'Faithfulness': Faithfulness,
    'AnswerRelevancy': AnswerRelevancy,
    'ContextPrecision': ContextPrecision,
    'ContextRecall': ContextRecall,
    'AnswerCorrectness': AnswerCorrectness,
    'AnswerSimilarity': AnswerSimilarity,
    'ContextRelevancy': ContextRelevancy,
}


def load_dataset(input_path: Path) -> List[Dict[str, Any]]:
    """Load dataset from JSON file."""
    print(f"📂 Loading dataset from: {input_path}")

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"✓ Loaded {len(data)} samples\n")
    return data


def run_evaluation(dataset: List[Dict[str, Any]], metrics: List[str], model: str) -> dict:
    """Run Ragas evaluation."""
    print(f"🚀 Starting evaluation with {model}")
    print(f"Metrics: {', '.join(metrics)}")
    print(f"Samples: {len(dataset)}\n")

    # Setup evaluator LLM
    evaluator_llm = llm_factory(model)

    # Initialize metrics
    metric_objects = []
    for metric_name in metrics:
        if metric_name not in AVAILABLE_METRICS:
            print(f"⚠️  Unknown metric: {metric_name}, skipping")
            continue

        metric_class = AVAILABLE_METRICS[metric_name]
        metric_objects.append(metric_class(llm=evaluator_llm))

    if not metric_objects:
        raise ValueError("No valid metrics specified")

    # Run evaluation
    print("⏳ Evaluating...")
    try:
        result = evaluate(
            dataset=dataset,
            metrics=metric_objects
        )
        print("✓ Evaluation complete\n")
        return result

    except Exception as e:
        print(f"❌ Evaluation failed: {e}")
        raise


def format_results(result: dict) -> str:
    """Format results as markdown table."""
    output = ["# Ragas Evaluation Results\n"]
    output.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    output.append("## Metrics\n")
    output.append("| Metric | Score |")
    output.append("|--------|-------|")

    for metric, score in result.items():
        if isinstance(score, (int, float)):
            output.append(f"| {metric} | {score:.4f} |")

    return '\n'.join(output)


def save_results(result: dict, output_path: Path, format_type: str):
    """Save evaluation results."""
    print(f"💾 Saving results to: {output_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if format_type == 'json':
        # Convert to serializable format
        serializable = {}
        for k, v in result.items():
            if isinstance(v, (int, float, str, bool, list, dict, type(None))):
                serializable[k] = v
            else:
                serializable[k] = str(v)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(serializable, f, indent=2, ensure_ascii=False)

    elif format_type == 'markdown':
        markdown = format_results(result)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown)

    print("✓ Saved successfully")


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate RAG systems using Ragas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic evaluation
  python evaluate_rag.py testset.json --metrics Faithfulness AnswerRelevancy

  # Evaluation with custom model
  python evaluate_rag.py testset.json --metrics Faithfulness --model gpt-4o-mini

  # Save results in different formats
  python evaluate_rag.py testset.json --metrics Faithfulness AnswerRelevancy \\
      --output results.json --format json

  # Multiple metrics
  python evaluate_rag.py testset.json \\
      --metrics Faithfulness AnswerRelevancy ContextPrecision ContextRecall
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
        required=True,
        choices=list(AVAILABLE_METRICS.keys()),
        help="Metrics to evaluate"
    )

    parser.add_argument(
        "--model",
        default="gpt-4o",
        help="LLM model for evaluation (default: gpt-4o)"
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results.json"),
        help="Output file path (default: results.json)"
    )

    parser.add_argument(
        "--format",
        choices=['json', 'markdown'],
        default='json',
        help="Output format (default: json)"
    )

    args = parser.parse_args()

    try:
        # Load dataset
        dataset = load_dataset(args.input)

        # Run evaluation
        result = run_evaluation(dataset, args.metrics, args.model)

        # Display results
        print("📊 Results Summary:")
        print("=" * 50)
        for metric, score in result.items():
            if isinstance(score, (int, float)):
                print(f"{metric}: {score:.4f}")
        print()

        # Save results
        save_results(result, args.output, args.format)

        print("\n✅ Done!")
        print(f"\n📄 Output: {args.output}")

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
