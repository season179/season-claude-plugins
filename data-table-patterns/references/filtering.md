# Column Filtering & Faceting

## Table of Contents
1. [Setup](#setup)
2. [Filter Functions](#filter-functions)
3. [Faceted Filtering](#faceted-filtering)
4. [Filter UI Components](#filter-ui-components)
5. [Custom Filter Functions](#custom-filter-functions)
6. [Server-Side Filtering](#server-side-filtering)

## Setup

```tsx
import {
  getFilteredRowModel,
  getFacetedRowModel,
  getFacetedUniqueValues,
  getFacetedMinMaxValues,
  type ColumnFiltersState,
} from "@tanstack/react-table"

const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([])

const table = useReactTable({
  data,
  columns,
  state: { columnFilters },
  onColumnFiltersChange: setColumnFilters,
  getFilteredRowModel: getFilteredRowModel(),
  // Faceting (for dynamic filter options)
  getFacetedRowModel: getFacetedRowModel(),
  getFacetedUniqueValues: getFacetedUniqueValues(),
  getFacetedMinMaxValues: getFacetedMinMaxValues(),
})
```

## Filter Functions

### Built-in Filter Functions

| Function | Description | Value Type |
|----------|-------------|------------|
| `includesString` | Case-insensitive substring | `string` |
| `includesStringSensitive` | Case-sensitive substring | `string` |
| `equalsString` | Exact match (case-insensitive) | `string` |
| `arrIncludes` | Array includes value | `any` |
| `arrIncludesAll` | Array includes all values | `any[]` |
| `arrIncludesSome` | Array includes some values | `any[]` |
| `equals` | Strict equality | `any` |
| `weakEquals` | Loose equality | `any` |
| `inNumberRange` | Between [min, max] | `[number, number]` |

### Column Definition with Filter

```tsx
const columns: ColumnDef<Data>[] = [
  {
    accessorKey: "status",
    filterFn: "equals", // Built-in
    meta: { filterVariant: "select" },
  },
  {
    accessorKey: "amount",
    filterFn: "inNumberRange",
    meta: { filterVariant: "range" },
  },
  {
    accessorKey: "tags",
    filterFn: "arrIncludesSome", // For array columns
  },
]
```

## Faceted Filtering

Faceting generates dynamic filter options from data.

### Get Unique Values for Select Filter

```tsx
function SelectFilter({ column }: { column: Column<any> }) {
  // Get unique values from column data
  const facetedValues = column.getFacetedUniqueValues()
  
  // Convert Map to sorted array
  const options = useMemo(() => {
    return Array.from(facetedValues.keys())
      .sort()
      .slice(0, 5000) // Limit for performance
  }, [facetedValues])

  return (
    <Select
      value={column.getFilterValue() as string}
      onValueChange={(value) => column.setFilterValue(value || undefined)}
    >
      <SelectTrigger>
        <SelectValue placeholder="Select..." />
      </SelectTrigger>
      <SelectContent>
        <SelectItem value="">All</SelectItem>
        {options.map((option) => (
          <SelectItem key={option} value={option}>
            {option}
            <span className="ml-2 text-muted-foreground">
              ({facetedValues.get(option)})
            </span>
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  )
}
```

### Get Min/Max for Range Filter

```tsx
function RangeFilter({ column }: { column: Column<any> }) {
  const [min, max] = column.getFacetedMinMaxValues() ?? [0, 100]
  const filterValue = column.getFilterValue() as [number, number] | undefined

  return (
    <div className="flex gap-2">
      <Input
        type="number"
        min={min}
        max={max}
        value={filterValue?.[0] ?? ""}
        onChange={(e) =>
          column.setFilterValue((old: [number, number]) => [
            e.target.value ? Number(e.target.value) : undefined,
            old?.[1],
          ])
        }
        placeholder={`Min (${min})`}
        className="w-24"
      />
      <Input
        type="number"
        min={min}
        max={max}
        value={filterValue?.[1] ?? ""}
        onChange={(e) =>
          column.setFilterValue((old: [number, number]) => [
            old?.[0],
            e.target.value ? Number(e.target.value) : undefined,
          ])
        }
        placeholder={`Max (${max})`}
        className="w-24"
      />
    </div>
  )
}
```

## Filter UI Components

### Dynamic Filter Based on Column Meta

```tsx
// Extend column meta type
declare module "@tanstack/react-table" {
  interface ColumnMeta<TData extends RowData, TValue> {
    filterVariant?: "text" | "range" | "select" | "multi-select"
  }
}

function ColumnFilter({ column }: { column: Column<any> }) {
  const { filterVariant } = column.columnDef.meta ?? {}

  switch (filterVariant) {
    case "range":
      return <RangeFilter column={column} />
    case "select":
      return <SelectFilter column={column} />
    case "multi-select":
      return <MultiSelectFilter column={column} />
    default:
      return <TextFilter column={column} />
  }
}
```

### Debounced Text Filter

```tsx
function TextFilter({ column }: { column: Column<any> }) {
  const [value, setValue] = useState(
    (column.getFilterValue() as string) ?? ""
  )

  // Debounce filter updates
  useEffect(() => {
    const timeout = setTimeout(() => {
      column.setFilterValue(value || undefined)
    }, 300)
    return () => clearTimeout(timeout)
  }, [value, column])

  // Sync with external changes
  useEffect(() => {
    setValue((column.getFilterValue() as string) ?? "")
  }, [column.getFilterValue()])

  // Autocomplete suggestions from faceted values
  const suggestions = useMemo(() => {
    return Array.from(column.getFacetedUniqueValues().keys())
      .sort()
      .slice(0, 10)
  }, [column.getFacetedUniqueValues()])

  return (
    <div className="relative">
      <Input
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Search..."
        list={`${column.id}-suggestions`}
      />
      <datalist id={`${column.id}-suggestions`}>
        {suggestions.map((suggestion) => (
          <option key={suggestion} value={suggestion} />
        ))}
      </datalist>
    </div>
  )
}
```

### Faceted Filter (shadcn/ui Command-based)

```tsx
function FacetedFilter({
  column,
  title,
  options,
}: {
  column: Column<any>
  title: string
  options: { label: string; value: string; icon?: React.ComponentType }[]
}) {
  const facets = column.getFacetedUniqueValues()
  const selectedValues = new Set(column.getFilterValue() as string[])

  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button variant="outline" size="sm" className="h-8 border-dashed">
          <PlusCircle className="mr-2 h-4 w-4" />
          {title}
          {selectedValues.size > 0 && (
            <>
              <Separator orientation="vertical" className="mx-2 h-4" />
              <Badge variant="secondary" className="rounded-sm px-1">
                {selectedValues.size}
              </Badge>
            </>
          )}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[200px] p-0" align="start">
        <Command>
          <CommandInput placeholder={title} />
          <CommandList>
            <CommandEmpty>No results found.</CommandEmpty>
            <CommandGroup>
              {options.map((option) => {
                const isSelected = selectedValues.has(option.value)
                return (
                  <CommandItem
                    key={option.value}
                    onSelect={() => {
                      if (isSelected) {
                        selectedValues.delete(option.value)
                      } else {
                        selectedValues.add(option.value)
                      }
                      const filterValues = Array.from(selectedValues)
                      column.setFilterValue(
                        filterValues.length ? filterValues : undefined
                      )
                    }}
                  >
                    <div
                      className={cn(
                        "mr-2 flex h-4 w-4 items-center justify-center rounded-sm border border-primary",
                        isSelected
                          ? "bg-primary text-primary-foreground"
                          : "opacity-50"
                      )}
                    >
                      {isSelected && <Check className="h-4 w-4" />}
                    </div>
                    {option.icon && (
                      <option.icon className="mr-2 h-4 w-4 text-muted-foreground" />
                    )}
                    <span>{option.label}</span>
                    {facets?.get(option.value) && (
                      <span className="ml-auto text-xs text-muted-foreground">
                        {facets.get(option.value)}
                      </span>
                    )}
                  </CommandItem>
                )
              })}
            </CommandGroup>
            {selectedValues.size > 0 && (
              <>
                <CommandSeparator />
                <CommandGroup>
                  <CommandItem
                    onSelect={() => column.setFilterValue(undefined)}
                    className="justify-center text-center"
                  >
                    Clear filters
                  </CommandItem>
                </CommandGroup>
              </>
            )}
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  )
}
```

## Custom Filter Functions

### Multi-Value Filter (Tags/Categories)

```tsx
const columns: ColumnDef<Data>[] = [
  {
    accessorKey: "tags",
    filterFn: (row, id, filterValues: string[]) => {
      if (!filterValues?.length) return true
      const rowTags = row.getValue<string[]>(id)
      return filterValues.some((filter) => rowTags?.includes(filter))
    },
  },
]
```

### Date Range Filter

```tsx
const columns: ColumnDef<Data>[] = [
  {
    accessorKey: "createdAt",
    filterFn: (row, id, filterValue: [Date, Date] | undefined) => {
      if (!filterValue) return true
      const [start, end] = filterValue
      const date = row.getValue<Date>(id)
      if (!date) return false
      return date >= start && date <= end
    },
  },
]
```

## Server-Side Filtering

For large datasets, filter on the server.

```tsx
const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([])

// Fetch data with filters
const { data, isLoading } = useQuery({
  queryKey: ["data", columnFilters],
  queryFn: () =>
    fetch("/api/data?" + new URLSearchParams({
      filters: JSON.stringify(columnFilters),
    })).then((r) => r.json()),
})

const table = useReactTable({
  data: data ?? [],
  columns,
  state: { columnFilters },
  onColumnFiltersChange: setColumnFilters,
  // Skip client-side filtering
  manualFiltering: true,
  // No getFilteredRowModel needed
})
```

### Filter State Format

Column filters are stored as:

```ts
type ColumnFiltersState = {
  id: string      // Column ID
  value: unknown  // Filter value (type depends on filterFn)
}[]

// Example state:
[
  { id: "status", value: "active" },
  { id: "amount", value: [100, 500] },
  { id: "tags", value: ["react", "typescript"] },
]
```

## DeepWiki Queries

For advanced filtering scenarios, query the DeepWiki MCP server:

```
DeepWiki:ask repo="tanstack/table" question="How to implement fuzzy search filtering?"
DeepWiki:ask repo="tanstack/table" question="How does column filtering interact with global filtering?"
DeepWiki:ask repo="tanstack/table" question="How to filter nested object properties?"
DeepWiki:ask repo="tanstack/table" question="What filter functions are available for array columns?"
DeepWiki:ask repo="tanstack/table" question="How to implement server-side faceting?"
```
