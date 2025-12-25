---
name: ai-sdk-agents
description: Expert guidance for building AI agents using the Vercel AI SDK. Use this skill when building agents with tools, implementing agentic loops, creating workflow patterns (sequential, parallel, routing, orchestrator-worker, evaluator-optimizer), or configuring agent loop control (stopWhen, prepareStep). Triggers on requests involving AI SDK Agent class, tool definitions, multi-step agent workflows, or structured AI pipelines.
---

# AI SDK Agents

Build agents using the Vercel AI SDK's `Agent` class and core functions.

## Core Concepts

Agents combine three components:
- **LLM** - Processes input, decides actions
- **Tools** - Extend capabilities (APIs, files, databases)
- **Loop** - Orchestrates execution with context management and stopping conditions

## Setup

```ts
import { createOpenRouter } from '@openrouter/ai-sdk-provider';

const openrouter = createOpenRouter({
  apiKey: process.env.OPENROUTER_API_KEY,
});
```

## Agent Class

```ts
import { Experimental_Agent as Agent, stepCountIs, tool } from 'ai';
import { createOpenRouter } from '@openrouter/ai-sdk-provider';
import { z } from 'zod';

const openrouter = createOpenRouter({
  apiKey: process.env.OPENROUTER_API_KEY,
});

const agent = new Agent({
  model: openrouter.chat('openai/gpt-oss-120b:nitro'),
  system: 'You are a helpful assistant.',
  tools: {
    myTool: tool({
      description: 'Tool description',
      inputSchema: z.object({ param: z.string() }),
      execute: async ({ param }) => ({ result: param }),
    }),
  },
  stopWhen: stepCountIs(20),
});
```

### Execution Methods

```ts
// One-time generation
const result = await agent.generate({ prompt: 'Query' });
console.log(result.text, result.steps);

// Streaming
const stream = agent.stream({ prompt: 'Query' });
for await (const chunk of stream.textStream) { console.log(chunk); }

// API response for UI
return agent.respond({ messages: await validateUIMessages({ messages }) });
```

## Loop Control

### Stop Conditions

Default: `stepCountIs(1)`. Configure for multi-step:

```ts
import { stepCountIs, hasToolCall } from 'ai';

stopWhen: stepCountIs(20)  // Max 20 steps
stopWhen: [stepCountIs(20), hasToolCall('finalTool')]  // Any condition met
```

Custom condition:

```ts
const hasAnswer: StopCondition<typeof tools> = ({ steps }) =>
  steps.some(step => step.text?.includes('ANSWER:')) ?? false;
```

### prepareStep

Modify settings before each step:

```ts
prepareStep: async ({ stepNumber, messages, steps }) => {
  // Dynamic model selection
  if (stepNumber > 2) return { model: openrouter.chat('openai/gpt-oss-120b:nitro') };
  
  // Context management
  if (messages.length > 20) return {
    messages: [messages[0], ...messages.slice(-10)]
  };
  
  // Tool selection by phase
  if (stepNumber <= 2) return { activeTools: ['search'], toolChoice: 'required' };
  if (stepNumber <= 5) return { activeTools: ['analyze'] };
  return { activeTools: ['summarize'] };
}
```

## Configuration Options

| Option | Description |
|--------|-------------|
| `model` | OpenRouter model via `openrouter.chat('model-id')` |
| `system` | System prompt defining behavior |
| `tools` | Tool definitions object |
| `toolChoice` | `'auto'` (default), `'required'`, `'none'`, or `{ type: 'tool', toolName: 'name' }` |
| `experimental_output` | Structured output schema with `Output.object({ schema })` |
| `stopWhen` | Stop condition(s) |
| `prepareStep` | Pre-step callback for dynamic config |

## Structured Output

```ts
import { Output } from 'ai';

const agent = new Agent({
  model: openrouter.chat('openai/gpt-oss-120b:nitro'),
  experimental_output: Output.object({
    schema: z.object({
      sentiment: z.enum(['positive', 'neutral', 'negative']),
      summary: z.string(),
      keyPoints: z.array(z.string()),
    }),
  }),
  stopWhen: stepCountIs(10),
});

const { experimental_output: output } = await agent.generate({ prompt: '...' });
```

## Type Safety

```ts
import { Experimental_InferAgentUIMessage as InferAgentUIMessage } from 'ai';

export type MyAgentUIMessage = InferAgentUIMessage<typeof myAgent>;

// In client component
const { messages } = useChat<MyAgentUIMessage>();
```

## When to Use

- **Agent class**: Most use cases—reduces boilerplate, reusable, single config location
- **Core functions** (`generateText`, `streamText`): Complex structured workflows needing explicit control

## References

**[Building Agents](references/building-agents.md)** - Comprehensive Agent class guide: configuration, system prompts, tools, structured output, execution methods, type safety

**[Loop Control](references/loop-control.md)** - Execution control: `stopWhen` conditions, `prepareStep` callback, dynamic model selection, context management, tool selection, manual loops

**[Workflow Patterns](references/workflows.md)** - Structured patterns using core functions: sequential processing, routing, parallel processing, orchestrator-worker, evaluator-optimizer, combining patterns

## Manual Loop

For complete control:

```ts
import { generateText, ModelMessage } from 'ai';
import { createOpenRouter } from '@openrouter/ai-sdk-provider';

const openrouter = createOpenRouter({
  apiKey: process.env.OPENROUTER_API_KEY,
});

const messages: ModelMessage[] = [{ role: 'user', content: '...' }];
let step = 0;

while (step < 10) {
  const result = await generateText({
    model: openrouter.chat('openai/gpt-oss-120b:nitro'),
    messages,
    tools: { /* ... */ },
  });
  messages.push(...result.response.messages);
  if (result.text) break;
  step++;
}
```
