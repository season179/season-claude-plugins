#!/usr/bin/env python3
"""
Merge multiple test datasets into one.

This script combines datasets while handling duplicates and balancing distributions.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any
from collections import Counter


def load_dataset(path: Path) -> List[Dict[str, Any]]:
    """Load dataset from JSON file."""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data if isinstance(data, list) else []


def merge_datasets(datasets: List[List[Dict[str, Any]]], deduplicate: bool = True) -> List[Dict[str, Any]]:
    """Merge multiple datasets."""
    print("🔀 Merging datasets...")

    merged = []
    seen_questions = set()

    for i, dataset in enumerate(datasets):
        added = 0
        for sample in dataset:
            question = sample.get('user_input', '')

            if deduplicate and question in seen_questions:
                continue

            merged.append(sample)
            seen_questions.add(question)
            added += 1

        print(f"  Dataset {i+1}: Added {added}/{len(dataset)} samples")

    print(f"\n✓ Merged into {len(merged)} total samples")
    return merged


def save_dataset(dataset: List[Dict[str, Any]], output_path: Path):
    """Save dataset to JSON file."""
    print(f"\n💾 Saving to: {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"✓ Saved {len(dataset)} samples")


def main():
    parser = argparse.ArgumentParser(
        description="Merge multiple test datasets",
        epilog="""
Examples:
  python merge_datasets.py dataset1.json dataset2.json --output merged.json
  python merge_datasets.py *.json --output all_tests.json --no-deduplicate
        """
    )

    parser.add_argument(
        "inputs",
        nargs='+',
        type=Path,
        help="Input datasets (JSON files)"
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("merged_dataset.json"),
        help="Output file path (default: merged_dataset.json)"
    )

    parser.add_argument(
        "--no-deduplicate",
        action="store_true",
        help="Keep duplicate questions"
    )

    args = parser.parse_args()

    try:
        print(f"📂 Loading {len(args.inputs)} datasets...\n")

        datasets = []
        for path in args.inputs:
            if not path.exists():
                print(f"⚠️  File not found: {path}, skipping")
                continue
            datasets.append(load_dataset(path))

        if not datasets:
            print("❌ No valid datasets found")
            sys.exit(1)

        merged = merge_datasets(datasets, deduplicate=not args.no_deduplicate)
        save_dataset(merged, args.output)

        print("\n✅ Done!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
