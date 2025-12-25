---
name: data-table-patterns
description: Provides advanced TanStack Table patterns for React with shadcn/ui integration. Covers grouping, aggregation, column/row pinning, faceted filtering, and column visibility toggles. Triggers on requests for data grids, admin dashboards, financial tables, or when combining multiple TanStack Table features together.
---

# Data Table Patterns

Advanced patterns for TanStack Table v8 with shadcn/ui integration. Focuses on complex features that require careful integration—not basics covered in docs.

## Quick Reference

| Feature | Row Model Required | State Type | Key APIs |
|---------|-------------------|------------|----------|
| Grouping | `getGroupedRowModel()` | `GroupingState` | `column.getToggleGroupingHandler()`, `row.getIsGrouped()` |
| Filtering | `getFilteredRowModel()` | `ColumnFiltersState` | `column.setFilterValue()`, `column.getFilterValue()` |
| Faceting | `getFacetedRowModel()` | - | `column.getFacetedUniqueValues()`, `column.getFacetedMinMaxValues()` |
| Col Pinning | - | `ColumnPinningState` | `column.pin()`, `column.getIsPinned()` |
| Row Pinning | - | `RowPinningState` | `row.pin()`, `row.getIsPinned()` |
| Visibility | - | `VisibilityState` | `column.toggleVisibility()`, `column.getIsVisible()` |

## Feature Guides

- **Grouping & Aggregation**: See [references/grouping.md](references/grouping.md)
- **Column & Row Pinning**: See [references/pinning.md](references/pinning.md)
- **Faceted Filtering**: See [references/filtering.md](references/filtering.md)
- **Column Visibility**: See [references/visibility.md](references/visibility.md)
- **shadcn/ui Components**: See [references/shadcn-components.md](references/shadcn-components.md)

## Multi-Feature Table Setup

When combining features, follow this checklist:

```
Multi-Feature Table Checklist:
- [ ] Define column definitions with all feature options
- [ ] Set up state for each feature (sorting, filtering, grouping, etc.)
- [ ] Import required row models
- [ ] Configure table options with state and handlers
- [ ] Implement cell rendering for grouped/aggregated cells
- [ ] Add UI controls (toolbar, pagination, view options)
- [ ] Test feature interactions (grouping + sorting, filtering + pagination)
```

Import row models and configure state in this order:

```tsx
import {
  useReactTable,
  getCoreRowModel,
  getFilteredRowModel,
  getSortedRowModel,
  getPaginationRowModel,
  getGroupedRowModel,
  getExpandedRowModel,
  getFacetedRowModel,
  getFacetedUniqueValues,
  getFacetedMinMaxValues,
  type ColumnDef,
  type ColumnFiltersState,
  type SortingState,
  type VisibilityState,
  type GroupingState,
  type ColumnPinningState,
  type RowPinningState,
  type ExpandedState,
} from "@tanstack/react-table"

const [sorting, setSorting] = useState<SortingState>([])
const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([])
const [columnVisibility, setColumnVisibility] = useState<VisibilityState>({})
const [grouping, setGrouping] = useState<GroupingState>([])
const [expanded, setExpanded] = useState<ExpandedState>({})
const [columnPinning, setColumnPinning] = useState<ColumnPinningState>({
  left: [],
  right: [],
})
const [rowPinning, setRowPinning] = useState<RowPinningState>({
  top: [],
  bottom: [],
})

const table = useReactTable({
  data,
  columns,
  state: {
    sorting,
    columnFilters,
    columnVisibility,
    grouping,
    expanded,
    columnPinning,
    rowPinning,
  },
  onSortingChange: setSorting,
  onColumnFiltersChange: setColumnFilters,
  onColumnVisibilityChange: setColumnVisibility,
  onGroupingChange: setGrouping,
  onExpandedChange: setExpanded,
  onColumnPinningChange: setColumnPinning,
  onRowPinningChange: setRowPinning,
  getCoreRowModel: getCoreRowModel(),
  getFilteredRowModel: getFilteredRowModel(),
  getSortedRowModel: getSortedRowModel(),
  getPaginationRowModel: getPaginationRowModel(),
  getGroupedRowModel: getGroupedRowModel(),
  getExpandedRowModel: getExpandedRowModel(),
  getFacetedRowModel: getFacetedRowModel(),
  getFacetedUniqueValues: getFacetedUniqueValues(),
  getFacetedMinMaxValues: getFacetedMinMaxValues(),
})
```

## Column Definition Patterns

### Advanced Column with All Features

```tsx
const columns: ColumnDef<Data>[] = [
  {
    accessorKey: "status",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Status" />,
    cell: ({ row }) => <Badge>{row.getValue("status")}</Badge>,
    // Filtering
    filterFn: "equals", // or custom: (row, id, value) => value.includes(row.getValue(id))
    // Grouping
    enableGrouping: true,
    aggregationFn: "count",
    aggregatedCell: ({ getValue }) => `${getValue()} items`,
    // Visibility
    enableHiding: true,
    // Pinning
    enablePinning: true,
    // Faceting - use meta for filter UI hints
    meta: { filterVariant: "select" }, // "text" | "range" | "select"
  },
  {
    accessorKey: "amount",
    header: "Amount",
    aggregationFn: "sum",
    aggregatedCell: ({ getValue }) => 
      new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" })
        .format(getValue<number>()),
    meta: { filterVariant: "range" },
  },
]
```

### TypeScript: Extend ColumnMeta

```tsx
declare module "@tanstack/react-table" {
  interface ColumnMeta<TData extends RowData, TValue> {
    filterVariant?: "text" | "range" | "select"
    align?: "left" | "center" | "right"
  }
}
```

## Cell Rendering for Grouped Rows

Handle grouped, aggregated, and placeholder cells differently:

```tsx
{row.getVisibleCells().map((cell) => (
  <TableCell key={cell.id}>
    {cell.getIsGrouped() ? (
      // Grouped cell - render expander + value
      <button onClick={row.getToggleExpandedHandler()}>
        {row.getIsExpanded() ? "▼" : "▶"}{" "}
        {flexRender(cell.column.columnDef.cell, cell.getContext())}
        {" "}({row.subRows.length})
      </button>
    ) : cell.getIsAggregated() ? (
      // Aggregated cell - use aggregatedCell renderer
      flexRender(cell.column.columnDef.aggregatedCell, cell.getContext())
    ) : cell.getIsPlaceholder() ? null : (
      // Regular cell
      flexRender(cell.column.columnDef.cell, cell.getContext())
    )}
  </TableCell>
))}
```

## Common Pitfalls

1. **Missing row models**: Features silently fail without their row model
2. **State order**: Pinning → Column ordering → Grouping (affects column flow)
3. **Grouped column mode**: Set `groupedColumnMode: false` to keep grouped columns in place
4. **Faceting depends on filtering**: `getFacetedRowModel` must come before faceted value functions
5. **Sticky pinning requires CSS**: TanStack only provides state, not styling

## Additional Research

For edge cases or features not covered here, query the **DeepWiki MCP server** for TanStack Table documentation:

```
# Example queries (using DeepWiki MCP tool):
DeepWiki:ask repo="tanstack/table" question="How do I implement manual server-side grouping?"
DeepWiki:ask repo="tanstack/table" question="What are the available built-in aggregation functions?"
DeepWiki:ask repo="tanstack/table" question="How does column ordering interact with pinning?"
DeepWiki:ask repo="tanstack/table" question="How to implement row virtualization with grouping?"
```

Useful topics: `grouping-and-expanding`, `column-pinning`, `row-pinning`, `column-filtering`, `column-visibility`, `virtualization`
