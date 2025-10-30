# TypeScript Patterns for OpenAI Responses API

This guide provides general TypeScript patterns and best practices for working with the OpenAI Node.js SDK. These patterns are language-specific and remain relatively stable, though **always verify current SDK syntax**.

## TypeScript Configuration

### Recommended tsconfig.json
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "lib": ["ES2022"],
    "moduleResolution": "node",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  }
}
```

### Package.json Setup
```json
{
  "type": "module",
  "dependencies": {
    "openai": "^4.0.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "typescript": "^5.0.0",
    "tsx": "^4.0.0"
  }
}
```

## Import Patterns

### ES Modules (Recommended)
```typescript
// Verify: current import syntax
import OpenAI from 'openai';
import type { Response, ResponseCreateParams } from 'openai/resources/responses';

// For environment variables
import * as dotenv from 'dotenv';
dotenv.config();
```

### CommonJS (If Required)
```typescript
// Verify if still supported
const OpenAI = require('openai');
```

### Type Imports
```typescript
// Import only types (erased at runtime)
import type {
  ChatCompletionMessageParam,
  ResponseCreateParams,
  Response,
} from 'openai/resources';
```

## Client Initialization Patterns

### Basic Client
```typescript
// Verify: current initialization syntax
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// Or use default (reads from OPENAI_API_KEY env var)
const client = new OpenAI();
```

### Client with Configuration
```typescript
// Verify: available configuration options
const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  timeout: 30000,  // Check: parameter name
  maxRetries: 3,   // Check: parameter name
  // Verify: other available options in docs
});
```

### Configuration Type
```typescript
interface OpenAIConfig {
  apiKey: string;
  model: string;
  temperature: number;
  maxTokens: number;
}

const config: OpenAIConfig = {
  apiKey: process.env.OPENAI_API_KEY!,
  model: 'gpt-4o',
  temperature: 0.7,
  maxTokens: 1000,
};

const client = new OpenAI({ apiKey: config.apiKey });
```

## Type-Safe Response Handling

### Basic Response
```typescript
// Verify: response type
async function generate(prompt: string): Promise<string> {
  const response = await client.responses.create({
    model: 'gpt-4o',
    input: prompt,
  });

  // Verify: response properties
  return response.output_text;
}
```

### Response with Full Type
```typescript
// Verify: import path for Response type
import type { Response } from 'openai/resources/responses';

async function generateTyped(prompt: string): Promise<Response> {
  const response = await client.responses.create({
    model: 'gpt-4o',
    input: prompt,
  });

  return response;
}
```

### Checking Response Status
```typescript
async function safeGenerate(prompt: string): Promise<string | null> {
  const response = await client.responses.create({
    model: 'gpt-4o',
    input: prompt,
  });

  // Verify: status checking properties
  if (response.incomplete_details) {
    console.error(`Incomplete: ${response.incomplete_details.reason}`);
    return null;
  }

  if (response.error) {
    console.error(`Error: ${response.error}`);
    return null;
  }

  return response.output_text;
}
```

### Accessing Output Items
```typescript
// Verify: output item types
async function processOutput(prompt: string): Promise<void> {
  const response = await client.responses.create({
    model: 'gpt-4o',
    input: prompt,
  });

  for (const item of response.output) {
    // Verify: available item types
    if (item.type === 'message') {
      console.log(item.content);
    } else if (item.type === 'function_call') {
      console.log(`Function: ${item.name}`);
      console.log(`Args: ${item.arguments}`);
    }
  }
}
```

## Streaming Patterns

### Basic Streaming
```typescript
// Verify: streaming syntax
async function stream(prompt: string): Promise<string> {
  const stream = await client.responses.create({
    model: 'gpt-4o',
    input: prompt,
    stream: true,
  });

  let fullText = '';

  // Verify: for-await-of syntax and event types
  for await (const event of stream) {
    if (event.type === 'response.output_text.delta') {  // Check type name
      fullText += event.delta;
      process.stdout.write(event.delta);
    }
  }

  return fullText;
}
```

### Streaming with Event Types
```typescript
// Verify: event type definitions
type StreamEvent = {
  type: string;
  delta?: string;
  error?: string;
};

async function streamTyped(prompt: string): Promise<string> {
  const stream = await client.responses.create({
    model: 'gpt-4o',
    input: prompt,
    stream: true,
  });

  let fullText = '';

  for await (const event of stream) {
    switch (event.type) {
      case 'response.output_text.delta':  // Verify type names
        if (event.delta) {
          fullText += event.delta;
          process.stdout.write(event.delta);
        }
        break;
      case 'error':
        console.error(`Stream error: ${event.error}`);
        break;
      case 'response.done':
        console.log('\n[Complete]');
        break;
    }
  }

  return fullText;
}
```

### Streaming with Error Handling
```typescript
async function streamWithErrors(prompt: string): Promise<string> {
  let fullText = '';

  try {
    const stream = await client.responses.create({
      model: 'gpt-4o',
      input: prompt,
      stream: true,
    });

    for await (const event of stream) {
      if (event.type === 'error') {
        throw new Error(`Stream error: ${event.error}`);
      } else if (event.type === 'response.output_text.delta') {
        fullText += event.delta;
      }
    }
  } catch (error) {
    console.error('Streaming failed:', error);
    throw error;
  }

  return fullText;
}
```

## Async/Await Patterns

### Basic Async Function
```typescript
async function asyncGenerate(prompt: string): Promise<string> {
  const response = await client.responses.create({
    model: 'gpt-4o',
    input: prompt,
  });

  return response.output_text;
}

// Usage
const result = await asyncGenerate('Hello');
```

### Concurrent Requests with Promise.all
```typescript
async function processBatch(prompts: string[]): Promise<string[]> {
  const promises = prompts.map(prompt =>
    client.responses.create({
      model: 'gpt-4o',
      input: prompt,
    })
  );

  const responses = await Promise.all(promises);
  return responses.map(r => r.output_text);
}

// Usage
const prompts = ['Prompt 1', 'Prompt 2', 'Prompt 3'];
const results = await processBatch(prompts);
```

### Concurrent with Error Handling
```typescript
interface Result {
  success: boolean;
  text?: string;
  error?: string;
  prompt: string;
}

async function safeGenerate(prompt: string): Promise<Result> {
  try {
    const response = await client.responses.create({
      model: 'gpt-4o',
      input: prompt,
    });
    return {
      success: true,
      text: response.output_text,
      prompt,
    };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : String(error),
      prompt,
    };
  }
}

async function processBatchSafe(prompts: string[]): Promise<Result[]> {
  const promises = prompts.map(safeGenerate);
  return Promise.all(promises);
}
```

### Promise.allSettled for Mixed Results
```typescript
async function processBatchMixed(prompts: string[]): Promise<PromiseSettledResult<string>[]> {
  const promises = prompts.map(prompt =>
    client.responses.create({
      model: 'gpt-4o',
      input: prompt,
    }).then(r => r.output_text)
  );

  return Promise.allSettled(promises);
}

// Usage
const results = await processBatchMixed(prompts);
results.forEach((result, index) => {
  if (result.status === 'fulfilled') {
    console.log(`Success ${index}: ${result.value}`);
  } else {
    console.error(`Failed ${index}: ${result.reason}`);
  }
});
```

### Rate-Limited Concurrent Requests
```typescript
class Semaphore {
  private counter: number;
  private waiting: Array<() => void> = [];

  constructor(max: number) {
    this.counter = max;
  }

  async acquire(): Promise<void> {
    if (this.counter > 0) {
      this.counter--;
      return;
    }

    return new Promise(resolve => {
      this.waiting.push(resolve);
    });
  }

  release(): void {
    this.counter++;
    const resolve = this.waiting.shift();
    if (resolve) {
      this.counter--;
      resolve();
    }
  }
}

async function rateLimitedBatch(
  prompts: string[],
  maxConcurrent: number = 5
): Promise<string[]> {
  const semaphore = new Semaphore(maxConcurrent);

  const promises = prompts.map(async prompt => {
    await semaphore.acquire();

    try {
      const response = await client.responses.create({
        model: 'gpt-4o',
        input: prompt,
      });
      return response.output_text;
    } finally {
      semaphore.release();
    }
  });

  return Promise.all(promises);
}
```

### Progress Tracking
```typescript
async function processWithProgress(prompts: string[]): Promise<string[]> {
  const total = prompts.length;
  let completed = 0;

  const results = await Promise.all(
    prompts.map(async prompt => {
      const response = await client.responses.create({
        model: 'gpt-4o',
        input: prompt,
      });

      completed++;
      console.log(`Progress: ${completed}/${total}`);

      return response.output_text;
    })
  );

  return results;
}
```

## Error Handling Patterns

### Comprehensive Error Handling
```typescript
// Verify: current error types
import { APIError, OpenAIError } from 'openai';

async function safeRequest(prompt: string): Promise<string | null> {
  try {
    const response = await client.responses.create({
      model: 'gpt-4o',
      input: prompt,
    });
    return response.output_text;

  } catch (error) {
    if (error instanceof OpenAI.APIError) {
      // Verify: error properties
      console.error('API Error:', {
        status: error.status,
        message: error.message,
        code: error.code,
      });
    } else if (error instanceof Error) {
      console.error('Error:', error.message);
    } else {
      console.error('Unknown error:', error);
    }

    return null;
  }
}
```

### Retry with Exponential Backoff
```typescript
async function retry<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  baseDelay: number = 1000
): Promise<T> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      // Check if error is retryable
      const isRateLimitError =
        error instanceof OpenAI.APIError && error.status === 429;

      const isServerError =
        error instanceof OpenAI.APIError && error.status >= 500;

      if (!isRateLimitError && !isServerError) {
        throw error;  // Don't retry non-retryable errors
      }

      if (attempt === maxRetries - 1) {
        throw error;  // Last attempt failed
      }

      const delay = baseDelay * Math.pow(2, attempt);
      console.log(`Retry attempt ${attempt + 1} in ${delay}ms...`);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }

  throw new Error('Should not reach here');
}

// Usage
const response = await retry(() =>
  client.responses.create({
    model: 'gpt-4o',
    input: 'Hello',
  })
);
```

### Custom Error Types
```typescript
class GenerationError extends Error {
  constructor(
    message: string,
    public readonly cause?: Error,
    public readonly prompt?: string
  ) {
    super(message);
    this.name = 'GenerationError';
  }
}

async function generateOrThrow(prompt: string): Promise<string> {
  try {
    const response = await client.responses.create({
      model: 'gpt-4o',
      input: prompt,
    });
    return response.output_text;
  } catch (error) {
    throw new GenerationError(
      'Failed to generate response',
      error instanceof Error ? error : undefined,
      prompt
    );
  }
}
```

## Structured Output Patterns

### Using Zod for Validation
```typescript
import { z } from 'zod';

// Define schema
const ArticleSchema = z.object({
  title: z.string(),
  author: z.string(),
  summary: z.string(),
  tags: z.array(z.string()),
});

type Article = z.infer<typeof ArticleSchema>;

async function extractArticle(text: string): Promise<Article> {
  // Verify: structured output syntax
  const response = await client.responses.create({
    model: 'gpt-4o',  // Check model support
    input: `Extract article info: ${text}`,
    text: {
      format: {
        type: 'json_schema',
        json_schema: {
          name: 'article',
          schema: zodToJsonSchema(ArticleSchema),  // Check helper
        },
      },
    },
  });

  // Parse and validate
  const parsed = JSON.parse(response.output_text);
  return ArticleSchema.parse(parsed);
}
```

### Converting Zod to JSON Schema
```typescript
import { zodToJsonSchema } from 'zod-to-json-schema';

function zodToOpenAISchema<T extends z.ZodType>(
  schema: T,
  name: string
) {
  return {
    name,
    schema: zodToJsonSchema(schema, name),
  };
}

// Usage
const responseSchema = zodToOpenAISchema(ArticleSchema, 'article');
```

### TypeScript Interfaces (without validation)
```typescript
interface Product {
  id: string;
  name: string;
  price: number;
  tags: string[];
}

async function extractProduct(text: string): Promise<Product> {
  const response = await client.responses.create({
    model: 'gpt-4o',
    input: `Extract product info: ${text}`,
    text: {
      format: {
        type: 'json_object',  // Simple JSON mode
      },
    },
  });

  // Parse (no validation)
  return JSON.parse(response.output_text) as Product;
}
```

### Handling Validation Errors
```typescript
async function safeExtract(text: string): Promise<Article | null> {
  try {
    const response = await client.responses.create(...);
    const parsed = JSON.parse(response.output_text);
    return ArticleSchema.parse(parsed);

  } catch (error) {
    if (error instanceof z.ZodError) {
      console.error('Validation errors:');
      error.errors.forEach(err => {
        console.error(`- ${err.path.join('.')}: ${err.message}`);
      });
    } else {
      console.error('Parsing error:', error);
    }
    return null;
  }
}
```

## Function Calling Patterns

### Type-Safe Function Definitions
```typescript
// Define function types
interface WeatherParams {
  location: string;
  unit: 'celsius' | 'fahrenheit';
}

interface WeatherResult {
  temp: number;
  unit: string;
  conditions: string;
}

function getWeather(params: WeatherParams): WeatherResult {
  // Implementation
  return {
    temp: 20,
    unit: params.unit,
    conditions: 'Sunny',
  };
}

// Verify: tool definition format
const tools = [{
  type: 'function' as const,
  function: {
    name: 'get_weather',
    description: 'Get current weather for a location',
    parameters: {
      type: 'object',
      properties: {
        location: {
          type: 'string',
          description: 'City name or coordinates',
        },
        unit: {
          type: 'string',
          enum: ['celsius', 'fahrenheit'],
          description: 'Temperature unit',
        },
      },
      required: ['location'],
    },
  },
}];
```

### Function Registry with Type Safety
```typescript
type FunctionHandler<T = any, R = any> = (params: T) => R | Promise<R>;

const functions = new Map<string, FunctionHandler>([
  ['get_weather', getWeather],
  ['search_web', searchWeb],
  ['query_db', queryDatabase],
]);

async function executeFunction(
  name: string,
  argumentsStr: string
): Promise<string> {
  const handler = functions.get(name);

  if (!handler) {
    return JSON.stringify({ error: `Unknown function: ${name}` });
  }

  try {
    const args = JSON.parse(argumentsStr);
    const result = await handler(args);
    return JSON.stringify(result);
  } catch (error) {
    return JSON.stringify({
      error: error instanceof Error ? error.message : String(error),
    });
  }
}
```

### Multi-Turn Agent
```typescript
async function agentWithTools(
  query: string,
  maxIterations: number = 5
): Promise<string> {
  let response = await client.responses.create({
    model: 'gpt-4o',
    input: query,
    tools,
    tool_choice: 'auto',
  });

  for (let i = 0; i < maxIterations; i++) {
    let hasFunctionCall = false;

    for (const item of response.output) {
      if (item.type === 'function_call') {
        hasFunctionCall = true;

        // Execute function
        const result = await executeFunction(item.name, item.arguments);

        // Send result back - verify syntax
        response = await client.responses.create({
          model: 'gpt-4o',
          previous_response_id: response.id,
          input: [{
            type: 'function_call_output',
            call_id: item.call_id,
            output: result,
          }],
        });
      }
    }

    if (!hasFunctionCall) {
      return response.output_text;
    }
  }

  return 'Max iterations reached';
}
```

## Configuration and Environment

### Environment Variables
```typescript
import * as dotenv from 'dotenv';
dotenv.config();

const apiKey = process.env.OPENAI_API_KEY;
if (!apiKey) {
  throw new Error('OPENAI_API_KEY not set');
}

const client = new OpenAI({ apiKey });
```

### Configuration Object
```typescript
interface Config {
  openai: {
    apiKey: string;
    model: string;
    temperature: number;
  };
}

function loadConfig(): Config {
  return {
    openai: {
      apiKey: process.env.OPENAI_API_KEY!,
      model: process.env.OPENAI_MODEL || 'gpt-4o',
      temperature: Number(process.env.OPENAI_TEMPERATURE) || 0.7,
    },
  };
}

const config = loadConfig();
const client = new OpenAI({ apiKey: config.openai.apiKey });
```

## Logging Patterns

### Simple Logging
```typescript
async function loggedRequest(prompt: string): Promise<string> {
  console.log(`[${new Date().toISOString()}] Generating response...`);

  const response = await client.responses.create({
    model: 'gpt-4o',
    input: prompt,
  });

  console.log(`[${new Date().toISOString()}] Response received`);
  return response.output_text;
}
```

### Structured Logging
```typescript
interface LogEntry {
  timestamp: string;
  level: 'info' | 'error' | 'warn';
  message: string;
  metadata?: Record<string, any>;
}

function log(level: LogEntry['level'], message: string, metadata?: Record<string, any>) {
  const entry: LogEntry = {
    timestamp: new Date().toISOString(),
    level,
    message,
    metadata,
  };
  console.log(JSON.stringify(entry));
}

async function trackedRequest(prompt: string): Promise<string> {
  const startTime = Date.now();

  log('info', 'Starting generation', { promptLength: prompt.length });

  try {
    const response = await client.responses.create({
      model: 'gpt-4o',
      input: prompt,
    });

    const duration = Date.now() - startTime;

    log('info', 'Generation complete', {
      duration,
      outputLength: response.output_text.length,
    });

    return response.output_text;
  } catch (error) {
    log('error', 'Generation failed', {
      error: error instanceof Error ? error.message : String(error),
    });
    throw error;
  }
}
```

## Testing Patterns

### Mocking with Jest
```typescript
import { jest } from '@jest/globals';

// Mock the OpenAI client
jest.mock('openai');

test('generation works', async () => {
  const mockCreate = jest.fn().mockResolvedValue({
    output_text: 'Test response',
    id: 'resp_123',
  });

  const MockOpenAI = OpenAI as jest.MockedClass<typeof OpenAI>;
  MockOpenAI.prototype.responses = {
    create: mockCreate,
  } as any;

  // Test your function
  const result = await yourFunction();
  expect(result).toBe('Test response');
  expect(mockCreate).toHaveBeenCalled();
});
```

## Best Practices Summary

1. **Use strict TypeScript** - Enable all strict checks
2. **Import types explicitly** - Use `import type` for types
3. **Leverage Zod for validation** - Type-safe structured outputs
4. **Use async/await** - Cleaner than Promises
5. **Handle errors comprehensively** - Check for specific error types
6. **Type your functions** - Full type annotations
7. **Use ES modules** - Modern import/export syntax
8. **Environment variables for config** - Never hardcode secrets
9. **Implement retry logic** - Handle transient failures
10. **Log structured data** - JSON logging for production
11. **Verify all syntax** - Always check current SDK documentation

Remember: These are **patterns**, not exact implementations. Always verify current SDK syntax and types against latest documentation!
