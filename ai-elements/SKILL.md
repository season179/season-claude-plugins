---
name: ai-elements
description: Provides React components and hooks for building AI chat interfaces with Vercel AI SDK. Covers useChat, useCompletion, useObject hooks for state management, plus pre-built UI components (Conversation, Message, PromptInput, Response, Tool, Reasoning) from shadcn/ui. Triggers on chatbots, conversational UIs, AI assistants, streaming responses, message.parts rendering, tool call UIs, generative UI, sendMessage, DefaultChatTransport, or production AI interface patterns with Next.js.
---

# AI SDK UI & Elements

Build AI chat interfaces using Vercel AI SDK hooks for state management and AI Elements components for production-ready UI.

## Verification with DeepWiki

Query DeepWiki when unsure about APIs, component props, or implementation patterns:

- **AI Elements**: `deepwiki("vercel/ai-elements")` - Component implementations, props
- **AI SDK**: `deepwiki("vercel/ai")` - Hooks, streaming, message formats

## Prerequisites

- Node.js 18+, Next.js with `@ai-sdk/react`
- React 19, Tailwind CSS 4 (CSS Variables mode)
- shadcn/ui initialized for AI Elements components

## Installation

```bash
# AI SDK (required)
npm install ai @ai-sdk/react

# AI Elements components (recommended)
npx ai-elements@latest
```

---

## Part 1: AI SDK Hooks

### Core Hooks

| Hook | Purpose | Server Function |
|------|---------|-----------------|
| `useChat` | Chat interfaces with streaming | `streamText` |
| `useCompletion` | Text completions | `streamText` |
| `useObject` | Streamed JSON objects | `streamObject` |

### useChat Quick Start

**Client:**
```tsx
'use client';
import { useChat } from '@ai-sdk/react';
import { DefaultChatTransport } from 'ai';
import { useState } from 'react';

export default function Chat() {
  const { messages, sendMessage, status } = useChat({
    transport: new DefaultChatTransport({ api: '/api/chat' }),
  });
  const [input, setInput] = useState('');

  return (
    <>
      {messages.map(message => (
        <div key={message.id}>
          {message.parts.map((part, i) =>
            part.type === 'text' ? <span key={i}>{part.text}</span> : null
          )}
        </div>
      ))}
      <form onSubmit={e => {
        e.preventDefault();
        if (input.trim()) { sendMessage({ text: input }); setInput(''); }
      }}>
        <input value={input} onChange={e => setInput(e.target.value)} disabled={status !== 'ready'} />
        <button type="submit" disabled={status !== 'ready'}>Send</button>
      </form>
    </>
  );
}
```

**Server:**
```ts
// app/api/chat/route.ts
import { convertToModelMessages, streamText, UIMessage } from 'ai';

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();
  const result = streamText({
    model: yourModel, // e.g., openai('gpt-4o')
    messages: convertToModelMessages(messages),
  });
  return result.toUIMessageStreamResponse();
}
```

### Message Parts

Always render using `message.parts` (not deprecated `content`):

```tsx
{message.parts.map((part, i) => {
  switch (part.type) {
    case 'text': return <span key={i}>{part.text}</span>;
    case 'reasoning': return <pre key={i}>{part.text}</pre>;
    case 'tool-myTool': return <MyToolComponent key={i} part={part} />;
    case 'source-url': return <a key={i} href={part.url}>{part.title}</a>;
    case 'file': return part.mediaType?.startsWith('image/') ? <img key={i} src={part.url} /> : null;
  }
})}
```

### Status States

| Status | Description |
|--------|-------------|
| `ready` | Idle, can submit |
| `submitted` | Request sent, awaiting response |
| `streaming` | Receiving chunks |
| `error` | Request failed |

```tsx
const { status, stop, error, reload } = useChat({...});

{(status === 'submitted' || status === 'streaming') && <Spinner />}
<button onClick={stop} disabled={status === 'ready'}>Stop</button>
{error && <button onClick={reload}>Retry</button>}
```

### Tools (Generative UI)

**Server:**
```ts
import { z } from 'zod';

const result = streamText({
  model: yourModel,
  messages: convertToModelMessages(messages),
  tools: {
    getWeather: {
      description: 'Get weather for a location',
      inputSchema: z.object({ city: z.string() }),
      execute: async ({ city }) => ({ city, weather: 'sunny', temp: 72 }),
    },
  },
});
```

**Client:**
```tsx
{message.parts.map((part, i) => {
  if (part.type === 'tool-getWeather') {
    switch (part.state) {
      case 'input-streaming': return <div key={i}>Loading...</div>;
      case 'input-available': return <div key={i}>Getting weather for {part.input.city}...</div>;
      case 'output-available': return <WeatherCard key={i} {...part.output} />;
      case 'output-error': return <div key={i}>Error: {part.errorText}</div>;
    }
  }
})}
```

### Hook References

- **[useChat Reference](references/usechat.md)** - Transport config, callbacks, request options, type inference
- **[useCompletion Reference](references/usecompletion.md)** - Text completion, throttling, callbacks
- **[useObject Reference](references/useobject.md)** - Streamed JSON, schema validation, partial rendering
- **[Tool Patterns](references/tools.md)** - Server/client tools, multi-step, error handling
- **[Streaming Data](references/streaming.md)** - Custom parts, sources, reconciliation
- **[Generative UI](references/generative-ui.md)** - Dynamic UI from tool results

---

## Part 2: AI Elements Components

Pre-built React components from shadcn/ui for production chat UIs. Install to `@/components/ai-elements/`.

### Conversation

Chat container with auto-scrolling:

```tsx
import {
  Conversation, ConversationContent, ConversationEmptyState,
} from '@/components/ai-elements/conversation';

<Conversation>
  <ConversationContent>
    {messages.length === 0 ? (
      <ConversationEmptyState title="Start a conversation" />
    ) : (
      messages.map((msg) => /* render messages */)
    )}
  </ConversationContent>
</Conversation>
```

### Message

Role-based styling (`from`: `'user' | 'assistant'`):

```tsx
import { Message, MessageContent, MessageActions, MessageAction } from '@/components/ai-elements/message';

<Message from={message.role}>
  <MessageContent>{/* content */}</MessageContent>
  <MessageActions>
    <MessageAction icon={CopyIcon} onClick={handleCopy} />
  </MessageActions>
</Message>
```

### Response

Markdown rendering with syntax highlighting, GFM, math:

```tsx
import { Response } from '@/components/ai-elements/response';

<Response>
  {message.parts?.filter(p => p.type === 'text').map(p => p.text).join('')}
</Response>
```

### PromptInput

Input with attachments, model selection:

```tsx
import { PromptInput, PromptInputTextarea, PromptInputSubmit } from '@/components/ai-elements/prompt-input';

<PromptInput onSubmit={(msg, e) => { e.preventDefault(); sendMessage({ text: msg.text }); }}>
  <PromptInputTextarea placeholder="Message..." disabled={status !== 'ready'} />
  <PromptInputSubmit disabled={status !== 'ready'} />
</PromptInput>
```

Additional: `PromptInputAttachments`, `PromptInputSelect`, `PromptInputSpeechButton`.

### Reasoning

AI thought process (auto-collapses when done):

```tsx
import { Reasoning } from '@/components/ai-elements/reasoning';

<Reasoning isStreaming={status === 'streaming'}>{reasoningContent}</Reasoning>
```

### Tool

Tool call visualization:

```tsx
import { Tool } from '@/components/ai-elements/tool';

<Tool name="search" status="complete">{toolResult}</Tool>
```

### CodeBlock

Syntax-highlighted code:

```tsx
import { CodeBlock } from '@/components/ai-elements/code-block';

<CodeBlock language="typescript">{codeString}</CodeBlock>
```

### All Components

| Component | Purpose |
|-----------|---------|
| `conversation` | Chat container with auto-scroll |
| `message` | Role-based message display |
| `response` | Markdown rendering |
| `prompt-input` | Smart input with attachments |
| `reasoning` | AI thought process |
| `tool` | Tool call display |
| `code-block` | Syntax highlighting |
| `sources` | Citation display |
| `inline-citation` | Inline citations |
| `actions` | Action buttons |
| `branch` | Conversation branching |
| `chain-of-thought` | Reasoning steps |
| `loader` | Loading states |
| `suggestion` | Quick actions |
| `confirmation` | Tool approval |
| `artifact` | Code/document display |
| `web-preview` | Embedded previews |

**Workflow (React Flow):** `canvas`, `node`, `edge`, `connection`, `controls`, `panel`, `toolbar`

---

## Complete Example

Combines AI SDK hooks with AI Elements components:

```tsx
'use client';

import { useChat } from '@ai-sdk/react';
import { DefaultChatTransport } from 'ai';
import { useState } from 'react';
import { Conversation, ConversationContent, ConversationEmptyState } from '@/components/ai-elements/conversation';
import { Message, MessageContent } from '@/components/ai-elements/message';
import { PromptInput, PromptInputTextarea, PromptInputSubmit } from '@/components/ai-elements/prompt-input';
import { Response } from '@/components/ai-elements/response';
import { Tool } from '@/components/ai-elements/tool';
import { Reasoning } from '@/components/ai-elements/reasoning';

export default function Chat() {
  const [input, setInput] = useState('');
  const { messages, sendMessage, status } = useChat({
    transport: new DefaultChatTransport({ api: '/api/chat' }),
  });
  const isLoading = status === 'submitted' || status === 'streaming';

  return (
    <div className="flex flex-col h-screen">
      <Conversation>
        <ConversationContent>
          {messages.length === 0 ? (
            <ConversationEmptyState title="Start a conversation" />
          ) : (
            messages.map((message) => (
              <Message key={message.id} from={message.role}>
                <MessageContent>
                  {message.parts.map((part, i) => {
                    switch (part.type) {
                      case 'text':
                        return message.role === 'assistant' 
                          ? <Response key={i}>{part.text}</Response>
                          : <span key={i}>{part.text}</span>;
                      case 'reasoning':
                        return <Reasoning key={i} isStreaming={isLoading}>{part.text}</Reasoning>;
                      default:
                        if (part.type.startsWith('tool-')) {
                          return <Tool key={i} name={part.type.slice(5)} status={part.state}>{JSON.stringify(part.output)}</Tool>;
                        }
                        return null;
                    }
                  })}
                </MessageContent>
              </Message>
            ))
          )}
        </ConversationContent>
      </Conversation>

      <div className="border-t p-4">
        <PromptInput
          onSubmit={(msg, e) => { e.preventDefault(); if (msg.text) { sendMessage({ text: msg.text }); setInput(''); }}}
          className="max-w-3xl mx-auto"
        >
          <PromptInputTextarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            disabled={isLoading}
          />
          <PromptInputSubmit disabled={isLoading} />
        </PromptInput>
      </div>
    </div>
  );
}
```

## Customization

AI Elements components live in `components/ai-elements/`. Edit directly for customization. Re-running `npx ai-elements@latest` prompts before overwriting.
