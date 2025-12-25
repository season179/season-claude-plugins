# HTTP Logging Reference

Integration patterns for web frameworks with pino and pino-http.

## Contents

- [pino-http Basics](#pino-http-basics)
- [Express Integration](#express-integration)
- [Fastify Integration](#fastify-integration)
- [Hono Integration](#hono-integration)
- [Elysia Integration](#elysia-integration)
- [Request/Response Serializers](#requestresponse-serializers)
- [Filtering and Skipping Logs](#filtering-and-skipping-logs)

## pino-http Basics

Install pino-http:

```bash
bun add pino-http
```

### Configuration Options

```typescript
import pinoHttp from "pino-http";
import pino from "pino";

const httpLogger = pinoHttp({
  logger: pino(),
  
  // Generate request IDs
  genReqId: (req) => {
    return req.headers["x-request-id"]?.toString() || crypto.randomUUID();
  },
  
  // Custom log level based on response
  customLogLevel: (req, res, error) => {
    if (res.statusCode >= 500 || error) return "error";
    if (res.statusCode >= 400) return "warn";
    return "info";
  },
  
  // Custom success message
  customSuccessMessage: (req, res, responseTime) => {
    return `${req.method} ${req.url} completed`;
  },
  
  // Skip certain requests
  autoLogging: {
    ignore: (req) => req.url === "/health",
  },
});
```

## Express Integration

```typescript
import express from "express";
import pino from "pino";
import pinoHttp from "pino-http";

const logger = pino({
  level: process.env.LOG_LEVEL || "info",
  redact: ["req.headers.authorization", "req.headers.cookie"],
});

const app = express();

app.use(
  pinoHttp({
    logger,
    
    autoLogging: {
      ignore: (req) => req.url === "/health",
    },
    
    genReqId: (req) =>
      req.headers["x-request-id"]?.toString() || crypto.randomUUID(),
    
    customLogLevel: (_req, res, error) => {
      if (error || res.statusCode >= 500) return "error";
      if (res.statusCode >= 400) return "warn";
      return "info";
    },
    
    serializers: {
      req: (req) => ({
        method: req.method,
        url: req.url,
      }),
      res: (res) => ({
        statusCode: res.statusCode,
      }),
    },
  })
);

app.use((err: Error, req: express.Request, res: express.Response, _next: express.NextFunction) => {
  req.log.error({ err }, "Request error");
  res.status(500).json({ error: "Internal server error" });
});
```

## Fastify Integration

Fastify has built-in Pino support:

```typescript
import Fastify from "fastify";

const fastify = Fastify({
  logger: {
    level: "info",
    transport:
      process.env.NODE_ENV === "development"
        ? {
            target: "pino-pretty",
            options: {
              translateTime: "HH:MM:ss Z",
              ignore: "pid,hostname",
            },
          }
        : undefined,
  },
});

fastify.get("/", async (request, reply) => {
  request.log.info("Processing request");
  return { status: "ok" };
});
```

### Custom Fastify Logger

```typescript
import Fastify from "fastify";
import pino from "pino";

const customLogger = pino({
  level: "info",
  formatters: {
    level: (label) => ({ level: label.toUpperCase() }),
  },
});

const fastify = Fastify({
  loggerInstance: customLogger,
});
```

## Hono Integration

### Basic Middleware

```typescript
import { Hono } from "hono";
import pino from "pino";

const logger = pino({ level: process.env.LOG_LEVEL || "info" });

type Variables = {
  log: pino.Logger;
  requestId: string;
};

const app = new Hono<{ Variables: Variables }>();

app.use("*", async (c, next) => {
  const requestId = c.req.header("x-request-id") || crypto.randomUUID();
  const start = Date.now();

  const reqLogger = logger.child({
    requestId,
    method: c.req.method,
    path: c.req.path,
  });

  c.set("log", reqLogger);
  c.set("requestId", requestId);
  c.header("x-request-id", requestId);

  reqLogger.info("Request started");

  try {
    await next();
  } catch (error) {
    reqLogger.error({ err: error }, "Request error");
    throw error;
  }

  reqLogger.info({
    status: c.res.status,
    responseTime: Date.now() - start,
  }, "Request completed");
});

app.get("/api/users", async (c) => {
  const log = c.get("log");
  log.info("Fetching users");
  return c.json({ users: [] });
});

export default app;
```

## Elysia Integration

```typescript
import { Elysia } from "elysia";
import pino from "pino";

const logger = pino();

const app = new Elysia()
  .derive(({ request }) => {
    const requestId = request.headers.get("x-request-id") || crypto.randomUUID();
    return {
      log: logger.child({
        requestId,
        method: request.method,
        path: new URL(request.url).pathname,
      }),
      requestId,
    };
  })
  .onRequest(({ log }) => {
    log.info("Request started");
  })
  .onAfterResponse(({ log, set }) => {
    log.info({ status: set.status }, "Request completed");
  })
  .get("/", ({ log }) => {
    log.info("Hello route");
    return "Hello Elysia";
  })
  .listen(3000);
```

## Request/Response Serializers

### Minimal Serializers

```typescript
const httpLogger = pinoHttp({
  serializers: {
    req(req) {
      return {
        id: req.id,
        method: req.method,
        url: req.url,
      };
    },
    res(res) {
      return {
        statusCode: res.statusCode,
      };
    },
  },
});
```

### Comprehensive Serializers

```typescript
const httpLogger = pinoHttp({
  serializers: {
    req(req) {
      return {
        id: req.id,
        method: req.method,
        url: req.url,
        headers: {
          "user-agent": req.headers["user-agent"],
          "content-type": req.headers["content-type"],
        },
      };
    },
    res(res) {
      return {
        statusCode: res.statusCode,
      };
    },
    err(err) {
      return {
        type: err.constructor.name,
        message: err.message,
        stack: err.stack,
      };
    },
  },
});
```

## Filtering and Skipping Logs

### Skip Specific Paths

```typescript
const httpLogger = pinoHttp({
  autoLogging: {
    ignore: (req) => {
      const skipPaths = ["/health", "/ready", "/metrics", "/favicon.ico"];
      return skipPaths.some((path) => req.url?.startsWith(path));
    },
  },
});
```

### Skip Static Assets

```typescript
const staticExtensions = [".css", ".js", ".png", ".jpg", ".ico", ".svg"];

const httpLogger = pinoHttp({
  autoLogging: {
    ignore: (req) => {
      return staticExtensions.some((ext) => req.url?.endsWith(ext));
    },
  },
});
```
