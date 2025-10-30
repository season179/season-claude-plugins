# Tools Guide: Staying Current with OpenAI Documentation

This guide explains how to use WebSearch, WebFetch, and deepwiki tools to always access the latest OpenAI Responses API information.

## Why These Tools Matter

The OpenAI API evolves rapidly. What worked last month might have changed today. These tools ensure you're always working with current information rather than outdated cached knowledge.

## Tool 1: WebSearch

### Purpose
Search the web for latest documentation, guides, examples, and community solutions.

### When to Use
- Finding latest official documentation
- Searching for specific features or parameters
- Looking for error message explanations
- Checking current model capabilities
- Finding community solutions

### Basic Usage Pattern

```typescript
WebSearch: "query string"
```

### Effective Search Queries

#### General Documentation
```
"OpenAI Responses API documentation site:platform.openai.com"
"OpenAI Responses API guide 2025"
"OpenAI SDK latest documentation"
```

#### Specific Features
```
"OpenAI Responses API streaming events"
"OpenAI structured output json_schema"
"OpenAI function calling guide"
"OpenAI conversation state management"
```

#### Model Information
```
"OpenAI models 2025"
"OpenAI gpt-4o capabilities"
"OpenAI model comparison 2025"
"OpenAI [model-name] token limits"
```

#### Error Messages
```
"OpenAI [exact-error-message]"
"OpenAI error code 429"
"OpenAI rate limit handling"
"OpenAI authentication error"
```

#### SDK-Specific
```
"OpenAI Python SDK latest version"
"OpenAI Python SDK streaming example"
"OpenAI TypeScript SDK async patterns"
"OpenAI SDK breaking changes 2025"
```

#### Changelog and Updates
```
"OpenAI API changelog 2025"
"OpenAI Responses API recent changes"
"OpenAI deprecated features"
"OpenAI SDK migration guide"
```

### Search Query Patterns

#### Pattern 1: Site-Specific Search
```
"[topic] site:platform.openai.com"
```
Example: `"streaming events site:platform.openai.com"`

Benefits:
- Only official documentation
- Most accurate information
- Latest updates

#### Pattern 2: Dated Search
```
"[topic] 2025"
"[topic] after:2025-01-01"
```
Example: `"OpenAI Responses API 2025"`

Benefits:
- Recent information
- Avoids outdated results
- Current best practices

#### Pattern 3: SDK Search
```
"OpenAI [SDK-language] [feature]"
```
Example: `"OpenAI Python async streaming"`

Benefits:
- Language-specific results
- SDK examples
- Implementation details

#### Pattern 4: Error Search
```
"OpenAI [exact error message]"
"OpenAI [error code]"
```
Example: `"OpenAI RateLimitError"`

Benefits:
- Direct problem solutions
- Common fixes
- Community help

#### Pattern 5: Comparison Search
```
"OpenAI [option-a] vs [option-b]"
```
Example: `"OpenAI json_object vs json_schema"`

Benefits:
- Understanding differences
- Choosing right approach
- Trade-offs

### Tips for Effective Searches

1. **Be Specific**: Include exact feature names
2. **Use Current Year**: Add "2025" to get recent results
3. **Site Restrict**: Use `site:` for official docs only
4. **Exact Phrases**: Use quotes for exact matches
5. **Error Messages**: Copy exact error text
6. **Include Version**: Mention SDK version if relevant
7. **Language Specific**: Add "Python" or "TypeScript"

### Examples by Use Case

**Starting new project:**
```
WebSearch: "OpenAI Responses API getting started 2025"
WebSearch: "OpenAI Python SDK installation"
WebSearch: "OpenAI API key setup best practices"
```

**Implementing streaming:**
```
WebSearch: "OpenAI Responses API streaming documentation"
WebSearch: "OpenAI streaming event types"
WebSearch: "OpenAI async streaming Python"
```

**Debugging error:**
```
WebSearch: "OpenAI RateLimitError handling"
WebSearch: "OpenAI 429 error retry strategy"
WebSearch: "OpenAI error codes documentation"
```

**Checking compatibility:**
```
WebSearch: "OpenAI gpt-4o structured output support"
WebSearch: "OpenAI models function calling support"
WebSearch: "OpenAI model capabilities comparison"
```

## Tool 2: WebFetch

### Purpose
Directly fetch and read content from specific URLs, particularly official documentation pages.

### When to Use
- Reading official API reference
- Getting complete guide content
- Checking specific documentation pages
- Reading changelog
- Fetching examples from docs

### Basic Usage Pattern

```typescript
WebFetch:
- url: "https://..."
- prompt: "What information to extract"
```

### Key URLs to Fetch

#### API Reference
```
URL: https://platform.openai.com/docs/api-reference/responses
Prompt: "What are all the parameters for responses.create()?"
```

```
URL: https://platform.openai.com/docs/api-reference/streaming
Prompt: "List all streaming event types with descriptions"
```

#### Guides
```
URL: https://platform.openai.com/docs/guides/text-generation
Prompt: "Show examples of basic text generation"
```

```
URL: https://platform.openai.com/docs/guides/structured-outputs
Prompt: "Explain json_object vs json_schema modes"
```

```
URL: https://platform.openai.com/docs/guides/function-calling
Prompt: "Show tool definition format with examples"
```

#### Model Information
```
URL: https://platform.openai.com/docs/models
Prompt: "List all available models with their capabilities"
```

#### Rate Limits
```
URL: https://platform.openai.com/docs/guides/rate-limits
Prompt: "What are the current rate limits by tier?"
```

#### Error Handling
```
URL: https://platform.openai.com/docs/guides/error-codes
Prompt: "List all error codes and recommended handling"
```

#### Changelog
```
URL: https://platform.openai.com/docs/changelog
Prompt: "What changed in the last 3 months?"
```

### Effective Prompts

#### Getting Complete Information
```
Prompt: "Summarize all the key information on this page"
Prompt: "List all parameters with their descriptions"
Prompt: "Extract all code examples"
```

#### Specific Queries
```
Prompt: "What are the required parameters?"
Prompt: "Show me the response object structure"
Prompt: "How do I handle errors according to this?"
```

#### Comparison
```
Prompt: "What's the difference between [option-a] and [option-b]?"
Prompt: "When should I use [feature-a] vs [feature-b]?"
```

#### Examples
```
Prompt: "Show me a complete example of [feature]"
Prompt: "What are the code examples on this page?"
```

### Fetch Workflow

1. **First, search to find the right page:**
   ```
   WebSearch: "OpenAI [feature] documentation"
   ```

2. **Then, fetch the specific page:**
   ```
   WebFetch:
   - url: "[URL from search]"
   - prompt: "[What you need]"
   ```

3. **Process the information:**
   - Extract relevant details
   - Compare with user's code
   - Verify syntax and parameters

### Examples by Use Case

**Understanding a parameter:**
```
WebFetch: https://platform.openai.com/docs/api-reference/responses/create
Prompt: "Explain the 'tool_choice' parameter with all possible values"
```

**Learning about streaming:**
```
WebFetch: https://platform.openai.com/docs/api-reference/streaming
Prompt: "Show me all event types and when they occur"
```

**Checking model support:**
```
WebFetch: https://platform.openai.com/docs/models
Prompt: "Which models support structured outputs?"
```

**Understanding rate limits:**
```
WebFetch: https://platform.openai.com/docs/guides/rate-limits
Prompt: "What are the rate limits for tier-1 and how to handle them?"
```

## Tool 3: deepwiki (MCP)

### Purpose
Query GitHub repositories to understand SDK implementation details, architecture, and patterns not fully documented in official docs.

### When to Use
- Understanding SDK internals
- Finding implementation details
- Checking how features work under the hood
- Discovering undocumented patterns
- Debugging SDK-specific issues

### Basic Usage Pattern

```typescript
Tool: mcp__deepwiki__ask_question
Parameters:
- repoName: "owner/repo"
- question: "Your specific question"
```

### Target Repositories

#### Python SDK
```
repoName: "openai/openai-python"
```

#### TypeScript/Node SDK
```
repoName: "openai/openai-node"
```

### Effective Questions

#### Implementation Details
```
question: "How is the responses.create() method implemented?"
question: "How does AsyncOpenAI handle concurrent requests?"
question: "How is streaming implemented internally?"
question: "How are responses parsed and validated?"
```

#### Type Information
```
question: "What TypeScript types are exported for Responses API?"
question: "What is the Response object type structure?"
question: "What are all the event types for streaming?"
```

#### Exception Handling
```
question: "What exception types are defined?"
question: "When is RateLimitError raised?"
question: "How should errors be handled according to the SDK?"
```

#### Authentication
```
question: "How does the SDK handle API key authentication?"
question: "How is the API key validated?"
question: "What authentication methods are supported?"
```

#### Architecture
```
question: "How is the SDK structured?"
question: "What are the main classes and their purposes?"
question: "How are requests made and processed?"
```

#### Patterns
```
question: "What are best practices for error handling in the SDK?"
question: "How should retries be implemented?"
question: "What patterns are recommended for async usage?"
```

### Examples by Use Case

**Understanding async implementation (Python):**
```
Tool: mcp__deepwiki__ask_question
repoName: "openai/openai-python"
question: "How does AsyncOpenAI work and how should it be used?"
```

**Finding event types (TypeScript):**
```
Tool: mcp__deepwiki__ask_question
repoName: "openai/openai-node"
question: "What are all the streaming event types and their TypeScript definitions?"
```

**Debugging error (Python):**
```
Tool: mcp__deepwiki__ask_question
repoName: "openai/openai-python"
question: "What causes APIConnectionError and how should it be handled?"
```

**Type safety (TypeScript):**
```
Tool: mcp__deepwiki__ask_question
repoName: "openai/openai-node"
question: "What are the TypeScript types for Response and OutputItem?"
```

**Best practices:**
```
Tool: mcp__deepwiki__ask_question
repoName: "openai/openai-python"
question: "What are the recommended patterns for retry and rate limit handling?"
```

## Combined Tool Workflow

### Complete Research Process

For any new feature implementation:

**Step 1: WebSearch for overview**
```
WebSearch: "OpenAI [feature] documentation 2025"
```
→ Get list of relevant documentation pages

**Step 2: WebFetch for details**
```
WebFetch: [URL from step 1]
Prompt: "Explain [feature] with all parameters and examples"
```
→ Get complete official documentation

**Step 3: deepwiki for SDK specifics**
```
Tool: mcp__deepwiki__ask_question
repoName: "openai/openai-[language]"
question: "How is [feature] implemented in the SDK?"
```
→ Get implementation details and patterns

**Step 4: Synthesize and implement**
- Combine information from all sources
- Verify parameter names and types
- Check for recent changes
- Implement with current syntax

### Example: Implementing Streaming

**Step 1: Search**
```
WebSearch: "OpenAI Responses API streaming 2025"
```
Result: Find documentation URL

**Step 2: Fetch docs**
```
WebFetch: https://platform.openai.com/docs/api-reference/streaming
Prompt: "List all streaming event types with their purposes"
```
Result: Get event types and structure

**Step 3: Query SDK**
```
Tool: mcp__deepwiki__ask_question
repoName: "openai/openai-python"
question: "How is streaming implemented? What's the event loop pattern?"
```
Result: Get SDK-specific implementation details

**Step 4: Implement**
```python
# Using information from all sources
stream = client.responses.create(
    model="gpt-4o",  # From Step 2
    input=prompt,
    stream=True,
)

for event in stream:  # Pattern from Step 3
    if event.type == "response.output_text.delta":  # Type from Step 2
        print(event.delta, end="")
```

## Best Practices

### 1. Always Start with Search
- Get overview first
- Find relevant pages
- Check multiple sources

### 2. Fetch Official Docs
- Read complete documentation
- Get authoritative information
- Verify parameter names

### 3. Query SDK When Needed
- For implementation details
- For patterns and best practices
- For debugging SDK issues

### 4. Verify Information
- Cross-reference multiple sources
- Check dates and versions
- Test with minimal examples

### 5. Stay Current
- Include year in searches
- Check changelog regularly
- Monitor for deprecations

### 6. Be Specific
- Ask precise questions
- Use exact feature names
- Include error messages verbatim

### 7. Document Sources
- Note where information came from
- Include documentation date
- Mention SDK version

## Tools Checklist

When implementing any feature:

- [ ] WebSearch for latest docs
- [ ] WebFetch API reference
- [ ] WebFetch relevant guides
- [ ] deepwiki for SDK details
- [ ] Check changelog for recent changes
- [ ] Verify model compatibility
- [ ] Cross-reference multiple sources
- [ ] Test with current SDK version

## Remember

These tools make this skill **evergreen**:
- No hardcoded information becomes outdated
- Always accessing latest documentation
- Adapting to API changes automatically
- Providing current, accurate guidance

**Use these tools every time** - don't rely on cached knowledge alone!
