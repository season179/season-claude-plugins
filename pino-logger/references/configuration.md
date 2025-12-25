# Pino Configuration Reference

## Contents

- [Logger Options](#logger-options)
- [Formatters](#formatters)
- [Timestamps](#timestamps)
- [Serializers](#serializers)
- [Redaction](#redaction)
- [Environment-Aware Configuration](#environment-aware-configuration)

## Logger Options

### Full Configuration Example

```typescript
import pino, { type LoggerOptions } from "pino";

const options: LoggerOptions = {
  // Minimum log level
  level: process.env.LOG_LEVEL || "info",
  
  // Logger name (appears in each log)
  name: "my-app",
  
  // Redact sensitive data
  redact: ["password", "token", "*.secret"],
  
  // Enable/disable logging
  enabled: true,
  
  // Base bindings (added to every log)
  base: {
    env: process.env.NODE_ENV,
    version: process.env.APP_VERSION,
  },
  
  // Message key name (default: "msg")
  messageKey: "msg",
  
  // Error key name (default: "err")
  errorKey: "err",
};

const logger = pino(options);
```

### Level Configuration

```typescript
// Dynamic level from environment
const logger = pino({
  level: process.env.PINO_LOG_LEVEL || "info",
});

// Change level at runtime
logger.level = "debug";

// Check if level is enabled before expensive operations
if (logger.isLevelEnabled("debug")) {
  logger.debug({ expensive: computeExpensiveData() }, "Debug data");
}
```

## Formatters

Formatters transform log data before output:

```typescript
const logger = pino({
  formatters: {
    // Transform level to uppercase string
    level(label, number) {
      return { level: label.toUpperCase() };
    },
    
    // Customize bindings
    bindings(bindings) {
      return {
        pid: bindings.pid,
        host: bindings.hostname,
        service: "my-service",
      };
    },
    
    // Transform the log object
    log(object) {
      return { ...object };
    },
  },
});
```

## Timestamps

```typescript
import pino from "pino";

// ISO timestamp (recommended)
const logger = pino({
  timestamp: pino.stdTimeFunctions.isoTime,
});
// Output: "time":"2024-01-15T10:30:00.000Z"

// Unix epoch milliseconds (default)
const loggerEpoch = pino({
  timestamp: pino.stdTimeFunctions.epochTime,
});
// Output: "time":1705315800000

// Custom timestamp with different key
const loggerCustom = pino({
  timestamp: () => `,"timestamp":"${new Date().toISOString()}"`,
});
```

## Serializers

Serializers transform specific object types:

```typescript
const logger = pino({
  serializers: {
    // Standard serializers
    req: pino.stdSerializers.req,
    res: pino.stdSerializers.res,
    err: pino.stdSerializers.err,
    
    // Custom user serializer
    user(user) {
      return {
        id: user.id,
        email: maskEmail(user.email),
        role: user.role,
        // Never log passwords, tokens
      };
    },
  },
});

function maskEmail(email: string): string {
  const [local, domain] = email.split("@");
  return `${local[0]}***@${domain}`;
}
```

## Redaction

### Path-based Redaction

```typescript
const logger = pino({
  redact: {
    paths: [
      // Direct properties
      "password",
      "token",
      "apiKey",
      
      // Nested properties
      "user.password",
      "config.database.password",
      
      // Wildcard - any property named password
      "*.password",
      "**.password", // Deep wildcard
      
      // HTTP headers
      "req.headers.authorization",
      "req.headers.cookie",
    ],
    
    // Custom censor value (default: "[Redacted]")
    censor: "[REDACTED]",
    
    // Or remove entirely
    remove: true,
  },
});
```

## Environment-Aware Configuration

### Production Setup

```typescript
import pino, { type LoggerOptions } from "pino";

type Environment = "development" | "test" | "production";

function createLogger(env: Environment = "development") {
  const baseOptions: LoggerOptions = {
    level: process.env.LOG_LEVEL || "info",
    formatters: {
      level: (label) => ({ level: label.toUpperCase() }),
    },
    timestamp: pino.stdTimeFunctions.isoTime,
    redact: {
      paths: ["password", "token", "*.password", "req.headers.authorization"],
      remove: true,
    },
  };

  const envConfigs: Record<Environment, Partial<LoggerOptions>> = {
    development: { level: "debug" },
    test: { level: "silent" },
    production: {
      level: "info",
      base: {
        env: "production",
        version: process.env.APP_VERSION,
      },
    },
  };

  return pino({ ...baseOptions, ...envConfigs[env] });
}

export const logger = createLogger(
  (process.env.NODE_ENV as Environment) || "development"
);
```

### Mixin for Dynamic Context

```typescript
const logger = pino({
  mixin(_context, level) {
    return {
      levelName: pino.levels.labels[level],
    };
  },
});
```
