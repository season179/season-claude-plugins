# Synthetic Test Data Generation

## Overview

Ragas provides sophisticated test data generation capabilities to create diverse evaluation datasets from documents without manual annotation. This addresses the challenge of obtaining high-quality evaluation data at scale.

## Why Synthetic Data Generation?

**Challenges with manual data creation:**
- Time-consuming and labor-intensive
- Expensive to scale
- Human-generated questions may lack diversity
- Difficult to cover edge cases systematically

**Benefits of synthetic generation:**
- Rapid dataset creation (generate 100+ samples in minutes)
- Diverse question types (simple, reasoning, multi-context)
- Controlled difficulty distribution
- Cost-effective scaling

## Basic Generation Workflow

### 1. Load Documents

Use document loaders from LangChain or LlamaIndex:

```python
from langchain_community.document_loaders import DirectoryLoader

# Load from directory
loader = DirectoryLoader("./docs", glob="**/*.md")
documents = loader.load()

# Or load specific files
from langchain_community.document_loaders import TextLoader
loader = TextLoader("document.txt")
documents = loader.load()
```

**Document requirements:**
- Must have `filename` in metadata (used for tracking)
- Content should be well-structured and informative
- Works with: .md, .txt, .pdf, .docx, .html

### 2. Setup Generator

```python
from ragas.testset.generator import TestsetGenerator
from ragas.llms import llm_factory
from langchain_openai import OpenAIEmbeddings

# Initialize LLM and embeddings (auto-wrapped)
generator_llm = llm_factory("gpt-4o")
generator_embeddings = OpenAIEmbeddings()  # Auto-wrapped by Ragas

# Create generator
generator = TestsetGenerator(
    llm=generator_llm,
    embedding_model=generator_embeddings
)
```

### 3. Generate Test Dataset

```python
# Generate with default settings
testset = generator.generate_with_langchain_docs(
    documents,
    testset_size=50
)

# Access generated data
testset_df = testset.to_pandas()
print(testset_df.head())
```

## Question Types & Distributions

Ragas generates three types of questions with different complexity levels:

### Simple Questions

**Characteristics:**
- Direct fact retrieval from single context
- Answer found in one specific location
- Minimal reasoning required

**Example:**
- Document: "Paris is the capital of France. It was founded in the 3rd century BC."
- Question: "What is the capital of France?"
- Answer: "Paris"

### Reasoning Questions

**Characteristics:**
- Requires inference across multiple facts
- Needs understanding of relationships
- More complex cognitive processing

**Example:**
- Document: "Paris has a population of 2.1M. Lyon has 0.5M. Marseille has 0.8M."
- Question: "Which French city has the highest population?"
- Answer: "Paris has the highest population at 2.1 million"

### Multi-Context Questions

**Characteristics:**
- Requires information from multiple documents
- Tests cross-document reasoning
- Most challenging question type

**Example:**
- Doc 1: "Paris is the capital of France"
- Doc 2: "The Eiffel Tower is located in Paris"
- Question: "In which country is the Eiffel Tower located?"
- Answer: "The Eiffel Tower is in France"

## Custom Question Distributions

Control the mix of question types:

```python
from ragas.testset.evolutions import simple, reasoning, multi_context

testset = generator.generate_with_langchain_docs(
    documents,
    testset_size=100,
    distributions={
        simple: 0.5,        # 50% simple questions
        reasoning: 0.3,     # 30% reasoning questions
        multi_context: 0.2  # 20% multi-context questions
    }
)
```

**Guidelines for distribution:**
- **Starting out:** Use 0.6 simple, 0.3 reasoning, 0.1 multi-context
- **Comprehensive testing:** Use balanced 0.33, 0.33, 0.34
- **Challenging evaluation:** Use 0.2 simple, 0.4 reasoning, 0.4 multi-context
- **Production monitoring:** Use 0.7 simple, 0.2 reasoning, 0.1 multi-context

## Advanced Generation Options

### Using LlamaIndex Documents

```python
from llama_index.core import SimpleDirectoryReader

# Load with LlamaIndex
documents = SimpleDirectoryReader("./docs").load_data()

# Generate
testset = generator.generate_with_llama_index_docs(
    documents,
    testset_size=50
)
```

### Generator with Critic LLM

Use separate LLMs for generation and quality assessment:

```python
from ragas.testset.generator import TestsetGenerator
from ragas.llms import llm_factory

# Use different quality models for different roles
generator_llm = llm_factory("gpt-4o-mini")  # Cheaper for generation
critic_llm = llm_factory("gpt-4o")  # Higher quality for validation

generator = TestsetGenerator.from_langchain(
    generator_llm=generator_llm,
    critic_llm=critic_llm,  # Higher quality model for validation
    embeddings=generator_embeddings
)
```

**Benefits:**
- Use cheaper model for generation
- Use better model for quality control
- Optimizes cost vs quality trade-off

### Controlling Generation Parameters

```python
# More control over generation process
testset = generator.generate_with_langchain_docs(
    documents,
    testset_size=100,
    distributions={simple: 0.4, reasoning: 0.4, multi_context: 0.2},
    num_contexts=10,  # Contexts per question (default: 2)
    raise_exceptions=False,  # Continue on errors
)
```

## Knowledge Graph Generation

Ragas builds a knowledge graph from documents to enable sophisticated question generation:

**Process:**
1. **Document Splitting:** Chunks documents into hierarchical nodes
2. **Information Extraction:** Extracts entities, themes, keyphrases
3. **Relationship Establishment:** Builds semantic connections between nodes
4. **Graph Traversal:** Generates questions by traversing the graph

**This enables:**
- Multi-hop reasoning questions
- Cross-document questions
- Diverse query patterns

## Dataset Quality Assessment

### Review Generated Data

```python
# Convert to pandas for inspection
df = testset.to_pandas()

# Check for duplicates
duplicates = df[df.duplicated(subset=['user_input'], keep=False)]
print(f"Found {len(duplicates)} duplicate questions")

# Review question complexity
print(df['evolution_type'].value_counts())
```

### Quality Checks

1. **Diversity:** Questions should cover different topics
2. **No duplicates:** Each question should be unique
3. **Answerable:** All questions should be answerable from provided context
4. **Natural language:** Questions should read naturally

### Filtering and Refinement

```python
# Remove duplicates
df_unique = df.drop_duplicates(subset=['user_input'], keep='first')

# Filter by evolution type if needed
simple_questions = df[df['evolution_type'] == 'simple']

# Manual review of sample
sample = df.sample(n=10)
for idx, row in sample.iterrows():
    print(f"\nQuestion: {row['user_input']}")
    print(f"Answer: {row['reference']}")
    print(f"Type: {row['evolution_type']}")
```

## Augmenting with Manual Questions

Combine synthetic with manually created questions:

```python
# Generate synthetic testset
synthetic_testset = generator.generate_with_langchain_docs(docs, testset_size=40)

# Add manual questions
manual_questions = [
    {
        "user_input": "What is the main advantage of RAG?",
        "reference": "RAG reduces hallucinations by grounding responses in retrieved context",
        "reference_contexts": ["RAG combines retrieval with generation..."]
    }
]

# Combine datasets
from ragas import EvaluationDataset
combined_dataset = EvaluationDataset.from_list(
    synthetic_testset.to_list() + manual_questions
)
```

## Domain-Specific Generation

### For Technical Documentation

- Focus on simple and reasoning questions
- Lower multi-context proportion
- Verify technical accuracy manually

```python
testset = generator.generate_with_langchain_docs(
    docs,
    testset_size=60,
    distributions={simple: 0.5, reasoning: 0.4, multi_context: 0.1}
)
```

### For Long-Form Content

- Increase reasoning and multi-context questions
- Use larger chunk sizes in document loading
- Higher testset size for coverage

```python
# Load with larger chunks
loader = DirectoryLoader(
    "./docs",
    glob="**/*.md",
    loader_kwargs={"chunk_size": 2000}  # Larger chunks
)
docs = loader.load()

testset = generator.generate_with_langchain_docs(
    docs,
    testset_size=100,
    distributions={simple: 0.3, reasoning: 0.4, multi_context: 0.3}
)
```

### For Conversational Data

- Emphasize reasoning questions
- Test understanding of context flow
- Include follow-up question patterns

## Best Practices

1. **Start small:** Generate 20-30 questions first, review quality
2. **Iterate on distribution:** Adjust question type mix based on use case
3. **Review manually:** Always spot-check generated questions
4. **Filter aggressively:** Remove low-quality or ambiguous questions
5. **Augment with manual:** Add domain-specific edge cases
6. **Version control:** Track testsets alongside code changes
7. **Split test/validation:** Create separate sets for tuning vs final evaluation
8. **Document metadata:** Keep track of generation parameters

## Cost Considerations

**Generation costs:**
- OpenAI GPT-4: ~$0.03-0.05 per question (depending on document size)
- GPT-3.5-turbo: ~$0.002-0.005 per question
- Claude Sonnet: ~$0.015-0.03 per question

**Optimization strategies:**
- Use GPT-3.5 for generation, GPT-4 for critic (hybrid approach)
- Generate larger batches to amortize setup costs
- Cache generated datasets for reuse
- Use local/open-source models for development

## Exporting Generated Data

```python
# Export to pandas DataFrame
df = testset.to_pandas()
df.to_csv('testset.csv', index=False)

# Export to JSON
testset_dict = testset.to_list()
import json
with open('testset.json', 'w') as f:
    json.dump(testset_dict, f, indent=2)

# Export to HuggingFace datasets format
from datasets import Dataset
hf_dataset = Dataset.from_pandas(df)
hf_dataset.save_to_disk('./testset_hf')
```

## Common Issues & Solutions

**Issue: Low-quality questions**
- Solution: Use better generator LLM (GPT-4 vs GPT-3.5)
- Solution: Add critic LLM for quality filtering
- Solution: Improve document quality/structure

**Issue: Duplicate questions**
- Solution: Increase document diversity
- Solution: Filter duplicates post-generation
- Solution: Adjust num_contexts parameter

**Issue: Unanswerable questions**
- Solution: Ensure documents contain complete information
- Solution: Review and filter manually
- Solution: Adjust evolution type distribution

**Issue: Generation is slow**
- Solution: Reduce testset_size or generate in batches
- Solution: Use faster LLM (GPT-3.5 vs GPT-4)
- Solution: Reduce document set size

**Issue: Questions too simple/complex**
- Solution: Adjust distribution parameters
- Solution: Use different document chunk sizes
- Solution: Review and manually select appropriate difficulty
