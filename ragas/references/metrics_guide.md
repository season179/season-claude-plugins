# Ragas Metrics Guide

**⚠️ Note:** This guide shows simplified examples using `metric.ascore()` for brevity. In Ragas v0.2, the recommended approach is to use `metric.single_turn_ascore(sample)` with `SingleTurnSample` objects. See the main Skill.md for v0.2-compliant examples, or consult: https://docs.ragas.io/en/stable/howtos/migrations/migrate_from_v01_to_v02/

## Overview

Ragas provides comprehensive metrics for evaluating RAG systems both component-wise and end-to-end. All metrics use LLMs for evaluation, enabling reference-free assessment in most cases.

## Retrieval Metrics

### Context Precision

**Purpose:** Evaluates whether relevant context chunks are ranked higher than irrelevant ones.

**What it measures:** Signal-to-noise ratio of retrieved context. Ideally, all relevant chunks should appear at the top ranks.

**Inputs required:**
- `user_input`: The query
- `retrieved_contexts`: List of context chunks
- `reference`: Ground truth answer (optional but improves accuracy)

**Score range:** 0 to 1 (higher is better)

**Usage:**
```python
from ragas.metrics import ContextPrecision

metric = ContextPrecision(llm=evaluator_llm)
score = await metric.ascore(
    user_input="What is the capital of France?",
    retrieved_contexts=["Paris is the capital...", "London is..."],
    reference="Paris"
)
```

**When to use:** Evaluate retrieval ranking quality. Low scores indicate poor retrieval ordering.

### Context Recall

**Purpose:** Measures if all relevant information required to answer the question was retrieved.

**What it measures:** Completeness of retrieved context relative to ground truth.

**Inputs required:**
- `user_input`: The query
- `retrieved_contexts`: List of context chunks
- `reference`: Ground truth answer (required)

**Score range:** 0 to 1 (higher is better)

**Note:** This is the only metric that requires ground truth answers.

**Usage:**
```python
from ragas.metrics import ContextRecall

metric = ContextRecall(llm=evaluator_llm)
score = await metric.ascore(
    user_input="What is the capital of France?",
    retrieved_contexts=["Paris is the capital..."],
    reference="Paris is the capital and largest city of France"
)
```

**When to use:** Verify retrieval completeness. Low scores indicate missing relevant context.

## Generation Metrics

### Faithfulness

**Purpose:** Measures factual consistency of the generated answer against retrieved context.

**What it measures:** Whether all claims in the answer can be inferred from the given context (hallucination detection).

**Inputs required:**
- `user_input`: The query
- `retrieved_contexts`: List of context chunks
- `response`: Generated answer

**Score range:** 0 to 1 (higher is better)

**How it works:**
1. Breaks down answer into individual claims
2. Verifies each claim against retrieved context
3. Score = (# supported claims) / (# total claims)

**Usage:**
```python
from ragas.metrics import Faithfulness

metric = Faithfulness(llm=evaluator_llm)
score = await metric.ascore(
    user_input="What is the capital of France?",
    retrieved_contexts=["Paris is the capital of France..."],
    response="The capital of France is Paris, established in 1889."
)
# Score would be lower because "established in 1889" is not in context
```

**When to use:** Detect hallucinations. Low scores indicate unfaithful generation.

**Best practices:**
- Higher quality LLMs (GPT-4, Claude Sonnet) provide better faithfulness evaluation
- Use alongside AnswerCorrectness for comprehensive assessment

### Answer Relevancy

**Purpose:** Assesses how pertinent the generated answer is to the query.

**What it measures:** Whether the answer directly addresses the question asked.

**Inputs required:**
- `user_input`: The query
- `response`: Generated answer

**Score range:** 0 to 1 (higher is better)

**How it works:**
1. Generates hypothetical questions from the answer
2. Compares similarity between generated questions and original query
3. Higher similarity indicates more relevant answer

**Usage:**
```python
from ragas.metrics import AnswerRelevancy

metric = AnswerRelevancy(llm=evaluator_llm, embeddings=evaluator_embeddings)
score = await metric.ascore(
    user_input="What is the capital of France?",
    response="Paris is the capital of France. It has many museums."
)
# Scores well because it directly answers the question
```

**When to use:** Evaluate if answers stay on topic. Low scores indicate tangential responses.

**Requirements:** Needs embeddings model for similarity computation.

## End-to-End Metrics

### Answer Correctness

**Purpose:** Evaluates factual and semantic correctness of the answer against ground truth.

**What it measures:** Combination of factual overlap and semantic similarity.

**Inputs required:**
- `user_input`: The query
- `response`: Generated answer
- `reference`: Ground truth answer (required)

**Score range:** 0 to 1 (higher is better)

**Components:**
- **F1 Score:** Factual overlap between answer and reference
- **Semantic Similarity:** Embedding similarity between answer and reference
- **Final Score:** Weighted combination (default: F1 weight = 0.75, similarity weight = 0.25)

**Usage:**
```python
from ragas.metrics import AnswerCorrectness

metric = AnswerCorrectness(llm=evaluator_llm, embeddings=evaluator_embeddings)
score = await metric.ascore(
    user_input="What is the capital of France?",
    response="Paris",
    reference="The capital of France is Paris"
)
```

**Customization:**
```python
# Adjust weights (higher weight to F1 score)
metric = AnswerCorrectness(
    llm=evaluator_llm,
    embeddings=evaluator_embeddings,
    weights=[0.8, 0.2]  # [F1 weight, similarity weight]
)
```

**When to use:** Overall quality assessment when ground truth is available.

### Answer Similarity

**Purpose:** Measures semantic similarity between generated and expected answers.

**What it measures:** How semantically close the answer is to the reference, regardless of exact wording.

**Inputs required:**
- `response`: Generated answer
- `reference`: Ground truth answer (required)

**Score range:** 0 to 1 (higher is better)

**Usage:**
```python
from ragas.metrics import AnswerSimilarity

metric = AnswerSimilarity(embeddings=evaluator_embeddings)
score = await metric.ascore(
    response="The capital is Paris",
    reference="Paris is the capital of France"
)
```

**When to use:** When exact factual match isn't required, focusing on semantic equivalence.

## Metric Selection Guide

### For Component-Level Evaluation

**Retrieval Quality:**
- Use `ContextPrecision` (with or without ground truth)
- Use `ContextRecall` (requires ground truth) for completeness

**Generation Quality:**
- Use `Faithfulness` to detect hallucinations
- Use `AnswerRelevancy` to check if answer addresses query

### For End-to-End Evaluation

**With Ground Truth:**
- Use `AnswerCorrectness` for comprehensive assessment
- Use `AnswerSimilarity` for semantic equivalence

**Without Ground Truth:**
- Combine `Faithfulness` + `AnswerRelevancy`
- Add `ContextPrecision` for retrieval assessment

### For Specific Issues

**Hallucination Detection:** Faithfulness
**Off-topic Responses:** AnswerRelevancy
**Poor Retrieval Ranking:** ContextPrecision
**Missing Information:** ContextRecall
**Incorrect Answers:** AnswerCorrectness

## Evaluation Dataset Structure

Ragas expects data in the following structure:

```python
from ragas.dataset_schema import SingleTurnSample

sample = SingleTurnSample(
    user_input="What is X?",
    retrieved_contexts=["Context 1", "Context 2"],
    response="The answer is...",
    reference="Ground truth answer"  # Optional for most metrics
)
```

Or as a dictionary:
```python
dataset = [
    {
        "user_input": "What is X?",
        "retrieved_contexts": ["Context 1", "Context 2"],
        "response": "The answer is...",
        "reference": "Ground truth"  # Optional
    }
]
```

## Batch Evaluation

Evaluate multiple samples efficiently:

```python
from ragas import evaluate
from ragas.metrics import Faithfulness, AnswerRelevancy

result = evaluate(
    dataset=evaluation_dataset,
    metrics=[Faithfulness(llm=evaluator_llm), AnswerRelevancy(llm=evaluator_llm)]
)

# Access results
print(result)  # Shows aggregate scores
result_df = result.to_pandas()  # Convert to DataFrame for analysis
```

## Best Practices

1. **Start with core metrics**: Faithfulness + AnswerRelevancy + ContextPrecision
2. **Use high-quality evaluator LLMs**: GPT-4, Claude Sonnet for better evaluation
3. **Consider cost vs accuracy**: Smaller models for development, larger for production
4. **Combine metrics**: No single metric tells the full story
5. **Track over time**: Monitor metrics across iterations to measure improvements
6. **Validate with human review**: Spot-check metric scores against human judgment
7. **Use appropriate baselines**: Compare against baseline RAG configurations

## Common Issues & Solutions

**Low Faithfulness but high ContextPrecision:**
- Issue: Generation model is hallucinating
- Solution: Improve prompt engineering, use stronger generation model

**High Faithfulness but low AnswerRelevancy:**
- Issue: Answer is factual but doesn't address query
- Solution: Improve prompt to focus on query intent

**Low ContextPrecision:**
- Issue: Retrieval returns irrelevant documents
- Solution: Improve embedding model, query preprocessing, or retrieval strategy

**Low ContextRecall:**
- Issue: Missing relevant information in retrieval
- Solution: Increase top-k, improve chunking strategy, or enhance document coverage
