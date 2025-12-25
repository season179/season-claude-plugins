# MermaidJS Layout Guide

Advanced layout strategies for visually balanced diagrams.

## Contents

- [Direction Strategy](#direction-strategy)
- [Node Arrangement](#node-arrangement)
- [Subgraph Layout](#subgraph-layout)
- [Spacing Techniques](#spacing-techniques)
- [Common Patterns](#common-patterns)
- [Sequence Diagram Layout](#sequence-diagram-layout)

---

## Direction Strategy

| Direction | Best For | Aspect |
|-----------|----------|--------|
| `TD` | Hierarchies, decisions | Portrait |
| `LR` | Pipelines, timelines | Landscape |
| `BT` | Inverted org charts | Portrait |
| `RL` | RTL content | Landscape |

---

## Node Arrangement

### Balanced Branching

Shorter branches first for visual balance:

```mermaid
flowchart TD
    A --> B{Check}
    B -->|No| C[Exit]
    B -->|Yes| D --> E --> F --> G
```

### Parallel Paths

Use `&` for simultaneous connections:

```mermaid
flowchart LR
    Start --> A & B & C
    A & B & C --> End
```

### Minimize Crossings

Reorder node declarations to reduce line crossings. Nodes declared first appear in earlier positions.

---

## Subgraph Layout

### Direction Override

Override parent direction inside subgraphs:

```mermaid
flowchart TD
    subgraph horizontal[Horizontal Section]
        direction LR
        A --> B --> C
    end
    horizontal --> D
```

### Nested Subgraphs

```mermaid
flowchart TD
    subgraph outer[System]
        subgraph inner[Core]
            A --> B
        end
    end
```

### Styling Subgraphs

```mermaid
flowchart TD
    subgraph api[API Layer]
        Gateway --> Services
    end
    style api fill:#e3f2fd,stroke:#1565c0
```

---

## Spacing Techniques

### Link Length

Extra dashes for longer links:

```mermaid
flowchart LR
    A --> B
    A ---> C
    A ----> D
```

### Multi-line Labels

Use `<br>` for line breaks:

```mermaid
flowchart TD
    A[User Authentication<br>and Authorization]
```

### Invisible Links

Use `~~~` for alignment without visible connections:

```mermaid
flowchart LR
    A ~~~ B ~~~ C
    A --> D
    B --> D
    C --> D
```

---

## Common Patterns

### Pipeline

```mermaid
flowchart LR
    subgraph input[Input]
        A[Parse]
    end
    subgraph process[Process]
        B[Transform]
    end
    subgraph output[Output]
        C[Export]
    end
    input --> process --> output
```

### Hub and Spoke

```mermaid
flowchart TD
    Hub((Central))
    Hub --> A & B & C & D
    A & B & C & D --> Hub
```

### Fork-Join

```mermaid
flowchart TD
    Start --> Fork{Split}
    Fork --> A & B & C
    A & B & C --> Join{Merge}
    Join --> End
```

### Layered Architecture

```mermaid
flowchart TD
    subgraph ui[Presentation]
        direction LR
        Web ~~~ Mobile
    end
    subgraph logic[Business]
        API --> Services
    end
    subgraph data[Data]
        direction LR
        DB[(SQL)] ~~~ Cache[(Redis)]
    end
    ui --> logic --> data
```

---

## Sequence Diagram Layout

### Participant Ordering

Order left-to-right by interaction flow (initiator → responder):

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant A as API
    participant D as Database
```

### Activation Boxes

Show processing duration:

```mermaid
sequenceDiagram
    C->>+S: Request
    Note right of S: Processing
    S-->>-C: Response
```

### Visual Grouping

Use `rect` for sections:

```mermaid
sequenceDiagram
    rect rgb(240,248,255)
        Note over A,B: Authentication
        A->>B: Login
        B-->>A: Token
    end
```
