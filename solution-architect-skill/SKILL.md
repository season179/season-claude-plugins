---
name: solution-architecting
description: >-
  Designs production systems using architecture styles (microservices, event-driven, CQRS, serverless),
  design patterns (circuit breaker, saga, outbox), and quality attributes (scalability, availability, performance).
  Implements with preferred stack: Cloudflare Workers, Hono, D1, AI SDK, WorkOS, Playwright, PostHog, GitHub Actions.
  Use when designing systems, evaluating architectural trade-offs, selecting technologies, planning APIs,
  modeling data, or making infrastructure decisions.
---

# Solution Architecting

## Decision Framework

1. **Clarify requirements** - Functional + NFRs
2. **Identify constraints** - Budget, timeline, team, compliance
3. **Evaluate trade-offs** - Optimize for what matters most
4. **Document decisions** - Use ADRs
5. **Plan for evolution** - Design for change

## Reference Files

| File | Content |
|------|---------|
| [architecture-styles.md](references/architecture-styles.md) | Monolith → Microservices → Event-Driven selection |
| [design-patterns.md](references/design-patterns.md) | Resilience, data, communication patterns |
| [quality-attributes.md](references/quality-attributes.md) | Scalability, availability, performance, security |
| [api-design.md](references/api-design.md) | REST/GraphQL/gRPC, versioning, error handling |
| [data-architecture.md](references/data-architecture.md) | Database selection, consistency, caching |
| [stack-cloudflare.md](references/stack-cloudflare.md) | Workers, D1, KV, R2, Durable Objects |
| [stack-hono.md](references/stack-hono.md) | Hono, Drizzle, Zod patterns |
| [stack-ai.md](references/stack-ai.md) | AI SDK, agents, tools, streaming |
| [stack-platform.md](references/stack-platform.md) | WorkOS, PostHog, Playwright, GitHub Actions |

## Stack Preferences

| Category | Default | Escalate When |
|----------|---------|---------------|
| **Compute** | Cloudflare Workers | >30s CPU, >128MB memory, GPU needed |
| **Database** | D1 | >10GB data, need JSONB/FTS, multi-region writes |
| **Framework** | Hono | - |
| **Auth** | WorkOS | - |
| **AI** | AI SDK | - |
| **Testing** | Playwright | - |
| **Analytics** | PostHog | - |
| **CI/CD** | GitHub Actions | - |

## Quick Decisions

### Architecture Style
```
Small team + unclear domain → Modular Monolith
Independent scaling needed → Microservices  
Async/loose coupling critical → Event-Driven
Variable load + minimal ops → Serverless (Workers)
```

### Database
```
Relational + <10GB + edge latency → D1
Relational + >10GB or advanced SQL → PostgreSQL via Hyperdrive
Key-value/config/cache → KV
Files/objects → R2
```

### When to Leave Workers
- Long-running processes >30 seconds
- Memory >128MB per request
- Persistent WebSockets >10 minutes
- Custom binaries or GPU

## ADR Template

```markdown
# ADR-{N}: {Title}

## Status
Proposed | Accepted | Deprecated

## Context
What motivates this decision?

## Decision
What change are we making?

## Consequences
What becomes easier/harder?
```
