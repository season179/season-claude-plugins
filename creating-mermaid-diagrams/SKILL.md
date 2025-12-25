---
name: creating-mermaid-diagrams
description: Creates visually appealing MermaidJS diagrams with proper layout, alignment, and structure. Use when generating flowcharts, sequence diagrams, class diagrams, ER diagrams, state diagrams, Gantt charts, pie charts, mindmaps, or any MermaidJS visualization. Triggers on requests for diagrams, flowcharts, visual workflows, architecture diagrams, or when .mmd files are involved.
---

# Creating MermaidJS Diagrams

Creates well-structured, visually balanced MermaidJS diagrams.

## Workflow

Copy this checklist and track progress:

```
Diagram Progress:
- [ ] Step 1: Select diagram type
- [ ] Step 2: Plan layout direction
- [ ] Step 3: Write diagram code
- [ ] Step 4: Validate syntax
- [ ] Step 5: Review and refine
```

**Step 1: Select diagram type**

| Content | Type |
|---------|------|
| Process flow, decisions | `flowchart` |
| API calls, interactions | `sequenceDiagram` |
| OOP structure | `classDiagram` |
| Database schema | `erDiagram` |
| Lifecycle, transitions | `stateDiagram-v2` |
| Project schedule | `gantt` |

**Step 2: Plan layout direction**

- `TD` (top-down): Hierarchies, decision trees
- `LR` (left-right): Pipelines, timelines, workflows
- `BT`/`RL`: Inverted flows, RTL content

**Step 3: Write diagram code**

Follow the layout principles below. See `references/layout-guide.md` for advanced patterns.

**Step 4: Validate syntax**

```bash
node scripts/validate_mermaid.js diagram.mmd
node scripts/validate_mermaid.js --code "flowchart TD; A-->B"
```

**Step 5: Review and refine**

Address any warnings about readability or style.

## Layout Principles

### Use descriptive node IDs

```mermaid
flowchart LR
    userInput[User Input] --> validateData[Validate] --> processOrder[Process]
```

### Balance branches

Place shorter branches first:

```mermaid
flowchart TD
    check{Valid?}
    check -->|No| error[Error]
    check -->|Yes| process --> validate --> save --> done
```

### Group with subgraphs

```mermaid
flowchart TD
    subgraph client[Client Layer]
        ui[Web UI]
    end
    subgraph server[Server Layer]
        api[API] --> db[(Database)]
    end
    client --> server
```

### Label decision branches

```mermaid
flowchart TD
    auth{Authorized?}
    auth -->|Yes| proceed[Continue]
    auth -->|No| deny[Access Denied]
```

### Control spacing

- `--->` for longer links
- `<br>` for multi-line labels
- `~~~` for invisible alignment links

## Examples

**Input**: "Show a user authentication flow"

**Output**:
```mermaid
flowchart TD
    start([Start]) --> checkToken{Has Token?}
    checkToken -->|No| login[Login Page]
    checkToken -->|Yes| validate{Token Valid?}
    login --> authenticate[Authenticate]
    authenticate --> issueToken[Issue Token]
    issueToken --> dashboard
    validate -->|Yes| dashboard[Dashboard]
    validate -->|No| login
```

**Input**: "API request sequence"

**Output**:
```mermaid
sequenceDiagram
    participant C as Client
    participant A as API
    participant D as Database

    C->>+A: POST /users
    A->>+D: INSERT user
    D-->>-A: user_id
    A-->>-C: 201 Created
```

**Input**: "Database schema for orders"

**Output**:
```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE_ITEM : contains
    PRODUCT ||--o{ LINE_ITEM : "ordered in"

    CUSTOMER {
        int id PK
        string name
        string email UK
    }
    ORDER {
        int id PK
        date created_at
        int customer_id FK
    }
```

## Diagram Type Reference

See `references/diagram-types.md` for syntax of each diagram type.

## Advanced Layout

See `references/layout-guide.md` for:
- Subgraph direction overrides
- Hub-and-spoke patterns
- Pipeline layouts
- Fork-join patterns
- Layered architecture
