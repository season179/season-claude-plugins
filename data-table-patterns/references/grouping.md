# Grouping & Aggregation

## Table of Contents
1. [Setup](#setup)
2. [Aggregation Functions](#aggregation-functions)
3. [Custom Aggregation](#custom-aggregation)
4. [UI Implementation](#ui-implementation)
5. [Grouped Column Mode](#grouped-column-mode)

## Setup

```tsx
import {
  getGroupedRowModel,
  getExpandedRowModel,
  type GroupingState,
  type ExpandedState,
} from "@tanstack/react-table"

const [grouping, setGrouping] = useState<GroupingState>([])
const [expanded, setExpanded] = useState<ExpandedState>({})

const table = useReactTable({
  data,
  columns,
  state: { grouping, expanded },
  onGroupingChange: setGrouping,
  onExpandedChange: setExpanded,
  getGroupedRowModel: getGroupedRowModel(),
  getExpandedRowModel: getExpandedRowModel(),
  // Keep grouped columns in their original position
  groupedColumnMode: false, // 'reorder' | 'remove' | false
})
```

## Aggregation Functions

### Built-in Functions

| Function | Description | Best For |
|----------|-------------|----------|
| `sum` | Sum of values | Numeric totals |
| `min` | Minimum value | Range boundaries |
| `max` | Maximum value | Range boundaries |
| `extent` | [min, max] tuple | Range display |
| `mean` | Average | Statistics |
| `median` | Middle value | Statistics |
| `unique` | Array of unique values | Categorical |
| `uniqueCount` | Count of unique | Categorical summary |
| `count` | Row count | All types |

### Column Definition with Aggregation

```tsx
{
  accessorKey: "revenue",
  header: "Revenue",
  // Built-in aggregation
  aggregationFn: "sum",
  // How to render aggregated value
  aggregatedCell: ({ getValue }) => (
    <span className="font-semibold">
      {new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
      }).format(getValue<number>())}
    </span>
  ),
  // Regular cell rendering
  cell: ({ getValue }) => (
    new Intl.NumberFormat("en-US", {
      style: "currency", 
      currency: "USD",
    }).format(getValue<number>())
  ),
}
```

## Custom Aggregation

### Define Custom Aggregation Function

```tsx
// Type declaration for custom aggregation
declare module "@tanstack/react-table" {
  interface AggregationFns {
    weightedAverage: AggregationFn<unknown>
    concatenate: AggregationFn<unknown>
  }
}

const table = useReactTable({
  // ...other options
  aggregationFns: {
    weightedAverage: (columnId, leafRows, childRows) => {
      let totalWeight = 0
      let weightedSum = 0
      
      leafRows.forEach((row) => {
        const value = row.getValue<number>(columnId)
        const weight = row.getValue<number>("quantity")
        if (value != null && weight != null) {
          weightedSum += value * weight
          totalWeight += weight
        }
      })
      
      return totalWeight > 0 ? weightedSum / totalWeight : 0
    },
    concatenate: (columnId, leafRows) => {
      const values = leafRows
        .map((row) => row.getValue<string>(columnId))
        .filter(Boolean)
      return [...new Set(values)].join(", ")
    },
  },
})

// Use in column def
{
  accessorKey: "price",
  aggregationFn: "weightedAverage",
}
```

### Override Grouping Value

```tsx
{
  accessorKey: "firstName",
  // Custom value used for grouping (not display)
  getGroupingValue: (row) => `${row.firstName} ${row.lastName}`,
}
```

## UI Implementation

### Header with Group Toggle

```tsx
function DataTableColumnHeader<TData>({ 
  column, 
  title 
}: { 
  column: Column<TData>
  title: string 
}) {
  return (
    <div className="flex items-center gap-2">
      {column.getCanGroup() && (
        <Button
          variant="ghost"
          size="sm"
          onClick={column.getToggleGroupingHandler()}
        >
          {column.getIsGrouped() ? (
            <Ungroup className="h-4 w-4" />
          ) : (
            <Group className="h-4 w-4" />
          )}
        </Button>
      )}
      <span>{title}</span>
      {column.getIsGrouped() && (
        <Badge variant="secondary">
          {column.getGroupedIndex() + 1}
        </Badge>
      )}
    </div>
  )
}
```

### Cell Rendering with Expansion

```tsx
function GroupedCell<TData>({ cell, row }: { cell: Cell<TData, unknown>; row: Row<TData> }) {
  if (cell.getIsGrouped()) {
    return (
      <Button
        variant="ghost"
        size="sm"
        onClick={row.getToggleExpandedHandler()}
        disabled={!row.getCanExpand()}
        className="gap-1"
      >
        {row.getIsExpanded() ? (
          <ChevronDown className="h-4 w-4" />
        ) : (
          <ChevronRight className="h-4 w-4" />
        )}
        {flexRender(cell.column.columnDef.cell, cell.getContext())}
        <Badge variant="outline">{row.subRows.length}</Badge>
      </Button>
    )
  }

  if (cell.getIsAggregated()) {
    return flexRender(
      cell.column.columnDef.aggregatedCell ?? cell.column.columnDef.cell,
      cell.getContext()
    )
  }

  if (cell.getIsPlaceholder()) {
    return null
  }

  return flexRender(cell.column.columnDef.cell, cell.getContext())
}
```

### Table Body with Visual Distinction

```tsx
<TableBody>
  {table.getRowModel().rows.map((row) => (
    <TableRow
      key={row.id}
      className={cn(
        row.getIsGrouped() && "bg-muted/50 font-medium",
        row.depth > 0 && "bg-muted/20"
      )}
    >
      {row.getVisibleCells().map((cell) => (
        <TableCell
          key={cell.id}
          style={{ paddingLeft: `${row.depth * 2 + 1}rem` }}
        >
          <GroupedCell cell={cell} row={row} />
        </TableCell>
      ))}
    </TableRow>
  ))}
</TableBody>
```

## Grouped Column Mode

Control how grouped columns are displayed:

```tsx
const table = useReactTable({
  // ...
  // 'reorder' - Move grouped columns to start (default)
  // 'remove' - Hide grouped columns from table
  // false - Keep columns in original position
  groupedColumnMode: false,
})
```

### When to Use Each Mode

| Mode | Use Case |
|------|----------|
| `'reorder'` | Pivot-table style, grouped columns as row headers |
| `'remove'` | Value shown in expand button, avoid duplication |
| `false` | Keep table structure intact, show value in cell |

## DeepWiki Queries

For advanced grouping scenarios, query the DeepWiki MCP server:

```
DeepWiki:ask repo="tanstack/table" question="How to implement server-side grouping with manual aggregation?"
DeepWiki:ask repo="tanstack/table" question="How does getGroupedRowModel handle nested grouping?"
DeepWiki:ask repo="tanstack/table" question="What is the difference between leafRows and childRows in aggregation?"
DeepWiki:ask repo="tanstack/table" question="How to show aggregated value in grouped cell instead of first leaf value?"
```
