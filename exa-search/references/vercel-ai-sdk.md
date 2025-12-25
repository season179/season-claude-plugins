# Vercel AI SDK Integration

Complete reference for the `@exalabs/ai-sdk` package.

## Table of Contents
- [Installation](#installation)
- [Quick Start](#quick-start)
- [webSearch Function](#websearch-function)
- [Configuration Options](#configuration-options)
- [Usage Patterns](#usage-patterns)
- [TypeScript Types](#typescript-types)

## Installation

```bash
bun add @exalabs/ai-sdk ai
```

## Quick Start

```typescript
import { generateText, stepCountIs } from "ai";
import { webSearch } from "@exalabs/ai-sdk";
import { anthropic } from "@ai-sdk/anthropic";

const { text } = await generateText({
  model: anthropic("claude-sonnet-4-20250514"),
  prompt: "What are the latest AI developments?",
  system: "Use web search to find current information.",
  tools: {
    webSearch: webSearch(),
  },
  stopWhen: stepCountIs(3),
});
```

## webSearch Function

The `webSearch()` function creates a tool compatible with Vercel AI SDK.

### Default Behavior

When called with no arguments, `webSearch()` uses these defaults:
- Type: `auto` (intelligent hybrid search)
- Results: `10`
- Text: `3000 characters per result`
- Livecrawl: `fallback`

### Environment Variable

The package automatically reads `EXA_API_KEY` from environment variables.

```bash
# .env.local
EXA_API_KEY=your-api-key-here
```

## Configuration Options

```typescript
webSearch({
  // Search Type
  type: "auto",  // "auto" | "neural" | "fast" | "deep"
  
  // Category Focus
  category: "news",  // "company" | "research paper" | "news" | "pdf" |
                     // "github" | "personal site" | "linkedin profile" |
                     // "financial report" | "people"
  
  // Result Count
  numResults: 10,
  
  // Domain Filtering
  includeDomains: ["linkedin.com", "github.com"],
  excludeDomains: ["wikipedia.com"],
  
  // Date Filtering (ISO 8601)
  startPublishedDate: "2025-01-01T00:00:00.000Z",
  endPublishedDate: "2025-12-31T23:59:59.999Z",
  startCrawlDate: "2025-01-01T00:00:00.000Z",
  endCrawlDate: "2025-12-31T23:59:59.999Z",
  
  // Text Filtering
  includeText: ["AI"],     // Must contain (1 string, 5 words max)
  excludeText: ["spam"],   // Must not contain
  
  // Location
  userLocation: "US",      // Two-letter country code
  
  // Content Options
  contents: {
    text: {
      maxCharacters: 1000,
      includeHtmlTags: false,
    },
    summary: {
      query: "Main points",
    },
    livecrawl: "fallback",  // "never" | "fallback" | "always" | "preferred"
    livecrawlTimeout: 10000,
    subpages: 5,
    subpageTarget: "about",
    extras: {
      links: 5,
      imageLinks: 3,
    },
  },
});
```

## Usage Patterns

### generateText with Web Search

```typescript
import { generateText, stepCountIs } from "ai";
import { webSearch } from "@exalabs/ai-sdk";
import { openai } from "@ai-sdk/openai";

const { text, steps } = await generateText({
  model: openai("gpt-4o"),
  prompt: "Find the top AI companies in Europe founded after 2018",
  tools: {
    webSearch: webSearch({
      type: "auto",
      numResults: 6,
      category: "company",
      contents: {
        text: { maxCharacters: 1000 },
        livecrawl: "preferred",
        summary: true,
      },
    }),
  },
  stopWhen: stepCountIs(5),
});
```

### streamText with Web Search

```typescript
import { streamText, stepCountIs } from "ai";
import { webSearch } from "@exalabs/ai-sdk";

// Next.js API Route
export async function POST(request: Request) {
  const { messages } = await request.json();
  
  const result = streamText({
    model: anthropic("claude-sonnet-4-20250514"),
    messages,
    tools: {
      webSearch: webSearch({
        numResults: 5,
        contents: {
          text: { maxCharacters: 2000 },
        },
      }),
    },
    stopWhen: stepCountIs(3),
  });
  
  return result.toDataStreamResponse();
}
```

### With Multiple Tools

```typescript
import { generateText, stepCountIs, tool } from "ai";
import { webSearch } from "@exalabs/ai-sdk";
import { z } from "zod";

const { text } = await generateText({
  model: anthropic("claude-sonnet-4-20250514"),
  prompt: "Research AI companies and summarize findings",
  tools: {
    webSearch: webSearch({ category: "company" }),
    summarize: tool({
      description: "Summarize the search results",
      parameters: z.object({
        content: z.string(),
      }),
      execute: async ({ content }) => {
        return `Summary: ${content.slice(0, 500)}...`;
      },
    }),
  },
  stopWhen: stepCountIs(5),
});
```

### Research-Focused Search

```typescript
const { text } = await generateText({
  model: anthropic("claude-sonnet-4-20250514"),
  prompt: "Find recent research on transformer architectures",
  tools: {
    webSearch: webSearch({
      category: "research paper",
      includeDomains: ["arxiv.org", "openreview.net"],
      startPublishedDate: "2024-01-01",
      numResults: 10,
      contents: {
        text: { maxCharacters: 3000 },
        highlights: true,
      },
    }),
  },
  stopWhen: stepCountIs(3),
});
```

### News Monitoring

```typescript
const { text } = await generateText({
  model: anthropic("claude-sonnet-4-20250514"),
  prompt: "What are the latest developments in AI regulation?",
  tools: {
    webSearch: webSearch({
      category: "news",
      startPublishedDate: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(),
      numResults: 8,
      contents: {
        text: { maxCharacters: 1500 },
        livecrawl: "always",
      },
    }),
  },
  stopWhen: stepCountIs(3),
});
```

## TypeScript Types

```typescript
import { webSearch, ExaSearchConfig, ExaSearchResult } from "@exalabs/ai-sdk";

// Configuration type
interface ExaSearchConfig {
  type?: "auto" | "neural" | "fast" | "deep";
  category?: string;
  numResults?: number;
  includeDomains?: string[];
  excludeDomains?: string[];
  startPublishedDate?: string;
  endPublishedDate?: string;
  startCrawlDate?: string;
  endCrawlDate?: string;
  includeText?: string[];
  excludeText?: string[];
  userLocation?: string;
  contents?: {
    text?: boolean | { maxCharacters?: number; includeHtmlTags?: boolean };
    summary?: boolean | { query?: string };
    livecrawl?: "never" | "fallback" | "always" | "preferred";
    livecrawlTimeout?: number;
    subpages?: number;
    subpageTarget?: string;
    extras?: {
      links?: number;
      imageLinks?: number;
    };
  };
}

// Usage with types
const config: ExaSearchConfig = {
  numResults: 10,
  type: "auto",
  contents: {
    text: { maxCharacters: 2000 },
    livecrawl: "fallback",
  },
};

const search = webSearch(config);
```

## stepCountIs Helper

The `stopWhen: stepCountIs(n)` parameter controls how many tool call iterations are allowed:

```typescript
import { stepCountIs } from "ai";

// Allow up to 3 steps (search → process → respond)
stopWhen: stepCountIs(3)

// For complex research, allow more steps
stopWhen: stepCountIs(5)
```

This is important because web search tools require multiple steps: the LLM first calls the search tool, then processes results in subsequent steps.
