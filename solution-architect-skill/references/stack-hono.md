# Hono + Drizzle + Zod

## Contents
- Hono setup
- Route groups
- Middleware
- Validation
- Error handling
- Drizzle setup
- Testing

## Hono Setup

```typescript
import { Hono } from 'hono'
import type { Env } from './types'

const app = new Hono<{ Bindings: Env }>()

app.get('/', (c) => c.text('Hello'))
app.get('/users/:id', (c) => c.json({ id: c.req.param('id') }))

export default app
```

## Route Groups

```typescript
const api = new Hono<{ Bindings: Env }>()

const users = new Hono<{ Bindings: Env }>()
  .get('/', listUsers)
  .post('/', createUser)
  .get('/:id', getUser)

const orders = new Hono<{ Bindings: Env }>()
  .get('/', listOrders)
  .post('/', createOrder)

api.route('/users', users)
api.route('/orders', orders)

app.route('/api', api)
```

## Middleware

### Built-in
```typescript
import { cors } from 'hono/cors'
import { logger } from 'hono/logger'
import { secureHeaders } from 'hono/secure-headers'

app.use('*', logger())
app.use('*', secureHeaders())
app.use('/api/*', cors({ origin: ['https://app.example.com'], credentials: true }))
```

### Custom Auth
```typescript
import { createMiddleware } from 'hono/factory'

const auth = createMiddleware<{
  Bindings: Env
  Variables: { user: User }
}>(async (c, next) => {
  const token = c.req.header('Authorization')?.replace('Bearer ', '')
  if (!token) return c.json({ error: 'Unauthorized' }, 401)
  
  const user = await verifyToken(token, c.env.JWT_SECRET)
  c.set('user', user)
  await next()
})

app.use('/api/*', auth)
app.get('/api/me', (c) => c.json(c.get('user')))
```

## Validation (Zod)

```typescript
import { z } from 'zod'
import { zValidator } from '@hono/zod-validator'

const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  role: z.enum(['user', 'admin']).default('user')
})

const querySchema = z.object({
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20)
})

app.post('/users', zValidator('json', createUserSchema), async (c) => {
  const data = c.req.valid('json') // Typed
})

app.get('/users', zValidator('query', querySchema), async (c) => {
  const { page, limit } = c.req.valid('query')
})
```

## Error Handling

```typescript
import { HTTPException } from 'hono/http-exception'

class AppError extends Error {
  constructor(public code: string, message: string, public status = 400) {
    super(message)
  }
}

app.onError((err, c) => {
  if (err instanceof AppError) {
    return c.json({ error: { code: err.code, message: err.message } }, err.status)
  }
  console.error(err)
  return c.json({ error: { code: 'INTERNAL_ERROR' } }, 500)
})

app.notFound((c) => c.json({ error: { code: 'NOT_FOUND' } }, 404))

// Usage
throw new AppError('USER_NOT_FOUND', 'User not found', 404)
```

## Drizzle Setup

```typescript
// src/db/index.ts
import { drizzle } from 'drizzle-orm/d1'
import * as schema from './schema'

export const createDb = (d1: D1Database) => drizzle(d1, { schema })
export type Database = ReturnType<typeof createDb>

// drizzle.config.ts
export default {
  schema: './src/db/schema.ts',
  out: './drizzle/migrations',
  dialect: 'sqlite'
}
```

### Schema
```typescript
import { sqliteTable, text, integer, index } from 'drizzle-orm/sqlite-core'
import { relations } from 'drizzle-orm'

export const users = sqliteTable('users', {
  id: text('id').primaryKey().$defaultFn(() => crypto.randomUUID()),
  email: text('email').notNull().unique(),
  name: text('name').notNull(),
  createdAt: integer('created_at', { mode: 'timestamp' }).$defaultFn(() => new Date())
}, (t) => ({
  emailIdx: index('email_idx').on(t.email)
}))

export const usersRelations = relations(users, ({ many }) => ({
  orders: many(orders)
}))
```

## Testing (Vitest)

```typescript
// vitest.config.ts
import { defineWorkersConfig } from '@cloudflare/vitest-pool-workers/config'

export default defineWorkersConfig({
  test: {
    poolOptions: { workers: { wrangler: { configPath: './wrangler.toml' } } }
  }
})

// tests/api.test.ts
import { env } from 'cloudflare:test'
import { describe, it, expect, beforeEach } from 'vitest'
import app from '../src/index'

describe('API', () => {
  beforeEach(async () => {
    await env.DB.exec('DELETE FROM users')
  })
  
  it('creates user', async () => {
    const res = await app.request('/api/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: 'test@example.com', name: 'Test' })
    }, env)
    
    expect(res.status).toBe(201)
  })
})
```
