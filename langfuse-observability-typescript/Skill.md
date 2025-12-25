---
name: langfuse-observability-typescript
description: "Integrates Langfuse observability (TypeScript SDK v4) into Node.js/Next.js LLM applications. Covers OpenAI SDK, Vercel AI SDK, and LangChain.js tracing with OpenTelemetry. Use when setting up Langfuse tracing, monitoring LLM calls, tracking costs/tokens, or debugging LLM apps in TypeScript/JavaScript. Triggers: langfuse, tracing, observability, llm monitoring, opentelemetry, vercel ai sdk telemetry, langchain callback."
---

# Langfuse TypeScript SDK v4 Observability

Built on OpenTelemetry for robust context propagation and automatic tracing.

**Requirements**: Self-hosted Langfuse requires platform version >= 3.95.0

## Quick Start

### Installation

```bash
npm install @langfuse/tracing @langfuse/otel @opentelemetry/sdk-node
```

### Environment Variables

```bash
LANGFUSE_SECRET_KEY="sk-lf-..."
LANGFUSE_PUBLIC_KEY="pk-lf-..."
LANGFUSE_BASE_URL="https://cloud.langfuse.com"  # EU region
# LANGFUSE_BASE_URL="https://us.cloud.langfuse.com"  # US region
```

### Initialize OpenTelemetry

Create `instrumentation.ts`:

```typescript
import { NodeSDK } from "@opentelemetry/sdk-node";
import { LangfuseSpanProcessor } from "@langfuse/otel";

export const langfuseSpanProcessor = new LangfuseSpanProcessor();

const sdk = new NodeSDK({
  spanProcessors: [langfuseSpanProcessor],
});

sdk.start();
```

Import instrumentation first in your entry file:

```typescript
import "./instrumentation"; // Must be first import
```

## OpenAI Integration

```bash
npm install @langfuse/openai openai
```

```typescript
import OpenAI from "openai";
import { observeOpenAI } from "@langfuse/openai";

const openai = new OpenAI();

const tracedOpenAI = observeOpenAI(openai, {
  traceName: "openai-chat",
  sessionId: "session-123",
  userId: "user-abc",
  tags: ["production"],
});

const completion = await tracedOpenAI.chat.completions.create({
  model: "gpt-4o",
  messages: [{ role: "user", content: "Hello" }],
});
```

## Vercel AI SDK Integration

```bash
npm install ai @ai-sdk/openai @langfuse/tracing @langfuse/otel @opentelemetry/sdk-node
```

### Basic Usage

```typescript
import { generateText } from "ai";
import { openai } from "@ai-sdk/openai";

const { text } = await generateText({
  model: openai("gpt-4o"),
  prompt: "What is OpenTelemetry?",
  experimental_telemetry: {
    isEnabled: true,
    functionId: "my-function",
    metadata: {
      sessionId: "session-123",
      userId: "user-abc",
      tags: ["vercel-ai"],
    },
  },
});
```

### Next.js Route Handler with Streaming

**instrumentation.ts** (project root):

```typescript
import { NodeSDK } from "@opentelemetry/sdk-node";
import { LangfuseSpanProcessor, ShouldExportSpan } from "@langfuse/otel";

const shouldExportSpan: ShouldExportSpan = ({ otelSpan }) => {
  return otelSpan.instrumentationScope.name !== "next.js";
};

export const langfuseSpanProcessor = new LangfuseSpanProcessor({ shouldExportSpan });

const sdk = new NodeSDK({
  spanProcessors: [langfuseSpanProcessor],
});

sdk.start();
```

**app/api/chat/route.ts**:

```typescript
import { streamText } from "ai";
import { openai } from "@ai-sdk/openai";
import { after } from "next/server";
import { langfuseSpanProcessor } from "@/instrumentation";

export async function POST(req: Request) {
  const { messages, chatId, userId } = await req.json();

  const result = streamText({
    model: openai("gpt-4o"),
    messages,
    experimental_telemetry: {
      isEnabled: true,
      metadata: { sessionId: chatId, userId },
    },
  });

  after(async () => await langfuseSpanProcessor.forceFlush());

  return result.toDataStreamResponse();
}
```

## LangChain.js Integration

```bash
npm install @langfuse/core @langfuse/langchain @langfuse/otel @opentelemetry/sdk-node
```

Initialize OpenTelemetry first, then:

```typescript
import { CallbackHandler } from "@langfuse/langchain";
import { ChatOpenAI } from "@langchain/openai";
import { ChatPromptTemplate } from "@langchain/core/prompts";

const langfuseHandler = new CallbackHandler({
  sessionId: "session-123",
  userId: "user-abc",
  tags: ["langchain"],
});

const llm = new ChatOpenAI({ model: "gpt-4o" });
const prompt = ChatPromptTemplate.fromTemplate("Answer: {question}");
const chain = prompt.pipe(llm);

await chain.invoke(
  { question: "What is Langfuse?" },
  { callbacks: [langfuseHandler] }
);
```

## Manual Tracing

### Context Manager (Recommended)

```typescript
import { startActiveObservation, propagateAttributes } from "@langfuse/tracing";

await startActiveObservation("user-request", async (span) => {
  span.update({ input: { query: "Capital of France?" } });

  await propagateAttributes(
    { userId: "user-123", sessionId: "session-abc" },
    async () => {
      // Nested observations inherit userId/sessionId
    }
  );

  span.update({ output: "Paris" });
});
```

### Observe Wrapper

```typescript
import { observe } from "@langfuse/tracing";

async function fetchData(source: string) {
  return { data: `from ${source}` };
}

const tracedFetch = observe(fetchData, { name: "fetch-data", asType: "span" });
await tracedFetch("api");
```

### Manual Observations

```typescript
import { startObservation } from "@langfuse/tracing";

const span = startObservation("process-request", { input: "data" });
const gen = span.startObservation("llm-call", { model: "gpt-4o" }, { asType: "generation" });
gen.update({ output: "response" }).end();
span.end(); // Required for manual observations
```

### Update Trace Attributes

```typescript
import { startActiveObservation } from "@langfuse/tracing";

await startActiveObservation("workflow", async (span) => {
  span.updateTrace({
    userId: "user-123",
    sessionId: "session-abc",
    tags: ["production"],
    metadata: { env: "prod" },
  });
});
```

## Serverless Best Practices

### Immediate Export Mode

For AWS Lambda, Vercel, Cloudflare Workers:

```typescript
const langfuseSpanProcessor = new LangfuseSpanProcessor({
  exportMode: "immediate",  // No batching
});
```

### Manual Flush

Always flush before handler exits:

```typescript
import { langfuseSpanProcessor } from "./instrumentation";

export async function handler(event) {
  // Your logic

  await langfuseSpanProcessor.forceFlush();
  return response;
}
```

## Common Gotchas

1. **LangChain > 0.3.0**: Set `LANGCHAIN_CALLBACKS_BACKGROUND=false` for serverless
2. **Next.js**: Use `NodeSDK` from `@opentelemetry/sdk-node`, not `@vercel/otel`
3. **Streaming**: Use `after()` from `next/server` to flush after response
4. **Manual spans**: Always call `.end()` on manually created observations
5. **Import order**: Instrumentation file must be imported before other modules

## Key Reminders

- SDK v4 is OpenTelemetry-based (breaking changes from v3)
- Use `span.update()` to modify observations
- Use `span.updateTrace()` for trace-level attributes
- Use `propagateAttributes()` to pass userId/sessionId to child observations
- Always `forceFlush()` in serverless environments
