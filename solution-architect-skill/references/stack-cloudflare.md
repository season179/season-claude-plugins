# Cloudflare Stack

## Contents
- Workers setup
- D1 database
- KV store
- R2 storage
- Durable Objects
- Queues

## Workers Setup

```toml
# wrangler.toml
name = "my-app"
main = "src/index.ts"
compatibility_date = "2024-01-01"

[vars]
ENVIRONMENT = "development"

[[d1_databases]]
binding = "DB"
database_name = "my-database"
database_id = "xxx"

[[kv_namespaces]]
binding = "KV"
id = "xxx"

[[r2_buckets]]
binding = "BUCKET"
bucket_name = "my-bucket"
```

### Bindings Type
```typescript
export interface Env {
  DB: D1Database
  KV: KVNamespace
  BUCKET: R2Bucket
  JWT_SECRET: string // Secret via `wrangler secret put`
}
```

## D1 Database

```typescript
// Query
const user = await env.DB.prepare('SELECT * FROM users WHERE id = ?')
  .bind(userId).first<User>()

// List
const { results } = await env.DB.prepare('SELECT * FROM users LIMIT ?')
  .bind(limit).all<User>()

// Insert
await env.DB.prepare('INSERT INTO users (id, email) VALUES (?, ?)')
  .bind(id, email).run()

// Batch (atomic)
await env.DB.batch([
  env.DB.prepare('INSERT INTO orders ...').bind(...),
  env.DB.prepare('UPDATE inventory ...').bind(...)
])
```

## KV Store

```typescript
// Set with TTL
await env.KV.put('session:abc', JSON.stringify(data), { expirationTtl: 3600 })

// Get
const value = await env.KV.get('session:abc', { type: 'json' })

// Delete
await env.KV.delete('session:abc')

// List
const { keys } = await env.KV.list({ prefix: 'session:' })
```

## R2 Storage

```typescript
// Upload
await env.BUCKET.put('uploads/file.png', file, {
  httpMetadata: { contentType: 'image/png' }
})

// Download
const object = await env.BUCKET.get('uploads/file.png')
if (object) {
  const data = await object.arrayBuffer()
}

// Delete
await env.BUCKET.delete('uploads/file.png')
```

## Durable Objects

```typescript
// Durable Object class
export class Room implements DurableObject {
  private connections = new Map<WebSocket, string>()
  
  async fetch(request: Request): Promise<Response> {
    const [client, server] = Object.values(new WebSocketPair())
    server.accept()
    this.connections.set(server, 'user')
    
    server.addEventListener('message', (e) => this.broadcast(e.data as string))
    server.addEventListener('close', () => this.connections.delete(server))
    
    return new Response(null, { status: 101, webSocket: client })
  }
  
  broadcast(msg: string) {
    for (const ws of this.connections.keys()) ws.send(msg)
  }
}

// Usage
const id = env.ROOM.idFromName(roomId)
const room = env.ROOM.get(id)
return room.fetch(request)
```

## Queues

```typescript
// Producer
await env.QUEUE.send({ type: 'process', orderId })

// Consumer (in worker export)
export default {
  async queue(batch: MessageBatch, env: Env) {
    for (const msg of batch.messages) {
      await process(msg.body)
      msg.ack()
    }
  }
}
```

## Cron Triggers

```toml
[triggers]
crons = ["0 * * * *"]  # Every hour
```

```typescript
export default {
  async scheduled(event: ScheduledEvent, env: Env) {
    if (event.cron === '0 * * * *') await hourlyTask(env)
  }
}
```

## Background Work

```typescript
app.post('/action', async (c) => {
  const result = await criticalWork()
  
  // Non-blocking background tasks
  c.executionCtx.waitUntil(Promise.all([
    sendEmail(result),
    logAnalytics(result)
  ]))
  
  return c.json(result)
})
```

## Local Development

```bash
wrangler dev              # Local with mocks
wrangler dev --local --persist  # Persist D1/KV locally
wrangler dev --remote     # Use remote bindings
```
