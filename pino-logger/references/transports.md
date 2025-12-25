# Transports Reference

Transports handle where and how logs are processed. Pino runs transports in worker threads to avoid blocking the main event loop.

## Contents

- [Basic Transports](#basic-transports)
- [Multi-Transport](#multi-transport)
- [File Transport](#file-transport)
- [Pretty Printing](#pretty-printing)
- [Custom Transports](#custom-transports)
- [Common Transport Packages](#common-transport-packages)

## Basic Transports

### Single Transport

```typescript
import pino from "pino";

const logger = pino({
  transport: {
    target: "pino-pretty",
    options: { colorize: true },
  },
});
```

**Note**: For Bun, prefer CLI piping over transport configuration. See [bun-specific.md](bun-specific.md).

## Multi-Transport

Send logs to multiple destinations:

```typescript
import pino from "pino";

const logger = pino({
  transport: {
    targets: [
      // Console with pretty printing
      {
        target: "pino-pretty",
        options: { colorize: true },
        level: "debug",
      },
      // File output
      {
        target: "pino/file",
        options: { destination: "./logs/app.log", mkdir: true },
        level: "info",
      },
      // Error-only file
      {
        target: "pino/file",
        options: { destination: "./logs/error.log", mkdir: true },
        level: "error",
      },
    ],
  },
});
```

## File Transport

### Basic File Logging

```typescript
const logger = pino({
  transport: {
    target: "pino/file",
    options: {
      destination: "./logs/app.log",
      mkdir: true,
    },
  },
});
```

### Destination Helper (Low-level)

For maximum performance without worker threads:

```typescript
import pino from "pino";

// Async writes (faster)
const logger = pino(
  pino.destination({
    dest: "./app.log",
    sync: false,
    mkdir: true,
  })
);
```

### Log Rotation

Install `pino-roll`:

```bash
bun add pino-roll
```

```typescript
const logger = pino({
  transport: {
    target: "pino-roll",
    options: {
      file: "./logs/app",
      frequency: "daily",
      mkdir: true,
      size: "10m",
      extension: ".log",
    },
  },
});
```

## Pretty Printing

### Development Configuration

```typescript
const logger = pino({
  transport: {
    target: "pino-pretty",
    options: {
      colorize: true,
      translateTime: "HH:MM:ss Z",
      ignore: "pid,hostname",
      levelFirst: true,
    },
  },
});
```

### Pretty Options

| Option | Description |
|--------|-------------|
| `colorize` | Enable colored output |
| `translateTime` | Format: `"HH:MM:ss Z"` or `"SYS:standard"` |
| `ignore` | Fields to hide: `"pid,hostname"` |
| `levelFirst` | Show level before timestamp |
| `singleLine` | Compact single-line output |

## Custom Transports

### Creating a Custom Transport

```typescript
// my-transport.ts
import build from "pino-abstract-transport";

export default async function (options: { destination: string }) {
  return build(async function (source) {
    for await (const obj of source) {
      const line = JSON.stringify(obj);
      await fetch(options.destination, {
        method: "POST",
        body: line,
      });
    }
  });
}
```

### Using Custom Transport

```typescript
const logger = pino({
  transport: {
    target: "./my-transport.ts",
    options: { destination: "https://logs.example.com/ingest" },
  },
});
```

## Common Transport Packages

### pino-loki (Grafana Loki)

```bash
bun add pino-loki
```

```typescript
const logger = pino({
  transport: {
    target: "pino-loki",
    options: {
      host: "http://localhost:3100",
      labels: { app: "my-app" },
      batching: true,
      interval: 5,
    },
  },
});
```

### pino-elasticsearch

```bash
bun add pino-elasticsearch
```

```typescript
const logger = pino({
  transport: {
    target: "pino-elasticsearch",
    options: {
      node: "http://localhost:9200",
      index: "logs",
      esVersion: 8,
    },
  },
});
```

### @axiomhq/pino

```bash
bun add @axiomhq/pino
```

```typescript
const logger = pino({
  transport: {
    target: "@axiomhq/pino",
    options: {
      dataset: process.env.AXIOM_DATASET,
      token: process.env.AXIOM_TOKEN,
    },
  },
});
```

### pino-opentelemetry-transport

```bash
bun add pino-opentelemetry-transport
```

```typescript
const logger = pino({
  transport: {
    target: "pino-opentelemetry-transport",
    options: {
      resourceAttributes: {
        "service.name": "my-service",
        "service.version": "1.0.0",
      },
    },
  },
});
```
