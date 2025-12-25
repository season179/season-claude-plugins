# Research API Reference

The Research API performs multi-step web research asynchronously, returning structured JSON results with citations.

## Table of Contents
- [Overview](#overview)
- [research.create Method](#researchcreate-method)
- [research.get Method](#researchget-method)
- [research.pollUntilFinished Method](#researchpolluntilfinished-method)
- [research.list Method](#researchlist-method)
- [Examples](#examples)
- [Types](#types)

## Overview

Research tasks are asynchronous operations that:
1. Perform multi-step web research
2. Return structured JSON based on your schema
3. Include citations for all data points

## research.create Method

Create a new research task.

```typescript
import Exa, { ResearchModel } from "exa-js";

const exa = new Exa(process.env.EXA_API_KEY);

const task = await exa.research.create({
  instructions: "What is the latest valuation of SpaceX?",
  outputSchema: {
    type: "object",
    properties: {
      valuation: { type: "string" },
      date: { type: "string" },
      source: { type: "string" },
    },
  },
  model: ResearchModel.exa_research,
});

console.log(`Task ID: ${task.researchId}`);
```

### Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| instructions | string | Natural language research instructions | Required |
| outputSchema | object | JSON Schema for structured output | undefined (auto-inferred) |
| model | ResearchModel | Research model to use | exa_research |

### Research Models

```typescript
enum ResearchModel {
  exa_research = "exa_research",
  exa_research_pro = "exa_research_pro",
}
```

### Response

```typescript
interface CreateTaskResponse {
  researchId: string;
}
```

## research.get Method

Get the status and results of a research task.

```typescript
const task = await exa.research.get(researchId);

if (task.status === "completed") {
  console.log("Results:", task.data);
  console.log("Citations:", task.citations);
}
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| researchId | string | The task ID from create |

### Response

```typescript
interface ResearchTask {
  researchId: string;
  status: "running" | "completed" | "failed";
  instructions: string;
  schema?: object;
  data?: object;         // Populated when completed
  citations?: Record<string, Citation[]>;  // Citations by field
}

interface Citation {
  id: string;
  url: string;
  title?: string;
  snippet: string;
}
```

## research.pollUntilFinished Method

Poll a task until completion (1 second interval, 10 minute timeout).

```typescript
const task = await exa.research.create({
  instructions: "Get information about Paris, France",
  outputSchema: {
    type: "object",
    properties: {
      name: { type: "string" },
      population: { type: "string" },
      founded_date: { type: "string" },
    },
  },
});

// Wait for completion
const result = await exa.research.pollUntilFinished(task.researchId);
console.log("Research complete:", result.data);
```

## research.list Method

List all research tasks with pagination.

```typescript
// List all tasks
const response = await exa.research.list();
console.log(`Found ${response.data.length} tasks`);

// With pagination
const page1 = await exa.research.list({ limit: 10 });

if (page1.hasMore) {
  const page2 = await exa.research.list({
    cursor: page1.nextCursor,
    limit: 10,
  });
}
```

### Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| cursor | string | Pagination cursor | undefined |
| limit | number | Results per page (1-200) | 25 |

### Response

```typescript
interface ListTasksResponse {
  data: ResearchTask[];
  hasMore: boolean;
  nextCursor?: string;
}
```

## Examples

### Company Research

```typescript
const task = await exa.research.create({
  instructions: "Research OpenAI's current valuation, key products, and main competitors",
  outputSchema: {
    type: "object",
    properties: {
      valuation: { type: "string" },
      products: {
        type: "array",
        items: { type: "string" },
      },
      competitors: {
        type: "array",
        items: { type: "string" },
      },
      ceo: { type: "string" },
      headquarters: { type: "string" },
    },
    required: ["valuation", "products"],
  },
});

const result = await exa.research.pollUntilFinished(task.researchId);

// Access structured data
console.log(`Valuation: ${result.data.valuation}`);
console.log(`Products: ${result.data.products.join(", ")}`);

// Access citations for specific fields
if (result.citations?.valuation) {
  console.log("Valuation sources:");
  result.citations.valuation.forEach(c => console.log(`  - ${c.url}`));
}
```

### Market Analysis

```typescript
const task = await exa.research.create({
  instructions: `
    Analyze the current state of the electric vehicle market in the US.
    Include market size, growth rate, key players, and trends.
  `,
  outputSchema: {
    type: "object",
    properties: {
      marketSize: { type: "string" },
      growthRate: { type: "string" },
      keyPlayers: {
        type: "array",
        items: {
          type: "object",
          properties: {
            name: { type: "string" },
            marketShare: { type: "string" },
          },
        },
      },
      trends: {
        type: "array",
        items: { type: "string" },
      },
    },
  },
  model: ResearchModel.exa_research_pro,
});

const result = await exa.research.pollUntilFinished(task.researchId);
```

### Schema-Less Research

Let the model infer the appropriate schema:

```typescript
const task = await exa.research.create({
  instructions: "What are the main benefits of meditation?",
  // No outputSchema - will be inferred
});

const result = await exa.research.pollUntilFinished(task.researchId);
console.log(result.data);  // Structure inferred by model
```

## Types

```typescript
import Exa, { ResearchModel, ResearchTask, Citation } from "exa-js";

interface ResearchCreateOptions {
  instructions: string;
  outputSchema?: object;
  model?: ResearchModel;
}

interface ResearchTask {
  researchId: string;
  status: "running" | "completed" | "failed";
  instructions: string;
  schema?: object;
  data?: object;
  citations?: Record<string, Citation[]>;
}

interface Citation {
  id: string;
  url: string;
  title?: string;
  snippet: string;
}

interface ListOptions {
  cursor?: string;
  limit?: number;  // 1-200, default 25
}
```

## Error Handling

```typescript
try {
  const result = await exa.research.pollUntilFinished(researchId);
  
  if (result.status === "failed") {
    console.error("Research failed");
    return;
  }
  
  console.log("Success:", result.data);
} catch (error) {
  if (error.message.includes("timeout")) {
    console.error("Research timed out after 10 minutes");
  } else {
    throw error;
  }
}
```
