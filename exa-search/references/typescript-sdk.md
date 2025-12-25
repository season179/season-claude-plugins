# TypeScript SDK Reference

Complete reference for the `exa-js` SDK.

## Table of Contents
- [Installation](#installation)
- [Client Initialization](#client-initialization)
- [search Method](#search-method)
- [searchAndContents Method](#searchandcontents-method)
- [findSimilar Method](#findsimilar-method)
- [findSimilarAndContents Method](#findsimilarandcontents-method)
- [getContents Method](#getcontents-method)
- [answer Method](#answer-method)
- [streamAnswer Method](#streamanswer-method)
- [Types Reference](#types-reference)

## Installation

```bash
bun add exa-js
```

## Client Initialization

```typescript
import Exa from "exa-js";

const exa = new Exa(process.env.EXA_API_KEY);
```

## search Method

Get search results as links only (no content).

```typescript
const result = await exa.search("hottest AI startups", {
  numResults: 10,
  type: "auto",
  category: "company",
});
```

### Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| query | string | Search query | Required |
| numResults | number | Number of results (max 100 for neural) | 10 |
| type | "auto" \| "neural" \| "fast" \| "deep" | Search type | "auto" |
| category | string | Content category filter | undefined |
| includeDomains | string[] | Include only these domains | undefined |
| excludeDomains | string[] | Exclude these domains | undefined |
| startCrawlDate | string | Only links crawled after date | undefined |
| endCrawlDate | string | Only links crawled before date | undefined |
| startPublishedDate | string | Only links published after date | undefined |
| endPublishedDate | string | Only links published before date | undefined |
| includeText | string[] | Must contain (1 string, 5 words max) | undefined |
| excludeText | string[] | Must not contain | undefined |

### Response

```typescript
interface SearchResponse {
  autopromptString?: string;
  results: Result[];
}

interface Result {
  url: string;
  id: string;
  title: string | null;
  publishedDate?: string;
  author?: string;
}
```

## searchAndContents Method

Search and retrieve content in one call.

```typescript
// Full text
const result = await exa.searchAndContents("AI in healthcare", {
  text: true,
  numResults: 5,
});

// With highlights
const result = await exa.searchAndContents("AI in healthcare", {
  highlights: { numSentences: 3, highlightsPerUrl: 2 },
  numResults: 5,
});

// RAG context
const result = await exa.searchAndContents("AI in healthcare", {
  context: { maxCharacters: 10000 },
  numResults: 5,
});

// Structured summary
const result = await exa.searchAndContents("OpenAI company", {
  summary: { schema: companySchema },
  category: "company",
  numResults: 3,
});

// Deep search with query variations
const result = await exa.searchAndContents("blog post about AI", {
  type: "deep",
  additionalQueries: ["AI blogpost", "machine learning blogs"],
  text: true,
  context: true,
});
```

### Additional Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| text | boolean \| { maxCharacters?: number, includeHtmlTags?: boolean } | Extract full text |
| highlights | boolean \| { query?: string, numSentences?: number, highlightsPerUrl?: number } | Extract highlights |
| context | boolean \| { maxCharacters?: number } | RAG-optimized context string |
| summary | boolean \| { schema?: object, query?: string } | AI-generated summary |
| additionalQueries | string[] | Extra query variations (for deep search) |

### Response

```typescript
interface SearchResult extends Result {
  text?: string;
  highlights?: string[];
  highlightScores?: number[];
  summary?: string;
}
```

## findSimilar Method

Find pages similar to a given URL.

```typescript
const result = await exa.findSimilar("https://www.example.com/article", {
  numResults: 5,
  excludeSourceDomain: true,
});
```

### Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| url | string | Source URL | Required |
| numResults | number | Number of results | undefined |
| excludeSourceDomain | boolean | Exclude source domain | undefined |
| includeDomains | string[] | Include only these domains | undefined |
| excludeDomains | string[] | Exclude these domains | undefined |
| category | string | Content category filter | undefined |

## findSimilarAndContents Method

Find similar pages with content extraction.

```typescript
const result = await exa.findSimilarAndContents("https://example.com/article", {
  text: true,
  highlights: true,
  numResults: 5,
  excludeSourceDomain: true,
});
```

## getContents Method

Retrieve content for specific URLs/IDs.

```typescript
// Single URL
const result = await exa.getContents("https://example.com/article");

// Multiple URLs
const result = await exa.getContents([
  "https://example.com/article1",
  "https://example.com/article2",
]);

// With options
const result = await exa.getContents(urls, {
  text: { maxCharacters: 1000 },
  highlights: { query: "AI", numSentences: 2 },
});
```

## answer Method

Generate an answer with citations.

```typescript
const response = await exa.answer("What is the capital of France?");
console.log(response.answer);
console.log(response.citations);

// With full text in citations
const response = await exa.answer("What is quantum computing?", { text: true });
```

### Response

```typescript
interface AnswerResponse {
  answer: string;
  citations: SearchResult[];
  requestId?: string;
}
```

## streamAnswer Method

Stream an answer with citations.

```typescript
for await (const chunk of exa.streamAnswer("Explain quantum entanglement")) {
  if (chunk.content) {
    process.stdout.write(chunk.content);
  }
  if (chunk.citations) {
    console.log("\nCitations:", chunk.citations);
  }
}
```

### Chunk Type

```typescript
interface AnswerStreamChunk {
  content?: string;
  citations?: Array<{
    id: string;
    url: string;
    title?: string;
    publishedDate?: string;
    author?: string;
    text?: string;
  }>;
}
```

## Types Reference

### Search Types

```typescript
type SearchType = "auto" | "neural" | "fast" | "deep";
```

### Categories

```typescript
type Category =
  | "company"
  | "research paper"
  | "news"
  | "github"
  | "tweet"
  | "personal site"
  | "pdf"
  | "financial report"
  | "people"
  | "linkedin profile";
```

### Livecrawl Options

```typescript
type Livecrawl = "never" | "fallback" | "always" | "preferred";
```

### Content Options

```typescript
interface TextOptions {
  maxCharacters?: number;
  includeHtmlTags?: boolean;
}

interface HighlightOptions {
  query?: string;
  numSentences?: number;
  highlightsPerUrl?: number;
}

interface ContextOptions {
  maxCharacters?: number;
}

interface SummaryOptions {
  query?: string;
  schema?: object; // JSON Schema for structured extraction
}

interface ContentsOptions {
  text?: boolean | TextOptions;
  highlights?: boolean | HighlightOptions;
  context?: boolean | ContextOptions;
  summary?: boolean | SummaryOptions;
  livecrawl?: Livecrawl;
  livecrawlTimeout?: number;
  subpages?: number;
  subpageTarget?: string;
}
```
