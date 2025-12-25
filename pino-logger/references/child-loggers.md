# Child Loggers Reference

Child loggers inherit parent configuration while adding contextual bindings.

## Contents

- [Basic Child Logger](#basic-child-logger)
- [Request-Scoped Logging](#request-scoped-logging)
- [Hierarchical Loggers](#hierarchical-loggers)
- [Child Logger Options](#child-logger-options)
- [Context Propagation Patterns](#context-propagation-patterns)

## Basic Child Logger

```typescript
import pino from "pino";

const logger = pino();

// Create child with additional bindings
const childLogger = logger.child({ module: "auth" });
childLogger.info("Authentication started");
// Output: { "module": "auth", "msg": "Authentication started" }

// Bindings are inherited by grandchildren
const grandchildLogger = childLogger.child({ method: "oauth" });
grandchildLogger.info("OAuth flow initiated");
// Output: { "module": "auth", "method": "oauth", "msg": "..." }
```

## Request-Scoped Logging

### Express Middleware

```typescript
import express from "express";
import pino from "pino";

const logger = pino();
const app = express();

declare global {
  namespace Express {
    interface Request {
      log: pino.Logger;
      requestId: string;
    }
  }
}

app.use((req, res, next) => {
  const requestId = (req.headers["x-request-id"] as string) || crypto.randomUUID();
  
  req.requestId = requestId;
  req.log = logger.child({
    requestId,
    method: req.method,
    url: req.url,
  });

  const startTime = Date.now();

  res.on("finish", () => {
    req.log.info({
      statusCode: res.statusCode,
      responseTime: Date.now() - startTime,
    }, "Request completed");
  });

  req.log.info("Request started");
  next();
});

app.get("/users/:id", async (req, res) => {
  req.log.info({ userId: req.params.id }, "Fetching user");
  // handler logic
});
```

### Hono Middleware (Bun)

```typescript
import { Hono } from "hono";
import pino from "pino";

const logger = pino();

type Variables = {
  log: pino.Logger;
  requestId: string;
};

const app = new Hono<{ Variables: Variables }>();

app.use("*", async (c, next) => {
  const requestId = c.req.header("x-request-id") || crypto.randomUUID();
  
  const reqLogger = logger.child({
    requestId,
    method: c.req.method,
    path: c.req.path,
  });

  c.set("log", reqLogger);
  c.set("requestId", requestId);

  const start = Date.now();
  reqLogger.info("Request started");

  await next();

  reqLogger.info({
    status: c.res.status,
    responseTime: Date.now() - start,
  }, "Request completed");
});

app.get("/api/users/:id", async (c) => {
  const log = c.get("log");
  log.info({ userId: c.req.param("id") }, "Fetching user");
});
```

## Hierarchical Loggers

Create structured logging hierarchy for complex applications:

```typescript
import pino from "pino";

const rootLogger = pino({ name: "my-app" });

// Service-level loggers
const authLogger = rootLogger.child({ service: "auth" });
const dbLogger = rootLogger.child({ service: "database" });
const apiLogger = rootLogger.child({ service: "api" });

export const loggers = {
  root: rootLogger,
  auth: authLogger,
  db: dbLogger,
  api: apiLogger,
} as const;
```

### Factory Pattern

```typescript
import pino, { type Logger } from "pino";

const rootLogger = pino();

interface LoggerContext {
  service?: string;
  component?: string;
}

export function createLogger(context: LoggerContext): Logger {
  return rootLogger.child(context);
}

// Usage
const userService = createLogger({ service: "users", component: "api" });
```

## Child Logger Options

Child loggers can override parent settings:

```typescript
const parentLogger = pino({ level: "info" });

// Override log level
const debugChild = parentLogger.child(
  { module: "debug-module" },
  { level: "debug" }
);

// Add message prefix
const prefixedChild = parentLogger.child(
  { module: "prefixed" },
  { msgPrefix: "[PREFIX] " }
);

prefixedChild.info("Hello");
// Output: { "msg": "[PREFIX] Hello", "module": "prefixed" }
```

## Context Propagation Patterns

### AsyncLocalStorage Pattern

```typescript
import { AsyncLocalStorage } from "async_hooks";
import pino from "pino";

interface RequestContext {
  requestId: string;
  logger: pino.Logger;
}

const asyncLocalStorage = new AsyncLocalStorage<RequestContext>();
const rootLogger = pino();

export function getLogger(): pino.Logger {
  return asyncLocalStorage.getStore()?.logger || rootLogger;
}

export function runWithContext<T>(
  requestId: string,
  fn: () => T
): T {
  const logger = rootLogger.child({ requestId });
  return asyncLocalStorage.run({ requestId, logger }, fn);
}

// Usage anywhere in call stack
function someDeepFunction() {
  const log = getLogger();
  log.info("This log includes request context automatically");
}
```

### Bindings Access

```typescript
const logger = pino();
const child = logger.child({ module: "auth", version: "1.0" });

// Get current bindings
const bindings = child.bindings();
// { module: "auth", version: "1.0" }

// Update bindings at runtime
child.setBindings({ module: "auth", version: "2.0" });
```
