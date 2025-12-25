# MermaidJS Diagram Types Reference

Quick syntax reference for each diagram type.

## Contents

- [Flowchart](#flowchart)
- [Sequence Diagram](#sequence-diagram)
- [Class Diagram](#class-diagram)
- [State Diagram](#state-diagram)
- [ER Diagram](#er-diagram)
- [Gantt Chart](#gantt-chart)
- [Pie Chart](#pie-chart)
- [Mindmap](#mindmap)
- [Timeline](#timeline)
- [Git Graph](#git-graph)

---

## Flowchart

```mermaid
flowchart TD
    start([Start]) --> check{Valid?}
    check -->|Yes| process[Process]
    check -->|No| error[Error]
    process --> done([End])
    error --> done
```

**Directions:** `TD` (top-down), `LR` (left-right), `BT` (bottom-top), `RL` (right-left)

**Node shapes:**
- `[text]` Rectangle
- `(text)` Rounded
- `{text}` Diamond
- `([text])` Stadium
- `[(text)]` Cylinder
- `((text))` Circle

**Arrows:**
- `-->` Arrow
- `---` Line
- `-.->` Dotted
- `==>` Thick
- `-->|label|` Labeled

---

## Sequence Diagram

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server
    participant D as Database

    C->>+S: Request
    S->>+D: Query
    D-->>-S: Data
    S-->>-C: Response
```

**Arrows:**
- `->` Solid line
- `-->` Dotted line
- `->>` Solid with arrowhead
- `-->>` Dotted with arrowhead
- `->>+` Activate target
- `-->>-` Deactivate target

**Blocks:** `alt`, `opt`, `loop`, `par`, `critical`, `rect`

---

## Class Diagram

```mermaid
classDiagram
    class Animal {
        +String name
        +makeSound() void
    }
    class Dog {
        +bark() void
    }
    Animal <|-- Dog
```

**Relationships:**
- `<|--` Inheritance
- `*--` Composition
- `o--` Aggregation
- `-->` Association
- `..>` Dependency

**Visibility:** `+` public, `-` private, `#` protected

---

## State Diagram

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Processing : start
    Processing --> Done : complete
    Processing --> Error : fail
    Done --> [*]
    Error --> Idle : retry
```

**Special states:**
- `[*]` Initial/final state
- `state "Name" as alias` State with description

---

## ER Diagram

```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE_ITEM : contains

    CUSTOMER {
        int id PK
        string name
        string email UK
    }
```

**Cardinality:**
- `||` Exactly one
- `o|` Zero or one
- `}|` One or more
- `}o` Zero or more

---

## Gantt Chart

```mermaid
gantt
    title Project Plan
    dateFormat YYYY-MM-DD

    section Phase 1
    Design    :a1, 2024-01-01, 7d
    Develop   :a2, after a1, 14d

    section Phase 2
    Test      :b1, after a2, 7d
    Deploy    :milestone, after b1, 0d
```

**Task modifiers:** `active`, `done`, `crit`, `milestone`

---

## Pie Chart

```mermaid
pie showData
    title Distribution
    "Category A" : 45
    "Category B" : 30
    "Category C" : 25
```

---

## Mindmap

```mermaid
mindmap
    root((Topic))
        Branch A
            Leaf 1
            Leaf 2
        Branch B
            Leaf 3
```

---

## Timeline

```mermaid
timeline
    title Project History
    2023 : Planning
    2024 : Development
         : Testing
    2025 : Launch
```

---

## Git Graph

```mermaid
gitGraph
    commit id: "Initial"
    branch develop
    checkout develop
    commit id: "Feature"
    checkout main
    merge develop
    commit id: "Release"
```
