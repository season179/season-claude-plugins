# UX Patterns Reference

## Contents
- State Management Patterns
- User Flow Patterns
- Feedback Patterns
- Data Interaction Patterns
- Navigation Patterns
- Confirmation Patterns

---

## State Management Patterns

### The Five UI States

Every data-driven component has five possible states:

```
┌─────────────┬────────────────────────────────────────────┐
│ State       │ Design Considerations                      │
├─────────────┼────────────────────────────────────────────┤
│ Empty       │ Explain why empty, provide clear CTA       │
│ Loading     │ Skeleton matches final layout, no shift    │
│ Partial     │ Show available data, indicate more loading │
│ Error       │ Explain what failed, how to recover        │
│ Ideal       │ Full data, all features available          │
└─────────────┴────────────────────────────────────────────┘
```

### State Transition Example

```jsx
function DataTable({ fetchData }) {
  const [state, setState] = useState('empty');
  const [data, setData] = useState([]);
  const [error, setError] = useState(null);

  // State transitions
  // empty → loading → ideal/error
  // ideal → loading (refresh) → ideal/error
  // error → loading (retry) → ideal/error

  if (state === 'loading') return <TableSkeleton rows={5} />;
  if (state === 'error') return <ErrorState error={error} onRetry={retry} />;
  if (state === 'empty') return <EmptyState onAdd={handleAdd} />;
  return <Table data={data} />;
}
```

### Optimistic Updates

For low-risk operations, update UI immediately:

```jsx
// GOOD: Optimistic update with rollback
async function toggleFavorite(id) {
  const previous = favorites;
  setFavorites(prev => [...prev, id]); // Optimistic
  
  try {
    await api.addFavorite(id);
  } catch (error) {
    setFavorites(previous); // Rollback
    showToast('Failed to save favorite');
  }
}
```

Use optimistic updates for: toggles, likes, bookmarks, simple edits
Avoid for: payments, deletions, complex operations

---

## User Flow Patterns

### Linear Flow (Wizard)

Best for: onboarding, checkout, multi-step forms

```
Step 1 → Step 2 → Step 3 → Complete
   ↓         ↓         ↓
 [Save]   [Save]   [Save]   ← Progress preserved
```

Implementation:
```jsx
const steps = ['Account', 'Profile', 'Preferences'];
const [currentStep, setCurrentStep] = useState(0);
const [formData, setFormData] = useState({});

// Persist progress
useEffect(() => {
  localStorage.setItem('onboarding', JSON.stringify({ currentStep, formData }));
}, [currentStep, formData]);

// Enable back without data loss
function goBack() {
  setCurrentStep(prev => Math.max(0, prev - 1));
}
```

### Hub-and-Spoke

Best for: dashboards, admin panels, settings

```
         ┌──────┐
         │ Hub  │
         └──┬───┘
    ┌───────┼───────┐
    ↓       ↓       ↓
 [Spoke] [Spoke] [Spoke]
    ↓       ↓       ↓
    └───────┴───────┘
         Return to Hub
```

### Progressive Disclosure

Reveal complexity as needed:

```jsx
<Card>
  <CardHeader>
    <Title>{item.name}</Title>
    <Button variant="ghost" onClick={() => setExpanded(!expanded)}>
      {expanded ? 'Less' : 'More'}
    </Button>
  </CardHeader>
  
  {expanded && (
    <CardContent>
      <AdvancedSettings />
    </CardContent>
  )}
</Card>
```

---

## Feedback Patterns

### Toast Notifications

```
┌─────────────────────────────────────────────────┐
│ Type       │ Duration │ Dismissable │ Action   │
├────────────┼──────────┼─────────────┼──────────┤
│ Success    │ 3s       │ Yes         │ Optional │
│ Info       │ 5s       │ Yes         │ Optional │
│ Warning    │ 8s       │ Yes         │ Yes      │
│ Error      │ Manual   │ Yes         │ Required │
└─────────────────────────────────────────────────┘
```

Position: Top-right for desktop, bottom-center for mobile

### Inline Feedback

Prefer inline feedback over toasts for form validation:

```jsx
<Input 
  error={touched.email && errors.email}
  success={touched.email && !errors.email && values.email}
  helperText={errors.email || 'Email address is valid'}
/>
```

### Progress Indicators

Choose based on duration:

| Duration | Indicator |
|----------|-----------|
| <1s | None (instant feedback) |
| 1-3s | Button loading state |
| 3-10s | Progress bar |
| >10s | Progress with percentage + cancel option |

---

## Data Interaction Patterns

### Search and Filter

```jsx
function SearchableList() {
  const [search, setSearch] = useState('');
  const [filters, setFilters] = useState({});
  
  const debouncedSearch = useDebounce(search, 300);
  const hasActiveFilters = Object.values(filters).some(Boolean) || search;
  
  return (
    <>
      <SearchInput 
        value={search} 
        onChange={setSearch}
        onClear={() => setSearch('')}
      />
      <FilterBar filters={filters} onChange={setFilters} />
      
      {hasActiveFilters && (
        <Button variant="ghost" onClick={clearAll}>
          Clear all filters
        </Button>
      )}
      
      <ResultCount count={results.length} />
      <List items={results} />
    </>
  );
}
```

### Pagination vs Infinite Scroll

| Use Case | Pattern |
|----------|---------|
| Data tables, admin panels | Pagination with page size selector |
| Social feeds, search results | Infinite scroll with "Load more" |
| Known total count | Pagination |
| Unknown/streaming data | Infinite scroll |

### Bulk Actions

```jsx
<Table>
  <TableHeader>
    <Checkbox 
      checked={allSelected}
      indeterminate={someSelected && !allSelected}
      onChange={toggleAll}
    />
  </TableHeader>
  
  {selectedCount > 0 && (
    <BulkActionBar>
      <span>{selectedCount} selected</span>
      <Button onClick={exportSelected}>Export</Button>
      <Button onClick={deleteSelected} variant="destructive">Delete</Button>
    </BulkActionBar>
  )}
</Table>
```

---

## Navigation Patterns

### Breadcrumb Navigation

Use for hierarchies deeper than 2 levels:

```jsx
<Breadcrumb>
  <BreadcrumbItem href="/">Home</BreadcrumbItem>
  <BreadcrumbItem href="/products">Products</BreadcrumbItem>
  {path.length > 4 && <BreadcrumbItem>...</BreadcrumbItem>}
  <BreadcrumbItem href="/products/electronics">Electronics</BreadcrumbItem>
  <BreadcrumbItem current>Laptop Pro 15"</BreadcrumbItem>
</Breadcrumb>
```

### Tab Navigation

Use for related content at the same hierarchy level:

```jsx
<Tabs value={activeTab} onValueChange={setActiveTab}>
  <TabsList>
    <TabsTrigger value="overview">Overview</TabsTrigger>
    <TabsTrigger value="analytics">Analytics</TabsTrigger>
    <TabsTrigger value="settings">Settings</TabsTrigger>
  </TabsList>
  
  <TabsContent value="overview">...</TabsContent>
  <TabsContent value="analytics">...</TabsContent>
  <TabsContent value="settings">...</TabsContent>
</Tabs>
```

### Command Palette / Spotlight

For power users in complex apps:

```
Keyboard: Cmd/Ctrl + K
Features:
- Recent actions
- Search across app
- Quick navigation
- Commands (new, delete, export)
```

---

## Confirmation Patterns

### Destructive Action Confirmation

```jsx
<AlertDialog>
  <AlertDialogTrigger asChild>
    <Button variant="destructive">Delete Project</Button>
  </AlertDialogTrigger>
  <AlertDialogContent>
    <AlertDialogHeader>
      <AlertDialogTitle>Delete "{project.name}"?</AlertDialogTitle>
      <AlertDialogDescription>
        This will permanently delete the project and all {project.itemCount} items.
        This action cannot be undone.
      </AlertDialogDescription>
    </AlertDialogHeader>
    
    {/* Type-to-confirm for critical operations */}
    <Input 
      placeholder={`Type "${project.name}" to confirm`}
      value={confirmation}
      onChange={e => setConfirmation(e.target.value)}
    />
    
    <AlertDialogFooter>
      <AlertDialogCancel>Cancel</AlertDialogCancel>
      <AlertDialogAction 
        disabled={confirmation !== project.name}
        onClick={handleDelete}
      >
        Delete
      </AlertDialogAction>
    </AlertDialogFooter>
  </AlertDialogContent>
</AlertDialog>
```

### Undo Pattern

Prefer undo over confirmation for reversible actions:

```jsx
function handleDelete(item) {
  markDeleted(item.id);
  
  showToast({
    message: `"${item.name}" deleted`,
    action: {
      label: 'Undo',
      onClick: () => restoreItem(item.id)
    },
    duration: 5000,
    onClose: () => permanentlyDelete(item.id)
  });
}
```
