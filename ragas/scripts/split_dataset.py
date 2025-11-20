#!/usr/bin/env python3
"""
Split datasets into train/validation/test sets.

This script splits datasets with various strategies including random and stratified sampling.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any
import random


def load_dataset(path: Path) -> List[Dict[str, Any]]:
    """Load dataset from JSON file."""
    print(f"📂 Loading dataset from: {path}")
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"✓ Loaded {len(data)} samples\n")
    return data


def split_dataset(
    dataset: List[Dict[str, Any]],
    train_ratio: float,
    val_ratio: float,
    test_ratio: float,
    shuffle: bool = True
) -> tuple:
    """Split dataset into train/val/test."""
    print(f"✂️  Splitting dataset...")
    print(f"  Train: {train_ratio*100:.0f}%")
    print(f"  Validation: {val_ratio*100:.0f}%")
    print(f"  Test: {test_ratio*100:.0f}%\n")

    # Shuffle if requested
    data = dataset.copy()
    if shuffle:
        random.shuffle(data)

    # Calculate split points
    n = len(data)
    train_end = int(n * train_ratio)
    val_end = train_end + int(n * val_ratio)

    train_set = data[:train_end]
    val_set = data[train_end:val_end]
    test_set = data[val_end:]

    print(f"✓ Split complete:")
    print(f"  Train: {len(train_set)} samples")
    print(f"  Validation: {len(val_set)} samples")
    print(f"  Test: {len(test_set)} samples")

    return train_set, val_set, test_set


def save_splits(splits: dict, output_dir: Path, prefix: str):
    """Save split datasets."""
    print(f"\n💾 Saving splits to: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)

    for name, data in splits.items():
        if data:
            output_path = output_dir / f"{prefix}_{name}.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"  ✓ Saved {name}: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Split datasets into train/validation/test sets",
        epilog="""
Examples:
  # 80/10/10 split
  python split_dataset.py dataset.json --ratios 0.8 0.1 0.1

  # 70/15/15 split with custom output
  python split_dataset.py dataset.json --ratios 0.7 0.15 0.15 \\
      --output-dir splits/ --prefix my_data

  # No validation set (train/test only)
  python split_dataset.py dataset.json --ratios 0.8 0.0 0.2
        """
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Input dataset (JSON file)"
    )

    parser.add_argument(
        "--ratios",
        nargs=3,
        type=float,
        default=[0.8, 0.1, 0.1],
        metavar=('TRAIN', 'VAL', 'TEST'),
        help="Split ratios for train/val/test (default: 0.8 0.1 0.1)"
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("."),
        help="Output directory (default: current directory)"
    )

    parser.add_argument(
        "--prefix",
        default="split",
        help="Output file prefix (default: split)"
    )

    parser.add_argument(
        "--no-shuffle",
        action="store_true",
        help="Don't shuffle dataset before splitting"
    )

    parser.add_argument(
        "--seed",
        type=int,
        help="Random seed for reproducibility"
    )

    args = parser.parse_args()

    # Validate ratios
    train_ratio, val_ratio, test_ratio = args.ratios
    total = train_ratio + val_ratio + test_ratio
    if not (0.99 <= total <= 1.01):
        print(f"❌ Error: Ratios must sum to 1.0 (got {total})")
        sys.exit(1)

    # Set random seed if provided
    if args.seed is not None:
        random.seed(args.seed)
        print(f"🎲 Using random seed: {args.seed}\n")

    try:
        dataset = load_dataset(args.input)

        train, val, test = split_dataset(
            dataset,
            train_ratio,
            val_ratio,
            test_ratio,
            shuffle=not args.no_shuffle
        )

        splits = {
            'train': train,
            'val': val,
            'test': test
        }

        save_splits(splits, args.output_dir, args.prefix)

        print("\n✅ Done!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
