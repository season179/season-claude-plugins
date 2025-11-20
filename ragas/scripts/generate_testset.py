#!/usr/bin/env python3
"""
Generate synthetic test datasets from documents using Ragas.

This script loads documents from various formats and generates diverse
test questions with ground truth answers for RAG evaluation.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional

try:
    from langchain_community.document_loaders import (
        DirectoryLoader,
        TextLoader,
        PDFMinerLoader,
        UnstructuredMarkdownLoader,
    )
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from ragas.testset.generator import TestsetGenerator
    from ragas.testset.evolutions import simple, reasoning, multi_context
    from ragas.llms import LangchainLLMWrapper
    from langchain_openai import ChatOpenAI
    from tqdm import tqdm
except ImportError as e:
    print(f"Error: Missing required dependencies. Run: pip install -r requirements.txt")
    print(f"Details: {e}")
    sys.exit(1)


def load_documents(path: Path, glob_pattern: str = "**/*") -> List:
    """Load documents from directory with support for multiple formats."""
    print(f"📂 Loading documents from: {path}")

    if not path.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")

    if path.is_file():
        # Single file
        ext = path.suffix.lower()
        if ext == '.pdf':
            loader = PDFMinerLoader(str(path))
        elif ext == '.md':
            loader = UnstructuredMarkdownLoader(str(path))
        else:
            loader = TextLoader(str(path))
        docs = loader.load()
    else:
        # Directory
        try:
            # Try loading with specific loaders based on extensions
            loaders = {
                "*.md": UnstructuredMarkdownLoader,
                "*.txt": TextLoader,
            }

            all_docs = []
            for pattern, loader_class in loaders.items():
                try:
                    loader = DirectoryLoader(
                        str(path),
                        glob=pattern,
                        loader_cls=loader_class,
                        show_progress=True
                    )
                    docs = loader.load()
                    all_docs.extend(docs)
                except Exception as e:
                    print(f"Warning: Could not load {pattern} files: {e}")

            docs = all_docs if all_docs else DirectoryLoader(
                str(path),
                glob=glob_pattern,
                show_progress=True
            ).load()

        except Exception as e:
            print(f"Warning: Error with DirectoryLoader, trying generic approach: {e}")
            docs = []

    print(f"✓ Loaded {len(docs)} documents")
    return docs


def chunk_documents(docs: List, chunk_size: int = 1000, chunk_overlap: int = 200) -> List:
    """Split documents into chunks for better processing."""
    print(f"✂️  Chunking documents (size={chunk_size}, overlap={chunk_overlap})")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )

    chunks = text_splitter.split_documents(docs)
    print(f"✓ Created {len(chunks)} chunks")
    return chunks


def generate_testset(
    docs: List,
    size: int,
    model: str = "gpt-4o",
    distributions: Optional[dict] = None,
) -> dict:
    """Generate synthetic test dataset."""
    print(f"\n🤖 Generating testset with {model}")
    print(f"Target size: {size} samples")

    # Setup generator LLM
    generator_llm = LangchainLLMWrapper(ChatOpenAI(model=model, temperature=0.7))
    generator = TestsetGenerator(llm=generator_llm)

    # Set default distributions if not provided
    if distributions is None:
        distributions = {
            simple: 0.4,
            reasoning: 0.4,
            multi_context: 0.2,
        }

    print("\n📊 Question type distribution:")
    for evolution, prob in distributions.items():
        print(f"  - {evolution.__name__}: {prob*100}%")

    # Generate testset with progress
    print("\n⏳ Generating questions...")
    try:
        testset = generator.generate_with_langchain_docs(
            docs,
            testset_size=size,
            distributions=distributions,
        )

        print(f"✓ Generated {len(testset)} test samples")
        return testset

    except Exception as e:
        print(f"❌ Error during generation: {e}")
        raise


def save_testset(testset, output_path: Path, format: str = "json"):
    """Save testset to file."""
    print(f"\n💾 Saving testset to: {output_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if format == "json":
        # Convert to dictionary format
        data = []
        for item in testset:
            data.append({
                "user_input": item.user_input,
                "reference": getattr(item, 'reference', None),
                "retrieved_contexts": getattr(item, 'retrieved_contexts', []),
                "response": getattr(item, 'response', ''),
            })

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    elif format == "csv":
        import csv
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            if len(testset) > 0:
                fieldnames = ['user_input', 'reference', 'retrieved_contexts', 'response']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for item in testset:
                    writer.writerow({
                        'user_input': item.user_input,
                        'reference': getattr(item, 'reference', ''),
                        'retrieved_contexts': str(getattr(item, 'retrieved_contexts', [])),
                        'response': getattr(item, 'response', ''),
                    })

    print(f"✓ Saved successfully")


def main():
    parser = argparse.ArgumentParser(
        description="Generate synthetic test datasets from documents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate 50 questions from markdown files
  python generate_testset.py docs/ --size 50 --output testset.json

  # Generate with custom model and question types
  python generate_testset.py docs/ --size 100 --model gpt-4o-mini \\
      --simple 0.5 --reasoning 0.3 --multi-context 0.2

  # Generate from single file
  python generate_testset.py document.pdf --size 20 --output test.json

  # Custom chunking for large documents
  python generate_testset.py docs/ --size 50 --chunk-size 1500 --chunk-overlap 300
        """
    )

    parser.add_argument(
        "input_path",
        type=Path,
        help="Path to documents (file or directory)"
    )

    parser.add_argument(
        "--size",
        type=int,
        default=50,
        help="Number of test samples to generate (default: 50)"
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("testset.json"),
        help="Output file path (default: testset.json)"
    )

    parser.add_argument(
        "--format",
        choices=["json", "csv"],
        default="json",
        help="Output format (default: json)"
    )

    parser.add_argument(
        "--model",
        default="gpt-4o",
        help="LLM model for generation (default: gpt-4o)"
    )

    parser.add_argument(
        "--chunk-size",
        type=int,
        default=1000,
        help="Chunk size for document splitting (default: 1000)"
    )

    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=200,
        help="Chunk overlap (default: 200)"
    )

    parser.add_argument(
        "--simple",
        type=float,
        default=0.4,
        help="Proportion of simple questions (default: 0.4)"
    )

    parser.add_argument(
        "--reasoning",
        type=float,
        default=0.4,
        help="Proportion of reasoning questions (default: 0.4)"
    )

    parser.add_argument(
        "--multi-context",
        type=float,
        default=0.2,
        help="Proportion of multi-context questions (default: 0.2)"
    )

    parser.add_argument(
        "--no-chunk",
        action="store_true",
        help="Skip document chunking (use raw documents)"
    )

    args = parser.parse_args()

    # Validate proportions sum to 1.0
    total = args.simple + args.reasoning + args.multi_context
    if not (0.99 <= total <= 1.01):
        print(f"Error: Question type proportions must sum to 1.0 (got {total})")
        sys.exit(1)

    try:
        # Load documents
        docs = load_documents(args.input_path)

        if len(docs) == 0:
            print("Error: No documents loaded")
            sys.exit(1)

        # Chunk documents unless disabled
        if not args.no_chunk:
            docs = chunk_documents(docs, args.chunk_size, args.chunk_overlap)

        # Prepare distributions
        distributions = {
            simple: args.simple,
            reasoning: args.reasoning,
            multi_context: args.multi_context,
        }

        # Generate testset
        testset = generate_testset(
            docs,
            args.size,
            model=args.model,
            distributions=distributions
        )

        # Save results
        save_testset(testset, args.output, format=args.format)

        print("\n✅ Done!")
        print(f"\n📄 Output: {args.output}")
        print(f"📊 Samples: {len(testset)}")

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
