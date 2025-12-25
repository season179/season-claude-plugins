# Column Visibility

## Table of Contents
1. [Setup](#setup)
2. [Column Configuration](#column-configuration)
3. [Visibility Toggle UI](#visibility-toggle-ui)
4. [Persist Visibility](#persist-visibility)

## Setup

```tsx
import { type VisibilityState } from "@tanstack/react-table"

const [columnVisibility, setColumnVisibility] = useState<VisibilityState>({
  // Hidden by default
  "internalId": false,
  "metadata": false,
})

const table = useReactTable({
  data,
  columns,
  state: { columnVisibility },
  onColumnVisibilityChange: setColumnVisibility,
})
```

### Initial Visibility via Table Options

```tsx
const table = useReactTable({
  data,
  columns,
  initialState: {
    columnVisibility: {
      description: false, // Hidden by default
      createdAt: false,
    },
  },
})
```

## Column Configuration

### Disable Hiding for Specific Columns

```tsx
const columns: ColumnDef<Data>[] = [
  {
    id: "select",
    enableHiding: false, // Always visible, not in toggle list
  },
  {
    accessorKey: "name",
    enableHiding: true, // Default, can be toggled
  },
  {
    id: "actions",
    enableHiding: false, // Actions should always be visible
  },
]
```

### Disable Column Visibility Globally

```tsx
const table = useReactTable({
  enableHiding: false, // Disable for all columns
})
```

## Visibility Toggle UI

### shadcn/ui View Options Dropdown

```tsx
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Button } from "@/components/ui/button"
import { Settings2 } from "lucide-react"

interface DataTableViewOptionsProps<TData> {
  table: Table<TData>
}

export function DataTableViewOptions<TData>({
  table,
}: DataTableViewOptionsProps<TData>) {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button
          variant="outline"
          size="sm"
          className="ml-auto hidden h-8 lg:flex"
        >
          <Settings2 className="mr-2 h-4 w-4" />
          View
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-[180px]">
        <DropdownMenuLabel>Toggle columns</DropdownMenuLabel>
        <DropdownMenuSeparator />
        {table
          .getAllColumns()
          .filter(
            (column) =>
              typeof column.accessorFn !== "undefined" && column.getCanHide()
          )
          .map((column) => {
            return (
              <DropdownMenuCheckboxItem
                key={column.id}
                className="capitalize"
                checked={column.getIsVisible()}
                onCheckedChange={(value) => column.toggleVisibility(!!value)}
              >
                {column.id}
              </DropdownMenuCheckboxItem>
            )
          })}
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
```

### Column Header with Hide Option

Integrate hide option into sortable column headers:

```tsx
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Button } from "@/components/ui/button"
import { ArrowDown, ArrowUp, ChevronsUpDown, EyeOff } from "lucide-react"

interface DataTableColumnHeaderProps<TData, TValue> {
  column: Column<TData, TValue>
  title: string
}

export function DataTableColumnHeader<TData, TValue>({
  column,
  title,
}: DataTableColumnHeaderProps<TData, TValue>) {
  if (!column.getCanSort() && !column.getCanHide()) {
    return <div>{title}</div>
  }

  return (
    <div className="flex items-center space-x-2">
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button
            variant="ghost"
            size="sm"
            className="-ml-3 h-8 data-[state=open]:bg-accent"
          >
            <span>{title}</span>
            {column.getIsSorted() === "desc" ? (
              <ArrowDown className="ml-2 h-4 w-4" />
            ) : column.getIsSorted() === "asc" ? (
              <ArrowUp className="ml-2 h-4 w-4" />
            ) : (
              <ChevronsUpDown className="ml-2 h-4 w-4" />
            )}
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="start">
          {column.getCanSort() && (
            <>
              <DropdownMenuItem onClick={() => column.toggleSorting(false)}>
                <ArrowUp className="mr-2 h-3.5 w-3.5 text-muted-foreground/70" />
                Asc
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => column.toggleSorting(true)}>
                <ArrowDown className="mr-2 h-3.5 w-3.5 text-muted-foreground/70" />
                Desc
              </DropdownMenuItem>
            </>
          )}
          {column.getCanSort() && column.getCanHide() && (
            <DropdownMenuSeparator />
          )}
          {column.getCanHide() && (
            <DropdownMenuItem onClick={() => column.toggleVisibility(false)}>
              <EyeOff className="mr-2 h-3.5 w-3.5 text-muted-foreground/70" />
              Hide
            </DropdownMenuItem>
          )}
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  )
}
```

### Show All / Hide All Buttons

```tsx
function VisibilityControls<TData>({ table }: { table: Table<TData> }) {
  const hidableColumns = table
    .getAllColumns()
    .filter((column) => column.getCanHide())

  const allVisible = hidableColumns.every((col) => col.getIsVisible())
  const noneVisible = hidableColumns.every((col) => !col.getIsVisible())

  return (
    <div className="flex gap-2">
      <Button
        variant="outline"
        size="sm"
        onClick={() => {
          hidableColumns.forEach((col) => col.toggleVisibility(true))
        }}
        disabled={allVisible}
      >
        Show all
      </Button>
      <Button
        variant="outline"
        size="sm"
        onClick={() => {
          hidableColumns.forEach((col) => col.toggleVisibility(false))
        }}
        disabled={noneVisible}
      >
        Hide all
      </Button>
    </div>
  )
}
```

## Persist Visibility

### Local Storage Persistence

```tsx
const STORAGE_KEY = "data-table-visibility"

function usePersistedVisibility() {
  const [columnVisibility, setColumnVisibility] = useState<VisibilityState>(
    () => {
      if (typeof window === "undefined") return {}
      const stored = localStorage.getItem(STORAGE_KEY)
      return stored ? JSON.parse(stored) : {}
    }
  )

  // Persist on change
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(columnVisibility))
  }, [columnVisibility])

  return [columnVisibility, setColumnVisibility] as const
}

// Usage
function DataTable() {
  const [columnVisibility, setColumnVisibility] = usePersistedVisibility()
  
  const table = useReactTable({
    state: { columnVisibility },
    onColumnVisibilityChange: setColumnVisibility,
    // ...
  })
}
```

### URL-based Persistence

```tsx
import { useSearchParams } from "next/navigation"

function useUrlVisibility() {
  const searchParams = useSearchParams()
  const router = useRouter()

  const columnVisibility = useMemo(() => {
    const hidden = searchParams.get("hidden")?.split(",") ?? []
    return hidden.reduce((acc, col) => ({ ...acc, [col]: false }), {})
  }, [searchParams])

  const setColumnVisibility: OnChangeFn<VisibilityState> = (updater) => {
    const newState =
      typeof updater === "function" ? updater(columnVisibility) : updater
    
    const hiddenColumns = Object.entries(newState)
      .filter(([_, visible]) => !visible)
      .map(([col]) => col)
    
    const params = new URLSearchParams(searchParams)
    if (hiddenColumns.length) {
      params.set("hidden", hiddenColumns.join(","))
    } else {
      params.delete("hidden")
    }
    router.push(`?${params.toString()}`)
  }

  return [columnVisibility, setColumnVisibility] as const
}
```

### Reset to Default

```tsx
function ResetVisibilityButton<TData>({ table }: { table: Table<TData> }) {
  return (
    <Button
      variant="ghost"
      size="sm"
      onClick={() => table.resetColumnVisibility()}
    >
      Reset columns
    </Button>
  )
}
```

## Column Visibility State Format

```ts
type VisibilityState = Record<string, boolean>

// Example:
{
  "id": false,        // Hidden
  "name": true,       // Visible (can be omitted, true is default)
  "email": true,
  "createdAt": false, // Hidden
}
```

## API Reference

| Method | Description |
|--------|-------------|
| `column.getCanHide()` | Whether column can be hidden |
| `column.getIsVisible()` | Current visibility state |
| `column.toggleVisibility(value?)` | Toggle or set visibility |
| `column.getToggleVisibilityHandler()` | Event handler for checkbox |
| `table.getVisibleLeafColumns()` | All currently visible columns |
| `table.resetColumnVisibility()` | Reset to initial state |
| `table.setColumnVisibility(state)` | Set visibility state |

## DeepWiki Queries

For advanced visibility scenarios, query the DeepWiki MCP server:

```
DeepWiki:ask repo="tanstack/table" question="How does column visibility interact with column groups?"
DeepWiki:ask repo="tanstack/table" question="How to hide columns on mobile using visibility state?"
DeepWiki:ask repo="tanstack/table" question="What happens to hidden columns during export?"
```
