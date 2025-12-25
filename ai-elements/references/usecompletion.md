# useCompletion Reference

## Contents
- Basic Setup
- Return Values
- Configuration Options
- Event Callbacks
- Server Route

## Basic Setup

```tsx
'use client';
import { useCompletion } from '@ai-sdk/react';

export default function Completion() {
  const { completion, input, handleInputChange, handleSubmit, isLoading, error } = useCompletion({
    api: '/api/completion',
  });

  return (
    <form onSubmit={handleSubmit}>
      <input value={input} onChange={handleInputChange} disabled={isLoading} />
      <button type="submit" disabled={isLoading}>Generate</button>
      <div>{completion}</div>
      {error && <div>Error: {error.message}</div>}
    </form>
  );
}
```

## Return Values

| Property | Type | Description |
|----------|------|-------------|
| `completion` | `string` | Current completion text |
| `input` | `string` | Current input value |
| `isLoading` | `boolean` | Request in progress |
| `error` | `Error \| undefined` | Error from last request |
| `handleInputChange` | `ChangeEventHandler` | Input onChange handler |
| `handleSubmit` | `FormEventHandler` | Form onSubmit handler |
| `setInput` | `(input: string) => void` | Set input programmatically |
| `complete` | `(prompt: string, options?) => void` | Trigger completion |
| `stop` | `() => void` | Abort current request |
| `setCompletion` | `(completion: string) => void` | Set completion text |

## Configuration Options

```tsx
useCompletion({
  api: '/api/completion',
  id: 'my-completion', // Shared state identifier
  initialInput: '', // Default input value
  initialCompletion: '', // Default completion
  headers: { Authorization: 'Bearer token' },
  body: { userId: '123' },
  credentials: 'same-origin',
  experimental_throttle: 50, // Throttle UI updates (ms)
})
```

## Event Callbacks

```tsx
useCompletion({
  onResponse: (response) => {
    // Validate response, throw to abort
    if (!response.ok) throw new Error('Failed');
  },
  onFinish: (prompt, completion) => {
    console.log('Completed:', completion);
  },
  onError: (error) => {
    console.error('Error:', error);
  },
})
```

## Server Route

```ts
import { streamText } from 'ai';

export async function POST(req: Request) {
  const { prompt } = await req.json();

  const result = streamText({
    model: yourModel,
    prompt,
  });

  return result.toTextStreamResponse();
}
```

## Programmatic Completion

```tsx
const { complete, completion } = useCompletion({...});

// Trigger without form
const handleClick = () => {
  complete('Write a haiku about coding', {
    body: { style: 'formal' },
  });
};
```

## With Custom Body Fields

```tsx
const { handleSubmit } = useCompletion({
  body: { language: 'typescript', maxTokens: 500 },
});

// Server receives: { prompt, language, maxTokens }
```
