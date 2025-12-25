# Building Agents Reference

Comprehensive guide to creating agents with the AI SDK Agent class.

## Table of Contents

- [Why Use the Agent Class](#why-use-the-agent-class)
- [Creating an Agent](#creating-an-agent)
- [Configuration Options](#configuration-options)
- [System Prompts](#system-prompts)
- [Tools](#tools)
- [Structured Output](#structured-output)
- [Execution Methods](#execution-methods)
- [Type Safety](#type-safety)

## Why Use the Agent Class

The Agent class is recommended for most use cases:

| Benefit | Description |
|---------|-------------|
| **Reduces boilerplate** | Manages loops and message arrays automatically |
| **Improves reusability** | Define once, use throughout application |
| **Simplifies maintenance** | Single place to update agent configuration |
| **Type safety** | Full TypeScript support for tools and outputs |
| **Consistency** | Same behavior and capabilities across codebase |

Use core functions (`generateText`, `streamText`) only when explicit control over each step is needed for complex structured workflows.

## Creating an Agent

### Basic Setup

```ts
import { Experimental_Agent as Agent } from 'ai';
import { createOpenRouter } from '@openrouter/ai-sdk-provider';

const openrouter = createOpenRouter({
  apiKey: process.env.OPENROUTER_API_KEY,
});

const myAgent = new Agent({
  model: openrouter.chat('openai/gpt-oss-120b:nitro'),
  system: 'You are a helpful assistant.',
  tools: {
    // Your tools here
  },
});
```

### Full Configuration Example

```ts
import { Experimental_Agent as Agent, stepCountIs, tool, Output } from 'ai';
import { createOpenRouter } from '@openrouter/ai-sdk-provider';
import { z } from 'zod';

const openrouter = createOpenRouter({
  apiKey: process.env.OPENROUTER_API_KEY,
});

const fullyConfiguredAgent = new Agent({
  // Model configuration
  model: openrouter.chat('openai/gpt-oss-120b:nitro'),
  
  // System prompt
  system: `You are an expert assistant.
  
  Guidelines:
  - Be concise and accurate
  - Use tools when needed
  - Explain your reasoning`,
  
  // Tools
  tools: {
    search: tool({
      description: 'Search for information',
      inputSchema: z.object({
        query: z.string().describe('Search query'),
      }),
      execute: async ({ query }) => {
        // Implementation
        return { results: [] };
      },
    }),
  },
  
  // Tool choice behavior
  toolChoice: 'auto', // 'auto' | 'required' | 'none' | { type: 'tool', toolName: 'name' }
  
  // Loop control
  stopWhen: stepCountIs(20),
  
  // Dynamic step configuration
  prepareStep: async ({ stepNumber, messages }) => {
    if (stepNumber > 5) {
      return { toolChoice: 'none' }; // Force text response after 5 steps
    }
    return {};
  },
  
  // Structured output (optional)
  experimental_output: Output.object({
    schema: z.object({
      answer: z.string(),
      confidence: z.number(),
    }),
  }),
});
```

## Configuration Options

### model

The LLM to use, provided via OpenRouter:

```ts
model: openrouter.chat('openai/gpt-oss-120b:nitro')
```

### system

System prompt defining agent behavior, personality, and constraints:

```ts
system: 'You are an expert data analyst providing clear insights.'
```

### tools

Object containing tool definitions:

```ts
tools: {
  toolName: tool({
    description: 'What the tool does',
    inputSchema: z.object({ /* params */ }),
    execute: async (params) => { /* implementation */ },
  }),
}
```

### toolChoice

Controls how the agent uses tools:

```ts
// Let model decide (default)
toolChoice: 'auto'

// Force tool use
toolChoice: 'required'

// Disable tools
toolChoice: 'none'

// Force specific tool
toolChoice: { type: 'tool', toolName: 'search' }
```

### stopWhen

Defines when to stop the agent loop. See [loop-control.md](loop-control.md) for details.

### prepareStep

Callback to modify settings before each step. See [loop-control.md](loop-control.md) for details.

### experimental_output

Schema for structured output:

```ts
experimental_output: Output.object({
  schema: z.object({
    field: z.string(),
  }),
})
```

## System Prompts

System prompts define agent behavior. Structure them based on complexity.

### Basic Role Definition

```ts
const agent = new Agent({
  model: openrouter.chat('openai/gpt-oss-120b:nitro'),
  system: 'You are an expert data analyst. Provide clear insights from complex data.',
});
```

### Detailed Behavioral Instructions

```ts
const codeReviewAgent = new Agent({
  model: openrouter.chat('openai/gpt-oss-120b:nitro'),
  system: `You are a senior software engineer conducting code reviews.

Your approach:
- Focus on security vulnerabilities first
- Identify performance bottlenecks
- Suggest improvements for readability and maintainability
- Be constructive and educational in feedback
- Always explain why something is an issue and how to fix it`,
});
```

### Constrained Behavior

```ts
const customerSupportAgent = new Agent({
  model: openrouter.chat('openai/gpt-oss-120b:nitro'),
  system: `You are a customer support specialist for an e-commerce platform.

Rules:
- Never make promises about refunds without checking the policy
- Always be empathetic and professional
- If you don't know something, say so and offer to escalate
- Keep responses concise and actionable
- Never share internal company information`,
  tools: {
    checkOrderStatus,
    lookupPolicy,
    createTicket,
  },
});
```

### Tool Usage Instructions

```ts
const researchAgent = new Agent({
  model: openrouter.chat('openai/gpt-oss-120b:nitro'),
  system: `You are a research assistant with access to search and document tools.

When researching:
1. Always start with a broad search to understand the topic
2. Use document analysis for detailed information
3. Cross-reference multiple sources before drawing conclusions
4. Cite your sources when presenting information
5. If information conflicts, present both viewpoints`,
  tools: {
    webSearch,
    analyzeDocument,
    extractQuotes,
  },
});
```

### Format and Style Instructions

```ts
const technicalWriterAgent = new Agent({
  model: openrouter.chat('openai/gpt-oss-120b:nitro'),
  system: `You are a technical documentation writer.

Writing style:
- Use clear, simple language
- Avoid jargon unless necessary
- Structure information with headers and bullet points
- Include code examples where relevant
- Write in second person ("you" instead of "the user")

Always format responses in Markdown.`,
});
```

## Tools

Tools extend agent capabilities beyond text generation.

### Tool Definition Structure

```ts
import { tool } from 'ai';
import { z } from 'zod';

const myTool = tool({
  // Description helps the model understand when to use it
  description: 'Detailed description of what this tool does and when to use it',
  
  // Zod schema for input validation
  inputSchema: z.object({
    requiredParam: z.string().describe('What this parameter is for'),
    optionalParam: z.number().optional().describe('Optional numeric value'),
  }),
  
  // Async execution function
  execute: async ({ requiredParam, optionalParam }) => {
    // Tool implementation
    const result = await someOperation(requiredParam, optionalParam);
    return { data: result };
  },
});
```

### Common Tool Patterns

#### API Integration

```ts
const fetchWeather = tool({
  description: 'Get current weather for a location',
  inputSchema: z.object({
    location: z.string().describe('City name or coordinates'),
    units: z.enum(['celsius', 'fahrenheit']).default('celsius'),
  }),
  execute: async ({ location, units }) => {
    const response = await fetch(`https://api.weather.com?q=${location}&units=${units}`);
    return response.json();
  },
});
```

#### Database Query

```ts
const queryDatabase = tool({
  description: 'Query the product database',
  inputSchema: z.object({
    table: z.enum(['products', 'orders', 'customers']),
    filters: z.record(z.string()).optional(),
    limit: z.number().max(100).default(10),
  }),
  execute: async ({ table, filters, limit }) => {
    const results = await db.query(table, { where: filters, limit });
    return { rows: results, count: results.length };
  },
});
```

#### File Operations

```ts
const readFile = tool({
  description: 'Read contents of a file',
  inputSchema: z.object({
    path: z.string().describe('File path to read'),
    encoding: z.enum(['utf8', 'base64']).default('utf8'),
  }),
  execute: async ({ path, encoding }) => {
    const content = await fs.readFile(path, encoding);
    return { content, size: content.length };
  },
});
```

#### Computation

```ts
const calculate = tool({
  description: 'Perform mathematical calculations',
  inputSchema: z.object({
    expression: z.string().describe('Math expression to evaluate'),
  }),
  execute: async ({ expression }) => {
    // Use a safe math parser
    const result = mathParser.evaluate(expression);
    return { expression, result };
  },
});
```

### Multiple Tools Example

```ts
const dataAnalystAgent = new Agent({
  model: openrouter.chat('openai/gpt-oss-120b:nitro'),
  system: 'You are a data analyst. Use tools to query, analyze, and visualize data.',
  tools: {
    queryData: tool({
      description: 'Query data from the warehouse',
      inputSchema: z.object({
        sql: z.string().describe('SQL query to execute'),
      }),
      execute: async ({ sql }) => {
        const results = await dataWarehouse.query(sql);
        return { data: results, rowCount: results.length };
      },
    }),
    
    computeStats: tool({
      description: 'Compute statistical measures on a dataset',
      inputSchema: z.object({
        data: z.array(z.number()),
        measures: z.array(z.enum(['mean', 'median', 'stddev', 'min', 'max'])),
      }),
      execute: async ({ data, measures }) => {
        const stats = {};
        for (const measure of measures) {
          stats[measure] = computeMeasure(data, measure);
        }
        return stats;
      },
    }),
    
    createChart: tool({
      description: 'Create a chart visualization',
      inputSchema: z.object({
        type: z.enum(['bar', 'line', 'pie', 'scatter']),
        data: z.array(z.object({ x: z.any(), y: z.number() })),
        title: z.string(),
      }),
      execute: async ({ type, data, title }) => {
        const chartUrl = await chartService.create({ type, data, title });
        return { chartUrl };
      },
    }),
  },
  stopWhen: stepCountIs(15),
});
```

## Structured Output

Force the agent to return data in a specific schema.

### Basic Structured Output

```ts
import { Output } from 'ai';

const sentimentAgent = new Agent({
  model: openrouter.chat('openai/gpt-oss-120b:nitro'),
  experimental_output: Output.object({
    schema: z.object({
      sentiment: z.enum(['positive', 'neutral', 'negative']),
      confidence: z.number().min(0).max(1),
      keywords: z.array(z.string()),
      summary: z.string(),
    }),
  }),
  stopWhen: stepCountIs(5),
});

const { experimental_output } = await sentimentAgent.generate({
  prompt: 'Analyze the sentiment of this review: "Great product, fast shipping!"',
});

console.log(experimental_output);
// { sentiment: 'positive', confidence: 0.95, keywords: ['great', 'fast'], summary: '...' }
```

### Complex Nested Schema

```ts
const analysisAgent = new Agent({
  model: openrouter.chat('openai/gpt-oss-120b:nitro'),
  experimental_output: Output.object({
    schema: z.object({
      document: z.object({
        title: z.string(),
        author: z.string().optional(),
        date: z.string().optional(),
      }),
      analysis: z.object({
        mainTopics: z.array(z.object({
          topic: z.string(),
          relevance: z.number().min(0).max(1),
        })),
        sentiment: z.enum(['positive', 'neutral', 'negative']),
        readability: z.enum(['easy', 'moderate', 'difficult']),
      }),
      recommendations: z.array(z.string()),
    }),
  }),
  stopWhen: stepCountIs(10),
});
```

## Execution Methods

### generate() - One-time Generation

```ts
const result = await myAgent.generate({
  prompt: 'What is the weather like in Tokyo?',
});

console.log(result.text);           // Final text response
console.log(result.steps);          // Array of steps taken
console.log(result.toolCalls);      // Tool calls made
console.log(result.toolResults);    // Results from tools
console.log(result.usage);          // Token usage statistics
```

### stream() - Streaming Response

```ts
const stream = myAgent.stream({
  prompt: 'Tell me a story about a robot',
});

// Stream text chunks
for await (const chunk of stream.textStream) {
  process.stdout.write(chunk);
}

// Or get full result after streaming
const result = await stream;
console.log(result.text);
```

### respond() - API Response for UI

```ts
// In API route (e.g., app/api/chat/route.ts)
import { validateUIMessages } from 'ai';

export async function POST(request: Request) {
  const { messages } = await request.json();

  return myAgent.respond({
    messages: await validateUIMessages({ messages }),
  });
}
```

## Type Safety

### Infer UIMessage Type

```ts
import {
  Experimental_Agent as Agent,
  Experimental_InferAgentUIMessage as InferAgentUIMessage,
} from 'ai';

const myAgent = new Agent({
  model: openrouter.chat('openai/gpt-oss-120b:nitro'),
  tools: {
    weather: weatherTool,
    search: searchTool,
  },
});

// Infer the UIMessage type
export type MyAgentUIMessage = InferAgentUIMessage<typeof myAgent>;
```

### Use in Client Components

```tsx
// components/chat.tsx
'use client';

import { useChat } from '@ai-sdk/react';
import type { MyAgentUIMessage } from '@/agents/my-agent';

export function Chat() {
  const { messages, input, handleInputChange, handleSubmit } = useChat<MyAgentUIMessage>();

  return (
    <div>
      {messages.map((message) => (
        <div key={message.id}>
          <strong>{message.role}:</strong>
          {message.content}
          {/* Full type safety for tool invocations */}
          {message.toolInvocations?.map((tool) => (
            <div key={tool.toolCallId}>
              Tool: {tool.toolName}
            </div>
          ))}
        </div>
      ))}
      <form onSubmit={handleSubmit}>
        <input value={input} onChange={handleInputChange} />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}
```

### Type-Safe Tool Results

```ts
// Define tools with explicit return types
const tools = {
  getUser: tool({
    description: 'Get user by ID',
    inputSchema: z.object({ id: z.string() }),
    execute: async ({ id }): Promise<{ name: string; email: string }> => {
      const user = await db.users.findById(id);
      return { name: user.name, email: user.email };
    },
  }),
} satisfies ToolSet;

// TypeScript knows the shape of tool results
type UserToolResult = Awaited<ReturnType<typeof tools.getUser.execute>>;
```
