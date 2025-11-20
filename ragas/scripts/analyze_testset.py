#!/usr/bin/env python3
"""
Analyze test dataset quality and characteristics.

This script provides comprehensive analysis of test datasets including
diversity metrics, coverage analysis, duplicate detection, and quality scores.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any
from collections import Counter, defaultdict
import re

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
except ImportError:
    print("Warning: sklearn not available. Some features will be limited.")
    print("Install with: pip install scikit-learn")


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


def analyze_basic_stats(dataset: List[Dict[str, Any]]) -> dict:
    """Analyze basic dataset statistics."""
    print("📊 Basic Statistics")
    print("=" * 50)

    stats = {
        'total_samples': len(dataset),
        'has_user_input': sum(1 for d in dataset if d.get('user_input')),
        'has_reference': sum(1 for d in dataset if d.get('reference')),
        'has_contexts': sum(1 for d in dataset if d.get('retrieved_contexts')),
        'has_response': sum(1 for d in dataset if d.get('response')),
    }

    print(f"Total samples: {stats['total_samples']}")
    print(f"With user_input: {stats['has_user_input']} ({stats['has_user_input']/stats['total_samples']*100:.1f}%)")
    print(f"With reference: {stats['has_reference']} ({stats['has_reference']/stats['total_samples']*100:.1f}%)")
    print(f"With retrieved_contexts: {stats['has_contexts']} ({stats['has_contexts']/stats['total_samples']*100:.1f}%)")
    print(f"With response: {stats['has_response']} ({stats['has_response']/stats['total_samples']*100:.1f}%)")

    # Length statistics
    if stats['has_user_input'] > 0:
        question_lengths = [len(d.get('user_input', '')) for d in dataset if d.get('user_input')]
        print(f"\nQuestion lengths:")
        print(f"  Min: {min(question_lengths)} chars")
        print(f"  Max: {max(question_lengths)} chars")
        print(f"  Avg: {sum(question_lengths)/len(question_lengths):.1f} chars")

    if stats['has_contexts'] > 0:
        context_counts = [len(d.get('retrieved_contexts', [])) for d in dataset if d.get('retrieved_contexts')]
        print(f"\nContext counts per sample:")
        print(f"  Min: {min(context_counts)}")
        print(f"  Max: {max(context_counts)}")
        print(f"  Avg: {sum(context_counts)/len(context_counts):.1f}")

    print()
    return stats


def analyze_diversity(dataset: List[Dict[str, Any]]) -> dict:
    """Analyze question diversity."""
    print("🎨 Diversity Analysis")
    print("=" * 50)

    questions = [d.get('user_input', '') for d in dataset if d.get('user_input')]

    if not questions:
        print("No questions found in dataset\n")
        return {}

    # Lexical diversity (unique words / total words)
    all_words = []
    for q in questions:
        words = re.findall(r'\b\w+\b', q.lower())
        all_words.extend(words)

    unique_words = set(all_words)
    lexical_diversity = len(unique_words) / len(all_words) if all_words else 0

    print(f"Lexical diversity: {lexical_diversity:.3f}")
    print(f"  Total words: {len(all_words)}")
    print(f"  Unique words: {len(unique_words)}")

    # Question type diversity (what/how/why/when/where/who)
    question_types = Counter()
    for q in questions:
        q_lower = q.lower()
        if q_lower.startswith('what'):
            question_types['what'] += 1
        elif q_lower.startswith('how'):
            question_types['how'] += 1
        elif q_lower.startswith('why'):
            question_types['why'] += 1
        elif q_lower.startswith('when'):
            question_types['when'] += 1
        elif q_lower.startswith('where'):
            question_types['where'] += 1
        elif q_lower.startswith('who'):
            question_types['who'] += 1
        else:
            question_types['other'] += 1

    print(f"\nQuestion type distribution:")
    for qtype, count in question_types.most_common():
        print(f"  {qtype}: {count} ({count/len(questions)*100:.1f}%)")

    # Top keywords
    word_freq = Counter(all_words)
    # Remove common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                  'of', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'what', 'how',
                  'why', 'when', 'where', 'who', 'which', 'this', 'that', 'these', 'those'}
    filtered_words = {w: c for w, c in word_freq.items() if w not in stop_words and len(w) > 2}

    print(f"\nTop 10 keywords:")
    for word, count in sorted(filtered_words.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {word}: {count}")

    print()
    return {
        'lexical_diversity': lexical_diversity,
        'question_types': dict(question_types),
        'top_keywords': dict(sorted(filtered_words.items(), key=lambda x: x[1], reverse=True)[:20])
    }


def detect_duplicates(dataset: List[Dict[str, Any]], threshold: float = 0.9) -> dict:
    """Detect exact and near duplicates."""
    print("🔍 Duplicate Detection")
    print("=" * 50)

    questions = [d.get('user_input', '') for d in dataset if d.get('user_input')]

    if not questions:
        print("No questions found in dataset\n")
        return {}

    # Exact duplicates
    question_counts = Counter(questions)
    exact_duplicates = {q: count for q, count in question_counts.items() if count > 1}

    print(f"Exact duplicates: {len(exact_duplicates)}")
    if exact_duplicates:
        print("\nTop exact duplicates:")
        for q, count in sorted(exact_duplicates.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  ({count}x) {q[:80]}...")

    # Near duplicates (using cosine similarity)
    try:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(questions)
        similarity_matrix = cosine_similarity(tfidf_matrix)

        near_duplicates = []
        for i in range(len(questions)):
            for j in range(i+1, len(questions)):
                if similarity_matrix[i, j] >= threshold:
                    near_duplicates.append((i, j, similarity_matrix[i, j]))

        print(f"\nNear duplicates (similarity >= {threshold}): {len(near_duplicates)}")
        if near_duplicates:
            print("\nTop near duplicates:")
            for i, j, sim in sorted(near_duplicates, key=lambda x: x[2], reverse=True)[:5]:
                print(f"  Similarity: {sim:.3f}")
                print(f"    Q1: {questions[i][:70]}...")
                print(f"    Q2: {questions[j][:70]}...")

    except Exception as e:
        print(f"\n⚠️  Could not compute near duplicates: {e}")
        near_duplicates = []

    print()
    return {
        'exact_duplicates': len(exact_duplicates),
        'near_duplicates': len(near_duplicates),
        'duplicate_examples': list(exact_duplicates.items())[:5]
    }


def analyze_coverage(dataset: List[Dict[str, Any]]) -> dict:
    """Analyze topic coverage."""
    print("🗺️  Coverage Analysis")
    print("=" * 50)

    questions = [d.get('user_input', '') for d in dataset if d.get('user_input')]

    if not questions:
        print("No questions found in dataset\n")
        return {}

    # Extract key topics using word frequency
    all_text = ' '.join(questions).lower()
    words = re.findall(r'\b[a-z]{4,}\b', all_text)  # Words with 4+ letters
    word_freq = Counter(words)

    # Remove common words
    stop_words = {'what', 'when', 'where', 'which', 'how', 'why', 'does', 'would',
                  'could', 'should', 'that', 'this', 'these', 'those', 'about'}
    topics = {w: c for w, c in word_freq.most_common(20) if w not in stop_words}

    print("Top topics (by frequency):")
    for topic, count in list(topics.items())[:10]:
        print(f"  {topic}: {count} mentions")

    # Topic distribution (how many questions mention each topic)
    topic_coverage = {}
    for topic in topics.keys():
        coverage = sum(1 for q in questions if topic in q.lower())
        topic_coverage[topic] = coverage

    print(f"\nTopic distribution score: {len(topics)}")
    print(f"  (Higher = more diverse topic coverage)")

    print()
    return {
        'num_topics': len(topics),
        'topics': topics,
        'topic_coverage': topic_coverage
    }


def analyze_quality(dataset: List[Dict[str, Any]]) -> dict:
    """Analyze data quality issues."""
    print("✅ Quality Analysis")
    print("=" * 50)

    issues = []

    # Check for empty fields
    for i, item in enumerate(dataset):
        if not item.get('user_input', '').strip():
            issues.append(f"Sample {i}: Empty user_input")

        if 'reference' in item and not item['reference']:
            issues.append(f"Sample {i}: Empty reference")

        if 'response' in item and not item['response']:
            issues.append(f"Sample {i}: Empty response")

        if 'retrieved_contexts' in item:
            contexts = item['retrieved_contexts']
            if not contexts or not any(contexts):
                issues.append(f"Sample {i}: Empty retrieved_contexts")

    # Check for very short questions
    short_questions = []
    for i, item in enumerate(dataset):
        question = item.get('user_input', '')
        if question and len(question.split()) < 3:
            short_questions.append((i, question))

    # Check for very long questions
    long_questions = []
    for i, item in enumerate(dataset):
        question = item.get('user_input', '')
        if question and len(question) > 500:
            long_questions.append((i, len(question)))

    print(f"Quality issues found: {len(issues)}")
    if issues:
        print("\nIssues (showing first 10):")
        for issue in issues[:10]:
            print(f"  - {issue}")

    print(f"\nVery short questions (<3 words): {len(short_questions)}")
    if short_questions:
        for i, q in short_questions[:3]:
            print(f"  Sample {i}: '{q}'")

    print(f"\nVery long questions (>500 chars): {len(long_questions)}")
    if long_questions:
        for i, length in long_questions[:3]:
            print(f"  Sample {i}: {length} chars")

    # Overall quality score
    total_checks = len(dataset) * 4  # 4 checks per sample
    quality_score = max(0, 1 - (len(issues) / total_checks))

    print(f"\n📈 Overall quality score: {quality_score:.2f}")
    print(f"   (1.0 = perfect, 0.0 = many issues)")

    print()
    return {
        'num_issues': len(issues),
        'quality_score': quality_score,
        'short_questions': len(short_questions),
        'long_questions': len(long_questions),
    }


def generate_report(results: dict, output_path: Path):
    """Generate JSON report with all analysis results."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"📄 Detailed report saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze test dataset quality and characteristics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a test dataset
  python analyze_testset.py testset.json

  # Save detailed report
  python analyze_testset.py testset.json --report analysis_report.json

  # Adjust duplicate detection threshold
  python analyze_testset.py testset.json --similarity-threshold 0.85
        """
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Input dataset (JSON file)"
    )

    parser.add_argument(
        "--report",
        type=Path,
        help="Save detailed report to JSON file"
    )

    parser.add_argument(
        "--similarity-threshold",
        type=float,
        default=0.9,
        help="Similarity threshold for near-duplicate detection (default: 0.9)"
    )

    args = parser.parse_args()

    try:
        # Load dataset
        dataset = load_dataset(args.input)

        # Run analyses
        results = {}
        results['basic_stats'] = analyze_basic_stats(dataset)
        results['diversity'] = analyze_diversity(dataset)
        results['duplicates'] = detect_duplicates(dataset, threshold=args.similarity_threshold)
        results['coverage'] = analyze_coverage(dataset)
        results['quality'] = analyze_quality(dataset)

        # Generate report if requested
        if args.report:
            generate_report(results, args.report)

        print("✅ Analysis complete!")

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
