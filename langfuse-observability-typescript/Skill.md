---
name: langfuse-observability-typescript
description: "Integrates LangFuse Observability (TypeScript SDK v4) into OpenAI, Vercel AI SDK, and LangChain.js. Tracing, monitoring, serverless patterns, cost tracking for Node.js/Next.js LLM apps."
---

# LangFuse TypeScript Observability

Expert guide for integrating LangFuse observability into TypeScript/JavaScript applications. SDK v4 is built on OpenTelemetry for robust context management and automatic tracing.

## When to Use This Skill

Use this skill when users ask to:
- Set up LangFuse observability/tracing in TypeScript/JavaScript/Node.js projects
- Integrate LangFuse with OpenAI, Vercel AI SDK, or LangChain.js
- Trace and monitor LLM calls in Next.js or serverless environments
- Track costs, tokens, and performance of TypeScript LLM applications

Also useful when debugging or optimizing LLM applications in production.

## Prerequisites

- Node.js >= 20 (required for `@langfuse/otel`)
- LangFuse account with API keys (cloud or self-hosted)

## Quick Start Setup

### 1. Installation

```bash
npm install @langfuse/tracing @langfuse/otel @opentelemetry/sdk-node
```

### 2. Environment Variables

```bash
LANGFUSE_SECRET_KEY="sk-lf-..."
LANGFUSE_PUBLIC_KEY="pk-lf-..."
LANGFUSE_BASE_URL="https://cloud.langfuse.com"  # EU region
# LANGFUSE_BASE_URL="https://us.cloud.langfuse.com"  # US region
```

### 3. Initialize OpenTelemetry

Create `instrumentation.ts`:

```typescript
import { NodeSDK } from "@opentelemetry/sdk-node";
import { LangfuseSpanProcessor } from "@langfuse/otel";

const sdk = new NodeSDK({
  spanProcessors: [new LangfuseSpanProcessor()],
});

sdk.start();
```

## OpenAI Integration

### Installation

```bash
npm install @langfuse/openai openai
```

### Usage

```typescript
import { OpenAI } from "openai";
import { observeOpenAI } from "@langfuse/openai";

const openai = new OpenAI();

// Wrap with Langfuse observability
const tracedOpenAI = observeOpenAI(openai, {
  traceName: "openai-chat",
  sessionId: "user-session-123",
  userId: "user-abc",
  tags: ["production"],
});

// Use normally - automatically traced
const completion = await tracedOpenAI.chat.completions.create({
  model: "gpt-4",
  messages: [{ role: "user", content: "What is OpenTelemetry?" }],
});
```

## Vercel AI SDK Integration

### Next.js Setup

**instrumentation.ts** (project root):

```typescript
import { LangfuseSpanProcessor, ShouldExportSpan } from "@langfuse/otel";
import { NodeTracerProvider } from "@opentelemetry/sdk-trace-node";

// Optional: filter Next.js internal spans
const shouldExportSpan: ShouldExportSpan = (span) => {
  return span.otelSpan.instrumentationScope.name !== "next.js";
};

export const langfuseSpanProcessor = new LangfuseSpanProcessor({
  shouldExportSpan,
});

const tracerProvider = new NodeTracerProvider({
  spanProcessors: [langfuseSpanProcessor],
});

tracerProvider.register();
```

### Route Handler with Streaming

**app/api/chat/route.ts**:

```typescript
import { streamText } from "ai";
import { after } from "next/server";
import { openai } from "@ai-sdk/openai";
import { observe, updateActiveObservation, updateActiveTrace } from "@langfuse/tracing";
import { trace } from "@opentelemetry/api";
import { langfuseSpanProcessor } from "@/instrumentation";

const handler = async (req: Request) => {
  const { messages, chatId, userId } = await req.json();

  const inputText = messages[messages.length - 1].content;

  updateActiveObservation({ input: inputText });
  updateActiveTrace({
    name: "chat-completion",
    sessionId: chatId,
    userId,
  });

  const result = streamText({
    model: openai("gpt-4o"),
    messages,
    experimental_telemetry: { isEnabled: true },  // Enable Vercel AI SDK tracing
    onFinish: async (result) => {
      updateActiveObservation({ output: result.text });
      updateActiveTrace({ output: result.text });
      trace.getActiveSpan()?.end();
    },
  });

  // Serverless flush (Vercel)
  after(async () => await langfuseSpanProcessor.forceFlush());

  return result.toDataStreamResponse();
};

export const POST = observe(handler, {
  name: "chat-handler",
  endOnExit: false,  // Important for streaming
});
```

## LangChain.js Integration

### Installation

```bash
npm install @langfuse/langchain @langfuse/otel @opentelemetry/sdk-node
```

### Setup

First, initialize OpenTelemetry (as shown in Quick Start), then:

```typescript
import { CallbackHandler } from "@langfuse/langchain";
import { ChatOpenAI } from "@langchain/openai";
import { ChatPromptTemplate } from "@langchain/core/prompts";

const langfuseHandler = new CallbackHandler({
  sessionId: "user-session-123",
  userId: "user-abc",
  tags: ["langchain"],
});

const llm = new ChatOpenAI({ model: "gpt-4" });
const prompt = ChatPromptTemplate.fromTemplate("Answer: {question}");
const chain = prompt.pipe(llm);

await chain.invoke(
  { question: "What is LangFuse?" },
  { callbacks: [langfuseHandler] }
);
```

## Manual Tracing Patterns

### Context Manager (Recommended)

```typescript
import { startActiveObservation } from "@langfuse/tracing";

await startActiveObservation("user-request", async (span) => {
  span.update({
    input: { query: "What is the capital of France?" },
    userId: "user-123",
  });

  // Nested operations automatically attached
  const result = await processQuery("France");

  span.update({ output: result });
});
```

### Decorator Wrapper

```typescript
import { observe, updateActiveObservation } from "@langfuse/tracing";

async function fetchData(source: string) {
  updateActiveObservation({ metadata: { source } });
  return { data: `data from ${source}` };
}

const tracedFetch = observe(fetchData, {
  name: "fetch-data",
  asType: "span",
});

await tracedFetch("api");
```

## Serverless Best Practices

### Immediate Export Mode (Recommended)

For AWS Lambda, Vercel, Cloudflare Workers:

```typescript
import { LangfuseSpanProcessor } from "@langfuse/otel";

const langfuseSpanProcessor = new LangfuseSpanProcessor({
  exportMode: "immediate",  // No batching, immediate export
});
```

### Manual Flush

If using default batching mode, flush before handler exits:

```typescript
import { langfuseSpanProcessor } from "./instrumentation";

export async function handler(event) {
  // Your logic here

  // Flush before exit
  await langfuseSpanProcessor.forceFlush();

  return response;
}
```

## Getting More Information

When you need detailed documentation, use these MCP tools available to Claude:

- **Search docs**: `mcp__langfuse-docs__searchLangfuseDocs` with query like "TypeScript SDK v4 advanced configuration"
- **Get specific page**: `mcp__langfuse-docs__getLangfuseDocsPage` with path like "/docs/observability/sdk/typescript/setup"
- **Get overview**: `mcp__langfuse-docs__getLangfuseOverview` for high-level structure

## Key Reminders

- **SDK v4** is OpenTelemetry-based (different from v3)
- **Next.js**: Use `NodeTracerProvider`, NOT `@vercel/otel`'s `registerOTel`
- **Serverless**: Use `exportMode: "immediate"` or manual `forceFlush()`
- **Streaming**: Set `endOnExit: false` in `observe()` wrapper
- **Environment**: Use environment variables for API keys, not hardcoded values

## Common Gotchas

1. **LangChain v0.3.0+**: Callbacks run in background. In serverless, set:
   ```bash
   LANGCHAIN_CALLBACKS_BACKGROUND=false
   ```

2. **Next.js compatibility**: Don't mix `@vercel/otel` with manual OpenTelemetry setup

3. **Flushing**: Always flush in serverless before response is returned
