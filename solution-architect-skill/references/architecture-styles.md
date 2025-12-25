# Architecture Styles

## Contents
- Selection guide
- Modular Monolith
- Microservices
- Event-Driven
- CQRS
- Serverless
- Hexagonal

## Selection Guide

| Start With | When |
|------------|------|
| **Modular Monolith** | Early stage, small team, unclear boundaries |
| **Microservices** | Large team, independent deployment/scaling needed |
| **Event-Driven** | Loose coupling, async processing, audit trails |
| **Serverless** | Variable load, minimal ops, event-driven workloads |

**Default**: Start with Modular Monolith, extract services when boundaries become clear.

## Modular Monolith

Single deployable unit with clear internal boundaries:

```
┌─────────────────────────────────────┐
│            Application              │
├───────────┬───────────┬─────────────┤
│  Users    │  Orders   │  Payments   │
│  Module   │  Module   │  Module     │
├───────────┴───────────┴─────────────┤
│          Shared Database            │
└─────────────────────────────────────┘
```

**Rules:**
- Modules communicate via interfaces, not direct DB access
- Each module owns its tables
- Prepare for future extraction

## Microservices

Independent services with own databases:

```
┌─────────┐  ┌─────────┐  ┌─────────┐
│ Users   │  │ Orders  │  │Payments │
├─────────┤  ├─────────┤  ├─────────┤
│   DB    │  │   DB    │  │   DB    │
└────┬────┘  └────┬────┘  └────┬────┘
     └───────────┬───────────┘
           API Gateway
```

**When:** Large teams, polyglot persistence, different scaling needs, clear domain boundaries.

**Avoid:** Small teams, tight coupling, operational complexity concerns.

## Event-Driven

Components communicate via events:

**Event Notification** (simple):
```typescript
// Publish: { type: "OrderCreated", orderId: "123" }
// Consumers fetch additional data if needed
```

**Event-Carried State Transfer** (avoid callbacks):
```typescript
// Publish: { type: "OrderCreated", orderId, customerId, items, total }
// Consumers have all needed data
```

**Event Sourcing** (events as source of truth):
```typescript
// Store: OrderCreated → ItemAdded → OrderPaid → OrderShipped
// Current state = replay(events)
```

## CQRS

Separate read and write models:

```
Commands (Write)          Queries (Read)
- Validations             - Denormalized
- Business rules    →     - Optimized
- Domain events           - Cached
```

**Use:** Read/write patterns differ significantly, need optimized read models.

## Serverless (Workers)

```
Request → Worker → Response
              ↓
         D1/KV/R2
```

**Constraints:** 30s CPU limit, 128MB memory, stateless.

**Benefits:** Sub-5ms cold starts, 300+ edge locations, pay-per-use.

## Hexagonal (Ports & Adapters)

Isolate business logic from external concerns:

```
     Adapters (API, CLI, Webhooks)
              ↓
     Ports (Interfaces)
              ↓
     Domain (Pure Business Logic)
              ↓
     Ports (Repository Interfaces)
              ↓
     Adapters (DB, Cache, APIs)
```

**Benefits:** Testable core, technology-agnostic, clear boundaries.
