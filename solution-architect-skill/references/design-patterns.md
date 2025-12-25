# Design Patterns

## Contents
- Resilience patterns
- Data patterns
- Communication patterns
- Caching patterns
- Migration patterns

## Resilience Patterns

### Circuit Breaker
Fail fast when downstream is unhealthy:

```typescript
class CircuitBreaker {
  private state: 'CLOSED' | 'OPEN' | 'HALF_OPEN' = 'CLOSED'
  private failures = 0
  
  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailure > this.timeout) {
        this.state = 'HALF_OPEN'
      } else {
        throw new Error('Circuit OPEN')
      }
    }
    try {
      const result = await fn()
      this.reset()
      return result
    } catch (error) {
      this.recordFailure()
      throw error
    }
  }
}
```

### Retry with Backoff
```typescript
async function withRetry<T>(fn: () => Promise<T>, maxRetries = 3): Promise<T> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn()
    } catch (error) {
      if (i === maxRetries - 1) throw error
      await new Promise(r => setTimeout(r, 1000 * Math.pow(2, i) + Math.random() * 1000))
    }
  }
  throw new Error('Unreachable')
}
```

### Bulkhead
Isolate failures by limiting concurrent operations:

```typescript
class Bulkhead {
  private running = 0
  constructor(private max: number) {}
  
  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.running >= this.max) throw new Error('Bulkhead full')
    this.running++
    try { return await fn() } 
    finally { this.running-- }
  }
}
```

### Timeout + Fallback
```typescript
const result = await Promise.race([
  primaryService(),
  new Promise((_, reject) => setTimeout(() => reject(new Error('Timeout')), 5000))
]).catch(() => fallbackService())
```

## Data Patterns

### Saga (Distributed Transactions)
Compensating actions for rollback:

```typescript
class OrderSaga {
  async execute(order: Order) {
    const completed: Array<{ compensate: () => Promise<void> }> = []
    
    const steps = [
      { action: () => this.reserveInventory(order), compensate: () => this.releaseInventory(order) },
      { action: () => this.processPayment(order), compensate: () => this.refundPayment(order) },
      { action: () => this.confirmOrder(order), compensate: () => this.cancelOrder(order) }
    ]
    
    for (const step of steps) {
      try {
        await step.action()
        completed.push(step)
      } catch {
        for (const s of completed.reverse()) await s.compensate()
        throw new Error('Saga failed')
      }
    }
  }
}
```

### Outbox Pattern
Reliable event publishing with DB write:

```sql
BEGIN TRANSACTION;
INSERT INTO orders (...) VALUES (...);
INSERT INTO outbox (event_type, payload) VALUES ('OrderCreated', '{"orderId": "..."}');
COMMIT;
-- Background process publishes from outbox table
```

## Communication Patterns

### API Gateway
Single entry point handling auth, rate limiting, routing.

### Backend for Frontend (BFF)
Dedicated backend per client type (web, mobile, IoT).

### Sidecar
Helper container alongside main service for cross-cutting concerns (proxy, logs, auth).

## Caching Patterns

### Cache-Aside
```typescript
async function get(key: string) {
  const cached = await cache.get(key)
  if (cached) return cached
  const data = await db.query(key)
  await cache.set(key, data, { ex: 3600 })
  return data
}
```

### Write-Through
```typescript
async function update(key: string, data: any) {
  await db.update(key, data)
  await cache.set(key, data) // Update cache immediately
}
```

### Cache Invalidation
- **TTL**: Automatic expiration
- **Event-based**: Delete on update
- **Version-based**: Include version in cache key

## Migration Patterns

### Strangler Fig
Gradually route traffic from legacy to new system.

### Anti-Corruption Layer
Translate between new and legacy system models.

### Expand-Contract
1. Add new column (nullable)
2. Dual-write old + new
3. Backfill data
4. Switch reads to new
5. Remove old column
