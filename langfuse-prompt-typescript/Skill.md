---
name: langfuse-prompt-typescript
description: "Manages LangFuse prompts in TypeScript: create, version, compile templates with variables, A/B testing with labels, integrate OpenAI SDK, link to traces, production caching."
---

# LangFuse Prompt Management (TypeScript)

Expert guide for managing prompts in LangFuse using TypeScript/JavaScript. Covers creating versioned prompts, compiling templates, A/B testing, and production patterns.

## When to Use This Skill

Use this skill when users ask to:
- Create or manage LangFuse prompts in TypeScript/JavaScript projects
- Version and deploy prompts with labels (production, staging)
- Compile prompt templates with variables
- Integrate LangFuse prompts with OpenAI or AI SDK
- Link prompts to traces for analytics
- Implement A/B testing or prompt experimentation

## Quick Start

**Prerequisites**: LangFuse account with API keys, Node.js project

### Installation

```bash
npm install @langfuse/client
```

### Initialize Client

```typescript
import { LangfuseClient } from "@langfuse/client";

const langfuse = new LangfuseClient({
  secretKey: process.env.LANGFUSE_SECRET_KEY,
  publicKey: process.env.LANGFUSE_PUBLIC_KEY,
  baseUrl: "https://cloud.langfuse.com"  // or self-hosted URL
});
```

## Creating Prompts

### Text Prompts

```typescript
await langfuse.prompt.create({
  name: "movie-critic",
  type: "text",
  prompt: "As a {{criticlevel}} critic, do you like {{movie}}?",
  labels: ["production"],
  config: {
    model: "gpt-4o",
    temperature: 0.7,
    max_tokens: 500
  }
});
```

### Chat Prompts

```typescript
await langfuse.prompt.create({
  name: "movie-critic-chat",
  type: "chat",
  prompt: [
    { role: "system", content: "You are an {{criticlevel}} movie critic" },
    { role: "user", content: "Do you like {{movie}}?" }
  ],
  labels: ["production"],
  config: {
    model: "gpt-4o",
    temperature: 0.7
  }
});
```

## Fetching & Compiling Prompts

### Fetch by Label or Version

```typescript
// Get production version (default)
const prompt = await langfuse.prompt.get("movie-critic");

// Get specific label
const stagingPrompt = await langfuse.prompt.get("movie-critic", {
  label: "staging"
});

// Get specific version
const v1Prompt = await langfuse.prompt.get("movie-critic", {
  version: 1
});

// Get latest version
const latestPrompt = await langfuse.prompt.get("movie-critic", {
  label: "latest"
});
```

### Compile with Variables

```typescript
// Text prompt compilation
const prompt = await langfuse.prompt.get("movie-critic");
const compiledText = prompt.compile({
  criticlevel: "expert",
  movie: "Dune 2"
});
// Result: "As an expert critic, do you like Dune 2?"

// Chat prompt compilation
const chatPrompt = await langfuse.prompt.get("movie-critic-chat");
const compiledMessages = chatPrompt.compile({
  criticlevel: "expert",
  movie: "Dune 2"
});
// Result: [
//   { role: "system", content: "You are an expert movie critic" },
//   { role: "user", content: "Do you like Dune 2?" }
// ]
```

### Chat Prompts with Message Placeholders

```typescript
// Inject message arrays into chat prompts
const compiledPrompt = chatPrompt.compile(
  // Variables
  { criticlevel: "expert" },
  // Placeholders (message arrays)
  {
    chat_history: [
      { role: "user", content: "I love Ron Fricke movies" },
      { role: "assistant", content: "Great taste!" }
    ]
  }
);
```

## Version Control

### Update Labels

```typescript
// Promote version 2 to production
await langfuse.prompt.update({
  name: "movie-critic",
  version: 2,
  newLabels: ["production"]
});

// Multi-label deployment
await langfuse.prompt.update({
  name: "movie-critic",
  version: 3,
  newLabels: ["production", "team-a", "experiment-1"]
});
```

### A/B Testing Pattern

```typescript
async function getPromptWithABTest(promptName: string) {
  const useVariantB = Math.random() < 0.5;

  const prompt = await langfuse.prompt.get(promptName, {
    label: useVariantB ? "prod-variant-b" : "prod-variant-a"
  });

  return { prompt, variant: useVariantB ? "B" : "A" };
}

// Usage
const { prompt, variant } = await getPromptWithABTest("movie-critic");
console.log(`Using variant ${variant}`);
```

## Integration with OpenAI

### Basic OpenAI Usage

```typescript
import { OpenAI } from "openai";

const prompt = await langfuse.prompt.get("movie-critic");
const openai = new OpenAI();

const response = await openai.chat.completions.create({
  model: prompt.config.model || "gpt-4o",
  messages: prompt.compile({ criticlevel: "expert", movie: "Dune 2" }) as any,
  temperature: prompt.config.temperature,
});
```

### With observeOpenAI (Links to Trace)

```typescript
import { observeOpenAI } from "@langfuse/openai";

const prompt = await langfuse.prompt.get("movie-critic-chat");

const response = await observeOpenAI(new OpenAI(), {
  langfusePrompt: prompt,  // Automatically links prompt to trace
}).chat.completions.create({
  model: "gpt-4o",
  messages: prompt.compile({
    criticlevel: "expert",
    movie: "Dune 2"
  }) as OpenAI.ChatCompletionMessageParam[],
});
```

## Linking Prompts to Traces

### Manual Generation Link

```typescript
import { startObservation } from "@langfuse/tracing";

const prompt = await langfuse.prompt.get("movie-critic");

const generation = startObservation(
  "llm-call",
  { prompt },
  { asType: "generation" }
);

// Your LLM call here
generation.update({ output: "Movie review..." });
generation.end();
```

### Context Manager Pattern

```typescript
import { startActiveObservation, updateActiveObservation } from "@langfuse/tracing";

await startActiveObservation("llm-generation", async (generation) => {
  const prompt = await langfuse.prompt.get("movie-critic");

  generation.update({ prompt });

  // Your LLM call
  const output = await callLLM(prompt.compile({ movie: "Dune 2" }));

  generation.update({ output });
}, { asType: "generation" });
```

## Production Patterns

### Caching (Default: 60 seconds)

```typescript
// Default caching (60s TTL)
const prompt = await langfuse.prompt.get("movie-critic");

// Custom cache TTL
const prompt = await langfuse.prompt.get("movie-critic", {
  cacheTtlSeconds: 300  // 5 minutes
});

// Disable caching (dev environments)
const prompt = await langfuse.prompt.get("movie-critic", {
  cacheTtlSeconds: 0,
  label: "latest"  // Always get freshest version
});
```

### Fallback Prompts (High Availability)

```typescript
// Text prompt with fallback
const prompt = await langfuse.prompt.get("movie-critic", {
  fallback: "Do you like {{movie}}?"
});

// Chat prompt with fallback
const chatPrompt = await langfuse.prompt.get("movie-critic-chat", {
  type: "chat",
  fallback: [
    { role: "system", content: "You are an expert on {{movie}}" }
  ]
});

// Check if fallback was used
if (prompt.isFallback) {
  console.log("⚠️ Using fallback prompt");
}
```

### Pre-fetch on Startup

```typescript
import express from "express";

const app = express();
const langfuse = new LangfuseClient();

async function warmupPrompts() {
  try {
    await langfuse.prompt.get("movie-critic");
    await langfuse.prompt.get("movie-critic-chat");
    console.log("✅ Prompts cached successfully");
  } catch (error) {
    console.error("❌ Failed to fetch prompts:", error);
    process.exit(1);
  }
}

warmupPrompts().then(() => {
  app.listen(3000, () => console.log("Server ready"));
});
```

## Prompt Attributes

```typescript
const prompt = await langfuse.prompt.get("movie-critic");

prompt.prompt       // Raw template (string or message array)
prompt.config       // Config object (model params, etc.)
prompt.name         // Prompt name
prompt.version      // Version number (1, 2, 3...)
prompt.labels       // Array of labels ["production", "team-a"]
prompt.isFallback   // Boolean (true if fallback was used)
```

## Getting More Information

When you need detailed documentation, use these MCP tools available to Claude:

- **Search docs**: `mcp__langfuse-docs__searchLangfuseDocs` with query like "prompt management TypeScript versioning"
- **Get specific page**: `mcp__langfuse-docs__getLangfuseDocsPage` with path like "/docs/prompt-management/get-started"
- **Get overview**: `mcp__langfuse-docs__getLangfuseOverview` for high-level structure

## Key Reminders

- **Labels vs Versions**: Labels are pointers (production, staging), versions are immutable (1, 2, 3)
- **Default label**: `production` label is served when no label specified
- **`latest` label**: Automatically maintained, always points to newest version
- **Caching**: 60s default TTL is production-ready, rarely needs tuning
- **Fallbacks**: Optional - LangFuse API has multi-layer caching for high availability
- **Type casting**: Chat messages may need casting for OpenAI SDK compatibility
- **Tracing integration**: Use `langfusePrompt` parameter with `observeOpenAI` for automatic linking

## Best Practices

1. **Use labels for environments**: `production`, `staging`, `dev`
2. **Version incrementally**: Create new versions, promote with labels
3. **Cache warmup**: Pre-fetch prompts on app startup for serverless
4. **Link to traces**: Enables analytics by prompt version
5. **A/B testing**: Use multiple labels pointing to different versions
6. **Config in prompts**: Store model parameters in `config` field for consistency
