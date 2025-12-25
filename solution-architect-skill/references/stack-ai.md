# AI SDK

## Contents
- Setup
- Core functions
- Tool calling
- Agents
- Streaming API
- React hooks

## Setup

```bash
npm install ai @ai-sdk/anthropic
```

```typescript
import { anthropic } from '@ai-sdk/anthropic'
import { createOpenAI } from '@ai-sdk/openai'

// Direct
const model = anthropic('claude-sonnet-4-20250514')

// Via OpenRouter
const openrouter = createOpenAI({
  baseURL: 'https://openrouter.ai/api/v1',
  apiKey: process.env.OPENROUTER_API_KEY
})
const model = openrouter('anthropic/claude-sonnet-4-20250514')
```

## Core Functions

### generateText
```typescript
import { generateText } from 'ai'

const { text, usage } = await generateText({
  model: anthropic('claude-sonnet-4-20250514'),
  system: 'You are a helpful assistant.',
  messages: [{ role: 'user', content: 'Hello' }],
  maxTokens: 1000
})
```

### streamText
```typescript
import { streamText } from 'ai'

const result = await streamText({
  model: anthropic('claude-sonnet-4-20250514'),
  messages: [{ role: 'user', content: 'Write a poem' }]
})

for await (const chunk of result.textStream) {
  process.stdout.write(chunk)
}

// Or in Hono
app.post('/chat', async (c) => {
  const { messages } = await c.req.json()
  const result = await streamText({ model, messages })
  return result.toDataStreamResponse()
})
```

### generateObject
```typescript
import { generateObject } from 'ai'
import { z } from 'zod'

const { object } = await generateObject({
  model: anthropic('claude-sonnet-4-20250514'),
  schema: z.object({
    name: z.string(),
    ingredients: z.array(z.string()),
    steps: z.array(z.string())
  }),
  prompt: 'Create a pasta recipe'
})
```

## Tool Calling

```typescript
import { generateText, tool } from 'ai'
import { z } from 'zod'

const weatherTool = tool({
  description: 'Get weather for a location',
  parameters: z.object({
    location: z.string(),
    unit: z.enum(['celsius', 'fahrenheit']).default('celsius')
  }),
  execute: async ({ location, unit }) => {
    return await fetchWeather(location, unit)
  }
})

const { text, toolCalls } = await generateText({
  model: anthropic('claude-sonnet-4-20250514'),
  tools: { weather: weatherTool },
  prompt: 'What is the weather in Tokyo?'
})
```

## Agents (Multi-step)

```typescript
const result = await generateText({
  model: anthropic('claude-sonnet-4-20250514'),
  tools: { weather: weatherTool, search: searchTool },
  maxSteps: 5, // Allow multiple tool calls
  prompt: 'Plan a trip to Tokyo'
})

// Each step available in result.steps
```

### Agent Class
```typescript
import { Agent } from 'ai'

const agent = new Agent({
  model: anthropic('claude-sonnet-4-20250514'),
  system: 'You are a research assistant.',
  tools: { search: searchTool },
  maxSteps: 10,
  stopWhen: (state) => state.text.includes('DONE')
})

const result = await agent.run({ prompt: 'Research quantum computing' })
```

## React Hooks

### useChat
```typescript
'use client'
import { useChat } from 'ai/react'

export function Chat() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/chat'
  })
  
  return (
    <div>
      {messages.map(m => <div key={m.id}>{m.role}: {m.content}</div>)}
      <form onSubmit={handleSubmit}>
        <input value={input} onChange={handleInputChange} />
        <button disabled={isLoading}>Send</button>
      </form>
    </div>
  )
}
```

### API Route
```typescript
// app/api/chat/route.ts
import { streamText } from 'ai'
import { anthropic } from '@ai-sdk/anthropic'

export async function POST(req: Request) {
  const { messages } = await req.json()
  const result = await streamText({
    model: anthropic('claude-sonnet-4-20250514'),
    messages
  })
  return result.toDataStreamResponse()
}
```

## Embeddings

```typescript
import { embed, embedMany } from 'ai'
import { openai } from '@ai-sdk/openai'

const { embedding } = await embed({
  model: openai.embedding('text-embedding-3-small'),
  value: 'The quick brown fox'
})

const { embeddings } = await embedMany({
  model: openai.embedding('text-embedding-3-small'),
  values: ['Doc 1', 'Doc 2', 'Doc 3']
})
```

## Error Handling

```typescript
import { APICallError } from 'ai'

try {
  const result = await generateText({ model, prompt })
} catch (error) {
  if (error instanceof APICallError) {
    console.error('API error:', error.message, error.statusCode)
  }
  throw error
}
```
