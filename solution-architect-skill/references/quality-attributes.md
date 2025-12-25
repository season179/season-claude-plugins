# Quality Attributes

## Contents
- Scalability
- Availability
- Performance
- Security
- Reliability

## Scalability

### Strategies
- **Stateless services**: No server-side session state
- **Horizontal scaling**: Add instances, not bigger machines
- **Auto-scaling**: CPU 60-70% target, queue depth, custom metrics

### Load Patterns
| Pattern | Strategy |
|---------|----------|
| Predictable | Schedule-based scaling |
| Spiky | Pre-warm + aggressive scaling |
| Steady growth | Capacity planning |

## Availability

### Targets
| Level | Downtime/Year | Use Case |
|-------|---------------|----------|
| 99% | 3.65 days | Internal tools |
| 99.9% | 8.76 hours | Business apps |
| 99.99% | 52.6 min | Financial systems |

### Strategies
- **Redundancy**: Multiple instances, replicated databases
- **Multi-region**: Active-passive or active-active
- **Workers**: Inherently HA (300+ edge locations, no SPOF)

### Recovery Objectives
- **RTO**: Max acceptable downtime
- **RPO**: Max acceptable data loss

## Performance

### Metrics
- **Latency**: p50, p95, p99 response times
- **Throughput**: Requests per second
- **TTFB/TTLB**: Time to first/last byte

### Latency Budget Example
```
Total: 200ms
├── Edge routing: 5ms
├── Auth: 10ms
├── Business logic: 50ms
├── Database: 100ms
├── External API: 30ms
└── Serialization: 5ms
```

### Optimization
- **Caching hierarchy**: Memory → Edge (KV) → Distributed → DB
- **Connection pooling**: Hyperdrive for PostgreSQL
- **Async processing**: `waitUntil()` for non-critical work

## Security

See [stack-platform.md](stack-platform.md) for WorkOS implementation.

### Principles
- **Defense in depth**: Multiple security layers
- **Zero trust**: Verify every request
- **Least privilege**: Minimum necessary permissions

### Checklist
- [ ] Input validation (Zod schemas)
- [ ] Authentication on protected routes
- [ ] Authorization checks (RBAC/ABAC)
- [ ] Secrets in environment variables
- [ ] HTTPS enforced
- [ ] Security headers (HSTS, CSP, X-Frame-Options)
- [ ] Rate limiting
- [ ] Audit logging
- [ ] SQL injection prevented (parameterized queries)
- [ ] XSS prevented (output encoding, CSP)

## Reliability

### Design Principles
1. **Design for failure**: Assume everything fails
2. **Graceful degradation**: Partial > complete failure
3. **Fail fast**: Detect and surface errors quickly
4. **Limit blast radius**: Isolate failure impact

### Health Checks
```typescript
// Liveness
app.get('/health/live', (c) => c.json({ status: 'ok' }))

// Readiness
app.get('/health/ready', async (c) => {
  const dbOk = await checkDb(c.env.DB).catch(() => false)
  return c.json({ db: dbOk }, dbOk ? 200 : 503)
})
```

## Documenting NFRs

```markdown
## NFR: API Response Time

**Requirement**: p95 < 200ms

**Measurement**: PostHog events + Cloudflare Analytics

**Priority**: Must Have

**Trade-offs**: Aggressive caching may serve stale data
```
