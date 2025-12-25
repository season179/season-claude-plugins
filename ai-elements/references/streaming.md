# Streaming Data Reference

## Contents
- Overview
- Type-Safe Setup
- Data Parts
- Sources
- Transient Data
- Data Reconciliation
- Processing on Client
- Use Cases

## Overview

Stream additional data alongside model responses using:
- `createUIMessageStream`: Create a data stream
- `createUIMessageStreamResponse`: Create streaming response
- `pipeUIMessageStreamToResponse`: Pipe to Node.js response

## Type-Safe Setup

Define custom message type with data part schemas:

```ts
// ai/types.ts
import { UIMessage } from 'ai';

export type MyUIMessage = UIMessage<
  never, // metadata type
  {
    weather: { city: string; weather?: string; status: 'loading' | 'success' };
    notification: { message: string; level: 'info' | 'warning' | 'error' };
  }
>;
```

## Server Implementation

```ts
import {
  createUIMessageStream,
  createUIMessageStreamResponse,
  streamText,
  convertToModelMessages,
} from 'ai';
import type { MyUIMessage } from '@/ai/types';

export async function POST(req: Request) {
  const { messages } = await req.json();

  const stream = createUIMessageStream<MyUIMessage>({
    execute: ({ writer }) => {
      // 1. Send loading state
      writer.write({
        type: 'data-weather',
        id: 'weather-1',
        data: { city: 'San Francisco', status: 'loading' },
      });

      const result = streamText({
        model: yourModel,
        messages: convertToModelMessages(messages),
        onFinish() {
          // 2. Update with final data (same ID = reconciliation)
          writer.write({
            type: 'data-weather',
            id: 'weather-1',
            data: { city: 'San Francisco', weather: 'sunny', status: 'success' },
          });
        },
      });

      writer.merge(result.toUIMessageStream());
    },
  });

  return createUIMessageStreamResponse({ stream });
}
```

## Data Parts (Persistent)

Added to message history, available in `message.parts`:

```ts
writer.write({
  type: 'data-weather',
  id: 'weather-1', // Optional: enables reconciliation
  data: { city: 'San Francisco', status: 'loading' },
});
```

## Sources

For RAG implementations showing referenced content:

```ts
writer.write({
  type: 'source',
  value: {
    type: 'source',
    sourceType: 'url',
    id: 'source-1',
    url: 'https://example.com',
    title: 'Example Source',
  },
});
```

Render sources:
```tsx
{message.parts
  .filter(part => part.type === 'source-url')
  .map(part => (
    <a key={part.id} href={part.url}>{part.title}</a>
  ))}
```

## Transient Data (Ephemeral)

Not added to message history, only via `onData`:

```ts
// Server
writer.write({
  type: 'data-notification',
  data: { message: 'Processing...', level: 'info' },
  transient: true, // Won't appear in message.parts
});

// Client
const [notification, setNotification] = useState<string>();

const { messages } = useChat({
  onData: (dataPart) => {
    if (dataPart.type === 'data-notification') {
      setNotification(dataPart.data.message);
    }
  },
});
```

## Data Reconciliation

Same ID updates existing part automatically:

```ts
// Initial loading state
writer.write({
  type: 'data-artifact',
  id: 'code-1',
  data: { content: '', status: 'generating' },
});

// Update as content streams
writer.write({
  type: 'data-artifact',
  id: 'code-1', // Same ID = update
  data: { content: partialCode, status: 'generating' },
});

// Final state
writer.write({
  type: 'data-artifact',
  id: 'code-1',
  data: { content: finalCode, status: 'complete' },
});
```

Use cases:
- **Collaborative artifacts**: Update code/documents in real-time
- **Progressive loading**: Loading → partial → complete
- **Live status**: Progress bars, counters
- **Interactive components**: Evolving UI elements

## Processing on Client

### onData Callback

Essential for transient parts:

```tsx
const { messages } = useChat<MyUIMessage>({
  onData: (dataPart) => {
    console.log('Received:', dataPart);
    
    if (dataPart.type === 'data-weather') {
      console.log('Weather update:', dataPart.data);
    }
    
    // Transient parts ONLY available here
    if (dataPart.type === 'data-notification') {
      showToast(dataPart.data.message, dataPart.data.level);
    }
  },
});
```

### Rendering Persistent Parts

```tsx
{messages.map(message => (
  <div key={message.id}>
    {/* Weather data */}
    {message.parts
      .filter(part => part.type === 'data-weather')
      .map((part, i) => (
        <div key={i}>
          {part.data.status === 'loading'
            ? `Getting weather for ${part.data.city}...`
            : `Weather in ${part.data.city}: ${part.data.weather}`}
        </div>
      ))}

    {/* Text content */}
    {message.parts
      .filter(part => part.type === 'text')
      .map((part, i) => <div key={i}>{part.text}</div>)}

    {/* Sources */}
    {message.parts
      .filter(part => part.type === 'source-url')
      .map(part => (
        <a key={part.id} href={part.url}>{part.title}</a>
      ))}
  </div>
))}
```

## Use Cases

| Use Case | Data Type | Transient? |
|----------|-----------|------------|
| RAG sources | `source` | No |
| Loading indicators | Custom data | Yes |
| Progress updates | Custom data | Yes |
| Collaborative editing | Custom data with ID | No |
| Toast notifications | Custom data | Yes |
| Token usage | Message metadata | No |

## Message Metadata vs Data Parts

| Aspect | Message Metadata | Data Parts |
|--------|-----------------|------------|
| Scope | Message-level | Part-level |
| Access | `message.metadata` | `message.parts` |
| Updates | Set once | Can reconcile |
| Transient | No | Yes |
| Use for | Timestamps, tokens, model | Dynamic content, sources |
