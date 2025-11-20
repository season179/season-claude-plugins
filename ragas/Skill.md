---
name: ragas
description: "Expert guide for evaluating RAG systems with Ragas: metrics, test generation, LangChain/LlamaIndex integration, and dataset management."
license: MIT
allowed-tools:
  - Read
  - Bash
  - WebSearch
  - WebFetch
  - mcp__deepwiki__ask_question
  - mcp__deepwiki__read_wiki_contents
metadata:
  version: 1.2.0
  author: Season
  dependencies: "python>=3.8, ragas>=0.3.0"
  frameworks: "LangChain, LlamaIndex, Langfuse, Phoenix"
---

# Ragas - RAG Evaluation Framework

## Instructions for Claude

When this skill is invoked, follow these steps:

1. **Identify the User's Specific Need:**
   - Are they evaluating an existing RAG system? → Guide them through the Quick Start Workflow or suggest `scripts/evaluate_rag.py`
   - Are they generating synthetic test data? → Reference synthetic_data.md and suggest `scripts/generate_testset.py`
   - Are they integrating with a framework? → Check which framework (LangChain/LlamaIndex) and reference integrations.md
   - Are they creating custom metrics? → Provide custom metric examples from Core Capabilities section
   - Do they have production data? → Suggest `scripts/convert_production_to_test.py`

2. **Suggest Helper Scripts When Appropriate:**
   - For test data generation → `scripts/generate_testset.py`, `scripts/augment_dataset.py`
   - For validation → `scripts/validate_dataset.py`, `scripts/analyze_testset.py`
   - For evaluation → `scripts/evaluate_rag.py`
   - See "Helper Scripts" section for complete list

3. **Check LLM Provider:**
   - If they mention Azure, AWS Bedrock, Anthropic, Google, or local models → reference llm_providers.md for specific configuration
   - Default to OpenAI examples if not specified

4. **Provide Context-Appropriate Code Examples:**
   - Always show complete, runnable code (not pseudocode)
   - Include necessary imports and setup
   - Match examples to their specific use case (component evaluation vs. end-to-end vs. agent evaluation)
   - For simple tasks, suggest using helper scripts instead of writing code

5. **Guide Metric Selection:**
   - For retrieval issues → ContextPrecision, ContextRecall
   - For generation quality → Faithfulness, AnswerRelevancy
   - For overall accuracy → AnswerCorrectness
   - For agent systems → AgentGoalAccuracyWithoutReference, ToolCallAccuracy
   - Can use `scripts/validate_dataset.py --suggest` to recommend metrics

6. **Reference Additional Documentation:**
   - Point to specific reference files for deep dives
   - Direct to scripts/README.md for script usage
   - Use WebSearch or DeepWiki MCP tools only if the user asks about very recent Ragas features not covered in references

7. **Warn About Common Pitfalls:**
   - Check the Common Pitfalls section before providing recommendations
   - Proactively mention relevant anti-patterns (e.g., using cheap models for evaluation)

## Overview

Ragas is a comprehensive framework for evaluating RAG (Retrieval-Augmented Generation) applications using reference-free, LLM-based metrics. It provides both evaluation capabilities and synthetic test data generation, enabling systematic assessment of retrieval quality and generation faithfulness without requiring extensive human-annotated ground truth data.

**⚠️ Version 0.2+ Breaking Changes:**
This skill uses Ragas v0.2+, which introduced significant breaking changes from v0.1:
- **Dataset API**: Now uses `EvaluationDataset` instead of HuggingFace Datasets
- **Metric Scoring**: Use `single_turn_ascore()` instead of deprecated `ascore()`
- **LLM Configuration**: Metrics now require LLM at initialization, not during `evaluate()`
- For migration from v0.1, see: https://docs.ragas.io/en/stable/howtos/migrations/migrate_from_v01_to_v02/

**⚠️ Version 0.3+ LLM Initialization:**
As of Ragas v0.3, the recommended approach for LLM initialization has changed:
- **Preferred**: Use `llm_factory()` for OpenAI, Anthropic, and Google models
- **Alternative**: Pass LangChain LLM objects directly (auto-wrapped internally)
- **Deprecated**: `LangchainLLMWrapper` still works but is deprecated

```python
# Modern approach (v0.3+)
from ragas.llms import llm_factory
evaluator_llm = llm_factory("gpt-4o")

# Or pass LangChain LLM directly (auto-wrapped)
from langchain_openai import ChatOpenAI
evaluator_llm = ChatOpenAI(model="gpt-4o")
```

## Core Capabilities

### 1. RAG Evaluation Metrics

Ragas provides specialized metrics to evaluate RAG pipelines component-wise and end-to-end:

**Retrieval Metrics:**
- `ContextPrecision`: Measures signal-to-noise ratio of retrieved context (ranking quality)
- `ContextRecall`: Measures if all relevant information needed to answer was retrieved

**Generation Metrics:**
- `Faithfulness`: Measures factual consistency of generated answer against retrieved context
- `AnswerRelevancy`: Assesses how pertinent the generated answer is to the query

**End-to-End Metrics:**
- `AnswerCorrectness`: Evaluates factual accuracy of response (combines factual and semantic similarity)
- `AnswerSimilarity`: Measures semantic similarity between generated and expected answers

**Basic Evaluation Pattern:**
```python
from ragas import evaluate
from ragas.metrics import Faithfulness, AnswerRelevancy, ContextPrecision
from ragas.llms import llm_factory

# Setup evaluator LLM (modern approach)
evaluator_llm = llm_factory("gpt-4o")

# Prepare evaluation dataset
dataset = [
    {
        "user_input": "What is the capital of France?",
        "retrieved_contexts": ["Paris is the capital of France..."],
        "response": "The capital of France is Paris.",
        "reference": "Paris"  # Optional ground truth
    }
]

# Evaluate
result = evaluate(
    dataset=dataset,
    metrics=[
        Faithfulness(llm=evaluator_llm),
        AnswerRelevancy(llm=evaluator_llm),
        ContextPrecision(llm=evaluator_llm)
    ]
)
```

### 2. Synthetic Test Data Generation

Generate diverse test datasets from documents without manual annotation:

```python
from ragas.testset.generator import TestsetGenerator
from langchain_community.document_loaders import DirectoryLoader
from ragas.llms import llm_factory

# Load documents
loader = DirectoryLoader("path/to/docs", glob="**/*.md")
docs = loader.load()

# Setup generator
generator_llm = llm_factory("gpt-4o")
generator = TestsetGenerator(llm=generator_llm)

# Generate synthetic testset
testset = generator.generate_with_langchain_docs(
    docs,
    testset_size=50
)
```

The generator creates questions with different characteristics:
- **Simple**: Direct fact retrieval from single context
- **Reasoning**: Requires inference across multiple facts
- **Multi-context**: Requires information from multiple documents

**💡 Quick Script Alternative:**
```bash
python scripts/generate_testset.py docs/ --size 50 --output testset.json
```

### 3. Framework Integrations

Ragas integrates seamlessly with popular frameworks:

**LangChain Integration:**
- Pass LangChain LLMs directly (auto-wrapped internally)
- Pass LangChain Embeddings directly (auto-wrapped internally)
- Integrate with LangSmith for experiment tracking

**LlamaIndex Integration:**
- Use `LlamaIndexLLMWrapper` for LLMs
- Evaluate query engines and agents
- Convert LlamaIndex events to Ragas format

**Observability Tools:**
- Langfuse, Phoenix, Arize - for tracing and visualization
- LangSmith - for dataset management and evaluation runs

### 4. Custom Metrics

Create custom metrics for domain-specific evaluation:

```python
from ragas.metrics import DiscreteMetric
from ragas import SingleTurnSample

# Binary pass/fail metric
custom_metric = DiscreteMetric(
    name="summary_accuracy",
    allowed_values=["accurate", "inaccurate"],
    prompt="""Evaluate if the summary captures key information.
    Response: {response}
    Answer with only 'accurate' or 'inaccurate'.""",
    llm=evaluator_llm
)

# Use in evaluation (v0.2 API)
sample = SingleTurnSample(
    user_input="Summarize this document",
    response="Summary text..."
)
score = await custom_metric.single_turn_ascore(sample)
```

### 5. Multi-Provider Support

Ragas works with various LLM providers:

**OpenAI:**
```python
from ragas.llms import llm_factory
evaluator_llm = llm_factory("gpt-4o")
```

**Anthropic Claude:**
```python
from ragas.llms import llm_factory

evaluator_llm = llm_factory(
    "claude-3-5-sonnet-20241022",
    provider="anthropic"
)
```

**Azure OpenAI, AWS Bedrock, Google Gemini, Local Models (Ollama):** See references/llm_providers.md for detailed configuration

### 6. Agent Evaluation

Evaluate agentic systems with specialized metrics:

```python
from ragas.metrics import (
    AgentGoalAccuracyWithoutReference,
    ToolCallAccuracy
)
from ragas.dataset_schema import MultiTurnSample

# Evaluate agent conversations
sample = MultiTurnSample(user_input=agent_conversation_history)
score = await agent_goal_accuracy.multi_turn_ascore(sample)
```

## Quick Start Workflow

1. **Install Ragas and helper scripts:**
   ```bash
   pip install ragas
   # Or use scripts:
   cd scripts && pip install -r requirements.txt
   ```

2. **Prepare evaluation data** with required fields:
   - `user_input`: The query/question
   - `retrieved_contexts`: List of retrieved context chunks
   - `response`: Generated answer from RAG
   - `reference`: Optional ground truth answer

   **Quick generation:** `python scripts/generate_testset.py docs/ --size 50`

3. **Validate your dataset** (recommended):
   ```bash
   python scripts/validate_dataset.py testset.json --suggest
   ```

4. **Select metrics** based on evaluation goals:
   - Component-level: Context metrics + Generation metrics
   - End-to-end: AnswerCorrectness, AnswerSimilarity
   - Custom: Define domain-specific metrics

5. **Run evaluation:**
   - **Using scripts:** `python scripts/evaluate_rag.py testset.json --metrics Faithfulness AnswerRelevancy`
   - **Using code:** Call the `evaluate()` function directly

6. **Analyze results** to identify weaknesses in retrieval or generation

## Common Patterns

**Pattern 1: Evaluating Existing RAG System**
- Collect queries and run through RAG pipeline
- Store user_input, retrieved_contexts, response
- Optionally add reference answers
- Evaluate with selected metrics

**Pattern 2: Synthetic Dataset + Evaluation**
- Generate testset from documents
- Run testset queries through RAG
- Evaluate results with metrics
- Iterate on RAG configuration

**Pattern 3: Production Monitoring**
- Integrate with observability tools (Langfuse, Phoenix)
- Score traces in real-time or batch
- Track metrics over time
- Surface problematic clusters

## Common Pitfalls to Avoid

### ❌ **Don't use cheap/small models for evaluation**
```python
# This will give poor evaluation quality
from ragas.llms import llm_factory
evaluator_llm = llm_factory("gpt-3.5-turbo")  # Too weak for accurate judgment
```

### ✅ **Do use high-quality models for evaluation**
```python
# Better evaluation quality and reliability
evaluator_llm = llm_factory("gpt-4o")  # Strong reasoning for accurate evaluation
```

### ❌ **Don't evaluate without retrieved_contexts**
```python
# This will fail - Faithfulness needs contexts
dataset = [{
    "user_input": "What is Paris?",
    "response": "Paris is the capital of France."
    # Missing: retrieved_contexts
}]
```

### ✅ **Do provide all required fields**
```python
# Complete data for evaluation
dataset = [{
    "user_input": "What is Paris?",
    "retrieved_contexts": ["Paris is the capital and largest city of France..."],
    "response": "Paris is the capital of France."
}]
```

### ❌ **Don't use ContextRecall without ground truth**
```python
# ContextRecall requires 'reference' field
metrics = [ContextRecall(llm=evaluator_llm)]  # Will fail without reference answers
```

### ✅ **Do match metrics to available data**
```python
# Use metrics that work with your data
# If you have ground truth:
metrics = [ContextRecall(llm=evaluator_llm), AnswerCorrectness(llm=evaluator_llm)]

# If you don't have ground truth:
metrics = [Faithfulness(llm=evaluator_llm), AnswerRelevancy(llm=evaluator_llm)]
```

### ❌ **Don't ignore metric requirements**
```python
# Different metrics need different fields:
# - Faithfulness: user_input, retrieved_contexts, response
# - ContextRecall: user_input, retrieved_contexts, reference
# - AnswerRelevancy: user_input, response
# - ContextPrecision: user_input, retrieved_contexts, reference
```

### ✅ **Do check metric documentation**
Refer to **references/metrics_guide.md** for detailed requirements of each metric.

### ❌ **Don't generate tiny test sets**
```python
# Too small to be statistically meaningful
testset = generator.generate_with_langchain_docs(docs, testset_size=5)
```

### ✅ **Do generate adequate test sets**
```python
# Sufficient size for reliable evaluation (50-200 recommended)
testset = generator.generate_with_langchain_docs(docs, testset_size=50)
```

## When NOT to Use This Skill

This skill is specifically for **RAG evaluation with Ragas**. Do NOT use this skill for:

- **General LLM evaluation** (use dedicated LLM eval frameworks like HELM, EleutherAI's lm-evaluation-harness)
- **Non-RAG applications** (chatbots without retrieval, code generation, classification tasks)
- **Traditional ML model evaluation** (scikit-learn metrics, confusion matrices, ROC curves)
- **Unit testing or integration testing** (use pytest, unittest instead)
- **Performance benchmarking** (latency, throughput - use profiling tools)
- **Prompt engineering without RAG** (use other evaluation methods)
- **Document similarity or semantic search** (use direct embedding similarity)

**Use this skill when:**
- You have a RAG pipeline (retrieval + generation)
- You need to measure retrieval quality, generation faithfulness, or end-to-end accuracy
- You want to generate synthetic test data from documents
- You're debugging RAG performance issues

## Helper Scripts

This skill includes 8 utility scripts to streamline RAG evaluation workflows. All scripts are in the `scripts/` directory.

### Test Data Generation (Priority)
- **`generate_testset.py`**: Generate synthetic test questions from documents
- **`augment_dataset.py`**: Add ground truth answers, contexts, or responses to existing datasets
- **`analyze_testset.py`**: Analyze dataset quality, diversity, and characteristics
- **`convert_production_to_test.py`**: Convert production traces (LangSmith, Langfuse, Phoenix) to test datasets

### Validation & Evaluation
- **`validate_dataset.py`**: Validate dataset structure and metric compatibility
- **`evaluate_rag.py`**: Run evaluations with CLI (simpler than writing code)

### Dataset Utilities
- **`merge_datasets.py`**: Combine multiple test datasets
- **`split_dataset.py`**: Split datasets into train/validation/test sets

### Installation & Usage
```bash
# Install dependencies
cd scripts && pip install -r requirements.txt

# Quick examples
python generate_testset.py docs/ --size 50 --output testset.json
python validate_dataset.py testset.json --suggest
python evaluate_rag.py testset.json --metrics Faithfulness AnswerRelevancy
```

**📖 Full documentation:** See `scripts/README.md` for complete usage guide with examples and workflows.

## Reference Documentation

For detailed information, see:
- **references/metrics_guide.md** - Comprehensive metric descriptions and usage
- **references/synthetic_data.md** - Test data generation strategies
- **references/llm_providers.md** - Configuration for different LLM providers
- **references/integrations.md** - LangChain, LlamaIndex, observability tools
- **references/advanced_usage.md** - Custom metrics, agent evaluation, optimization

## Installation & Setup

```bash
# Basic installation
pip install ragas

# With specific framework support
pip install ragas langchain langchain-openai  # For LangChain
pip install ragas llama-index  # For LlamaIndex

# Set environment variables
export OPENAI_API_KEY="your-api-key"
```

## Key Principles

1. **Reference-free evaluation**: Most metrics don't require ground truth answers
2. **Component-wise assessment**: Evaluate retrieval and generation separately
3. **LLM-based scoring**: Uses LLMs to judge quality systematically
4. **Synthetic data generation**: Bootstrap evaluation datasets from documents
5. **Framework agnostic**: Works with any RAG implementation
