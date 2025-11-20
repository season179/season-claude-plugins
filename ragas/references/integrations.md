# Framework Integrations

## Overview

Ragas integrates seamlessly with popular LLM frameworks and observability tools, enabling streamlined evaluation workflows within existing development pipelines.

## LangChain Integration

### Basic Setup

```python
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from ragas.llms import LangchainLLMWrapper
```

### Evaluating LangChain RAG Pipeline

```python
# Create your LangChain RAG pipeline
from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA

vectorstore = Chroma(embedding_function=OpenAIEmbeddings())
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4o"),
    retriever=vectorstore.as_retriever(),
    return_source_documents=True
)

# Run queries and collect results
results = []
for query in test_queries:
    response = qa_chain({"query": query})
    results.append({
        "user_input": query,
        "retrieved_contexts": [doc.page_content for doc in response["source_documents"]],
        "response": response["result"]
    })

# Evaluate with Ragas
from ragas import evaluate
from ragas.metrics import Faithfulness, AnswerRelevancy

evaluation_result = evaluate(
    dataset=results,
    metrics=[Faithfulness(), AnswerRelevancy()]
)
```

### LangChain Evaluation Chains

Use RagasEvaluatorChain for LangChain integration:

```python
from ragas.langchain.evalchain import RagasEvaluatorChain
from ragas.metrics import faithfulness, answer_relevancy

# Create evaluation chains
faithfulness_chain = RagasEvaluatorChain(metric=faithfulness)
relevancy_chain = RagasEvaluatorChain(metric=answer_relevancy)

# Evaluate a result
result = qa_chain({"query": "What is Paris?"})
faithfulness_score = faithfulness_chain(result)
relevancy_score = relevancy_chain(result)
```

### Document Loading

```python
from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
    PDFLoader,
    UnstructuredMarkdownLoader
)

# Load from directory
loader = DirectoryLoader("./docs", glob="**/*.md")
documents = loader.load()

# Load specific file types
pdf_loader = PDFLoader("document.pdf")
text_loader = TextLoader("document.txt")
```

## LangSmith Integration

### Setup

```bash
pip install langsmith ragas
```

```python
import os
os.environ["LANGCHAIN_API_KEY"] = "your-api-key"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "your-project-name"
```

### Upload Dataset to LangSmith

```python
from ragas.integrations.langsmith import upload_dataset
from ragas import EvaluationDataset

# Create Ragas dataset
dataset = EvaluationDataset.from_list(your_data)

# Upload to LangSmith
upload_dataset(
    dataset=dataset,
    dataset_name="my-rag-testset"
)
```

### Run Evaluation on LangSmith Dataset

```python
from ragas.integrations.langsmith import evaluate
from ragas.metrics import Faithfulness, AnswerRelevancy

# Define factory function for your QA chain
def create_qa_chain():
    return RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model="gpt-4o"),
        retriever=vectorstore.as_retriever(),
        return_source_documents=True
    )

# Run evaluation
results = evaluate(
    dataset_name="my-rag-testset",
    llm_or_chain_factory=create_qa_chain,
    metrics=[Faithfulness(), AnswerRelevancy()],
    experiment_name="rag-eval-v1"
)
```

**Benefits:**
- Automatic experiment tracking
- Results visualization in LangSmith UI
- Dataset versioning
- Comparison across runs

## LlamaIndex Integration

### Basic Setup

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from ragas.llms import LlamaIndexLLMWrapper
```

### Evaluating LlamaIndex Query Engine

```python
# Create LlamaIndex query engine
documents = SimpleDirectoryReader("./docs").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

# Generate test queries
test_queries = ["What is X?", "How does Y work?"]

# Collect responses
results = []
for query in test_queries:
    response = query_engine.query(query)
    results.append({
        "user_input": query,
        "retrieved_contexts": [node.text for node in response.source_nodes],
        "response": str(response)
    })

# Evaluate with Ragas
from ragas.integrations.llama_index import evaluate
from ragas.metrics import Faithfulness, AnswerRelevancy

llm = LlamaIndexLLMWrapper(OpenAI(model="gpt-4o"))
result = evaluate(
    query_engine=query_engine,
    metrics=[Faithfulness(llm=llm), AnswerRelevancy(llm=llm)],
    dataset=results
)
```

### Test Data Generation with LlamaIndex

```python
from llama_index.core import SimpleDirectoryReader
from ragas.testset.generator import TestsetGenerator
from ragas.llms import LlamaIndexLLMWrapper

# Load documents
documents = SimpleDirectoryReader("./docs").load_data()

# Setup generator
generator_llm = LlamaIndexLLMWrapper(OpenAI(model="gpt-4o"))
generator = TestsetGenerator(llm=generator_llm)

# Generate testset
testset = generator.generate_with_llama_index_docs(
    documents,
    testset_size=50
)
```

### Agent Evaluation

```python
from ragas.integrations.llama_index import convert_to_ragas_messages
from ragas.metrics import AgentGoalAccuracyWithoutReference

# Collect agent events
agent_events = []  # List of agent interaction events

# Convert to Ragas format
ragas_messages = convert_to_ragas_messages(agent_events)

# Evaluate
from ragas.dataset_schema import MultiTurnSample
sample = MultiTurnSample(user_input=ragas_messages)
score = await agent_goal_accuracy.multi_turn_ascore(sample)
```

## Langfuse Integration

### Setup

```bash
pip install langfuse ragas
```

### Trace-Based Evaluation

```python
from langfuse import Langfuse
from ragas.metrics import Faithfulness, AnswerRelevancy
from ragas.dataset_schema import SingleTurnSample

# Initialize Langfuse
langfuse = Langfuse(
    public_key="your-public-key",
    secret_key="your-secret-key"
)

# Score function
async def score_with_ragas(query, chunks, answer):
    sample = SingleTurnSample(
        user_input=query,
        retrieved_contexts=chunks,
        response=answer
    )
    
    scores = {}
    for metric in [Faithfulness(), AnswerRelevancy()]:
        scores[metric.name] = await metric.single_turn_ascore(sample)
    
    return scores

# Score each trace
trace = langfuse.trace(name="rag-query")
scores = await score_with_ragas(query, contexts, response)

# Log scores to Langfuse
for metric_name, score in scores.items():
    trace.score(name=metric_name, value=score.value)
```

### Batch Evaluation

```python
# Fetch traces from Langfuse
traces = langfuse.get_traces(limit=100)

# Evaluate in batch
results = []
for trace in traces:
    query = trace.input["query"]
    contexts = trace.output["contexts"]
    response = trace.output["response"]
    
    scores = await score_with_ragas(query, contexts, response)
    results.append({
        "trace_id": trace.id,
        "scores": scores
    })
```

**Benefits:**
- Real-time trace evaluation
- Production monitoring
- Visualization of metrics
- Issue detection and alerting

## Phoenix (Arize AI) Integration

### Setup

```bash
pip install arize-phoenix ragas
```

### Trace Collection & Evaluation

```python
import phoenix as px
from ragas.metrics import Faithfulness, AnswerCorrectness

# Launch Phoenix
session = px.launch_app()

# Evaluate RAG pipeline
result = evaluate(
    dataset=evaluation_dataset,
    metrics=[Faithfulness(), AnswerCorrectness()]
)

# Export to Phoenix for visualization
result.to_phoenix()
```

### Cluster Analysis

Phoenix provides embedding-based cluster analysis:

1. Reduces dimensionality of embeddings
2. Clusters semantically similar queries
3. Visualizes performance per cluster
4. Identifies problematic query patterns

**Workflow:**
- Generate embeddings for queries/contexts
- Run Ragas evaluation
- Export to Phoenix
- Visualize clusters colored by metric scores
- Identify low-performing clusters

## Weights & Biases Integration

### Setup

```bash
pip install wandb ragas
```

### Logging Evaluations

```python
import wandb
from ragas import evaluate

# Initialize W&B run
wandb.init(project="rag-evaluation", name="experiment-1")

# Run evaluation
result = evaluate(
    dataset=evaluation_dataset,
    metrics=[Faithfulness(), AnswerRelevancy()]
)

# Log results
wandb.log({
    "faithfulness": result["faithfulness"],
    "answer_relevancy": result["answer_relevancy"]
})

# Log dataset
wandb.log({"evaluation_results": wandb.Table(dataframe=result.to_pandas())})

wandb.finish()
```

### Comparing Experiments

```python
# Run multiple experiments
experiments = [
    {"name": "baseline", "config": config1},
    {"name": "improved", "config": config2}
]

for exp in experiments:
    wandb.init(project="rag-evaluation", name=exp["name"])
    # Run evaluation with different configs
    result = evaluate(dataset, metrics, **exp["config"])
    wandb.log(result)
    wandb.finish()
```

## MLflow Integration

### Setup

```bash
pip install mlflow ragas
```

### Logging with MLflow

```python
import mlflow
from ragas import evaluate

# Start MLflow run
with mlflow.start_run(run_name="rag-eval-v1"):
    # Log parameters
    mlflow.log_param("chunk_size", 500)
    mlflow.log_param("top_k", 5)
    
    # Run evaluation
    result = evaluate(dataset, metrics)
    
    # Log metrics
    mlflow.log_metrics({
        "faithfulness": result["faithfulness"],
        "answer_relevancy": result["answer_relevancy"]
    })
    
    # Log artifact
    result.to_pandas().to_csv("results.csv")
    mlflow.log_artifact("results.csv")
```

## Custom Integration Pattern

For tools not directly supported:

```python
from ragas import evaluate

def evaluate_and_log_to_custom_tool(dataset, metrics, tool_client):
    """Generic pattern for custom integrations."""
    
    # Run Ragas evaluation
    result = evaluate(dataset=dataset, metrics=metrics)
    
    # Convert to format for your tool
    results_dict = {
        "metrics": result.to_dict(),
        "timestamp": datetime.now().isoformat(),
        "dataset_size": len(dataset)
    }
    
    # Log to your tool
    tool_client.log_evaluation(results_dict)
    
    # Optionally export detailed results
    df = result.to_pandas()
    tool_client.upload_dataframe(df)
    
    return result
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: RAG Evaluation

on: [push, pull_request]

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install ragas langchain openai
      - name: Run evaluation
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          python evaluate_rag.py
      - name: Upload results
        uses: actions/upload-artifact@v2
        with:
          name: evaluation-results
          path: results.csv
```

### Evaluation Script (evaluate_rag.py)

```python
#!/usr/bin/env python3
from ragas import evaluate
from ragas.metrics import Faithfulness, AnswerRelevancy
import sys

# Load test dataset
dataset = load_testset()

# Run evaluation
result = evaluate(
    dataset=dataset,
    metrics=[Faithfulness(), AnswerRelevancy()]
)

# Check thresholds
if result["faithfulness"] < 0.8 or result["answer_relevancy"] < 0.7:
    print("Evaluation failed: scores below threshold")
    sys.exit(1)

# Save results
result.to_pandas().to_csv("results.csv")
print("Evaluation passed!")
```

## Best Practices for Integrations

1. **Version control testsets:** Track datasets alongside code
2. **Automate evaluations:** Run in CI/CD on every change
3. **Track experiments:** Use observability tools for comparison
4. **Set quality gates:** Define minimum score thresholds
5. **Monitor production:** Continuous evaluation on live data
6. **Visualize trends:** Track metrics over time
7. **Alert on degradation:** Set up notifications for score drops

## Common Integration Patterns

**Development Workflow:**
1. Generate synthetic testset
2. Evaluate baseline RAG
3. Track scores in Langfuse/W&B
4. Iterate on improvements
5. Re-evaluate and compare

**Production Monitoring:**
1. Trace production queries
2. Sample traces periodically
3. Evaluate with Ragas
4. Log to observability tool
5. Alert on metric degradation

**Experiment Tracking:**
1. Define experiment parameters
2. Run evaluation for each config
3. Log to MLflow/W&B
4. Compare results
5. Select best configuration
