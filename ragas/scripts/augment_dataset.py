#!/usr/bin/env python3
"""
Augment existing datasets by adding missing fields.

This script adds ground truth answers, retrieved contexts, or responses
to existing question datasets using LLMs or retrieval systems.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any
from tqdm import tqdm

try:
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
except ImportError as e:
    print(f"Error: Missing required dependencies. Run: pip install -r requirements.txt")
    print(f"Details: {e}")
    sys.exit(1)


def load_dataset(input_path: Path) -> List[Dict[str, Any]]:
    """Load dataset from JSON file."""
    print(f"📂 Loading dataset from: {input_path}")

    if not input_path.exists():
        raise FileNotFoundError(f"File not found: {input_path}")

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Dataset must be a list of dictionaries")

    print(f"✓ Loaded {len(data)} samples")
    return data


def generate_ground_truth(questions: List[str], model: str = "gpt-4o") -> List[str]:
    """Generate ground truth answers for questions."""
    print(f"\n🤖 Generating ground truth answers with {model}")

    llm = ChatOpenAI(model=model, temperature=0)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert assistant. Provide accurate, concise answers to questions. "
                   "Be factual and direct. If uncertain, acknowledge limitations."),
        ("user", "{question}")
    ])

    chain = prompt | llm

    answers = []
    for question in tqdm(questions, desc="Generating answers"):
        try:
            response = chain.invoke({"question": question})
            answers.append(response.content)
        except Exception as e:
            print(f"\n⚠️  Error generating answer for '{question[:50]}...': {e}")
            answers.append("")

    return answers


def generate_contexts(
    questions: List[str],
    knowledge_base: str = "",
    model: str = "gpt-4o",
    num_contexts: int = 3
) -> List[List[str]]:
    """Generate mock retrieved contexts for questions."""
    print(f"\n🤖 Generating retrieved contexts with {model}")

    llm = ChatOpenAI(model=model, temperature=0.3)

    if knowledge_base:
        system_msg = (
            f"You are a retrieval system. Given a question, generate {num_contexts} relevant "
            f"context passages that would help answer it. Base your contexts on this knowledge:\n\n"
            f"{knowledge_base}\n\n"
            f"Return {num_contexts} distinct passages separated by '---'."
        )
    else:
        system_msg = (
            f"You are a retrieval system. Given a question, generate {num_contexts} relevant "
            f"context passages that would help answer it. Return {num_contexts} distinct passages "
            f"separated by '---'."
        )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_msg),
        ("user", "Question: {question}\n\nGenerate {num_contexts} relevant context passages:")
    ])

    chain = prompt | llm

    all_contexts = []
    for question in tqdm(questions, desc="Generating contexts"):
        try:
            response = chain.invoke({"question": question, "num_contexts": num_contexts})
            # Split by separator and clean up
            contexts = [ctx.strip() for ctx in response.content.split('---')]
            contexts = [ctx for ctx in contexts if ctx][:num_contexts]

            # Ensure we have the right number
            while len(contexts) < num_contexts:
                contexts.append("")

            all_contexts.append(contexts)
        except Exception as e:
            print(f"\n⚠️  Error generating contexts for '{question[:50]}...': {e}")
            all_contexts.append([""] * num_contexts)

    return all_contexts


def generate_responses(
    questions: List[str],
    contexts: List[List[str]],
    model: str = "gpt-4o"
) -> List[str]:
    """Generate RAG responses using questions and contexts."""
    print(f"\n🤖 Generating RAG responses with {model}")

    llm = ChatOpenAI(model=model, temperature=0.3)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Answer the question based on the provided context. "
                   "If the context doesn't contain relevant information, acknowledge this."),
        ("user", "Context:\n{context}\n\nQuestion: {question}\n\nAnswer:")
    ])

    chain = prompt | llm

    responses = []
    for question, ctx_list in tqdm(zip(questions, contexts), desc="Generating responses", total=len(questions)):
        try:
            context = "\n\n".join(ctx_list)
            response = chain.invoke({"question": question, "context": context})
            responses.append(response.content)
        except Exception as e:
            print(f"\n⚠️  Error generating response for '{question[:50]}...': {e}")
            responses.append("")

    return responses


def augment_dataset(
    dataset: List[Dict[str, Any]],
    add_reference: bool = False,
    add_contexts: bool = False,
    add_response: bool = False,
    model: str = "gpt-4o",
    knowledge_base_path: Path = None,
    num_contexts: int = 3,
) -> List[Dict[str, Any]]:
    """Augment dataset with missing fields."""
    print("\n🔧 Augmenting dataset...")

    # Load knowledge base if provided
    knowledge_base = ""
    if knowledge_base_path and knowledge_base_path.exists():
        print(f"📖 Loading knowledge base from: {knowledge_base_path}")
        with open(knowledge_base_path, 'r', encoding='utf-8') as f:
            knowledge_base = f.read()

    # Extract questions
    questions = [item.get('user_input', '') for item in dataset]

    # Generate missing fields
    if add_reference:
        print("\n📝 Adding ground truth answers...")
        references = generate_ground_truth(questions, model=model)
        for item, ref in zip(dataset, references):
            item['reference'] = ref

    if add_contexts:
        print("\n📚 Adding retrieved contexts...")
        contexts_list = generate_contexts(questions, knowledge_base, model=model, num_contexts=num_contexts)
        for item, contexts in zip(dataset, contexts_list):
            item['retrieved_contexts'] = contexts

    if add_response:
        print("\n💬 Adding RAG responses...")
        # Get or generate contexts first
        if 'retrieved_contexts' in dataset[0]:
            contexts_list = [item['retrieved_contexts'] for item in dataset]
        elif add_contexts:
            # Already generated above
            contexts_list = [item['retrieved_contexts'] for item in dataset]
        else:
            print("⚠️  No contexts available. Generating contexts first...")
            contexts_list = generate_contexts(questions, knowledge_base, model=model, num_contexts=num_contexts)
            for item, contexts in zip(dataset, contexts_list):
                item['retrieved_contexts'] = contexts

        responses = generate_responses(questions, contexts_list, model=model)
        for item, response in zip(dataset, responses):
            item['response'] = response

    return dataset


def save_dataset(dataset: List[Dict[str, Any]], output_path: Path):
    """Save augmented dataset."""
    print(f"\n💾 Saving augmented dataset to: {output_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"✓ Saved {len(dataset)} samples")


def main():
    parser = argparse.ArgumentParser(
        description="Augment datasets by adding missing fields",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add ground truth answers to questions
  python augment_dataset.py questions.json --add-reference --output augmented.json

  # Add retrieved contexts
  python augment_dataset.py questions.json --add-contexts --num-contexts 3

  # Add contexts based on knowledge base
  python augment_dataset.py questions.json --add-contexts \\
      --knowledge-base docs.txt

  # Add everything (reference, contexts, response)
  python augment_dataset.py questions.json --add-all --output complete_dataset.json

  # Use cheaper model
  python augment_dataset.py questions.json --add-reference --model gpt-4o-mini
        """
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Input dataset (JSON file with questions)"
    )

    parser.add_argument(
        "--output",
        type=Path,
        help="Output file path (default: input_augmented.json)"
    )

    parser.add_argument(
        "--add-reference",
        action="store_true",
        help="Add ground truth answers (reference field)"
    )

    parser.add_argument(
        "--add-contexts",
        action="store_true",
        help="Add retrieved contexts"
    )

    parser.add_argument(
        "--add-response",
        action="store_true",
        help="Add RAG responses"
    )

    parser.add_argument(
        "--add-all",
        action="store_true",
        help="Add all missing fields (reference, contexts, response)"
    )

    parser.add_argument(
        "--model",
        default="gpt-4o",
        help="LLM model to use (default: gpt-4o)"
    )

    parser.add_argument(
        "--knowledge-base",
        type=Path,
        help="Knowledge base file for context generation (optional)"
    )

    parser.add_argument(
        "--num-contexts",
        type=int,
        default=3,
        help="Number of context passages to generate (default: 3)"
    )

    args = parser.parse_args()

    # Set default output path
    if not args.output:
        args.output = args.input.parent / f"{args.input.stem}_augmented.json"

    # Enable all if --add-all is specified
    if args.add_all:
        args.add_reference = True
        args.add_contexts = True
        args.add_response = True

    # Check that at least one field is being added
    if not (args.add_reference or args.add_contexts or args.add_response):
        print("Error: Must specify at least one of --add-reference, --add-contexts, "
              "--add-response, or --add-all")
        sys.exit(1)

    try:
        # Load dataset
        dataset = load_dataset(args.input)

        # Augment dataset
        augmented = augment_dataset(
            dataset,
            add_reference=args.add_reference,
            add_contexts=args.add_contexts,
            add_response=args.add_response,
            model=args.model,
            knowledge_base_path=args.knowledge_base,
            num_contexts=args.num_contexts,
        )

        # Save results
        save_dataset(augmented, args.output)

        print("\n✅ Done!")
        print(f"\n📄 Output: {args.output}")
        print(f"📊 Samples: {len(augmented)}")

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
