# API Design

## Contents
- Style selection
- REST patterns
- Versioning
- Error handling
- Rate limiting

## Style Selection

| Style | Use When |
|-------|----------|
| **REST** | CRUD, resource-oriented, broad client support |
| **GraphQL** | Flexible queries, multiple clients with different needs |
| **gRPC** | Service-to-service, high performance, streaming |

**Default**: REST for external APIs, gRPC for internal service communication.

## REST Patterns

### Resource Naming
```
GET    /users              # List
POST   /users              # Create
GET    /users/{id}         # Read
PUT    /users/{id}         # Replace
PATCH  /users/{id}         # Partial update
DELETE /users/{id}         # Delete

GET    /users/{id}/orders  # Nested resource
POST   /orders/{id}/cancel # Action as sub-resource
```

### Status Codes
| Code | Use |
|------|-----|
| 200 | Success with body |
| 201 | Created |
| 204 | Success, no body |
| 400 | Validation error |
| 401 | Not authenticated |
| 403 | Not authorized |
| 404 | Not found |
| 409 | Conflict |
| 429 | Rate limited |
| 500 | Server error |

### Response Format
```typescript
// Success
{ "data": {...}, "meta": { "requestId": "..." } }

// Collection
{ "data": [...], "meta": { "total": 100, "nextCursor": "..." } }

// Error
{ "error": { "code": "VALIDATION_ERROR", "message": "...", "details": [...] } }
```

### Pagination (Cursor-based)
```typescript
app.get('/users', async (c) => {
  const cursor = c.req.query('cursor')
  const limit = Math.min(Number(c.req.query('limit') || 20), 100)
  
  const users = await db.query.users.findMany({
    where: cursor ? gt(users.id, atob(cursor)) : undefined,
    limit: limit + 1,
    orderBy: asc(users.id)
  })
  
  const hasMore = users.length > limit
  const results = hasMore ? users.slice(0, -1) : users
  
  return c.json({
    data: results,
    meta: { nextCursor: hasMore ? btoa(results.at(-1)!.id) : null }
  })
})
```

## Versioning

**Default**: URL path versioning (`/v1/users`).

Other options: Header (`Accept: application/vnd.api+json; version=2`), Query param.

## Error Handling

```typescript
class APIError extends Error {
  constructor(public code: string, message: string, public status = 400) {
    super(message)
  }
}

app.onError((err, c) => {
  if (err instanceof APIError) {
    return c.json({ error: { code: err.code, message: err.message } }, err.status)
  }
  console.error(err)
  return c.json({ error: { code: 'INTERNAL_ERROR', message: 'Unexpected error' } }, 500)
})

// Usage
throw new APIError('USER_NOT_FOUND', 'User not found', 404)
```

## Rate Limiting

```typescript
app.use(async (c, next) => {
  const key = c.req.header('Authorization') || c.req.header('CF-Connecting-IP')
  const { success, remaining, reset } = await c.env.RATE_LIMITER.limit({ key })
  
  c.header('X-RateLimit-Remaining', String(remaining))
  c.header('X-RateLimit-Reset', String(reset))
  
  if (!success) return c.json({ error: { code: 'RATE_LIMITED' } }, 429)
  await next()
})
```

## Idempotency

```typescript
app.post('/payments', async (c) => {
  const key = c.req.header('Idempotency-Key')
  if (!key) throw new APIError('MISSING_IDEMPOTENCY_KEY', 'Required header')
  
  const existing = await c.env.KV.get(`idempotency:${key}`)
  if (existing) return c.json(JSON.parse(existing))
  
  const result = await processPayment(await c.req.json())
  await c.env.KV.put(`idempotency:${key}`, JSON.stringify(result), { expirationTtl: 86400 })
  
  return c.json(result, 201)
})
```

## Input Validation

```typescript
import { z } from 'zod'
import { zValidator } from '@hono/zod-validator'

const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  role: z.enum(['user', 'admin']).default('user')
})

app.post('/users', zValidator('json', createUserSchema), async (c) => {
  const data = c.req.valid('json') // Typed and validated
  // ...
})
```
