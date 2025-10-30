# OpenAI Responses API - Detailed Workflow Guide

This guide provides step-by-step workflows for common OpenAI Responses API tasks. Each workflow emphasizes **fetching latest documentation first**.

## Core Principle

**Never implement without researching first.** The OpenAI API evolves rapidly, so always:
1. Search for latest docs
2. Verify current syntax
3. Check model compatibility
4. Implement with version awareness

## Workflow 1: Setting Up a New Project

### Step 1: Research Latest SDK Version

**Search:**
```
WebSearch: "OpenAI Python SDK latest version 2025"
WebSearch: "OpenAI TypeScript SDK npm latest"
```

**Verify:**
```
# Python
pip index versions openai

# TypeScript
npm view openai versions
```

### Step 2: Check Installation Instructions

**Fetch official docs:**
```
WebFetch: https://platform.openai.com/docs/libraries
Prompt: "What are the current installation instructions?"
```

### Step 3: Verify API Key Setup

**Search for best practices:**
```
WebSearch: "OpenAI API key setup best practices"
WebSearch: "OpenAI API key environment variables"
```

### Step 4: Test Basic Connection

**Get minimal example:**
```
WebFetch: https://platform.openai.com/docs/api-reference/responses
Prompt: "Show me the simplest possible example"
```

### Step 5: Implement and Verify

Create minimal test script with version logging:

**Python:**
```python
import openai
print(f"OpenAI SDK version: {openai.__version__}")

client = openai.OpenAI()
# Test connection with current syntax
```

**TypeScript:**
```typescript
import OpenAI from 'openai';
console.log(`Using OpenAI SDK`);

const client = new OpenAI();
// Test connection with current syntax
```

## Workflow 2: Implementing Text Generation

### Step 1: Research Current Syntax

**Search:**
```
WebSearch: "OpenAI Responses API create method documentation"
WebSearch: "OpenAI Responses API examples"
```

**Fetch:**
```
WebFetch: https://platform.openai.com/docs/api-reference/responses/create
Prompt: "What are all parameters for responses.create()?"
```

### Step 2: Check Available Models

**Search:**
```
WebSearch: "OpenAI models 2025"
WebSearch: "gpt-4o vs gpt-4o-mini comparison"
```

**Verify which models to use for your use case:**
- GPT-4o: Complex tasks, reasoning
- GPT-4o-mini: Fast, cost-effective
- o-series: Extended reasoning

### Step 3: Implement Basic Generation

**Template (verify all syntax):**
```python
# Verify: import path
from openai import OpenAI

client = OpenAI()

# Verify: method name, parameter names
response = client.responses.create(
    model="<CURRENT_MODEL>",  # From Step 2
    instructions="<system-instructions>",  # Verify parameter name
    input="<user-input>",  # Verify parameter name
)

# Verify: response access pattern
print(response.output_text)  # or response.output[0]?
```

### Step 4: Add Error Handling

**Research exception types:**
```
Tool: mcp__deepwiki__ask_question
repoName: "openai/openai-python"
question: "What exception types are defined?"
```

**Implement:**
```python
from openai import OpenAIError, RateLimitError

try:
    response = client.responses.create(...)
except RateLimitError:
    # Handle rate limits
    pass
except OpenAIError as e:
    # Handle other errors
    pass
```

### Step 5: Test and Validate

- Test with various inputs
- Verify response format
- Check token usage
- Log any unexpected behavior

## Workflow 3: Implementing Streaming

### Step 1: Research Streaming Events

**Search:**
```
WebSearch: "OpenAI Responses API streaming events"
WebSearch: "OpenAI streaming delta handling"
```

**Fetch:**
```
WebFetch: https://platform.openai.com/docs/api-reference/streaming
Prompt: "List all event types and their structures"
```

### Step 2: Check Async Requirements

**Determine if async needed:**
- Single stream? Sync is fine
- Multiple concurrent streams? Use async
- UI with non-blocking updates? Use async

**Research async patterns:**
```
WebSearch: "OpenAI AsyncOpenAI streaming example"
```

### Step 3: Implement Streaming

**Sync pattern (verify syntax):**
```python
stream = client.responses.create(
    model="<current-model>",
    input="<prompt>",
    stream=True,  # Verify parameter name
)

for event in stream:
    # Verify event types from Step 1
    if event.type == "<CHECK_DOCS>":
        print(event.delta, end="", flush=True)
```

**Async pattern (verify syntax):**
```python
from openai import AsyncOpenAI

async def stream_response():
    client = AsyncOpenAI()
    stream = await client.responses.create(
        model="<current-model>",
        input="<prompt>",
        stream=True,
    )

    async for event in stream:
        # Verify event types
        if event.type == "<CHECK_DOCS>":
            print(event.delta, end="")
```

### Step 4: Handle Stream Errors

**Research error patterns:**
```
WebSearch: "OpenAI streaming error handling"
```

**Implement:**
```python
try:
    for event in stream:
        if event.type == "error":  # Verify type name
            # Handle error event
            break
except Exception as e:
    # Handle stream interruption
    pass
```

### Step 5: Optimize Buffering

**Research best practices:**
```
WebSearch: "OpenAI streaming buffering best practices"
```

- Consider accumulating deltas
- Implement progress tracking
- Handle incomplete tokens

## Workflow 4: Implementing Structured Outputs

### Step 1: Research Structured Output Modes

**Search:**
```
WebSearch: "OpenAI structured output json_schema vs json_object"
WebSearch: "OpenAI strict mode structured output"
```

**Fetch:**
```
WebFetch: https://platform.openai.com/docs/guides/structured-outputs
Prompt: "Explain json_object vs json_schema modes"
```

### Step 2: Choose Validation Library

**Python options:**
- Pydantic (most common)
- dataclasses with json-schema
- attrs

**TypeScript options:**
- Zod (recommended)
- TypeScript interfaces + JSON schema
- class-validator

**Research integration:**
```
WebSearch: "OpenAI Pydantic structured output"
WebSearch: "OpenAI Zod TypeScript"
```

### Step 3: Define Schema

**Python with Pydantic:**
```python
from pydantic import BaseModel, Field

class OutputSchema(BaseModel):
    """Verify: Is Pydantic still recommended?"""
    field1: str = Field(description="...")
    field2: list[str]
    field3: int
```

**TypeScript with Zod:**
```typescript
import { z } from 'zod';

const OutputSchema = z.object({
  field1: z.string(),
  field2: z.array(z.string()),
  field3: z.number(),
});
```

### Step 4: Research Model Support

**Check which models support structured outputs:**
```
WebSearch: "OpenAI structured output model support"
```

Typically: GPT-4o, GPT-4o-mini support json_schema

### Step 5: Implement with Schema

**Python template:**
```python
response = client.responses.create(
    model="<CHECK_MODEL_SUPPORT>",
    input="<prompt>",
    text={  # Verify parameter structure
        "format": {
            "type": "json_schema",  # vs "json_object"
            "json_schema": {
                "name": "output_schema",
                "schema": OutputSchema.model_json_schema(),
                "strict": True  # Verify if available
            }
        }
    }
)

# Verify parsing method
result = OutputSchema.model_validate_json(response.output_text)
```

### Step 6: Handle Validation Errors

```python
from pydantic import ValidationError

try:
    result = OutputSchema.model_validate_json(response.output_text)
except ValidationError as e:
    # Handle schema mismatch
    print(f"Validation error: {e}")
```

## Workflow 5: Implementing Function Calling

### Step 1: Research Tool Definition Format

**Search:**
```
WebSearch: "OpenAI function calling Responses API"
WebSearch: "OpenAI tool definition JSON schema"
```

**Fetch:**
```
WebFetch: https://platform.openai.com/docs/guides/function-calling
Prompt: "Show tool definition format and examples"
```

### Step 2: Check Model Support

**Verify which models support function calling:**
```
WebSearch: "OpenAI function calling model support"
```

### Step 3: Define Functions

**Template (verify format):**
```python
tools = [{
    "type": "function",  # Verify type value
    "function": {
        "name": "function_name",
        "description": "Clear description of what it does",
        "parameters": {
            # Verify JSON schema format
            "type": "object",
            "properties": {
                "param1": {
                    "type": "string",
                    "description": "What param1 is for",
                },
                "param2": {
                    "type": "number",
                    "description": "What param2 is for",
                }
            },
            "required": ["param1"],
        }
    }
}]
```

### Step 4: Research tool_choice Options

**Search:**
```
WebSearch: "OpenAI tool_choice parameter options"
```

**Typical options:**
- "auto" - Model decides
- "required" - Must call a tool
- "none" - Don't call tools
- Specific tool object - Call specific tool

### Step 5: Implement Function Calling Loop

**Template:**
```python
response = client.responses.create(
    model="<CHECK_SUPPORT>",
    input="<prompt>",
    tools=tools,
    tool_choice="auto",  # Verify options
)

# Verify: How to check for function calls?
for item in response.output:
    if item.type == "function_call":  # Verify type name
        # Verify: attribute names
        func_name = item.name
        arguments = item.arguments  # string? dict?

        # Execute function
        result = execute_function(func_name, arguments)

        # Send result back - verify syntax
        response = client.responses.create(
            model="<model>",
            previous_response_id=response.id,  # Or conversation?
            input=[{
                "type": "function_call_output",  # Verify type
                "call_id": item.call_id,  # Verify attribute
                "output": json.dumps(result),
            }]
        )
```

### Step 6: Handle Multi-turn Tool Calls

**Research:**
```
WebSearch: "OpenAI parallel function calls"
WebSearch: "OpenAI multi-turn function calling"
```

Implement loop for multiple iterations if needed.

## Workflow 6: Implementing Conversation State

### Step 1: Research State Management Options

**Search:**
```
WebSearch: "OpenAI conversation state management"
WebSearch: "OpenAI previous_response_id vs conversation"
```

**Fetch:**
```
WebFetch: https://platform.openai.com/docs/api-reference/responses
Prompt: "Explain conversation state management options"
```

### Step 2: Choose Approach

**Option 1: previous_response_id**
- Simpler for short conversations
- Manual state tracking

**Option 2: conversation objects**
- Better for long conversations
- Automatic state management

**Research which to use:**
```
WebSearch: "OpenAI previous_response_id vs conversation object"
```

### Step 3: Implement with previous_response_id

**Template:**
```python
# First turn - verify syntax
response1 = client.responses.create(
    model="<model>",
    input="First message",
    store=True,  # Verify: Is this required?
)

# Follow-up - verify parameter name
response2 = client.responses.create(
    model="<model>",
    input="Follow-up message",
    previous_response_id=response1.id,  # Verify attribute
)
```

### Step 4: Or Implement with Conversation Objects

**Template:**
```python
# Verify conversation object structure
conversation_id = "conv_unique_id"

response1 = client.responses.create(
    model="<model>",
    conversation={"id": conversation_id},  # Verify structure
    input="First message",
)

response2 = client.responses.create(
    model="<model>",
    conversation={"id": conversation_id},
    input="Follow-up message",
)
```

### Step 5: Implement Conversation Management

**For production systems:**
- Store conversation IDs per user
- Handle conversation expiration
- Implement conversation reset
- Monitor token usage across turns

## Workflow 7: Implementing Async/Concurrent Requests

### Step 1: Determine Concurrency Needs

**When to use async:**
- Processing multiple prompts in parallel
- Real-time streaming with other operations
- High-throughput applications
- Non-blocking UI updates

### Step 2: Research Async SDK Usage

**Python:**
```
WebSearch: "OpenAI AsyncOpenAI usage"
Tool: mcp__deepwiki__ask_question
repoName: "openai/openai-python"
question: "How does AsyncOpenAI work?"
```

**TypeScript:**
```
WebSearch: "OpenAI Node.js async patterns"
```

### Step 3: Implement Async Pattern

**Python:**
```python
from openai import AsyncOpenAI
import asyncio

async def process_prompts(prompts: list[str]):
    client = AsyncOpenAI()

    # Create tasks
    tasks = [
        client.responses.create(
            model="<model>",
            input=prompt
        )
        for prompt in prompts
    ]

    # Execute concurrently
    results = await asyncio.gather(*tasks)
    return results

# Run
results = asyncio.run(process_prompts(["prompt1", "prompt2", "prompt3"]))
```

**TypeScript:**
```typescript
async function processPrompts(prompts: string[]) {
  const client = new OpenAI();

  const promises = prompts.map(prompt =>
    client.responses.create({
      model: '<model>',
      input: prompt,
    })
  );

  const results = await Promise.all(promises);
  return results;
}
```

### Step 4: Handle Errors in Concurrent Requests

**Python with error handling:**
```python
async def safe_request(client, prompt):
    try:
        return await client.responses.create(model="<model>", input=prompt)
    except Exception as e:
        return {"error": str(e), "prompt": prompt}

async def process_with_errors(prompts):
    client = AsyncOpenAI()
    tasks = [safe_request(client, p) for p in prompts]
    results = await asyncio.gather(*tasks)
    return results
```

### Step 5: Implement Rate Limiting

**Research rate limits:**
```
WebSearch: "OpenAI rate limits"
WebFetch: https://platform.openai.com/docs/guides/rate-limits
```

**Implement throttling:**
```python
import asyncio
from asyncio import Semaphore

async def rate_limited_requests(prompts, max_concurrent=5):
    semaphore = Semaphore(max_concurrent)

    async def limited_request(prompt):
        async with semaphore:
            return await client.responses.create(
                model="<model>",
                input=prompt
            )

    tasks = [limited_request(p) for p in prompts]
    return await asyncio.gather(*tasks)
```

## General Troubleshooting Workflow

### When Something Doesn't Work

1. **Check SDK Version**
   ```bash
   pip show openai  # Python
   npm list openai  # TypeScript
   ```

2. **Search for Current Docs**
   ```
   WebSearch: "OpenAI [feature] 2025"
   WebSearch: "OpenAI [error-message]"
   ```

3. **Fetch Official Examples**
   ```
   WebFetch: https://platform.openai.com/docs/api-reference/[endpoint]
   ```

4. **Check Recent Changes**
   ```
   WebSearch: "OpenAI API changelog [year]"
   WebFetch: https://platform.openai.com/docs/changelog
   ```

5. **Query SDK Repository**
   ```
   Tool: mcp__deepwiki__ask_question
   repoName: "openai/openai-python" or "openai/openai-node"
   question: "How does [feature] work?"
   ```

6. **Verify Against Fresh Example**
   - Create minimal reproduction from latest docs
   - Compare with user's code
   - Identify differences

## Remember

Every workflow starts with **research**:
1. Search for latest documentation
2. Verify current syntax and parameters
3. Check model compatibility
4. Implement with version awareness
5. Test and validate

The API evolves - always fetch fresh information before implementing.
