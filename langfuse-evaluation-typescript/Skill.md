---
name: langfuse-evaluation-typescript
description: "Evaluates and tests LLM outputs in TypeScript: custom scores, datasets, experiments, LLM-as-a-judge evaluators, AutoEvals, CI/CD testing. For quality assurance and regression testing."
---

# LangFuse Evaluation (TypeScript)

Expert guide for evaluating LLM outputs using LangFuse in TypeScript/JavaScript. Covers custom scores, datasets, experiments, evaluators, and automated testing.

## When to Use This Skill

Use this skill when users ask to:
- Create custom scores for LLM outputs in TypeScript/JavaScript projects
- Set up LLM-as-a-judge evaluators
- Build datasets and run experiments
- Implement evaluation workflows with LangFuse
- Automate LLM testing in CI/CD pipelines
- Integrate pre-built evaluators (AutoEvals)

Also useful when measuring LLM quality, debugging failures, or A/B testing prompts.

## Quick Start

**Prerequisites**: LangFuse account with API keys, Node.js project

### Installation

```bash
npm install @langfuse/client
npm install autoevals  # Optional: for pre-built evaluators
```

### Initialize Client

```typescript
import { LangfuseClient } from "@langfuse/client";

const langfuse = new LangfuseClient({
  secretKey: process.env.LANGFUSE_SECRET_KEY,
  publicKey: process.env.LANGFUSE_PUBLIC_KEY,
  baseUrl: "https://cloud.langfuse.com"
});
```

## Custom Scores

### Numeric Scores

```typescript
await langfuse.score.create({
  traceId: "trace-abc-123",
  name: "accuracy",
  value: 0.95,
  dataType: "NUMERIC",
  comment: "High accuracy on test set"
});
```

### Boolean Scores

```typescript
await langfuse.score.create({
  traceId: "trace-abc-123",
  name: "factual_correctness",
  value: 1,  // 1 for true, 0 for false
  dataType: "BOOLEAN",
  comment: "All facts verified"
});
```

### Categorical Scores

```typescript
await langfuse.score.create({
  traceId: "trace-abc-123",
  name: "sentiment",
  value: "positive",  // or "negative", "neutral"
  dataType: "CATEGORICAL",
  comment: "Customer feedback analysis"
});
```

### Score Validation with ConfigId

```typescript
// Create score config in UI first, then reference it
await langfuse.score.create({
  traceId: "trace-abc-123",
  name: "quality",
  value: 0.85,
  configId: "config-quality-v1",  // Validates against config
  comment: "Quality assessment"
});
```

### Idempotent Scoring

```typescript
// Prevents duplicate scores with same ID
await langfuse.score.create({
  id: "score-unique-123",  // Custom ID for idempotency
  traceId: "trace-abc-123",
  name: "coherence",
  value: 0.9
});
```

## Datasets

### Create Dataset

```typescript
const dataset = await langfuse.api.datasets.create({
  name: "customer-support-qa",
  description: "Customer support Q&A test set",
  metadata: { version: "1.0", category: "support" }
});
```

### Add Dataset Items

```typescript
await langfuse.api.datasets.createItem({
  datasetName: "customer-support-qa",
  input: { question: "How do I reset my password?" },
  expectedOutput: "Click 'Forgot Password' on the login page.",
  metadata: { difficulty: "easy" }
});
```

### Fetch Dataset

```typescript
const dataset = await langfuse.dataset.get("customer-support-qa");

for (const item of dataset.items) {
  console.log(item.input);
  console.log(item.expectedOutput);
}
```

## Experiments

### Basic Experiment

```typescript
import { LangfuseClient } from "@langfuse/client";
import { NodeSDK } from "@opentelemetry/sdk-node";
import { LangfuseSpanProcessor } from "@langfuse/otel";

// Initialize OpenTelemetry
const otelSdk = new NodeSDK({
  spanProcessors: [new LangfuseSpanProcessor()]
});
otelSdk.start();

const langfuse = new LangfuseClient();

// Define task function
async function myTask(item) {
  const question = item.input.question;

  // Your LLM call here
  const response = await callLLM(question);

  return { output: response };
}

// Run experiment
const result = await langfuse.experiment.run({
  name: "Customer Support Q&A v1",
  data: [
    { input: { question: "How do I reset my password?" } },
    { input: { question: "What are your business hours?" } }
  ],
  task: myTask
});

console.log(await result.format());

// Flush before exit
await otelSdk.shutdown();
```

### Experiment with Dataset

```typescript
const dataset = await langfuse.dataset.get("customer-support-qa");

const result = await dataset.runExperiment({
  name: "GPT-4 Customer Support Test",
  description: "Testing GPT-4 on customer support queries",
  task: myTask
});

console.log(await result.format());
```

### Evaluators

#### Item-Level Evaluator

```typescript
import { Evaluation } from "@langfuse/client";

function accuracyEvaluator({ input, output, expectedOutput, metadata }): Evaluation {
  const isCorrect = output.toLowerCase().includes(expectedOutput.toLowerCase());

  return {
    name: "accuracy",
    value: isCorrect ? 1 : 0,
    dataType: "BOOLEAN",
    comment: isCorrect ? "Correct answer" : "Incorrect answer"
  };
}

// Use in experiment
const result = await langfuse.experiment.run({
  name: "Experiment with Evaluation",
  data: myData,
  task: myTask,
  evaluators: [accuracyEvaluator]
});
```

#### Run-Level Evaluator

```typescript
function avgScoreEvaluator({ results }): Evaluation {
  const scores = results.map(r => r.scores.find(s => s.name === "accuracy")?.value || 0);
  const average = scores.reduce((a, b) => a + b, 0) / scores.length;

  return {
    name: "average_accuracy",
    value: average,
    dataType: "NUMERIC",
    comment: `Average accuracy across ${scores.length} items`
  };
}

// Use in experiment
const result = await langfuse.experiment.run({
  name: "Experiment with Run-Level Eval",
  data: myData,
  task: myTask,
  evaluators: [accuracyEvaluator],
  runEvaluators: [avgScoreEvaluator]
});
```

## AutoEvals Integration

### Using Pre-Built Evaluators

```typescript
import { Factuality } from "autoevals";
import { createEvaluatorFromAutoevals } from "@langfuse/client";

// Wrap AutoEvals evaluator
const factualityEvaluator = createEvaluatorFromAutoevals(Factuality);

// Complete example
const result = await langfuse.experiment.run({
  name: "Factuality Check",
  data: [
    {
      input: { question: "What is the capital of France?" },
      expectedOutput: "Paris"
    },
    {
      input: { question: "When was the Eiffel Tower built?" },
      expectedOutput: "1889"
    }
  ],
  task: async (item) => {
    const response = await callLLM(item.input.question);
    return { output: response };
  },
  evaluators: [factualityEvaluator]
});

// Check factuality scores
result.results.forEach(r => {
  const score = r.scores.find(s => s.name === "factuality");
  console.log(`Factuality: ${score?.value} - ${score?.comment}`);
});
```

### Available AutoEvals Evaluators

```typescript
import {
  Factuality,      // Checks factual accuracy
  Humor,           // Evaluates humor quality
  Security,        // Detects security issues
  Translation,     // Translation quality
  ClosedQA,        // Closed-domain Q&A
  OpenQA           // Open-domain Q&A
} from "autoevals";
```

## CI/CD Testing with Vitest

### Basic Test Setup

```typescript
import { describe, it, expect } from "vitest";
import { LangfuseClient } from "@langfuse/client";

describe("LLM Evaluation Tests", () => {
  it("should pass accuracy threshold", async () => {
    const langfuse = new LangfuseClient();

    const result = await langfuse.experiment.run({
      name: "CI Test Run",
      data: testDataset,
      task: myTask,
      evaluators: [accuracyEvaluator]
    });

    const avgAccuracy = result.summary.scores.find(
      s => s.name === "average_accuracy"
    )?.value;

    expect(avgAccuracy).toBeGreaterThan(0.8);
  });
});
```

### Assertion Patterns

```typescript
it("should have high factuality score", async () => {
  const result = await runExperiment();

  const factualityScores = result.results
    .map(r => r.scores.find(s => s.name === "factuality")?.value)
    .filter(v => v !== undefined);

  const avgFactuality = factualityScores.reduce((a, b) => a + b, 0) / factualityScores.length;

  expect(avgFactuality).toBeGreaterThan(0.9);
  expect(factualityScores.every(s => s > 0.7)).toBe(true);
});
```

## Common Gotchas

1. **Forgetting OpenTelemetry setup**: Experiments require `NodeSDK` initialization
   ```typescript
   const otelSdk = new NodeSDK({
     spanProcessors: [new LangfuseSpanProcessor()]
   });
   otelSdk.start();
   ```

2. **Not shutting down SDK**: Always call `await otelSdk.shutdown()` after experiments to flush traces

3. **Score value types**: Boolean scores use `1` (true) or `0` (false) as numbers, not `true`/`false`
   ```typescript
   value: 1,  // ✅ Correct
   value: true,  // ❌ Wrong
   ```

4. **Dataset naming**: Dataset names are case-sensitive in `langfuse.dataset.get()`

## Getting More Information

When you need detailed documentation, use these MCP tools available to Claude:

- **Search docs**: `mcp__langfuse-docs__searchLangfuseDocs` with query like "TypeScript evaluation experiments"
- **Get specific page**: `mcp__langfuse-docs__getLangfuseDocsPage` with path like "/docs/evaluation/experiments/experiments-via-sdk"
- **Get overview**: `mcp__langfuse-docs__getLangfuseOverview` for high-level structure

## Key Reminders

- **Score Types**: NUMERIC (float), BOOLEAN (0/1), CATEGORICAL (string)
- **ConfigId**: Use to validate scores against pre-defined configs
- **Idempotency**: Provide custom `id` to prevent duplicate scores
- **OpenTelemetry**: Required for experiments - initialize `NodeSDK` with `LangfuseSpanProcessor`
- **Shutdown**: Always call `otelSdk.shutdown()` at end of experiments
- **Evaluators**: Item-level run per item, run-level run once for entire experiment
- **AutoEvals**: Wrap with `createEvaluatorFromAutoevals()` before use

## Best Practices

1. **Validate scores**: Use `configId` to ensure scores match expected schema
2. **Dataset versioning**: Include version in metadata for reproducibility
3. **Evaluator composition**: Combine multiple evaluators for comprehensive evaluation
4. **CI/CD integration**: Set score thresholds to fail builds on regressions
5. **Idempotency**: Use custom IDs to safely retry scoring operations
6. **Async/await**: All LangFuse operations are async - always await
