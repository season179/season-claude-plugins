---
name: exa-search
description: Expert integration with Exa's AI-powered semantic search API. Use when building web search, RAG systems, content retrieval, or research features with TypeScript/Bun, React, and Next.js. Triggers on requests involving Exa API, Exa SDK, semantic web search, AI search tools, search and contents retrieval, find similar links, research automation, or Vercel AI SDK web search integration. Covers exa-js SDK, @exalabs/ai-sdk, search types (neural, auto, deep), content extraction, livecrawling, highlights, summaries, and structured research tasks.
---

# Exa Search Integration

Exa is an AI-powered semantic search API that retrieves high-quality web content for AI applications. It uses embeddings-based search to find content by meaning rather than keywords.

## Tech Stack

- **Runtime**: Bun
- **Language**: TypeScript
- **Framework**: Next.js with React
- **AI Integration**: Vercel AI SDK

## Installation

```bash
# Core SDK for direct API access
bun add exa-js

# Vercel AI SDK integration (recommended for AI apps)
bun add @exalabs/ai-sdk
```

## Environment Setup

```bash
# .env.local
EXA_API_KEY=your-api-key-here
```

Get API key from https://dashboard.exa.ai/api-keys

## Quick Start Patterns

### Pattern 1: Vercel AI SDK Integration (Recommended)

```typescript
import { generateText, stepCountIs } from "ai";
import { webSearch } from "@exalabs/ai-sdk";
import { anthropic } from "@ai-sdk/anthropic";

const { text } = await generateText({
  model: anthropic("claude-sonnet-4-20250514"),
  prompt: "What are the latest developments in AI?",
  system: "Use web search to find current information.",
  tools: {
    webSearch: webSearch({
      type: "auto",
      numResults: 5,
      contents: {
        text: { maxCharacters: 2000 },
        livecrawl: "fallback",
      },
    }),
  },
  stopWhen: stepCountIs(3),
});
```

### Pattern 2: Direct SDK Usage

```typescript
import Exa from "exa-js";

const exa = new Exa(process.env.EXA_API_KEY);

const results = await exa.searchAndContents("AI startups in healthcare", {
  type: "auto",
  numResults: 10,
  text: true,
  highlights: true,
  category: "company",
});
```

### Pattern 3: RAG Context Retrieval

```typescript
const results = await exa.searchAndContents("machine learning best practices", {
  context: { maxCharacters: 10000 },
  numResults: 5,
  category: "research paper",
});
```

## Search Types

| Type | Use Case |
|------|----------|
| `auto` | Default - intelligent hybrid of neural + keyword |
| `neural` | Semantic meaning-based search (max 100 results) |
| `fast` | Quick keyword-based search |
| `deep` | Multi-query expansion with thorough results |

## Categories

Focus search on specific content types: `company`, `research paper`, `news`, `github`, `pdf`, `tweet`, `personal site`, `financial report`, `people`, `linkedin profile`

## Content Options

```typescript
await exa.searchAndContents(query, {
  text: true, // or { maxCharacters: 1000, includeHtmlTags: false }
  highlights: true, // or { numSentences: 3, highlightsPerUrl: 2 }
  context: true, // or { maxCharacters: 10000 } - RAG optimized
  summary: true, // or { schema: jsonSchema } for structured extraction
});
```

## Livecrawling Options

- `never` - Only cached content
- `fallback` - Livecrawl if cache unavailable (default)
- `always` - Always fetch fresh
- `preferred` - Prefer fresh when possible

## Filtering

```typescript
await exa.searchAndContents(query, {
  includeDomains: ["arxiv.org", "github.com"],
  excludeDomains: ["reddit.com"],
  startPublishedDate: "2024-01-01",
  endPublishedDate: "2024-12-31",
  includeText: ["artificial intelligence"], // max 1 string, 5 words
  excludeText: ["advertisement"],
});
```

## Limitations & Gotchas

### Domain filtering does NOT support wildcards

```typescript
// ✅ Works - specific domains only
includeDomains: ["kemenkeu.go.id", "bappenas.go.id"]

// ❌ Does NOT work - no wildcard patterns
includeDomains: ["*.go.id"]  // Will not match subdomains
```

**Workaround for TLD filtering** (e.g., all `.go.id` domains):
1. List specific domains explicitly
2. Post-filter results in code:
   ```typescript
   const results = await exa.searchAndContents(query, { numResults: 50 });
   const filtered = results.results.filter(r => r.url.includes('.go.id'));
   ```

### Text filtering constraints
- `includeText`/`excludeText`: Only 1 string allowed, max 5 words
- `excludeText` checks first 1000 words only

### Result limits
- `neural` search: max 100 results
- Contact sales for higher limits

## Key Methods

| Method | Purpose |
|--------|---------|
| `search()` | Get links only |
| `searchAndContents()` | Links + content |
| `findSimilar()` | Similar pages to URL |
| `findSimilarAndContents()` | Similar + content |
| `getContents()` | Content for URLs |
| `answer()` | Direct answer with citations |
| `streamAnswer()` | Stream answer |
| `research.create()` | Async research task |

## Reference Documentation

- **TypeScript SDK**: See [references/typescript-sdk.md](references/typescript-sdk.md)
- **Vercel AI SDK**: See [references/vercel-ai-sdk.md](references/vercel-ai-sdk.md)
- **Research API**: See [references/research-api.md](references/research-api.md)

## Common Patterns

### Next.js API Route

```typescript
// app/api/search/route.ts
import Exa from "exa-js";
import { NextResponse } from "next/server";

const exa = new Exa(process.env.EXA_API_KEY);

export async function POST(request: Request) {
  const { query } = await request.json();
  
  const results = await exa.searchAndContents(query, {
    type: "auto",
    numResults: 5,
    text: { maxCharacters: 500 },
    highlights: true,
  });
  
  return NextResponse.json(results);
}
```

### Streaming Chat with Search

```typescript
import { streamText, stepCountIs } from "ai";
import { webSearch } from "@exalabs/ai-sdk";

export async function POST(request: Request) {
  const { messages } = await request.json();
  
  const result = streamText({
    model: anthropic("claude-sonnet-4-20250514"),
    messages,
    tools: {
      webSearch: webSearch({
        type: "auto",
        numResults: 5,
        contents: { text: { maxCharacters: 1500 }, summary: true },
      }),
    },
    stopWhen: stepCountIs(3),
  });
  
  return result.toDataStreamResponse();
}
```

### Structured Data Extraction

```typescript
const companySchema = {
  type: "object",
  properties: {
    name: { type: "string" },
    industry: { type: "string" },
    foundedYear: { type: "number" },
    keyProducts: { type: "array", items: { type: "string" } },
  },
  required: ["name", "industry"],
};

const results = await exa.searchAndContents("OpenAI company", {
  summary: { schema: companySchema },
  category: "company",
  numResults: 3,
});

const data = JSON.parse(results.results[0].summary);
```

## Performance Tips

1. Use appropriate `numResults` (fewer = faster)
2. Limit response size with `text: { maxCharacters: N }`
3. Use `highlights` instead of full `text` when excerpts suffice
4. Use `context` for RAG - optimized for LLM consumption
5. Use `category` to focus search and improve relevance
6. Use `livecrawl: "fallback"` unless fresh content critical
