# Troubleshooting Methodology for OpenAI Responses API

This guide provides a systematic approach to debugging issues with the OpenAI Responses API. Rather than listing specific error fixes (which become outdated), we teach the **methodology** for troubleshooting.

## Core Principle

**Never guess - always research.** When something doesn't work, follow a systematic process to identify and fix the issue using current documentation.

## General Troubleshooting Workflow

### Step 1: Identify the Problem

**Be specific about what's failing:**
- What were you trying to do?
- What did you expect to happen?
- What actually happened?
- What error message did you get (exact text)?

**Gather context:**
- SDK version (pip show openai / npm list openai)
- Language/runtime version
- Code snippet that reproduces the issue
- Full error stack trace

### Step 2: Check SDK Version

**Python:**
```bash
pip show openai
# Note the version number

pip index versions openai
# See available versions
```

**TypeScript:**
```bash
npm list openai
# Note the version number

npm view openai versions
# See available versions
```

**Common issue:** Using outdated SDK with changed API

**Solution pattern:**
```
WebSearch: "OpenAI SDK [version] breaking changes"
WebSearch: "OpenAI SDK upgrade guide [old-version] to [new-version]"
```

### Step 3: Search for Current Documentation

**For API errors:**
```
WebSearch: "OpenAI [exact-error-message]"
WebSearch: "OpenAI [error-code] meaning"
WebSearch: "OpenAI API error [status-code]"
```

**For feature issues:**
```
WebSearch: "OpenAI Responses API [feature] 2025"
WebFetch: https://platform.openai.com/docs/api-reference/responses
```

**For SDK-specific issues:**
```
Tool: mcp__deepwiki__ask_question
repoName: "openai/openai-python" or "openai/openai-node"
question: "How does [feature] work? Why might it fail?"
```

### Step 4: Verify Against Latest Documentation

**Fetch official examples:**
```
WebFetch: https://platform.openai.com/docs/api-reference/responses
Prompt: "Show me examples of [feature-you're-trying-to-use]"
```

**Compare your code:**
- Parameter names match?
- Data types correct?
- Required fields present?
- API version compatible?

### Step 5: Create Minimal Reproduction

**Strip down to simplest case:**
```python
# Python minimal example
from openai import OpenAI

client = OpenAI()

# Simplest possible request
response = client.responses.create(
    model="gpt-4o",
    input="Hello",
)

print(response.output_text)
```

**If this works:** Add complexity incrementally until you find the issue
**If this fails:** SDK installation or API key problem

### Step 6: Check Recent Changes

**Search for breaking changes:**
```
WebSearch: "OpenAI API changelog 2025"
WebSearch: "OpenAI breaking changes [current-month]"
WebFetch: https://platform.openai.com/docs/changelog
```

**Check GitHub issues:**
```
WebSearch: "OpenAI SDK [your-issue] github"
WebSearch: "site:github.com/openai/openai-python [error-message]"
```

## Common Problem Categories

### Category 1: Authentication Issues

**Symptoms:**
- "Invalid API key"
- "Authentication failed"
- 401 errors

**Debugging process:**

1. **Verify API key is set:**
   ```python
   import os
   print("API key:", os.environ.get("OPENAI_API_KEY"))
   ```

2. **Check .env file is loaded:**
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   print("Loaded:", os.environ.get("OPENAI_API_KEY") is not None)
   ```

3. **Verify key format:**
   - Should start with "sk-"
   - No extra whitespace
   - No quotes around the value in .env

4. **Test key directly:**
   ```
   WebFetch: https://platform.openai.com/docs/api-reference/authentication
   Prompt: "How do I test if my API key is valid?"
   ```

5. **Search for authentication docs:**
   ```
   WebSearch: "OpenAI API key validation"
   WebSearch: "OpenAI authentication best practices"
   ```

### Category 2: Rate Limiting

**Symptoms:**
- "Rate limit exceeded"
- 429 status code
- "Too many requests"

**Debugging process:**

1. **Check current rate limits:**
   ```
   WebFetch: https://platform.openai.com/docs/guides/rate-limits
   Prompt: "What are the current rate limits for [your-tier]?"
   ```

2. **Search for rate limit handling:**
   ```
   WebSearch: "OpenAI rate limit best practices 2025"
   WebSearch: "OpenAI exponential backoff implementation"
   ```

3. **Implement retry logic:**
   - Use exponential backoff
   - Check retry-after header
   - Limit concurrent requests

4. **Monitor usage:**
   - Check OpenAI dashboard
   - Log request rates
   - Implement throttling

### Category 3: Model or Feature Not Available

**Symptoms:**
- "Model not found"
- "Feature not supported"
- "Invalid parameter"

**Debugging process:**

1. **Check current models:**
   ```
   WebSearch: "OpenAI models 2025"
   WebSearch: "OpenAI [model-name] availability"
   ```

2. **Verify feature support:**
   ```
   WebSearch: "OpenAI [model-name] capabilities"
   WebSearch: "OpenAI [feature] model support"
   ```

3. **Check parameter names:**
   ```
   WebFetch: https://platform.openai.com/docs/api-reference/responses/create
   Prompt: "List all valid parameters"
   ```

4. **Search for deprecations:**
   ```
   WebSearch: "OpenAI deprecated features 2025"
   WebSearch: "OpenAI [feature] replacement"
   ```

### Category 4: Unexpected Responses

**Symptoms:**
- Empty responses
- Truncated output
- Wrong format
- Missing expected fields

**Debugging process:**

1. **Check response status:**
   ```python
   # Verify: current response attributes
   if response.incomplete_details:
       print(f"Incomplete: {response.incomplete_details.reason}")

   if response.error:
       print(f"Error: {response.error}")
   ```

2. **Verify token limits:**
   ```
   WebSearch: "OpenAI [model-name] token limits"
   WebSearch: "OpenAI max_output_tokens"
   ```

3. **Check response format:**
   ```
   WebSearch: "OpenAI Responses API output structure"
   WebFetch: https://platform.openai.com/docs/api-reference/responses
   Prompt: "Explain the response object structure"
   ```

4. **Inspect actual response:**
   ```python
   import json
   print(json.dumps(response.model_dump(), indent=2))
   ```

### Category 5: Streaming Issues

**Symptoms:**
- Stream hangs
- Events not received
- Incomplete streams
- Wrong event types

**Debugging process:**

1. **Verify streaming syntax:**
   ```
   WebFetch: https://platform.openai.com/docs/api-reference/streaming
   Prompt: "Show current streaming event types and example"
   ```

2. **Check event types:**
   ```
   Tool: mcp__deepwiki__ask_question
   repoName: "openai/openai-python"
   question: "What are all the streaming event types?"
   ```

3. **Add event logging:**
   ```python
   for event in stream:
       print(f"Event type: {event.type}")
       print(f"Event data: {event}")
   ```

4. **Test without streaming:**
   - Does non-streaming work?
   - If yes: SDK streaming issue
   - If no: General API issue

### Category 6: Type or Import Errors

**Symptoms:**
- Import fails
- Type errors in TypeScript
- Module not found
- Attribute errors

**Debugging process:**

1. **Verify installation:**
   ```bash
   pip show openai  # Python
   npm list openai  # TypeScript
   ```

2. **Check import paths:**
   ```
   Tool: mcp__deepwiki__ask_question
   repoName: "openai/openai-python"
   question: "What are the correct import paths?"
   ```

3. **Search for breaking changes:**
   ```
   WebSearch: "OpenAI SDK import changes [version]"
   WebSearch: "OpenAI SDK migration guide"
   ```

4. **Reinstall if needed:**
   ```bash
   pip install --upgrade --force-reinstall openai
   npm install openai@latest
   ```

### Category 7: Structured Output Issues

**Symptoms:**
- Invalid JSON
- Schema validation fails
- Wrong format returned
- Pydantic/Zod errors

**Debugging process:**

1. **Check model support:**
   ```
   WebSearch: "OpenAI structured output model support"
   WebSearch: "OpenAI [model-name] json_schema support"
   ```

2. **Verify schema format:**
   ```
   WebFetch: https://platform.openai.com/docs/guides/structured-outputs
   Prompt: "Show JSON schema format requirements"
   ```

3. **Test with json_object first:**
   ```python
   # Try simpler mode first
   response = client.responses.create(
       model="gpt-4o",
       input="...",
       text={"format": {"type": "json_object"}}
   )
   ```

4. **Validate schema separately:**
   ```python
   # Test Pydantic model
   test_data = '{"field": "value"}'
   MyModel.model_validate_json(test_data)
   ```

### Category 8: Function Calling Issues

**Symptoms:**
- Functions not called
- Wrong arguments
- Call loop doesn't work
- Function output ignored

**Debugging process:**

1. **Verify tool definition format:**
   ```
   WebFetch: https://platform.openai.com/docs/guides/function-calling
   Prompt: "Show correct tool definition format"
   ```

2. **Check tool_choice:**
   ```
   WebSearch: "OpenAI tool_choice options"
   # Try: "auto", "required", specific tool
   ```

3. **Inspect function calls:**
   ```python
   for item in response.output:
       print(f"Item type: {item.type}")
       if item.type == "function_call":
           print(f"Function: {item.name}")
           print(f"Args: {item.arguments}")
   ```

4. **Verify result format:**
   ```
   WebSearch: "OpenAI function call result format"
   # Check how to send function output back
   ```

## Debugging Checklist

When you encounter an issue, work through this checklist:

- [ ] Collected exact error message and stack trace
- [ ] Checked SDK version (pip show / npm list)
- [ ] Searched for error message in documentation
- [ ] Fetched latest API reference for the feature
- [ ] Created minimal reproduction
- [ ] Verified API key is valid
- [ ] Checked for recent breaking changes
- [ ] Compared code with official examples
- [ ] Tested with simplest possible request
- [ ] Checked GitHub issues for similar problems
- [ ] Verified model supports the feature
- [ ] Inspected actual response structure
- [ ] Added debug logging
- [ ] Tried with different parameters

## Advanced Debugging Techniques

### Enable Debug Logging

**Python:**
```python
import logging

# Enable OpenAI SDK debug logs
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('openai')
logger.setLevel(logging.DEBUG)
```

**TypeScript:**
```typescript
// Check if SDK provides debug mode
// Search: "OpenAI Node SDK debug logging"
```

### Inspect Raw HTTP Requests

**Python (with httpx):**
```python
# If SDK uses httpx, enable request logging
# Check current SDK implementation
```

**Capture network traffic:**
- Use tools like mitmproxy
- Inspect actual API requests/responses
- Compare with documentation

### Bisect SDK Versions

If issue started recently:

1. Find last working version
2. Find first broken version
3. Check changelog between versions
4. Search for relevant changes

### Check Community Solutions

```
WebSearch: "OpenAI [your-issue] stackoverflow"
WebSearch: "OpenAI [your-issue] reddit"
WebSearch: "site:github.com openai [issue]"
```

## When to Update the Skill

If you consistently find that:
- API has fundamentally changed
- New features added
- Major SDK refactor
- Documentation structure changed

Then: Update this skill to reflect new patterns!

But for individual errors: **Always search first, don't rely on cached knowledge.**

## Remember

1. **Don't guess** - Search for current information
2. **Verify everything** - Compare with latest docs
3. **Isolate the issue** - Create minimal reproduction
4. **Check versions** - SDK version matters
5. **Read changelogs** - Breaking changes happen
6. **Test incrementally** - Add complexity slowly
7. **Log everything** - Debug information is crucial
8. **Ask specifically** - Use precise search terms

The methodology is the same regardless of the specific issue: **Research current documentation, verify your code against it, and test systematically.**
