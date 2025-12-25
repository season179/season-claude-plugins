---
name: pino-logger
description: Provides patterns and configuration for Pino, the high-performance JSON logger. Triggers when building logging systems, configuring transports, creating child loggers, implementing log redaction, integrating with Express/Fastify/Hono, or working with pino-http, pino-pretty, structured logging, request logging, or TypeScript/Bun logging setups.
---

# Pino Logger

Pino is a super-fast, low-overhead JSON logger. This skill provides patterns optimized for Bun runtime, React, and TypeScript.

## Learning More About Pino

For additional Pino documentation beyond this skill, use the deepwiki MCP tool to ask questions about the `pinojs/pino` repository. Example queries:

- "How do I configure pino transports in pinojs/pino?"
- "What are the pino child logger options in pinojs/pino?"
- "How does pino redaction work in pinojs/pino?"
- "What TypeScript types does pino export in pinojs/pino?"

Always include `pinojs/pino` in your query to target the correct repository.

## Setup Workflow

Copy this checklist when setting up Pino logging:

```
Pino Setup Progress:
- [ ] Step 1: Install packages
- [ ] Step 2: Create base logger configuration
- [ ] Step 3: Add environment-aware settings
- [ ] Step 4: Configure redaction for sensitive data
- [ ] Step 5: Test logger output
```

**Step 1: Install packages**

```bash
bun add pino
bun add -d pino-pretty
```

For HTTP request logging, also install:
```bash
bun add pino-http
```

**Step 2: Create base logger**

Create `src/lib/logger.ts`:

```typescript
import pino from "pino";

export const logger = pino({
  level: process.env.LOG_LEVEL || "info",
});
```

**Step 3: Add environment-aware settings**

See [references/configuration.md](references/configuration.md) for complete options.

**Step 4: Configure redaction**

Add sensitive field redaction (see Redaction section below).

**Step 5: Test logger output**

```typescript
logger.info({ userId: 123 }, "Test message");
// Run: bun run src/index.ts | bunx pino-pretty
```

## Reference Files

- **[references/configuration.md](references/configuration.md)**: Logger options, formatters, timestamps, serializers, redaction
- **[references/child-loggers.md](references/child-loggers.md)**: Request-scoped logging, context propagation
- **[references/transports.md](references/transports.md)**: Multi-destination logging, file output, external services
- **[references/http-logging.md](references/http-logging.md)**: Express, Fastify, Hono, Elysia integration
- **[references/bun-specific.md](references/bun-specific.md)**: Bun runtime considerations, bundling

## Core Patterns

### Recommended Base Logger

Use this as the default logger configuration:

```typescript
import pino, { type Logger } from "pino";

export const logger: Logger = pino({
  level: process.env.LOG_LEVEL || "info",
  formatters: {
    level: (label) => ({ level: label.toUpperCase() }),
  },
  timestamp: pino.stdTimeFunctions.isoTime,
});
```

### Child Logger for Request Context

```typescript
function createRequestLogger(
  parentLogger: pino.Logger,
  requestId: string,
  userId?: string
): pino.Logger {
  return parentLogger.child({
    requestId,
    ...(userId && { userId }),
  });
}
```

### Redaction (Required for Production)

Always configure redaction for sensitive data:

```typescript
const logger = pino({
  redact: {
    paths: [
      "password",
      "token",
      "apiKey",
      "*.password",
      "req.headers.authorization",
      "req.headers.cookie",
    ],
    remove: true,
  },
});
```

### Development Pretty Printing

In development, pipe output to pino-pretty instead of using transport:

```bash
bun run src/index.ts | bunx pino-pretty
```

Or in package.json:
```json
{
  "scripts": {
    "dev": "bun --watch src/index.ts | bunx pino-pretty"
  }
}
```

## Key Concepts

### Log Levels

Pino uses numeric levels (lower number = higher severity):

| Level | Number | Use Case |
|-------|--------|----------|
| fatal | 60 | Application crash |
| error | 50 | Operation failed |
| warn | 40 | Potential issue |
| info | 30 | Normal operation (default) |
| debug | 20 | Development details |
| trace | 10 | Fine-grained debugging |

### Structured Logging

Always pass objects as the first argument for structured data:

```typescript
// Correct - structured data is searchable
logger.info({ userId: 123, action: "login" }, "User logged in");

// Avoid - string interpolation loses structure
logger.info(`User ${userId} logged in`);
```

### Error Logging

Pass errors in the `err` field:

```typescript
try {
  await riskyOperation();
} catch (err) {
  logger.error({ err }, "Operation failed");
}
```

## Hono Integration (Bun)

```typescript
import { Hono } from "hono";
import pino from "pino";

const logger = pino({ level: "info" });

type Variables = { log: pino.Logger; requestId: string };
const app = new Hono<{ Variables: Variables }>();

app.use("*", async (c, next) => {
  const requestId = c.req.header("x-request-id") || crypto.randomUUID();
  const start = Date.now();

  const log = logger.child({
    requestId,
    method: c.req.method,
    path: c.req.path,
  });

  c.set("log", log);
  c.set("requestId", requestId);
  c.header("x-request-id", requestId);

  log.info("Request started");
  await next();
  log.info({ status: c.res.status, ms: Date.now() - start }, "Request completed");
});
```

## Bun Bundling

When bundling with `Bun.build()`, transports require `bun-plugin-pino`:

```bash
bun add -d bun-plugin-pino
```

```typescript
import { bunPluginPino } from "bun-plugin-pino";

await Bun.build({
  entrypoints: ["./src/index.ts"],
  outdir: "./dist",
  plugins: [bunPluginPino({ transports: ["pino-pretty"] })],
});
```

For simpler setups, avoid transports and use CLI piping instead.

## TypeScript Type Augmentation

Extend Pino types for custom bindings:

```typescript
declare module "pino" {
  interface Bindings {
    requestId?: string;
    userId?: string;
    service?: string;
  }
}
```
