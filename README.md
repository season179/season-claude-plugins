# Season's Claude Code Plugins

A marketplace of Claude Code plugins for AI development, web app UX, observability, and productivity.

## Installation

Add this marketplace to Claude Code:

```
/plugin marketplace add season179/season-claude-plugins
```

Then install individual plugins:

```
/plugin install <plugin-name>@season-claude-plugins
```

## Available Plugins

### AI Development

| Plugin | Description |
|--------|-------------|
| **ai-elements** | React components and hooks for AI chat interfaces with Vercel AI SDK |
| **ai-sdk-agents** | Building AI agents with Vercel AI SDK (tools, workflows, loop control) |
| **exa-search** | Exa semantic search API integration for RAG and web search |
| **using-tavily-search** | Tavily search, extract, crawl APIs for LLM tools |
| **langfuse-observability-typescript** | Langfuse TypeScript SDK v4 for LLM observability |

### Design & UX

| Plugin | Description |
|--------|-------------|
| **designing-web-app-ux** | Web application UI/UX patterns and accessibility |
| **design-system-extractor** | Extract design tokens from websites/screenshots |
| **data-table-patterns** | TanStack Table patterns with shadcn/ui (grouping, pinning, filtering) |
| **creating-mermaid-diagrams** | MermaidJS diagrams with proper layout |

### Developer Tools

| Plugin | Description |
|--------|-------------|
| **biome-lint-advisor** | Context-aware Biome linting analysis |
| **pino-logger** | Pino logger patterns for TypeScript/Bun |
| **solution-architect-skill** | System design with Cloudflare/Hono stack |

### Automation & Productivity

| Plugin | Description |
|--------|-------------|
| **n8n-workflow-builder** | n8n workflow configuration guidance |
| **xlsx** | Excel spreadsheet operations with formulas |

## Documentation

- [Claude Code Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Marketplace Configuration](.claude-plugin/marketplace.json)

## License

MIT
