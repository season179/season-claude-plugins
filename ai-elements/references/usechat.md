# useChat Reference

## Contents
- Basic Setup
- Transport Configuration
- Return Values
- Event Callbacks
- Request Configuration
- Message Management
- Type Inference
- Common Patterns

## Basic Setup

```tsx
import { useChat } from '@ai-sdk/react';
import { DefaultChatTransport } from 'ai';

const { messages, sendMessage, status, error, stop, reload, setMessages, addToolOutput } = useChat({
  transport: new DefaultChatTransport({ api: '/api/chat' }),
  id: 'my-chat', // Optional: shared state across components
  initialMessages: [], // Optional: pre-populate messages
});
```

## Transport Configuration

### DefaultChatTransport Options

```tsx
new DefaultChatTransport({
  api: '/api/chat',
  headers: { Authorization: 'Bearer token' },
  body: { userId: '123' },
  credentials: 'same-origin',
})
```

### Dynamic Configuration

```tsx
new DefaultChatTransport({
  api: '/api/chat',
  headers: () => ({ Authorization: `Bearer ${getToken()}` }),
  body: () => ({ sessionId: getSessionId() }),
})
```

### Custom Request Preparation

```tsx
new DefaultChatTransport({
  prepareSendMessagesRequest: ({ id, messages, trigger, messageId }) => {
    if (trigger === 'submit-user-message') {
      return { body: { id, message: messages[messages.length - 1] } };
    }
    if (trigger === 'regenerate-assistant-message') {
      return { body: { id, messageId, regenerate: true } };
    }
    throw new Error(`Unsupported trigger: ${trigger}`);
  },
})
```

### Text Stream Transport

```tsx
import { TextStreamChatTransport } from 'ai';

// For plain text streams (no tool calls, usage info, or finish reasons)
const { messages } = useChat({
  transport: new TextStreamChatTransport({ api: '/api/chat' }),
});
```

## Return Values

| Property | Type | Description |
|----------|------|-------------|
| `messages` | `UIMessage[]` | Array of chat messages |
| `status` | `'ready' \| 'submitted' \| 'streaming' \| 'error'` | Current chat status |
| `error` | `Error \| undefined` | Error from last request |
| `sendMessage` | `(message, options?) => void` | Send a new message |
| `stop` | `() => void` | Abort current stream |
| `reload` | `(options?) => void` | Regenerate last assistant message |
| `regenerate` | `(messageId?) => void` | Regenerate specific message |
| `setMessages` | `(messages) => void` | Update messages locally |
| `addToolOutput` | `(output) => void` | Provide tool result |

## Event Callbacks

```tsx
useChat({
  onFinish: ({ message, messages, isAbort, isDisconnect, isError }) => {
    console.log('Response complete', message);
  },
  onError: (error) => {
    console.error('Request failed:', error);
  },
  onData: (dataPart) => {
    // Handle streaming data parts (including transient)
    if (dataPart.type === 'data-notification') {
      showToast(dataPart.data.message);
    }
  },
  onToolCall: async ({ toolCall }) => {
    // Handle client-side tool execution
    if (toolCall.dynamic) return;
    if (toolCall.toolName === 'myTool') {
      addToolOutput({
        tool: 'myTool',
        toolCallId: toolCall.toolCallId,
        output: await executeMyTool(toolCall.input),
      });
    }
  },
  sendAutomaticallyWhen: lastAssistantMessageIsCompleteWithToolCalls,
})
```

## Request Configuration

### Per-Request Options (Recommended)

```tsx
sendMessage(
  { text: input },
  {
    headers: { 'X-Custom': 'value' },
    body: { temperature: 0.7, userId: '123' },
    metadata: { sessionId: 'session456' },
  }
);
```

### Server-Side Access

```ts
export async function POST(req: Request) {
  const { messages, temperature, userId } = await req.json();
  // Use custom body fields
}
```

## Message Management

### Modifying Messages

```tsx
const { messages, setMessages } = useChat({...});

// Delete a message
const handleDelete = (id: string) => {
  setMessages(messages.filter(m => m.id !== id));
};

// Edit a message
const handleEdit = (id: string, newText: string) => {
  setMessages(messages.map(m => 
    m.id === id ? { ...m, parts: [{ type: 'text', text: newText }] } : m
  ));
};
```

### Stop and Regenerate

```tsx
const { stop, reload, regenerate, status } = useChat({...});

<button onClick={stop} disabled={status === 'ready'}>Stop</button>
<button onClick={() => reload()} disabled={status !== 'ready'}>Retry Last</button>
<button onClick={() => regenerate(messageId)}>Regenerate This</button>
```

## Type Inference

### Custom UIMessage Type

```tsx
import { UIMessage, InferUITools, UIDataTypes } from 'ai';

// Define tools type
type MyUITools = InferUITools<typeof tools>;

// Define metadata type
type MyMetadata = { totalTokens: number; model: string };

// Create custom message type
type MyUIMessage = UIMessage<MyMetadata, UIDataTypes, MyUITools>;

// Use in hook
const { messages } = useChat<MyUIMessage>({...});
```

### Accessing Typed Metadata

```tsx
{messages.map(m => (
  <div key={m.id}>
    {m.metadata?.totalTokens && <span>{m.metadata.totalTokens} tokens</span>}
  </div>
))}
```

## Common Patterns

### Throttled UI Updates

```tsx
useChat({
  experimental_throttle: 50, // Update UI every 50ms max
})
```

### Stream Resume on Disconnect

```tsx
useChat({
  experimental_resumeStream: true,
})
```

### Shared Chat State

```tsx
// Component A
const chatA = useChat({ id: 'shared-chat' });

// Component B - same state!
const chatB = useChat({ id: 'shared-chat' });
```
