# Advanced Usage Guide

**⚠️ Note:** Some examples in this guide use deprecated `metric.ascore()` syntax for brevity. In Ragas v0.2, use `metric.single_turn_ascore(sample)` with `SingleTurnSample` objects instead. See: https://docs.ragas.io/en/stable/howtos/migrations/migrate_from_v01_to_v02/

## Custom Metrics

### Creating DiscreteMetric (Binary/Categorical)

DiscreteMetric is ideal for pass/fail or categorical evaluations:

```python
from ragas.metrics import DiscreteMetric
from ragas.llms import llm_factory

evaluator_llm = llm_factory("gpt-4o")

# Binary metric
tone_appropriateness = DiscreteMetric(
    name="tone_appropriateness",
    allowed_values=["appropriate", "inappropriate"],
    prompt="""Evaluate if the response tone is appropriate for the context.
    User Input: {user_input}
    Response: {response}
    
    Answer with only 'appropriate' or 'inappropriate'.""",
    llm=evaluator_llm
)

# Categorical metric
response_category = DiscreteMetric(
    name="response_type",
    allowed_values=["factual", "opinion", "unclear"],
    prompt="""Categorize the response type.
    Response: {response}
    
    Answer with only 'factual', 'opinion', or 'unclear'.""",
    llm=evaluator_llm
)

# Use the metric
score = await tone_appropriateness.ascore(
    user_input="Explain quantum computing",
    response="Quantum computing uses quantum mechanics..."
)
```

### Creating ContinuousMetric

For numeric scoring (0-1 range):

```python
from ragas.metrics import ContinuousMetric

clarity_score = ContinuousMetric(
    name="clarity",
    prompt="""Rate the clarity of the response on a scale from 0 to 1.
    0 = very unclear, 1 = perfectly clear
    
    Response: {response}
    
    Provide only a number between 0 and 1.""",
    llm=evaluator_llm
)

score = await clarity_score.ascore(response="Your response text")
```

### AspectCritic Pattern

For evaluating specific aspects:

```python
from ragas.metrics import AspectCritic

# Code quality evaluator
code_quality = AspectCritic(
    name="code_quality",
    llm=evaluator_llm,
    definition="""Score 1 if the code follows best practices:
    - Proper error handling
    - Clear variable names
    - Appropriate comments
    Score 0 otherwise."""
)

# Bias detection
bias_detector = AspectCritic(
    name="bias_free",
    llm=evaluator_llm,
    definition="""Score 1 if the response is free from gender, racial, or other biases.
    Score 0 if any bias is detected."""
)

# Domain accuracy
medical_accuracy = AspectCritic(
    name="medical_accuracy",
    llm=evaluator_llm,
    definition="""Score 1 if medical information is accurate and current.
    Score 0 if any medical inaccuracies are present."""
)
```

### Multi-Aspect Evaluation

Combine multiple custom metrics:

```python
custom_metrics = [
    AspectCritic(name="safety", definition="...", llm=evaluator_llm),
    AspectCritic(name="helpfulness", definition="...", llm=evaluator_llm),
    AspectCritic(name="accuracy", definition="...", llm=evaluator_llm),
    DiscreteMetric(name="tone", allowed_values=["professional", "casual"], prompt="...", llm=evaluator_llm)
]

# Evaluate with all metrics
from ragas import evaluate
result = evaluate(dataset=dataset, metrics=custom_metrics)
```

### Domain-Specific Metrics

#### Finance/Legal

```python
compliance_check = AspectCritic(
    name="regulatory_compliance",
    llm=evaluator_llm,
    definition="""Score 1 if the advice complies with financial regulations:
    - Includes proper disclaimers
    - Doesn't guarantee returns
    - Mentions risks appropriately
    Score 0 otherwise."""
)

citation_quality = AspectCritic(
    name="citation_quality",
    llm=evaluator_llm,
    definition="""Score 1 if legal citations are:
    - Properly formatted
    - Accurate case references
    - Current law (not outdated)
    Score 0 otherwise."""
)
```

#### Technical Documentation

```python
completeness = AspectCritic(
    name="documentation_completeness",
    llm=evaluator_llm,
    definition="""Score 1 if documentation includes:
    - Prerequisites
    - Step-by-step instructions
    - Expected outcomes
    - Troubleshooting
    Score 0 if any critical section is missing."""
)

code_example_quality = AspectCritic(
    name="code_examples",
    llm=evaluator_llm,
    definition="""Score 1 if code examples are:
    - Syntactically correct
    - Well-commented
    - Show best practices
    Score 0 otherwise."""
)
```

## Agent Evaluation

### Single-Turn Agent Evaluation

For simple agent interactions:

```python
from ragas.metrics import AgentGoalAccuracyWithoutReference
from ragas.dataset_schema import SingleTurnSample

metric = AgentGoalAccuracyWithoutReference(llm=evaluator_llm)

sample = SingleTurnSample(
    user_input="Book a flight to Paris",
    response="I've found 3 flights to Paris. Would you like to book the 10am departure?"
)

score = await metric.single_turn_ascore(sample)
```

### Multi-Turn Agent Evaluation

For conversational agents:

```python
from ragas.metrics import AgentGoalAccuracyWithReference
from ragas.dataset_schema import MultiTurnSample
from ragas.messages import HumanMessage, AIMessage, ToolMessage

# Build conversation history
messages = [
    HumanMessage(content="Book me a flight to Paris"),
    AIMessage(content="When would you like to travel?"),
    HumanMessage(content="Next Monday"),
    ToolMessage(content="Search results: 3 flights available", tool_name="search_flights"),
    AIMessage(content="I found 3 flights. The 10am flight is cheapest at $350.")
]

sample = MultiTurnSample(
    user_input=messages,
    reference="Successfully help user book a flight to Paris for next Monday"
)

metric = AgentGoalAccuracyWithReference(llm=evaluator_llm)
score = await metric.multi_turn_ascore(sample)
```

### Tool Call Evaluation

```python
from ragas.metrics import ToolCallAccuracy
from ragas.messages import ToolCall as RagasToolCall

# Define expected tool calls
expected_tools = [
    RagasToolCall(
        name="search_flights",
        args={"destination": "Paris", "date": "2024-01-15"}
    ),
    RagasToolCall(
        name="book_flight",
        args={"flight_id": "FL123"}
    )
]

sample = MultiTurnSample(
    user_input=agent_messages,
    reference_tool_calls=expected_tools
)

metric = ToolCallAccuracy()
score = await metric.multi_turn_ascore(sample)
```

### Agent-Specific Metrics

```python
# Task completion
task_completion = AspectCritic(
    name="task_completion",
    llm=evaluator_llm,
    definition="""Score 1 if the agent successfully completed the user's task.
    Score 0 if task was not completed or completed incorrectly."""
)

# Efficiency
efficiency = AspectCritic(
    name="efficiency",
    llm=evaluator_llm,
    definition="""Score 1 if agent used minimal steps and appropriate tools.
    Score 0 if agent was inefficient or used wrong tools."""
)

# Error handling
error_handling = AspectCritic(
    name="error_handling",
    llm=evaluator_llm,
    definition="""Score 1 if agent gracefully handled errors:
    - Clear error messages
    - Suggested alternatives
    - Recovered appropriately
    Score 0 otherwise."""
)
```

## Optimization Strategies

### Cost Optimization

#### Selective Metric Usage

```python
# Development: Use subset of metrics
dev_metrics = [Faithfulness(), AnswerRelevancy()]

# Production: Use comprehensive set
prod_metrics = [
    Faithfulness(),
    AnswerRelevancy(),
    ContextPrecision(),
    AnswerCorrectness()
]
```

#### Tiered Evaluation

```python
# Tier 1: Fast screening (cheap metrics)
tier1_metrics = [Faithfulness()]
tier1_result = evaluate(dataset, tier1_metrics)

# Tier 2: Only evaluate samples that passed Tier 1
passed_samples = [s for s, score in zip(dataset, tier1_result) if score > 0.7]
tier2_metrics = [AnswerCorrectness(), ContextPrecision()]
tier2_result = evaluate(passed_samples, tier2_metrics)
```

#### Mixed Model Strategy

```python
from ragas.llms import llm_factory

# Use cheaper model for simple metrics
cheap_llm = llm_factory("gpt-3.5-turbo")
expensive_llm = llm_factory("gpt-4o")

faithfulness = Faithfulness(llm=cheap_llm)
answer_correctness = AnswerCorrectness(llm=expensive_llm)
```

### Sampling Strategies

#### Random Sampling

```python
import random

# Evaluate random sample instead of full dataset
sample_size = 100
sampled_dataset = random.sample(full_dataset, sample_size)
result = evaluate(sampled_dataset, metrics)
```

#### Stratified Sampling

```python
# Sample proportionally from different query types
simple_queries = [q for q in dataset if q["type"] == "simple"]
complex_queries = [q for q in dataset if q["type"] == "complex"]

sample = (
    random.sample(simple_queries, 30) +
    random.sample(complex_queries, 20)
)
```

#### Confidence-Based Sampling

```python
# Evaluate uncertain predictions more frequently
def get_confidence_score(sample):
    """Implement your confidence scoring logic."""
    return sample.get("confidence", 0.5)

# Sort by confidence and sample more from low-confidence
sorted_samples = sorted(dataset, key=get_confidence_score)
sample = sorted_samples[:100]  # Evaluate bottom 100
```

### Parallel Evaluation

```python
import asyncio
from ragas.metrics import Faithfulness

metric = Faithfulness()

async def evaluate_batch(samples):
    """Evaluate multiple samples in parallel."""
    tasks = [metric.ascore(**sample) for sample in samples]
    return await asyncio.gather(*tasks)

# Run parallel evaluation
results = asyncio.run(evaluate_batch(dataset))
```

### Caching Strategies

```python
import hashlib
import json
import shelve

class CachedEvaluator:
    def __init__(self, metric, cache_file="eval_cache.db"):
        self.metric = metric
        self.cache = shelve.open(cache_file)
    
    def get_cache_key(self, sample):
        """Generate unique key for sample."""
        content = json.dumps(sample, sort_keys=True)
        return hashlib.md5(content.encode()).hexdigest()
    
    async def evaluate(self, sample):
        """Evaluate with caching."""
        cache_key = self.get_cache_key(sample)
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        result = await self.metric.ascore(**sample)
        self.cache[cache_key] = result
        return result
    
    def close(self):
        self.cache.close()

# Usage
cached_evaluator = CachedEvaluator(Faithfulness())
result = await cached_evaluator.evaluate(sample)
cached_evaluator.close()
```

## Performance Optimization

### Batch Processing

```python
from ragas import evaluate

# Process in batches to manage memory
batch_size = 50
all_results = []

for i in range(0, len(dataset), batch_size):
    batch = dataset[i:i + batch_size]
    result = evaluate(batch, metrics)
    all_results.append(result)
```

### Async Evaluation

```python
async def evaluate_async(dataset, metrics):
    """Asynchronous evaluation for better performance."""
    tasks = []
    for sample in dataset:
        for metric in metrics:
            task = metric.ascore(**sample)
            tasks.append(task)
    
    results = await asyncio.gather(*tasks)
    return results

# Run async evaluation
results = asyncio.run(evaluate_async(dataset, metrics))
```

### GPU Acceleration

For local models using GPU:

```python
from langchain_community.llms import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load model with GPU
model_name = "mistralai/Mistral-7B-Instruct-v0.2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"  # Automatic GPU placement
)

# Create pipeline
pipeline = HuggingFacePipeline(
    model=model,
    tokenizer=tokenizer
)

# Use with Ragas (auto-wrapped internally)
llm = pipeline  # Pass directly - Ragas auto-wraps LangChain LLMs
```

## Advanced Dataset Management

### Dataset Versioning

```python
from datetime import datetime
import json

class VersionedDataset:
    def __init__(self, name):
        self.name = name
        self.versions = []
    
    def add_version(self, dataset, metadata=None):
        """Add a new dataset version."""
        version = {
            "timestamp": datetime.now().isoformat(),
            "data": dataset,
            "metadata": metadata or {},
            "version_number": len(self.versions) + 1
        }
        self.versions.append(version)
    
    def get_version(self, version_number):
        """Retrieve specific version."""
        return self.versions[version_number - 1]
    
    def save(self, filepath):
        """Save all versions."""
        with open(filepath, 'w') as f:
            json.dump(self.versions, f, indent=2)
    
    def load(self, filepath):
        """Load versions from file."""
        with open(filepath, 'r') as f:
            self.versions = json.load(f)

# Usage
dataset_manager = VersionedDataset("rag-testset")
dataset_manager.add_version(
    dataset,
    metadata={"config": "baseline", "size": len(dataset)}
)
dataset_manager.save("testset_versions.json")
```

### Dataset Augmentation

```python
def augment_dataset(dataset, augmentation_factor=2):
    """Create variations of existing samples."""
    augmented = []
    
    for sample in dataset:
        augmented.append(sample)  # Original
        
        # Create variations
        for i in range(augmentation_factor - 1):
            variation = {
                "user_input": rephrase_query(sample["user_input"]),
                "retrieved_contexts": sample["retrieved_contexts"],
                "response": sample["response"],
                "reference": sample["reference"]
            }
            augmented.append(variation)
    
    return augmented

def rephrase_query(query):
    """Rephrase query while maintaining intent."""
    # Implement using LLM or paraphrasing tool
    pass
```

## Evaluation Pipeline Patterns

### Comprehensive RAG Evaluation Pipeline

```python
class RAGEvaluationPipeline:
    def __init__(self, rag_system, metrics, testset):
        self.rag = rag_system
        self.metrics = metrics
        self.testset = testset
        self.results = []
    
    async def run_evaluation(self):
        """Execute full evaluation pipeline."""
        # Step 1: Generate responses
        print("Generating responses...")
        dataset = await self.generate_responses()
        
        # Step 2: Evaluate with metrics
        print("Evaluating with Ragas...")
        eval_results = evaluate(dataset, self.metrics)
        
        # Step 3: Analyze results
        print("Analyzing results...")
        analysis = self.analyze_results(eval_results)
        
        # Step 4: Generate report
        print("Generating report...")
        report = self.generate_report(analysis)
        
        return report
    
    async def generate_responses(self):
        """Run testset through RAG system."""
        dataset = []
        for sample in self.testset:
            response = await self.rag.query(sample["user_input"])
            dataset.append({
                "user_input": sample["user_input"],
                "retrieved_contexts": response["contexts"],
                "response": response["answer"],
                "reference": sample.get("reference")
            })
        return dataset
    
    def analyze_results(self, results):
        """Analyze evaluation results."""
        df = results.to_pandas()
        return {
            "mean_scores": df.mean(),
            "low_performers": df[df["faithfulness"] < 0.7],
            "high_performers": df[df["faithfulness"] > 0.9]
        }
    
    def generate_report(self, analysis):
        """Generate evaluation report."""
        return f"""
        RAG Evaluation Report
        ====================
        Mean Scores: {analysis['mean_scores']}
        Low Performers: {len(analysis['low_performers'])}
        High Performers: {len(analysis['high_performers'])}
        """
```

## Best Practices Summary

1. **Start simple:** Begin with core metrics, add complexity as needed
2. **Iterate quickly:** Use cheap models and small samples for development
3. **Cache aggressively:** Avoid re-evaluating identical samples
4. **Monitor costs:** Track API usage and optimize based on budget
5. **Version everything:** Track datasets, configs, and results
6. **Automate evaluation:** Integrate into CI/CD pipeline
7. **Human validation:** Spot-check metric scores regularly
8. **Domain customization:** Create custom metrics for specific requirements
