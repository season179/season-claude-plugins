# Python Patterns for OpenAI Responses API

This guide provides general Python patterns and best practices for working with the OpenAI SDK. These patterns are language-specific and remain relatively stable, though **always verify current SDK syntax**.

## Python Version Requirements

This skill targets **Python 3.11+** for:
- Modern type hints with `|` syntax
- Better async/await performance
- Improved error messages
- `ExceptionGroup` support

## Import Patterns

### Basic Imports
```python
# Verify: current import paths
from openai import OpenAI, AsyncOpenAI
from openai import OpenAIError, APIError, RateLimitError
import os
```

### Type Hints (Python 3.11+)
```python
from typing import AsyncIterator, Iterator
from collections.abc import Sequence

# Python 3.11+ union syntax
def process_response(response: dict | None) -> str | None:
    pass

# Generic lists (Python 3.9+)
def batch_process(prompts: list[str]) -> list[dict]:
    pass
```

### Pydantic for Structured Outputs
```python
from pydantic import BaseModel, Field, validator
from pydantic import ValidationError
```

## Client Initialization Patterns

### Basic Sync Client
```python
# Verify: current initialization syntax
from openai import OpenAI

# API key from environment (recommended)
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

# Or use default (reads from OPENAI_API_KEY env var)
client = OpenAI()
```

### Async Client
```python
from openai import AsyncOpenAI

# Async client for concurrent operations
async_client = AsyncOpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)
```

### Client with Custom Configuration
```python
# Verify: available configuration options
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    timeout=30.0,  # Check: parameter name
    max_retries=3,  # Check: parameter name
    # Verify: other available options in docs
)
```

### Context Manager Pattern
```python
# Check: Does SDK support context managers?
# If so, use this pattern:
with OpenAI() as client:
    response = client.responses.create(...)
```

## Response Handling Patterns

### Basic Response
```python
# Verify: response object structure
response = client.responses.create(
    model="gpt-4o",
    input="Hello, world!"
)

# Verify: attribute names
text = response.output_text  # or response.output[0].message.content?
response_id = response.id
model_used = response.model
```

### Checking Response Status
```python
# Verify: status checking attributes
if hasattr(response, 'incomplete_details') and response.incomplete_details:
    reason = response.incomplete_details.reason
    if reason == "max_output_tokens":
        print("Response truncated")
    elif reason == "content_filter":
        print("Content filtered")

# Check for errors
if hasattr(response, 'error') and response.error:
    print(f"Error: {response.error}")
```

### Accessing Output Items
```python
# Verify: output structure
for item in response.output:
    # Check: available item types
    if item.type == "message":
        print(item.content)  # Verify attribute
    elif item.type == "function_call":
        print(f"Function: {item.name}")
        print(f"Args: {item.arguments}")
```

## Streaming Patterns

### Sync Streaming
```python
# Verify: streaming syntax
stream = client.responses.create(
    model="gpt-4o",
    input="Write a story",
    stream=True,
)

# Process events
full_text = ""
for event in stream:
    # Verify: event types and structure
    if event.type == "response.output_text.delta":  # Check type name
        delta = event.delta  # Verify attribute
        full_text += delta
        print(delta, end="", flush=True)
```

### Async Streaming
```python
from openai import AsyncOpenAI
import asyncio

async def stream_response(prompt: str) -> str:
    client = AsyncOpenAI()

    # Verify: async streaming syntax
    stream = await client.responses.create(
        model="gpt-4o",
        input=prompt,
        stream=True,
    )

    full_text = ""
    async for event in stream:
        # Verify: event types
        if event.type == "response.output_text.delta":
            delta = event.delta
            full_text += delta
            print(delta, end="", flush=True)

    return full_text

# Usage
result = asyncio.run(stream_response("Hello"))
```

### Streaming with Error Handling
```python
def stream_with_errors(prompt: str) -> str:
    full_text = ""

    try:
        stream = client.responses.create(
            model="gpt-4o",
            input=prompt,
            stream=True,
        )

        for event in stream:
            if event.type == "error":  # Verify type name
                print(f"Stream error: {event.error}")
                break
            elif event.type == "response.output_text.delta":
                full_text += event.delta
                print(event.delta, end="", flush=True)

    except Exception as e:
        print(f"Streaming failed: {e}")
        # Handle interruption

    return full_text
```

## Async/Await Patterns

### Basic Async Pattern
```python
import asyncio
from openai import AsyncOpenAI

async def async_generate(prompt: str) -> str:
    client = AsyncOpenAI()

    response = await client.responses.create(
        model="gpt-4o",
        input=prompt,
    )

    return response.output_text

# Run single request
result = asyncio.run(async_generate("Hello"))
```

### Concurrent Requests
```python
async def process_multiple(prompts: list[str]) -> list[str]:
    client = AsyncOpenAI()

    # Create tasks for all prompts
    tasks = [
        client.responses.create(model="gpt-4o", input=prompt)
        for prompt in prompts
    ]

    # Execute concurrently
    responses = await asyncio.gather(*tasks)

    # Extract text
    return [r.output_text for r in responses]

# Usage
prompts = ["Prompt 1", "Prompt 2", "Prompt 3"]
results = asyncio.run(process_multiple(prompts))
```

### Concurrent with Error Handling
```python
async def safe_generate(client: AsyncOpenAI, prompt: str) -> dict:
    """Generate with error handling."""
    try:
        response = await client.responses.create(
            model="gpt-4o",
            input=prompt,
        )
        return {"success": True, "text": response.output_text}
    except Exception as e:
        return {"success": False, "error": str(e), "prompt": prompt}

async def process_with_errors(prompts: list[str]) -> list[dict]:
    client = AsyncOpenAI()

    tasks = [safe_generate(client, p) for p in prompts]
    results = await asyncio.gather(*tasks)

    return results
```

### Rate-Limited Concurrent Requests
```python
from asyncio import Semaphore

async def rate_limited_batch(
    prompts: list[str],
    max_concurrent: int = 5
) -> list[str]:
    """Process requests with concurrency limit."""
    client = AsyncOpenAI()
    semaphore = Semaphore(max_concurrent)

    async def limited_request(prompt: str) -> str:
        async with semaphore:
            response = await client.responses.create(
                model="gpt-4o",
                input=prompt,
            )
            return response.output_text

    tasks = [limited_request(p) for p in prompts]
    results = await asyncio.gather(*tasks)

    return results

# Usage
results = asyncio.run(rate_limited_batch(prompts, max_concurrent=3))
```

### Progress Tracking with Async
```python
from tqdm.asyncio import tqdm

async def process_with_progress(prompts: list[str]) -> list[str]:
    client = AsyncOpenAI()

    async def generate_one(prompt: str) -> str:
        response = await client.responses.create(
            model="gpt-4o",
            input=prompt,
        )
        return response.output_text

    # Process with progress bar
    results = []
    for prompt in tqdm(prompts, desc="Processing"):
        result = await generate_one(prompt)
        results.append(result)

    return results
```

## Error Handling Patterns

### Comprehensive Exception Handling
```python
# Verify: current exception types
from openai import (
    OpenAIError,
    APIError,
    RateLimitError,
    APIConnectionError,
    AuthenticationError,
)

def safe_request(prompt: str) -> str | None:
    try:
        response = client.responses.create(
            model="gpt-4o",
            input=prompt,
        )
        return response.output_text

    except AuthenticationError:
        print("Invalid API key")
        return None

    except RateLimitError as e:
        print(f"Rate limit exceeded: {e}")
        # Implement retry with backoff
        return None

    except APIConnectionError:
        print("Connection failed")
        return None

    except APIError as e:
        print(f"API error: {e}")
        return None

    except OpenAIError as e:
        print(f"OpenAI error: {e}")
        return None
```

### Retry with Exponential Backoff
```python
import time
from typing import Callable, TypeVar

T = TypeVar('T')

def retry_with_backoff(
    func: Callable[[], T],
    max_retries: int = 3,
    base_delay: float = 1.0,
) -> T:
    """Retry function with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            print(f"Rate limited. Retrying in {delay}s...")
            time.sleep(delay)
        except APIConnectionError:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            print(f"Connection error. Retrying in {delay}s...")
            time.sleep(delay)

# Usage
response = retry_with_backoff(
    lambda: client.responses.create(model="gpt-4o", input="Hello")
)
```

### Async Retry Pattern
```python
import asyncio

async def async_retry(
    func: Callable,
    max_retries: int = 3,
    base_delay: float = 1.0,
):
    """Async retry with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return await func()
        except (RateLimitError, APIConnectionError):
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            await asyncio.sleep(delay)
```

## Structured Output Patterns

### Using Pydantic Models
```python
from pydantic import BaseModel, Field

class Article(BaseModel):
    """Article structure - verify Pydantic is still recommended."""
    title: str = Field(description="Article title")
    author: str = Field(description="Author name")
    summary: str = Field(description="Brief summary")
    tags: list[str] = Field(description="Topic tags")

def extract_article(text: str) -> Article:
    # Verify: structured output syntax
    response = client.responses.create(
        model="gpt-4o",  # Check model support
        input=f"Extract article info: {text}",
        text={
            "format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "article",
                    "schema": Article.model_json_schema(),
                    "strict": True  # Verify if available
                }
            }
        }
    )

    # Parse and validate
    return Article.model_validate_json(response.output_text)
```

### Handling Validation Errors
```python
from pydantic import ValidationError

def safe_extract(text: str) -> Article | None:
    try:
        response = client.responses.create(...)
        return Article.model_validate_json(response.output_text)

    except ValidationError as e:
        print(f"Validation failed: {e}")
        # Log errors for debugging
        for error in e.errors():
            print(f"- {error['loc']}: {error['msg']}")
        return None
```

### Nested Models
```python
class Author(BaseModel):
    name: str
    email: str

class Article(BaseModel):
    title: str
    author: Author  # Nested model
    content: str
    tags: list[str]

# Use as normal - Pydantic handles nesting
article = extract_structured_data(text)
print(article.author.name)
```

## Function Calling Patterns

### Type-Safe Function Definitions
```python
from typing import Literal

def get_weather(
    location: str,
    unit: Literal["celsius", "fahrenheit"] = "celsius"
) -> dict:
    """Get weather for a location."""
    # Implementation
    return {"temp": 20, "unit": unit}

# Verify: tool definition format
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name or coordinates"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature unit"
                }
            },
            "required": ["location"]
        }
    }
}]
```

### Function Dispatcher Pattern
```python
import json
from typing import Callable

# Function registry
FUNCTIONS: dict[str, Callable] = {
    "get_weather": get_weather,
    "search_web": search_web,
    "query_db": query_database,
}

def execute_function_call(name: str, arguments: str) -> str:
    """Execute function from registry."""
    if name not in FUNCTIONS:
        return json.dumps({"error": f"Unknown function: {name}"})

    try:
        args = json.loads(arguments)
        result = FUNCTIONS[name](**args)
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})
```

### Multi-Turn Function Calling
```python
def agent_with_tools(query: str, max_iterations: int = 5) -> str:
    """Agent that can call functions multiple times."""
    # Verify: tool calling syntax
    response = client.responses.create(
        model="gpt-4o",
        input=query,
        tools=tools,
        tool_choice="auto",
    )

    iterations = 0
    while iterations < max_iterations:
        # Check for function calls
        has_function_call = False

        for item in response.output:
            if item.type == "function_call":  # Verify type
                has_function_call = True

                # Execute function
                result = execute_function_call(item.name, item.arguments)

                # Send result back - verify syntax
                response = client.responses.create(
                    model="gpt-4o",
                    previous_response_id=response.id,
                    input=[{
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": result,
                    }]
                )

        if not has_function_call:
            # No more function calls - return final answer
            return response.output_text

        iterations += 1

    return "Max iterations reached"
```

## Configuration and Environment

### Environment Variables
```python
import os
from pathlib import Path

# Load from .env file
from dotenv import load_dotenv
load_dotenv()

# Access variables
api_key = os.environ.get("OPENAI_API_KEY")
org_id = os.environ.get("OPENAI_ORG_ID")

# Validate presence
if not api_key:
    raise ValueError("OPENAI_API_KEY not set")
```

### Configuration Class Pattern
```python
from dataclasses import dataclass

@dataclass
class OpenAIConfig:
    """OpenAI configuration."""
    api_key: str
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 1000

    @classmethod
    def from_env(cls) -> "OpenAIConfig":
        return cls(
            api_key=os.environ["OPENAI_API_KEY"],
            model=os.environ.get("OPENAI_MODEL", "gpt-4o"),
        )

# Usage
config = OpenAIConfig.from_env()
client = OpenAI(api_key=config.api_key)
```

## Logging Patterns

### Basic Logging
```python
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def logged_request(prompt: str) -> str:
    logger.info(f"Generating response for prompt: {prompt[:50]}...")

    try:
        response = client.responses.create(
            model="gpt-4o",
            input=prompt,
        )
        logger.info(f"Response received: {len(response.output_text)} chars")
        return response.output_text

    except Exception as e:
        logger.error(f"Request failed: {e}")
        raise
```

### Token Usage Tracking
```python
def track_usage(prompt: str) -> tuple[str, dict]:
    """Generate response and track token usage."""
    response = client.responses.create(
        model="gpt-4o",
        input=prompt,
    )

    # Verify: usage tracking attributes
    usage = {
        "prompt_tokens": getattr(response, "input_tokens", 0),
        "completion_tokens": getattr(response, "output_tokens", 0),
        "total_tokens": getattr(response, "total_tokens", 0),
    }

    logger.info(f"Token usage: {usage}")

    return response.output_text, usage
```

## Testing Patterns

### Mocking for Tests
```python
from unittest.mock import Mock, patch

def test_generation():
    # Mock response
    mock_response = Mock()
    mock_response.output_text = "Test response"
    mock_response.id = "resp_123"

    with patch('openai.OpenAI') as mock_client:
        mock_client.return_value.responses.create.return_value = mock_response

        # Test your function
        result = your_function()
        assert result == "Test response"
```

## Best Practices Summary

1. **Use Python 3.11+ features** - Modern type hints, better performance
2. **Always use async for concurrency** - Much better than threading
3. **Implement retry logic** - Handle rate limits gracefully
4. **Use Pydantic for structured data** - Type safety and validation
5. **Log extensively** - Track usage and debug issues
6. **Environment variables for secrets** - Never hardcode API keys
7. **Type hints everywhere** - Better IDE support and fewer bugs
8. **Context managers when available** - Proper resource cleanup
9. **Verify all syntax** - Always check current SDK documentation

Remember: These are **patterns**, not exact implementations. Always verify current SDK syntax against latest documentation!
