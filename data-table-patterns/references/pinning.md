# Column & Row Pinning

## Table of Contents
1. [Column Pinning Setup](#column-pinning-setup)
2. [Sticky CSS Implementation](#sticky-css-implementation)
3. [Split Table Approach](#split-table-approach)
4. [Row Pinning](#row-pinning)
5. [shadcn/ui Pin Controls](#shadcnui-pin-controls)

## Column Pinning Setup

```tsx
import {
  type ColumnPinningState,
} from "@tanstack/react-table"

const [columnPinning, setColumnPinning] = useState<ColumnPinningState>({
  left: ["select", "name"], // Column IDs to pin left
  right: ["actions"],       // Column IDs to pin right
})

const table = useReactTable({
  data,
  columns,
  state: { columnPinning },
  onColumnPinningChange: setColumnPinning,
  // Disable pinning for specific columns
  enableColumnPinning: true, // or per-column: enablePinning: false
})
```

### Initial Pinning via Column Definition

```tsx
const columns: ColumnDef<Data>[] = [
  {
    id: "select",
    enablePinning: true,
    // Pin by default - set in initialState instead
  },
  {
    accessorKey: "name",
    enablePinning: true,
  },
  {
    id: "actions",
    enablePinning: false, // Cannot be pinned
  },
]

// Set initial pinning
const table = useReactTable({
  initialState: {
    columnPinning: {
      left: ["select"],
      right: ["actions"],
    },
  },
})
```

## Sticky CSS Implementation

TanStack Table only manages state—sticky positioning requires CSS.

### Helper Function for Pinned Styles

```tsx
function getPinnedCellStyles(column: Column<any>): React.CSSProperties {
  const isPinned = column.getIsPinned()
  const isLastLeftPinned = 
    isPinned === "left" && column.getIsLastColumn("left")
  const isFirstRightPinned =
    isPinned === "right" && column.getIsFirstColumn("right")

  return {
    position: isPinned ? "sticky" : "relative",
    left: isPinned === "left" ? `${column.getStart("left")}px` : undefined,
    right: isPinned === "right" ? `${column.getAfter("right")}px` : undefined,
    zIndex: isPinned ? 1 : 0,
    backgroundColor: isPinned ? "hsl(var(--background))" : undefined,
    // Shadow to indicate pinned edge
    boxShadow: isLastLeftPinned
      ? "-4px 0 4px -4px hsl(var(--border)) inset"
      : isFirstRightPinned
        ? "4px 0 4px -4px hsl(var(--border)) inset"
        : undefined,
  }
}
```

### Table with Sticky Columns

```tsx
<div className="relative overflow-auto">
  <Table>
    <TableHeader>
      {table.getHeaderGroups().map((headerGroup) => (
        <TableRow key={headerGroup.id}>
          {headerGroup.headers.map((header) => (
            <TableHead
              key={header.id}
              colSpan={header.colSpan}
              style={{
                ...getPinnedCellStyles(header.column),
                width: header.getSize(),
              }}
            >
              {/* Header content */}
            </TableHead>
          ))}
        </TableRow>
      ))}
    </TableHeader>
    <TableBody>
      {table.getRowModel().rows.map((row) => (
        <TableRow key={row.id}>
          {row.getVisibleCells().map((cell) => (
            <TableCell
              key={cell.id}
              style={{
                ...getPinnedCellStyles(cell.column),
                width: cell.column.getSize(),
              }}
            >
              {flexRender(cell.column.columnDef.cell, cell.getContext())}
            </TableCell>
          ))}
        </TableRow>
      ))}
    </TableBody>
  </Table>
</div>
```

### Tailwind Classes for Sticky (Alternative)

```tsx
<TableHead
  className={cn(
    header.column.getIsPinned() && "sticky bg-background z-10",
    header.column.getIsPinned() === "left" && "left-0",
    header.column.getIsPinned() === "right" && "right-0",
    header.column.getIsLastColumn("left") && "shadow-[inset_-4px_0_4px_-4px_hsl(var(--border))]",
    header.column.getIsFirstColumn("right") && "shadow-[inset_4px_0_4px_-4px_hsl(var(--border))]"
  )}
  style={{
    left: header.column.getIsPinned() === "left" 
      ? `${header.column.getStart("left")}px` 
      : undefined,
    right: header.column.getIsPinned() === "right"
      ? `${header.column.getAfter("right")}px`
      : undefined,
  }}
>
```

## Split Table Approach

Alternative: render pinned columns as separate tables.

```tsx
function SplitPinnedTable({ table }: { table: Table<Data> }) {
  const leftPinned = table.getLeftHeaderGroups()
  const center = table.getCenterHeaderGroups()
  const rightPinned = table.getRightHeaderGroups()

  return (
    <div className="flex overflow-hidden">
      {/* Left pinned table */}
      {leftPinned.length > 0 && (
        <Table className="flex-none border-r">
          <TableHeader>
            {leftPinned.map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <TableHead key={header.id}>
                    {flexRender(header.column.columnDef.header, header.getContext())}
                  </TableHead>
                ))}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows.map((row) => (
              <TableRow key={row.id}>
                {row.getLeftVisibleCells().map((cell) => (
                  <TableCell key={cell.id}>
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}

      {/* Center scrollable table */}
      <div className="flex-1 overflow-x-auto">
        <Table>
          {/* ... center columns ... */}
        </Table>
      </div>

      {/* Right pinned table */}
      {rightPinned.length > 0 && (
        <Table className="flex-none border-l">
          {/* ... right pinned columns ... */}
        </Table>
      )}
    </div>
  )
}
```

## Row Pinning

Keep specific rows at top/bottom of table.

```tsx
import { type RowPinningState } from "@tanstack/react-table"

const [rowPinning, setRowPinning] = useState<RowPinningState>({
  top: [],    // Row IDs to pin to top
  bottom: [], // Row IDs to pin to bottom
})

const table = useReactTable({
  data,
  columns,
  state: { rowPinning },
  onRowPinningChange: setRowPinning,
  // Keep pinned rows visible across pagination/filtering
  keepPinnedRows: true,
})
```

### Row Pin Toggle

```tsx
function RowPinButton({ row }: { row: Row<Data> }) {
  const isPinned = row.getIsPinned()
  
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon">
          <Pin className={cn("h-4 w-4", isPinned && "fill-current")} />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent>
        <DropdownMenuItem onClick={() => row.pin("top")}>
          Pin to top
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => row.pin("bottom")}>
          Pin to bottom
        </DropdownMenuItem>
        {isPinned && (
          <DropdownMenuItem onClick={() => row.pin(false)}>
            Unpin
          </DropdownMenuItem>
        )}
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
```

### Render Pinned Rows Separately

```tsx
<TableBody>
  {/* Top pinned rows */}
  {table.getTopRows().map((row) => (
    <TableRow key={row.id} className="bg-muted/50 sticky top-0 z-10">
      {/* ... */}
    </TableRow>
  ))}
  
  {/* Regular rows */}
  {table.getCenterRows().map((row) => (
    <TableRow key={row.id}>
      {/* ... */}
    </TableRow>
  ))}
  
  {/* Bottom pinned rows */}
  {table.getBottomRows().map((row) => (
    <TableRow key={row.id} className="bg-muted/50 sticky bottom-0 z-10">
      {/* ... */}
    </TableRow>
  ))}
</TableBody>
```

## shadcn/ui Pin Controls

### Column Header with Pin Options

```tsx
function DataTableColumnHeader<TData>({
  column,
  title,
}: {
  column: Column<TData>
  title: string
}) {
  if (!column.getCanPin()) {
    return <div>{title}</div>
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="sm" className="-ml-3 h-8">
          <span>{title}</span>
          {column.getIsPinned() && (
            <Pin className="ml-2 h-3 w-3 fill-current" />
          )}
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="start">
        {column.getIsPinned() !== "left" && (
          <DropdownMenuItem onClick={() => column.pin("left")}>
            <PinLeft className="mr-2 h-3.5 w-3.5" />
            Pin to left
          </DropdownMenuItem>
        )}
        {column.getIsPinned() !== "right" && (
          <DropdownMenuItem onClick={() => column.pin("right")}>
            <PinRight className="mr-2 h-3.5 w-3.5" />
            Pin to right
          </DropdownMenuItem>
        )}
        {column.getIsPinned() && (
          <>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={() => column.pin(false)}>
              <PinOff className="mr-2 h-3.5 w-3.5" />
              Unpin
            </DropdownMenuItem>
          </>
        )}
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
```

## DeepWiki Queries

For advanced pinning scenarios, query the DeepWiki MCP server:

```
DeepWiki:ask repo="tanstack/table" question="How does column pinning interact with column ordering?"
DeepWiki:ask repo="tanstack/table" question="How to implement sticky row pinning with virtualization?"
DeepWiki:ask repo="tanstack/table" question="What is the difference between getStart and getAfter for pinned columns?"
DeepWiki:ask repo="tanstack/table" question="How to pin columns by default in initialState?"
```
