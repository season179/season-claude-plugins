---
name: using-tavily-search
description: Implements Tavily search, extract, crawl, and map APIs for AI-powered web search and content extraction. Use when building LLM search tools, RAG pipelines, web scraping, site crawlers, or content extraction features. Triggers on Tavily, @tavily/core, @tavily/ai-sdk, agentic search, web search API, or URL content extraction. Tech stack is Bun, TypeScript, Vercel AI SDK v5, Next.js.
---

# Tavily Search

## Installation

```bash
bun add @tavily/core        # Core SDK
bun add @tavily/ai-sdk      # AI SDK v5 tools
```

Set `TAVILY_API_KEY` environment variable.

## Quick Start

```typescript
import { tavily } from "@tavily/core";
const tvly = tavily({ apiKey: process.env.TAVILY_API_KEY });

// Search
const results = await tvly.search("query", { searchDepth: "advanced" });

// Extract content from URLs
const content = await tvly.extract(["https://example.com"]);

// Crawl a site
const pages = await tvly.crawl("https://docs.example.com", {
  instructions: "Find API documentation",
  selectPaths: ["/docs/.*"],
});

// Map site structure
const urls = await tvly.map("https://example.com");
```

## Search API

Default method for web search. Use `searchDepth: "advanced"` for RAG (2 credits).

```typescript
await tvly.search("latest AI research", {
  searchDepth: "advanced",      // Better content extraction
  topic: "general",             // "general" | "news" | "finance"
  maxResults: 5,
  includeAnswer: true,          // LLM-generated answer
  includeRawContent: "markdown",
  includeDomains: ["arxiv.org"],
  excludeDomains: ["pinterest.com"],
  timeRange: "week",            // "day" | "week" | "month" | "year"
});
```

## Extract API

Extract content from specific URLs (max 20).

```typescript
await tvly.extract([
  "https://docs.tavily.com/sdk/javascript/quick-start",
  "https://example.com/article"
], {
  extractDepth: "advanced",
  format: "markdown",
});
```

## Crawl API

Intelligent site exploration with natural language guidance.

```typescript
await tvly.crawl("https://docs.example.com", {
  maxDepth: 3,
  limit: 50,
  instructions: "Find all API documentation",
  selectPaths: ["/docs/.*", "/api/.*"],
  excludePaths: ["/admin/.*"],
  extractDepth: "advanced",
});
```

## Map API

Discover site structure without extracting content.

```typescript
await tvly.map("https://example.com", {
  maxDepth: 2,
  limit: 100,
  instructions: "Find product pages",
  selectPaths: ["/products/.*"],
});
```

## Regex Patterns for Crawl/Map

The `selectPaths`, `excludePaths`, `selectDomains`, `excludeDomains` parameters use regex:

```typescript
// Path patterns
selectPaths: ["/docs/.*", "/api/v[0-9]+/.*"]
excludePaths: ["/admin/.*", ".*\\.pdf$"]

// Domain patterns  
selectDomains: ["^docs\\.example\\.com$"]
excludeDomains: ["^blog\\.example\\.com$"]
```

## AI SDK v5 Integration

For agentic workflows with Vercel AI SDK:

```typescript
import { tavilySearch, tavilyExtract, tavilyCrawl, tavilyMap } from "@tavily/ai-sdk";
import { generateText, gateway, stepCountIs } from "ai";

await generateText({
  model: gateway("anthropic/claude-sonnet-4-20250514"),
  prompt: "Research quantum computing",
  tools: {
    tavilySearch: tavilySearch({ searchDepth: "advanced", maxResults: 5 }),
    tavilyExtract: tavilyExtract(),
  },
  stopWhen: stepCountIs(5),
});
```

## Common Pattern: RAG Pipeline

```typescript
// 1. Search for sources
const search = await tvly.search(query, { searchDepth: "advanced", maxResults: 5 });

// 2. Extract full content from top results
const urls = search.results.slice(0, 3).map(r => r.url);
const content = await tvly.extract(urls, { format: "markdown" });

// 3. Use content.results[].rawContent as LLM context
```

## API Reference

For complete parameters and response types: [references/api-reference.md](references/api-reference.md)

## DeepWiki

For implementation questions about tavily-js internals: https://deepwiki.com/tavily-ai/tavily-js
