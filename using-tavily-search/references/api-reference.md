# Tavily API Reference

## Contents

- [Search Parameters](#search-parameters)
- [Search Response](#search-response)
- [Extract Parameters](#extract-parameters)
- [Extract Response](#extract-response)
- [Crawl Parameters](#crawl-parameters)
- [Crawl Response](#crawl-response)
- [Map Parameters](#map-parameters)
- [Map Response](#map-response)
- [AI SDK Tools](#ai-sdk-tools)
- [Regex Pattern Examples](#regex-pattern-examples)
- [API Credits](#api-credits)

---

## Search Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `string` | **required** | Search query |
| `searchDepth` | `"basic"` \| `"advanced"` | `"basic"` | Advanced uses 2 credits, better for RAG |
| `topic` | `"general"` \| `"news"` \| `"finance"` | `"general"` | Search category |
| `timeRange` | `"day"` \| `"week"` \| `"month"` \| `"year"` | — | Time filter |
| `startDate` | `string` | — | YYYY-MM-DD format |
| `endDate` | `string` | — | YYYY-MM-DD format |
| `maxResults` | `number` | `5` | 0-20 |
| `chunksPerSource` | `number` | `3` | 1-3, advanced only |
| `includeAnswer` | `boolean` \| `"basic"` \| `"advanced"` | `false` | LLM answer |
| `includeRawContent` | `boolean` \| `"markdown"` \| `"text"` | `false` | Full page content |
| `includeImages` | `boolean` | `false` | Image URLs |
| `includeImageDescriptions` | `boolean` | `false` | LLM image descriptions |
| `includeDomains` | `string[]` | `[]` | Max 300 |
| `excludeDomains` | `string[]` | `[]` | Max 150 |
| `country` | `string` | — | Boost results from country |
| `includeFavicon` | `boolean` | `false` | Favicon URLs |
| `timeout` | `number` | `60` | Seconds |

## Search Response

```typescript
interface SearchResponse {
  query: string;
  responseTime: number;
  requestId: string;
  answer?: string;
  images?: Array<{ url: string; description?: string }>;
  results: Array<{
    title: string;
    url: string;
    content: string;
    score: number;
    rawContent?: string;
    publishedDate?: string;
    favicon?: string;
  }>;
}
```

---

## Extract Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `urls` | `string[]` | **required** | Max 20 URLs |
| `extractDepth` | `"basic"` \| `"advanced"` | `"basic"` | Advanced gets tables/embedded |
| `format` | `"markdown"` \| `"text"` | `"markdown"` | Output format |
| `includeImages` | `boolean` | `false` | Extract images |
| `includeFavicon` | `boolean` | `false` | Favicon URLs |
| `timeout` | `number` | 10s basic, 30s advanced | 1-60 seconds |

## Extract Response

```typescript
interface ExtractResponse {
  results: Array<{
    url: string;
    rawContent: string;
    images?: string[];
    favicon?: string;
  }>;
  failedResults: Array<{ url: string; error: string }>;
  responseTime: number;
  requestId: string;
}
```

---

## Crawl Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | `string` | **required** | Starting URL |
| `maxDepth` | `number` | `1` | Depth from base URL |
| `maxBreadth` | `number` | `20` | Links per page |
| `limit` | `number` | `50` | Total links to process |
| `instructions` | `string` | — | Natural language guidance |
| `selectPaths` | `string[]` | `[]` | Regex patterns to include |
| `excludePaths` | `string[]` | `[]` | Regex patterns to exclude |
| `selectDomains` | `string[]` | `[]` | Regex for allowed domains |
| `excludeDomains` | `string[]` | `[]` | Regex for excluded domains |
| `allowExternal` | `boolean` | `true` | Follow external links |
| `includeImages` | `boolean` | `false` | Extract images |
| `extractDepth` | `"basic"` \| `"advanced"` | `"basic"` | Content extraction depth |
| `format` | `"markdown"` \| `"text"` | `"markdown"` | Output format |
| `categories` | `string` | — | See categories below |
| `includeFavicon` | `boolean` | `false` | Favicon URLs |
| `timeout` | `number` | `150` | 10-150 seconds |

**Categories**: `"Careers"`, `"Blogs"`, `"Documentation"`, `"About"`, `"Pricing"`, `"Community"`, `"Developers"`, `"Contact"`, `"Media"`

## Crawl Response

```typescript
interface CrawlResponse {
  baseUrl: string;
  results: Array<{
    url: string;
    rawContent: string;
    images?: string[];
    favicon?: string;
  }>;
  responseTime: number;
  requestId: string;
}
```

---

## Map Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | `string` | **required** | Starting URL |
| `maxDepth` | `number` | `1` | Depth from base URL |
| `maxBreadth` | `number` | `20` | Links per page |
| `limit` | `number` | `50` | Total links |
| `instructions` | `string` | — | Natural language guidance |
| `selectPaths` | `string[]` | `[]` | Regex to include |
| `excludePaths` | `string[]` | `[]` | Regex to exclude |
| `selectDomains` | `string[]` | `[]` | Domain regex |
| `excludeDomains` | `string[]` | `[]` | Domain regex |
| `allowExternal` | `boolean` | `true` | External links |
| `timeout` | `number` | `150` | 10-150 seconds |

## Map Response

```typescript
interface MapResponse {
  baseUrl: string;
  results: string[];  // Discovered URLs
  responseTime: number;
  requestId: string;
}
```

---

## AI SDK Tools

```typescript
import { tavilySearch, tavilyExtract, tavilyCrawl, tavilyMap } from "@tavily/ai-sdk";

// All tools accept their respective API parameters
tavilySearch({ searchDepth: "advanced", maxResults: 5 })
tavilyExtract({ extractDepth: "advanced" })
tavilyCrawl({ maxDepth: 2, limit: 50 })
tavilyMap({ maxDepth: 2 })
```

---

## Regex Pattern Examples

### Path Patterns

```typescript
selectPaths: [
  "/docs/.*",              // All /docs/* pages
  "/api/v[0-9]+/.*",       // /api/v1/*, /api/v2/*
  "/blog/[0-9]{4}/.*",     // Year-based blog paths
]

excludePaths: [
  "/admin/.*",
  "/private/.*",
  ".*\\.(pdf|zip)$",       // File downloads
]
```

### Domain Patterns

```typescript
selectDomains: [
  "^docs\\.example\\.com$",     // Exact match
  "^.*\\.example\\.com$",       // All subdomains
]

excludeDomains: [
  "^blog\\.example\\.com$",
  "^(staging|dev)\\..*",        // Staging/dev environments
]
```

---

## API Credits

| Operation | Cost |
|-----------|------|
| Search Basic | 1 credit |
| Search Advanced | 2 credits |
| Extract Basic | 1 credit / 5 URLs |
| Extract Advanced | 2 credits / 5 URLs |
| Crawl/Map | Varies by pages |

Free tier: 1,000 credits/month
