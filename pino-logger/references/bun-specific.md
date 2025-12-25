# Bun-Specific Pino Usage

Pino works with Bun but requires special consideration for transports and bundling.

## Contents

- [Basic Usage](#basic-usage)
- [Known Issues and Workarounds](#known-issues-and-workarounds)
- [Bundling with Bun](#bundling-with-bun)
- [Development Setup](#development-setup)
- [Production Setup](#production-setup)
- [Recommended Patterns](#recommended-patterns)

## Basic Usage

Pino works out of the box for basic logging:

```typescript
import pino from "pino";

const logger = pino({
  level: process.env.LOG_LEVEL || "info",
});

logger.info("Hello from Bun!");
```

## Known Issues and Workarounds

### Transport Compatibility

Pino transports use Node.js worker threads internally. Some may have compatibility issues with Bun versions.

**Preferred approach**: Use CLI piping instead of transport configuration:

```bash
# Development - pipe to pino-pretty
bun run src/index.ts | bunx pino-pretty
```

```json
{
  "scripts": {
    "dev": "bun --watch src/index.ts | bunx pino-pretty",
    "start": "bun src/index.ts"
  }
}
```

### File Destination (Reliable)

Using `pino.destination()` works reliably in Bun:

```typescript
import pino from "pino";

const logger = pino(
  { level: "info" },
  pino.destination({
    dest: "./logs/app.log",
    sync: false,
    mkdir: true,
  })
);
```

## Bundling with Bun

When bundling with `Bun.build()`, transports are resolved at runtime and need special handling.

### Using bun-plugin-pino

Install the plugin:

```bash
bun add -d bun-plugin-pino
```

Create build script:

```typescript
// build.ts
import { bunPluginPino } from "bun-plugin-pino";

await Bun.build({
  entrypoints: ["./src/index.ts"],
  outdir: "./dist",
  target: "bun",
  plugins: [
    bunPluginPino({
      transports: ["pino-pretty"], // List all transports used
    }),
  ],
});
```

### Without Plugin

Avoid transports in bundled code. Use simple logger configuration:

```typescript
// logger.ts - safe for bundling
import pino from "pino";

export const logger = pino({
  level: process.env.LOG_LEVEL || "info",
  formatters: {
    level: (label) => ({ level: label.toUpperCase() }),
  },
  timestamp: pino.stdTimeFunctions.isoTime,
});
```

Then pipe to pino-pretty via CLI in development.

## Development Setup

```json
{
  "scripts": {
    "dev": "NODE_ENV=development bun --watch src/index.ts | bunx pino-pretty",
    "start": "NODE_ENV=production bun src/index.ts",
    "build": "bun run build.ts"
  }
}
```

## Production Setup

### With File Logging

```typescript
import pino from "pino";

const isProd = process.env.NODE_ENV === "production";

export const logger = isProd
  ? pino(
      {
        level: "info",
        formatters: {
          level: (label) => ({ level: label.toUpperCase() }),
        },
        timestamp: pino.stdTimeFunctions.isoTime,
      },
      pino.destination({
        dest: process.env.LOG_FILE || "./logs/app.log",
        mkdir: true,
        sync: false,
      })
    )
  : pino({ level: "debug" });
```

### Multi-Destination

```typescript
import pino from "pino";

function createLogger() {
  const level = process.env.LOG_LEVEL || "info";
  const baseConfig = {
    level,
    formatters: {
      level: (label: string) => ({ level: label.toUpperCase() }),
    },
    timestamp: pino.stdTimeFunctions.isoTime,
  };

  if (process.env.NODE_ENV === "production") {
    const streams = [
      { stream: process.stdout },
      {
        stream: pino.destination({
          dest: "./logs/app.log",
          mkdir: true,
          sync: false,
        }),
      },
      {
        level: "error" as const,
        stream: pino.destination({
          dest: "./logs/error.log",
          mkdir: true,
          sync: false,
        }),
      },
    ];

    return pino(baseConfig, pino.multistream(streams));
  }

  return pino({ ...baseConfig, level: "debug" });
}

export const logger = createLogger();
```

## Recommended Patterns

### Pattern 1: Simple Console Logger

Best for most use cases:

```typescript
import pino from "pino";

export const logger = pino({
  level: process.env.LOG_LEVEL || "info",
  formatters: {
    level: (label) => ({ level: label.toUpperCase() }),
  },
  timestamp: pino.stdTimeFunctions.isoTime,
  base: {
    service: process.env.SERVICE_NAME || "app",
  },
  redact: {
    paths: ["password", "token", "*.password"],
    remove: true,
  },
});
```

### Pattern 2: Hono Request Context

```typescript
import { Hono } from "hono";
import pino from "pino";

const logger = pino({
  level: process.env.LOG_LEVEL || "info",
  formatters: {
    level: (label) => ({ level: label.toUpperCase() }),
  },
  timestamp: pino.stdTimeFunctions.isoTime,
});

type Env = {
  Variables: {
    log: pino.Logger;
    requestId: string;
  };
};

const app = new Hono<Env>();

app.use("*", async (c, next) => {
  const requestId = c.req.header("x-request-id") || crypto.randomUUID();
  const start = Bun.nanoseconds();

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

  const durationMs = (Bun.nanoseconds() - start) / 1_000_000;
  log.info({ status: c.res.status, durationMs: durationMs.toFixed(2) }, "Request completed");
});

export default app;
```

### Pattern 3: Logger Module

```typescript
// src/lib/logger.ts
import pino, { type Logger, type LoggerOptions } from "pino";

const baseOptions: LoggerOptions = {
  formatters: {
    level: (label) => ({ level: label.toUpperCase() }),
  },
  timestamp: pino.stdTimeFunctions.isoTime,
  base: {
    service: process.env.SERVICE_NAME || "app",
    version: process.env.APP_VERSION || "unknown",
  },
  redact: {
    paths: ["password", "token", "*.password", "*.token"],
    remove: true,
  },
};

const level = process.env.NODE_ENV === "production"
  ? (process.env.LOG_LEVEL || "info")
  : "debug";

export const logger: Logger = pino({ ...baseOptions, level });

export function createChildLogger(bindings: Record<string, unknown>): Logger {
  return logger.child(bindings);
}

export function createRequestLogger(requestId: string, userId?: string): Logger {
  return logger.child({
    requestId,
    ...(userId && { userId }),
  });
}
```
