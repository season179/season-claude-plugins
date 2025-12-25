# Data Architecture

## Contents
- Database selection
- Consistency models
- Schema design with Drizzle
- Indexing
- Transactions
- Migrations

## Database Selection

| Need | Choice |
|------|--------|
| Relational + <10GB + edge | **D1** |
| Relational + >10GB or advanced SQL | **PostgreSQL via Hyperdrive** |
| Key-value / cache / config | **KV** |
| Files / objects | **R2** |
| Stateful compute / WebSockets | **Durable Objects** |

## Consistency Models

| Model | Guarantee | Example |
|-------|-----------|---------|
| Strong | All reads see latest write | D1, PostgreSQL |
| Eventual | Reads eventually consistent | KV |
| Read-your-writes | User sees own writes | Cache after write |

### Read-Your-Writes Pattern
```typescript
// After write, cache for immediate reads
await db.update(users).set(data).where(eq(users.id, id))
await kv.put(`user:${id}`, JSON.stringify(data), { expirationTtl: 60 })
```

## Schema Design (Drizzle)

```typescript
import { sqliteTable, text, integer, real, index } from 'drizzle-orm/sqlite-core'
import { relations } from 'drizzle-orm'

export const users = sqliteTable('users', {
  id: text('id').primaryKey().$defaultFn(() => crypto.randomUUID()),
  email: text('email').notNull().unique(),
  name: text('name').notNull(),
  organizationId: text('organization_id').references(() => organizations.id),
  createdAt: integer('created_at', { mode: 'timestamp' }).$defaultFn(() => new Date()),
  updatedAt: integer('updated_at', { mode: 'timestamp' }).$defaultFn(() => new Date())
}, (t) => ({
  emailIdx: index('users_email_idx').on(t.email),
  orgIdx: index('users_org_idx').on(t.organizationId)
}))

export const usersRelations = relations(users, ({ one, many }) => ({
  organization: one(organizations, {
    fields: [users.organizationId],
    references: [organizations.id]
  }),
  orders: many(orders)
}))
```

## Indexing

**Index when:** Column in WHERE, JOIN, ORDER BY, foreign keys.

**Skip when:** Small tables, low cardinality, heavy write tables.

### Composite Index
```typescript
// Query: WHERE status = ? AND created_at > ?
index('orders_status_created_idx').on(t.status, t.createdAt)
// Left-most column must be in query
```

## Transactions (D1 Batch)

```typescript
const results = await db.batch([
  db.insert(orders).values({ id: orderId, userId, total }),
  db.insert(orderItems).values(items.map(i => ({ orderId, ...i }))),
  db.update(users).set({ lastOrderAt: new Date() }).where(eq(users.id, userId))
])
// All succeed or all fail
```

## Queries

```typescript
import { eq, and, or, like, gt, desc, sql } from 'drizzle-orm'

// Find one with relations
const user = await db.query.users.findFirst({
  where: eq(users.id, id),
  with: { organization: true, orders: { limit: 5 } }
})

// List with filters
const results = await db.query.users.findMany({
  where: and(
    eq(users.organizationId, orgId),
    or(like(users.name, `%${search}%`), like(users.email, `%${search}%`))
  ),
  limit: 20,
  offset: (page - 1) * 20,
  orderBy: desc(users.createdAt)
})

// Count
const [{ count }] = await db.select({ count: sql<number>`count(*)` }).from(users)
```

## Migrations

```bash
# Generate from schema changes
npx drizzle-kit generate

# Apply locally
wrangler d1 migrations apply my-database --local

# Apply to production
wrangler d1 migrations apply my-database --remote
```

## Backup & Recovery

**D1**: 30-day point-in-time recovery (Time Travel)

```bash
# Export
wrangler d1 export my-database --output=backup.sql

# Time travel query
wrangler d1 time-travel my-database --timestamp=2024-01-15T10:00:00Z
```
