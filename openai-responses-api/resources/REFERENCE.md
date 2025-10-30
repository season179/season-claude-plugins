# OpenAI Responses API - Documentation Reference Guide

This file teaches you **how to find** the latest OpenAI documentation, rather than duplicating it. Since OpenAI's API evolves rapidly, always consult official sources for current information.

## Philosophy

**This skill is evergreen** - instead of hardcoding API details that become outdated, we teach you how to always access the latest information using WebSearch, WebFetch, and deepwiki tools.

## Official Documentation Sources

### Primary API Reference
**URL**: https://platform.openai.com/docs/api-reference/responses

**What you'll find:**
- Complete Responses API parameter reference
- Request/response object structures
- Current model compatibility
- Authentication methods

**How to fetch:**
```
WebFetch: https://platform.openai.com/docs/api-reference/responses
```

### API Guides
**URL**: https://platform.openai.com/docs/guides

**What you'll find:**
- Implementation tutorials
- Best practices
- Use case examples
- Migration guides

**How to fetch:**
```
WebFetch: https://platform.openai.com/docs/guides
WebSearch: "OpenAI guides [feature] site:platform.openai.com"
```

### Streaming Documentation
**URL**: https://platform.openai.com/docs/api-reference/streaming

**What you'll find:**
- Event types and structures
- Streaming patterns
- Error handling

**How to fetch:**
```
WebFetch: https://platform.openai.com/docs/api-reference/streaming
```

### Model Information
**URL**: https://platform.openai.com/docs/models

**What you'll find:**
- Available models
- Capabilities per model
- Context windows
- Pricing

**How to search:**
```
WebSearch: "OpenAI models 2025"
WebSearch: "OpenAI [model-name] capabilities"
```

## SDK Repositories

### Python SDK
**Repository**: openai/openai-python
**GitHub**: https://github.com/openai/openai-python

**How to query:**
```
Using deepwiki (MCP):
mcp__deepwiki__ask_question
- repoName: "openai/openai-python"
- question: "How does streaming work in Responses API?"

Using WebSearch:
"openai-python [feature] github"
"openai python SDK changelog"
```

**Common queries:**
- "How is AsyncOpenAI implemented?"
- "What are the exception types?"
- "How does response parsing work?"
- "What are the streaming event types?"

### TypeScript/Node SDK
**Repository**: openai/openai-node
**GitHub**: https://github.com/openai/openai-node

**How to query:**
```
Using deepwiki (MCP):
mcp__deepwiki__ask_question
- repoName: "openai/openai-node"
- question: "What TypeScript types are exported?"

Using WebSearch:
"openai-node [feature] github"
"openai typescript SDK types"
```

**Common queries:**
- "What are the TypeScript type definitions?"
- "How is streaming implemented?"
- "What error types are available?"
- "How to use with ES modules?"

## Using WebSearch Effectively

### General Pattern
```
"OpenAI [feature] [year]"
"OpenAI [feature] site:platform.openai.com"
"OpenAI SDK [language] [feature] latest"
```

### Specific Queries

#### Finding Current Models
```
WebSearch: "OpenAI models list 2025"
WebSearch: "gpt-4o vs gpt-4o-mini comparison"
WebSearch: "OpenAI o-series models capabilities"
```

#### Streaming
```
WebSearch: "OpenAI Responses API streaming 2025"
WebSearch: "OpenAI streaming events documentation"
WebSearch: "OpenAI async streaming Python"
```

#### Structured Outputs
```
WebSearch: "OpenAI structured output json_schema"
WebSearch: "OpenAI json_object vs json_schema"
WebSearch: "OpenAI strict mode structured output"
```

#### Function Calling
```
WebSearch: "OpenAI function calling Responses API"
WebSearch: "OpenAI tool_choice options"
WebSearch: "OpenAI parallel function calls"
```

#### Conversation State
```
WebSearch: "OpenAI conversation state management"
WebSearch: "OpenAI previous_response_id usage"
WebSearch: "OpenAI conversation object API"
```

#### Error Handling
```
WebSearch: "OpenAI API error codes"
WebSearch: "OpenAI rate limiting best practices"
WebSearch: "OpenAI [error-message]"
```

## Using WebFetch Effectively

### Direct Documentation Access

**Fetch a specific page:**
```
WebFetch:
- url: "https://platform.openai.com/docs/api-reference/responses"
- prompt: "What are all the parameters for responses.create()?"
```

**Fetch guides:**
```
WebFetch:
- url: "https://platform.openai.com/docs/guides/text-generation"
- prompt: "Show me examples of structured outputs"
```

**Fetch changelog:**
```
WebFetch:
- url: "https://platform.openai.com/docs/changelog"
- prompt: "What changed in the Responses API recently?"
```

### Common Fetch Queries

**Parameter details:**
```
WebFetch: https://platform.openai.com/docs/api-reference/responses
Prompt: "List all parameters for responses.create with descriptions"
```

**Event types:**
```
WebFetch: https://platform.openai.com/docs/api-reference/streaming
Prompt: "What are all the streaming event types?"
```

**Error codes:**
```
WebFetch: https://platform.openai.com/docs/guides/error-codes
Prompt: "List all error codes and their meanings"
```

## Using deepwiki Effectively

### Python SDK Queries

**Implementation details:**
```
Tool: mcp__deepwiki__ask_question
repoName: "openai/openai-python"
question: "How is the responses.create() method implemented?"
```

**Exception handling:**
```
Tool: mcp__deepwiki__ask_question
repoName: "openai/openai-python"
question: "What exception types are defined and when are they raised?"
```

**Async implementation:**
```
Tool: mcp__deepwiki__ask_question
repoName: "openai/openai-python"
question: "How does AsyncOpenAI handle concurrent requests?"
```

**Response parsing:**
```
Tool: mcp__deepwiki__ask_question
repoName: "openai/openai-python"
question: "How are response objects structured and parsed?"
```

### TypeScript SDK Queries

**Type definitions:**
```
Tool: mcp__deepwiki__ask_question
repoName: "openai/openai-node"
question: "What TypeScript types are exported for Responses API?"
```

**Streaming implementation:**
```
Tool: mcp__deepwiki__ask_question
repoName: "openai/openai-node"
question: "How is streaming implemented in the TypeScript SDK?"
```

**Error handling:**
```
Tool: mcp__deepwiki__ask_question
repoName: "openai/openai-node"
question: "What error classes are available?"
```

## Checking for Updates

### SDK Version Checking

**Python:**
```bash
pip show openai
pip index versions openai  # See available versions
```

**TypeScript:**
```bash
npm list openai
npm view openai versions  # See available versions
```

### Changelog Monitoring

**Search for changes:**
```
WebSearch: "OpenAI API changelog 2025"
WebSearch: "OpenAI Python SDK releases"
WebFetch: https://github.com/openai/openai-python/releases
```

### Breaking Changes

**Search pattern:**
```
WebSearch: "OpenAI API breaking changes [year]"
WebSearch: "OpenAI SDK migration guide"
WebSearch: "OpenAI deprecated features"
```

## Quick Reference: Key Documentation URLs

| Topic | URL |
|-------|-----|
| Responses API Reference | https://platform.openai.com/docs/api-reference/responses |
| Streaming | https://platform.openai.com/docs/api-reference/streaming |
| Models | https://platform.openai.com/docs/models |
| Guides | https://platform.openai.com/docs/guides |
| Error Codes | https://platform.openai.com/docs/guides/error-codes |
| Rate Limits | https://platform.openai.com/docs/guides/rate-limits |
| Python SDK | https://github.com/openai/openai-python |
| TypeScript SDK | https://github.com/openai/openai-node |
| API Changelog | https://platform.openai.com/docs/changelog |

## Workflow for Finding Information

### Step-by-Step Process

1. **Start with WebSearch** - Get overview and find relevant pages
   ```
   "OpenAI [feature] documentation 2025"
   ```

2. **Use WebFetch** - Read specific documentation pages
   ```
   Fetch the URLs found in step 1
   ```

3. **Query with deepwiki** - Get SDK-specific implementation details
   ```
   Ask specific questions about the repository
   ```

4. **Verify Version** - Check if information matches user's SDK version
   ```
   Ask user: "What version of the SDK are you using?"
   ```

5. **Provide Solution** - With version awareness and source citations
   ```
   "Based on docs from [date], using SDK version [version]..."
   ```

## Common Research Patterns

### Pattern: New Feature Implementation

1. Search: "OpenAI [feature-name] documentation"
2. Fetch: API reference page for the feature
3. Query: deepwiki for SDK implementation
4. Check: Model compatibility
5. Provide: Current example with version info

### Pattern: Debugging Error

1. Search: "OpenAI [error-message]"
2. Fetch: Error codes documentation
3. Query: deepwiki for exception handling
4. Check: Recent issues in GitHub
5. Provide: Solution with verification steps

### Pattern: Migration/Upgrade

1. Search: "OpenAI SDK migration guide [old-version] to [new-version]"
2. Fetch: Changelog and migration docs
3. Query: deepwiki for breaking changes
4. Check: Deprecated features
5. Provide: Migration steps with current syntax

## Tips for Staying Current

1. **Always check documentation date** - APIs evolve rapidly
2. **Verify SDK version** - Different versions may have different APIs
3. **Search with year** - Include current year in searches
4. **Check multiple sources** - API docs + SDK docs + GitHub
5. **Test examples** - Recommend users verify with their setup
6. **Monitor deprecations** - Watch for "deprecated" warnings
7. **Read changelogs** - Stay aware of recent changes

## Remember

This skill's value is in **knowing HOW to find current information**, not in memorizing static details. When in doubt, search first, then provide solutions based on the latest documentation.

**Never guess - always fetch the latest information.**
