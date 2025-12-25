# Generative UI Reference

## Contents
- Concept Overview
- Basic Implementation
- Tool Definition
- UI Component Creation
- Rendering Tool Parts
- Expanding with More Tools
- Patterns and Best Practices

## Concept Overview

Generative UI connects tool results to React components:

1. Model receives prompt + tools
2. Model decides to call a tool
3. Tool executes and returns data
4. Data renders as a React component

```
User → "What's the weather?" → Model → getWeather("SF") → { temp: 72 } → <WeatherCard />
```

## Basic Implementation

### 1. Define Tools

```ts
// ai/tools.ts
import { tool as createTool } from 'ai';
import { z } from 'zod';

export const weatherTool = createTool({
  description: 'Display weather for a location',
  inputSchema: z.object({
    location: z.string().describe('City name'),
  }),
  execute: async ({ location }) => {
    // Real implementation would call weather API
    await new Promise(resolve => setTimeout(resolve, 1000));
    return { location, weather: 'Sunny', temperature: 72 };
  },
});

export const tools = { displayWeather: weatherTool };
```

### 2. Create API Route

```ts
// app/api/chat/route.ts
import { streamText, convertToModelMessages, UIMessage, stepCountIs } from 'ai';
import { tools } from '@/ai/tools';

export async function POST(request: Request) {
  const { messages }: { messages: UIMessage[] } = await request.json();

  const result = streamText({
    model: yourModel,
    system: 'You are a helpful assistant with weather data access.',
    messages: convertToModelMessages(messages),
    tools,
    stopWhen: stepCountIs(5),
  });

  return result.toUIMessageStreamResponse();
}
```

### 3. Create UI Component

```tsx
// components/weather.tsx
type WeatherProps = {
  location: string;
  weather: string;
  temperature: number;
};

export function Weather({ location, weather, temperature }: WeatherProps) {
  return (
    <div className="p-4 rounded-lg bg-blue-100">
      <h3 className="font-bold">{location}</h3>
      <p>{weather}</p>
      <p className="text-2xl">{temperature}°F</p>
    </div>
  );
}
```

### 4. Render in Chat

```tsx
// app/page.tsx
'use client';
import { useChat } from '@ai-sdk/react';
import { DefaultChatTransport } from 'ai';
import { useState } from 'react';
import { Weather } from '@/components/weather';

export default function Chat() {
  const [input, setInput] = useState('');
  const { messages, sendMessage, status } = useChat({
    transport: new DefaultChatTransport({ api: '/api/chat' }),
  });

  return (
    <div>
      {messages.map(message => (
        <div key={message.id}>
          <strong>{message.role}:</strong>
          {message.parts.map((part, i) => {
            // Text content
            if (part.type === 'text') {
              return <span key={i}>{part.text}</span>;
            }

            // Weather tool
            if (part.type === 'tool-displayWeather') {
              switch (part.state) {
                case 'input-available':
                  return <div key={i}>Loading weather for {part.input.location}...</div>;
                case 'output-available':
                  return <Weather key={i} {...part.output} />;
                case 'output-error':
                  return <div key={i}>Error: {part.errorText}</div>;
              }
            }

            return null;
          })}
        </div>
      ))}

      <form onSubmit={e => {
        e.preventDefault();
        if (input.trim()) {
          sendMessage({ text: input });
          setInput('');
        }
      }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Ask about the weather..."
          disabled={status !== 'ready'}
        />
        <button type="submit" disabled={status !== 'ready'}>Send</button>
      </form>
    </div>
  );
}
```

## Expanding with More Tools

### Add Stock Tool

```ts
// ai/tools.ts
export const stockTool = createTool({
  description: 'Get stock price for a symbol',
  inputSchema: z.object({
    symbol: z.string().describe('Stock ticker symbol'),
  }),
  execute: async ({ symbol }) => {
    // Real implementation would call stock API
    return { symbol, price: 150.25, change: +2.5 };
  },
});

export const tools = {
  displayWeather: weatherTool,
  getStockPrice: stockTool,
};
```

### Stock Component

```tsx
// components/stock.tsx
type StockProps = {
  symbol: string;
  price: number;
  change: number;
};

export function Stock({ symbol, price, change }: StockProps) {
  return (
    <div className="p-4 rounded-lg bg-gray-100">
      <h3 className="font-bold">{symbol}</h3>
      <p className="text-2xl">${price.toFixed(2)}</p>
      <p className={change >= 0 ? 'text-green-600' : 'text-red-600'}>
        {change >= 0 ? '+' : ''}{change.toFixed(2)}%
      </p>
    </div>
  );
}
```

### Render Both Tools

```tsx
{message.parts.map((part, i) => {
  if (part.type === 'text') {
    return <span key={i}>{part.text}</span>;
  }

  if (part.type === 'tool-displayWeather') {
    return part.state === 'output-available'
      ? <Weather key={i} {...part.output} />
      : <div key={i}>Loading weather...</div>;
  }

  if (part.type === 'tool-getStockPrice') {
    return part.state === 'output-available'
      ? <Stock key={i} {...part.output} />
      : <div key={i}>Loading stock...</div>;
  }

  return null;
})}
```

## Patterns and Best Practices

### Loading States

Always handle all tool states:

```tsx
if (part.type === 'tool-myTool') {
  switch (part.state) {
    case 'input-streaming':
      return <Skeleton key={i} />; // Show placeholder
    case 'input-available':
      return <Loading key={i} message={`Processing ${part.input.query}...`} />;
    case 'output-available':
      return <MyComponent key={i} data={part.output} />;
    case 'output-error':
      return <Error key={i} message={part.errorText} />;
  }
}
```

### Streaming Tool Inputs

Show partial inputs as they stream:

```tsx
if (part.state === 'input-streaming') {
  return (
    <div key={i} className="animate-pulse">
      <pre>{JSON.stringify(part.input, null, 2)}</pre>
    </div>
  );
}
```

### Component Organization

```
components/
├── tools/
│   ├── weather.tsx
│   ├── stock.tsx
│   ├── calendar.tsx
│   └── index.ts (re-exports)
└── chat/
    ├── message.tsx
    └── tool-renderer.tsx
```

### Generic Tool Renderer

```tsx
// components/chat/tool-renderer.tsx
import { Weather } from '../tools/weather';
import { Stock } from '../tools/stock';

const toolComponents = {
  'tool-displayWeather': Weather,
  'tool-getStockPrice': Stock,
};

export function ToolRenderer({ part }) {
  const Component = toolComponents[part.type];
  
  if (!Component) {
    return <pre>{JSON.stringify(part, null, 2)}</pre>;
  }

  switch (part.state) {
    case 'input-available':
      return <div>Loading...</div>;
    case 'output-available':
      return <Component {...part.output} />;
    case 'output-error':
      return <div>Error: {part.errorText}</div>;
    default:
      return null;
  }
}
```

### Multiple Tool Calls

Model can call multiple tools in sequence:

```tsx
{message.parts.map((part, i) => {
  // Step boundaries
  if (part.type === 'step-start' && i > 0) {
    return <hr key={i} className="my-4" />;
  }
  
  // Render tools
  return <ToolRenderer key={i} part={part} />;
})}
```
