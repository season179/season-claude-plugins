# useObject Reference

## Contents
- Basic Setup
- Return Values
- Schema Definition
- Handling Partial Objects
- Enum Output Mode
- Server Route

## Basic Setup

```tsx
'use client';
import { experimental_useObject as useObject } from '@ai-sdk/react';
import { z } from 'zod';

const notificationSchema = z.object({
  notifications: z.array(z.object({
    name: z.string(),
    message: z.string(),
    priority: z.enum(['low', 'medium', 'high']),
  })),
});

export default function Notifications() {
  const { object, submit, isLoading, error, stop } = useObject({
    api: '/api/notifications',
    schema: notificationSchema,
  });

  return (
    <div>
      <button onClick={() => submit('Generate notifications')} disabled={isLoading}>
        Generate
      </button>
      {object?.notifications?.map((n, i) => (
        <div key={i}>
          <strong>{n?.name}</strong>: {n?.message}
        </div>
      ))}
    </div>
  );
}
```

## Return Values

| Property | Type | Description |
|----------|------|-------------|
| `object` | `DeepPartial<T> \| undefined` | Partial/complete generated object |
| `isLoading` | `boolean` | Request in progress |
| `error` | `Error \| undefined` | Error from last request |
| `submit` | `(input: string) => void` | Trigger generation |
| `stop` | `() => void` | Abort current request |
| `clear` | `() => void` | Clear the object state |

## Schema Definition

Define schema in a shared file for client and server:

```ts
// schemas/notifications.ts
import { z } from 'zod';

export const notificationSchema = z.object({
  notifications: z.array(z.object({
    name: z.string().describe('User name'),
    message: z.string().describe('Notification message'),
    priority: z.enum(['low', 'medium', 'high']),
    timestamp: z.string().optional(),
  })),
});

export type NotificationData = z.infer<typeof notificationSchema>;
```

## Handling Partial Objects

Objects stream incrementally—handle undefined values:

```tsx
{object?.notifications?.map((notification, i) => (
  <div key={i} className={notification?.priority ? 'visible' : 'loading'}>
    {notification?.name ?? 'Loading...'}
    {notification?.message ?? '...'}
    {notification?.priority && <Badge>{notification.priority}</Badge>}
  </div>
))}
```

## Enum Output Mode

For classification/categorization:

```tsx
const classifierSchema = z.object({
  enum: z.enum(['positive', 'neutral', 'negative']),
});

const { object, submit } = useObject({
  api: '/api/classify',
  schema: classifierSchema,
});

// object?.enum === 'positive' | 'neutral' | 'negative' | undefined
```

## Configuration Options

```tsx
useObject({
  api: '/api/generate',
  schema: mySchema,
  id: 'my-object', // Shared state identifier
  initialValue: { items: [] }, // Default object
  headers: { Authorization: 'Bearer token' },
  credentials: 'same-origin',
  onFinish: ({ object, error }) => {
    if (object) console.log('Generated:', object);
  },
  onError: (error) => {
    console.error('Error:', error);
  },
})
```

## Server Route

```ts
import { streamObject } from 'ai';
import { notificationSchema } from '@/schemas/notifications';

export async function POST(req: Request) {
  const { prompt } = await req.json();

  const result = streamObject({
    model: yourModel,
    schema: notificationSchema,
    prompt,
  });

  return result.toTextStreamResponse();
}
```

## Error Handling Pattern

```tsx
const { object, error, isLoading, submit, stop } = useObject({...});

return (
  <div>
    <button onClick={() => submit(prompt)} disabled={isLoading}>
      {isLoading ? 'Generating...' : 'Generate'}
    </button>
    {isLoading && <button onClick={stop}>Stop</button>}
    {error && <div className="error">Error: {error.message}</div>}
    {object && <ObjectDisplay data={object} />}
  </div>
);
```
