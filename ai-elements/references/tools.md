# Tool Patterns Reference

## Contents
- Tool Types Overview
- Server-Side Tools
- Client-Side Auto-Execute Tools
- User Interaction Tools
- Tool Part States
- Multi-Step Tool Calls
- Dynamic Tools
- Error Handling
- Type Inference

## Tool Types Overview

| Type | Execution | Use Case |
|------|-----------|----------|
| Server-side | Automatic on server | API calls, database queries |
| Client auto-execute | Automatic via `onToolCall` | Browser APIs, local data |
| User interaction | Manual via UI | Confirmations, user input |

## Server-Side Tools

Tools with `execute` function run automatically on server:

```ts
// app/api/chat/route.ts
import { z } from 'zod';
import { convertToModelMessages, streamText, UIMessage } from 'ai';

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  const result = streamText({
    model: yourModel,
    messages: convertToModelMessages(messages),
    tools: {
      getWeather: {
        description: 'Get weather for a location',
        inputSchema: z.object({
          city: z.string().describe('City name'),
        }),
        execute: async ({ city }) => {
          const data = await fetchWeatherAPI(city);
          return { city, weather: data.condition, temp: data.temperature };
        },
      },
    },
  });

  return result.toUIMessageStreamResponse();
}
```

## Client-Side Auto-Execute Tools

Tools without `execute` handled via `onToolCall`:

```tsx
// Server: define tool without execute
tools: {
  getLocation: {
    description: 'Get user location',
    inputSchema: z.object({}),
    // No execute = client-side tool
  },
}

// Client: handle in onToolCall
const { addToolOutput } = useChat({
  async onToolCall({ toolCall }) {
    if (toolCall.dynamic) return; // Type guard
    
    if (toolCall.toolName === 'getLocation') {
      const position = await navigator.geolocation.getCurrentPosition();
      addToolOutput({
        tool: 'getLocation',
        toolCallId: toolCall.toolCallId,
        output: { lat: position.coords.latitude, lng: position.coords.longitude },
      });
    }
  },
  sendAutomaticallyWhen: lastAssistantMessageIsCompleteWithToolCalls,
});
```

## User Interaction Tools

Tools requiring user input rendered in UI:

```tsx
// Server
tools: {
  askForConfirmation: {
    description: 'Ask user for confirmation',
    inputSchema: z.object({
      message: z.string().describe('Confirmation message'),
    }),
    // No execute = rendered in UI
  },
}

// Client: render UI for tool
{message.parts.map((part, i) => {
  if (part.type === 'tool-askForConfirmation') {
    if (part.state === 'input-available') {
      return (
        <div key={i}>
          <p>{part.input.message}</p>
          <button onClick={() => addToolOutput({
            tool: 'askForConfirmation',
            toolCallId: part.toolCallId,
            output: 'confirmed',
          })}>Yes</button>
          <button onClick={() => addToolOutput({
            tool: 'askForConfirmation',
            toolCallId: part.toolCallId,
            output: 'denied',
          })}>No</button>
        </div>
      );
    }
    if (part.state === 'output-available') {
      return <div key={i}>User responded: {part.output}</div>;
    }
  }
})}
```

## Tool Part States

| State | Description |
|-------|-------------|
| `input-streaming` | Tool input being generated |
| `input-available` | Input ready, awaiting execution |
| `output-available` | Tool executed successfully |
| `output-error` | Tool execution failed |

```tsx
switch (part.state) {
  case 'input-streaming':
    return <div>Preparing {part.toolName}...</div>;
  case 'input-available':
    return <div>Executing {part.toolName} with {JSON.stringify(part.input)}</div>;
  case 'output-available':
    return <div>Result: {JSON.stringify(part.output)}</div>;
  case 'output-error':
    return <div>Error: {part.errorText}</div>;
}
```

## Multi-Step Tool Calls

Enable automatic continuation with `stopWhen`:

```ts
import { stepCountIs } from 'ai';

const result = streamText({
  model: yourModel,
  messages: convertToModelMessages(messages),
  tools: { /* ... */ },
  stopWhen: stepCountIs(5), // Max 5 steps
});
```

Render step boundaries:

```tsx
{message.parts.map((part, i) => {
  if (part.type === 'step-start' && i > 0) {
    return <hr key={i} />;
  }
  // ... render other parts
})}
```

## Dynamic Tools

For runtime-defined tools (MCP, user functions):

```tsx
{message.parts.map((part, i) => {
  // Static tools
  if (part.type === 'tool-getWeather') {
    return <WeatherCard key={i} {...part.output} />;
  }
  
  // Dynamic tools
  if (part.type === 'dynamic-tool') {
    return (
      <div key={i}>
        <h4>Tool: {part.toolName}</h4>
        {part.state === 'output-available' && (
          <pre>{JSON.stringify(part.output, null, 2)}</pre>
        )}
      </div>
    );
  }
})}
```

## Error Handling

### Client-Side Tool Errors

```tsx
onToolCall: async ({ toolCall }) => {
  if (toolCall.toolName === 'riskyTool') {
    try {
      const result = await executeRiskyTool(toolCall.input);
      addToolOutput({
        tool: 'riskyTool',
        toolCallId: toolCall.toolCallId,
        output: result,
      });
    } catch (err) {
      addToolOutput({
        tool: 'riskyTool',
        toolCallId: toolCall.toolCallId,
        state: 'output-error',
        errorText: 'Failed to execute tool',
      });
    }
  }
}
```

### Server-Side Error Masking

```ts
return result.toUIMessageStreamResponse({
  onError: (error) => {
    // Return user-friendly message (default: "An error occurred")
    if (error instanceof Error) return error.message;
    return 'Unknown error';
  },
});
```

## Type Inference

```tsx
import { InferUITool, InferUITools } from 'ai';

// Single tool type
type WeatherTool = InferUITool<typeof weatherTool>;
// { input: { city: string }; output: { weather: string; temp: number } }

// All tools type
type MyTools = InferUITools<typeof tools>;
// { getWeather: {...}; askForConfirmation: {...} }

// Use in custom UIMessage
type MyUIMessage = UIMessage<never, UIDataTypes, MyTools>;
const { messages } = useChat<MyUIMessage>({...});
```
