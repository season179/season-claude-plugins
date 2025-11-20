#!/usr/bin/env python3
"""
Convert production traces/logs to test datasets.

This script converts various trace formats (LangSmith, Langfuse, Phoenix, raw JSON)
into Ragas-compatible test datasets for evaluation.
"""

import argparse
import json
import sys
import re
from pathlib import Path
from typing import List, Dict, Any
from collections import defaultdict

def load_traces(input_path: Path) -> dict:
    """Load traces from JSON file."""
    print(f"📂 Loading traces from: {input_path}")

    if not input_path.exists():
        raise FileNotFoundError(f"File not found: {input_path}")

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"✓ Loaded data")
    return data


def detect_format(data: dict) -> str:
    """Detect trace format."""
    print("🔍 Detecting trace format...")

    # Check for LangSmith format
    if isinstance(data, list) and len(data) > 0:
        first_item = data[0]
        if 'run_id' in first_item or 'trace_id' in first_item:
            print("✓ Detected: LangSmith format")
            return 'langsmith'

    # Check for Langfuse format
    if isinstance(data, dict) and 'traces' in data:
        print("✓ Detected: Langfuse format")
        return 'langfuse'

    # Check for Phoenix format
    if isinstance(data, dict) and 'spans' in data:
        print("✓ Detected: Phoenix format")
        return 'phoenix'

    # Check for generic RAG format
    if isinstance(data, list) and len(data) > 0:
        first_item = data[0]
        if 'query' in first_item or 'question' in first_item:
            print("✓ Detected: Generic RAG format")
            return 'generic'

    print("⚠️  Unknown format, trying generic conversion")
    return 'unknown'


def convert_langsmith(data: List[dict]) -> List[Dict[str, Any]]:
    """Convert LangSmith traces to Ragas format."""
    print("\n🔄 Converting LangSmith traces...")

    dataset = []
    for trace in data:
        try:
            # Extract relevant fields from LangSmith trace
            sample = {}

            # Get user input
            if 'inputs' in trace:
                inputs = trace['inputs']
                sample['user_input'] = inputs.get('question', inputs.get('query', inputs.get('input', '')))

            # Get contexts
            if 'extra' in trace and 'contexts' in trace['extra']:
                sample['retrieved_contexts'] = trace['extra']['contexts']
            elif 'metadata' in trace and 'contexts' in trace['metadata']:
                sample['retrieved_contexts'] = trace['metadata']['contexts']

            # Get response
            if 'outputs' in trace:
                outputs = trace['outputs']
                sample['response'] = outputs.get('answer', outputs.get('output', outputs.get('text', '')))

            # Get reference if available
            if 'reference' in trace:
                sample['reference'] = trace['reference']

            if sample.get('user_input'):
                dataset.append(sample)

        except Exception as e:
            print(f"⚠️  Skipping trace: {e}")
            continue

    print(f"✓ Converted {len(dataset)} samples")
    return dataset


def convert_langfuse(data: dict) -> List[Dict[str, Any]]:
    """Convert Langfuse traces to Ragas format."""
    print("\n🔄 Converting Langfuse traces...")

    dataset = []
    traces = data.get('traces', [])

    for trace in traces:
        try:
            sample = {}

            # Extract from observations
            observations = trace.get('observations', [])

            for obs in observations:
                obs_type = obs.get('type', '')

                # Get user input
                if obs_type == 'generation' and 'input' in obs:
                    if not sample.get('user_input'):
                        sample['user_input'] = obs['input']

                # Get contexts from retrieval
                if obs_type == 'span' and obs.get('name') == 'retrieval':
                    if 'output' in obs:
                        sample['retrieved_contexts'] = obs['output']

                # Get response
                if obs_type == 'generation' and 'output' in obs:
                    sample['response'] = obs['output']

            if sample.get('user_input'):
                dataset.append(sample)

        except Exception as e:
            print(f"⚠️  Skipping trace: {e}")
            continue

    print(f"✓ Converted {len(dataset)} samples")
    return dataset


def convert_phoenix(data: dict) -> List[Dict[str, Any]]:
    """Convert Phoenix traces to Ragas format."""
    print("\n🔄 Converting Phoenix traces...")

    dataset = []
    spans = data.get('spans', [])

    # Group spans by trace_id
    traces = defaultdict(list)
    for span in spans:
        trace_id = span.get('trace_id')
        if trace_id:
            traces[trace_id].append(span)

    for trace_id, trace_spans in traces.items():
        try:
            sample = {}

            for span in trace_spans:
                span_kind = span.get('span_kind', '')

                # Get user input
                if 'input' in span and not sample.get('user_input'):
                    sample['user_input'] = span['input'].get('value', '')

                # Get contexts
                if span_kind == 'RETRIEVAL' and 'output' in span:
                    sample['retrieved_contexts'] = span['output'].get('value', [])

                # Get response
                if span_kind == 'CHAIN' and 'output' in span:
                    sample['response'] = span['output'].get('value', '')

            if sample.get('user_input'):
                dataset.append(sample)

        except Exception as e:
            print(f"⚠️  Skipping trace: {e}")
            continue

    print(f"✓ Converted {len(dataset)} samples")
    return dataset


def convert_generic(data: List[dict]) -> List[Dict[str, Any]]:
    """Convert generic format to Ragas format."""
    print("\n🔄 Converting generic format...")

    dataset = []
    for item in data:
        try:
            sample = {}

            # Map common field names
            query_fields = ['query', 'question', 'user_input', 'input', 'prompt']
            for field in query_fields:
                if field in item:
                    sample['user_input'] = item[field]
                    break

            context_fields = ['contexts', 'retrieved_contexts', 'context', 'documents']
            for field in context_fields:
                if field in item:
                    contexts = item[field]
                    if isinstance(contexts, list):
                        sample['retrieved_contexts'] = contexts
                    elif isinstance(contexts, str):
                        sample['retrieved_contexts'] = [contexts]
                    break

            response_fields = ['answer', 'response', 'output', 'result']
            for field in response_fields:
                if field in item:
                    sample['response'] = item[field]
                    break

            reference_fields = ['reference', 'ground_truth', 'expected_answer']
            for field in reference_fields:
                if field in item:
                    sample['reference'] = item[field]
                    break

            if sample.get('user_input'):
                dataset.append(sample)

        except Exception as e:
            print(f"⚠️  Skipping item: {e}")
            continue

    print(f"✓ Converted {len(dataset)} samples")
    return dataset


def clean_pii(text: str, patterns: List[str] = None) -> str:
    """Remove PII from text."""
    if not text:
        return text

    # Default patterns
    if patterns is None:
        patterns = [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # Phone
            r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
        ]

    cleaned = text
    for pattern in patterns:
        cleaned = re.sub(pattern, '[REDACTED]', cleaned)

    return cleaned


def clean_dataset(dataset: List[Dict[str, Any]], remove_pii: bool = True) -> List[Dict[str, Any]]:
    """Clean and normalize dataset."""
    print("\n🧹 Cleaning dataset...")

    cleaned = []
    for item in dataset:
        cleaned_item = {}

        # Clean user_input
        if 'user_input' in item:
            text = item['user_input']
            if remove_pii:
                text = clean_pii(text)
            cleaned_item['user_input'] = text.strip()

        # Clean contexts
        if 'retrieved_contexts' in item:
            contexts = item['retrieved_contexts']
            if isinstance(contexts, list):
                cleaned_contexts = []
                for ctx in contexts:
                    if isinstance(ctx, str):
                        if remove_pii:
                            ctx = clean_pii(ctx)
                        cleaned_contexts.append(ctx.strip())
                    elif isinstance(ctx, dict) and 'text' in ctx:
                        text = ctx['text']
                        if remove_pii:
                            text = clean_pii(text)
                        cleaned_contexts.append(text.strip())
                cleaned_item['retrieved_contexts'] = cleaned_contexts

        # Clean response
        if 'response' in item:
            text = item['response']
            if remove_pii:
                text = clean_pii(text)
            cleaned_item['response'] = text.strip()

        # Clean reference
        if 'reference' in item:
            text = item['reference']
            if remove_pii:
                text = clean_pii(text)
            cleaned_item['reference'] = text.strip()

        cleaned.append(cleaned_item)

    print(f"✓ Cleaned {len(cleaned)} samples")
    return cleaned


def sample_dataset(dataset: List[Dict[str, Any]], strategy: str, size: int) -> List[Dict[str, Any]]:
    """Sample dataset using various strategies."""
    print(f"\n📊 Sampling dataset (strategy: {strategy}, size: {size})...")

    if len(dataset) <= size:
        print(f"⚠️  Dataset already has {len(dataset)} samples (≤ {size}), returning all")
        return dataset

    if strategy == 'random':
        import random
        sampled = random.sample(dataset, size)

    elif strategy == 'first':
        sampled = dataset[:size]

    elif strategy == 'diverse':
        # Simple diversity sampling based on question length variety
        sorted_by_length = sorted(dataset, key=lambda x: len(x.get('user_input', '')))
        step = len(sorted_by_length) // size
        sampled = [sorted_by_length[i * step] for i in range(size)]

    else:
        print(f"⚠️  Unknown strategy '{strategy}', using random")
        import random
        sampled = random.sample(dataset, size)

    print(f"✓ Sampled {len(sampled)} samples")
    return sampled


def save_dataset(dataset: List[Dict[str, Any]], output_path: Path):
    """Save dataset to JSON file."""
    print(f"\n💾 Saving dataset to: {output_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"✓ Saved {len(dataset)} samples")


def main():
    parser = argparse.ArgumentParser(
        description="Convert production traces to test datasets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert LangSmith traces
  python convert_production_to_test.py langsmith_export.json --output testset.json

  # Convert with PII removal
  python convert_production_to_test.py traces.json --remove-pii --output clean_testset.json

  # Sample 100 diverse examples
  python convert_production_to_test.py traces.json --sample-size 100 --sample-strategy diverse

  # Force specific format
  python convert_production_to_test.py data.json --format langfuse --output testset.json
        """
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Input traces file (JSON)"
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("testset.json"),
        help="Output file path (default: testset.json)"
    )

    parser.add_argument(
        "--format",
        choices=['auto', 'langsmith', 'langfuse', 'phoenix', 'generic'],
        default='auto',
        help="Trace format (default: auto-detect)"
    )

    parser.add_argument(
        "--remove-pii",
        action="store_true",
        help="Remove personally identifiable information"
    )

    parser.add_argument(
        "--sample-size",
        type=int,
        help="Sample N examples from dataset"
    )

    parser.add_argument(
        "--sample-strategy",
        choices=['random', 'first', 'diverse'],
        default='random',
        help="Sampling strategy (default: random)"
    )

    args = parser.parse_args()

    try:
        # Load traces
        data = load_traces(args.input)

        # Detect or use specified format
        if args.format == 'auto':
            format_type = detect_format(data)
        else:
            format_type = args.format
            print(f"✓ Using specified format: {format_type}")

        # Convert to Ragas format
        if format_type == 'langsmith':
            dataset = convert_langsmith(data if isinstance(data, list) else [data])
        elif format_type == 'langfuse':
            dataset = convert_langfuse(data)
        elif format_type == 'phoenix':
            dataset = convert_phoenix(data)
        else:
            dataset = convert_generic(data if isinstance(data, list) else [data])

        if len(dataset) == 0:
            print("❌ No samples converted. Check input format.")
            sys.exit(1)

        # Clean dataset
        dataset = clean_dataset(dataset, remove_pii=args.remove_pii)

        # Sample if requested
        if args.sample_size:
            dataset = sample_dataset(dataset, args.sample_strategy, args.sample_size)

        # Save dataset
        save_dataset(dataset, args.output)

        print("\n✅ Done!")
        print(f"\n📄 Output: {args.output}")
        print(f"📊 Samples: {len(dataset)}")

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
