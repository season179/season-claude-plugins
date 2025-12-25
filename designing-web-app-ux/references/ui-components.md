# UI Components Reference

## Contents
- Form Components
- Data Display Components
- Navigation Components
- Overlay Components
- Layout Components

---

## Form Components

### Input Fields

```jsx
<FormField>
  <Label htmlFor="username" required>Username</Label>
  <Input
    id="username"
    type="text"
    placeholder="Enter username"
    aria-describedby="username-hint username-error"
    aria-invalid={!!error}
    disabled={isSubmitting}
  />
  <FormHint id="username-hint">3-20 characters, letters and numbers only</FormHint>
  {error && <FormError id="username-error">{error}</FormError>}
</FormField>
```

**Input States:**
```
Default → Focus → Filled → Error → Disabled
          ↓
        Typing → Blur → Validation
```

**Input Types by Data:**
| Data Type | Input Type | Extras |
|-----------|------------|--------|
| Email | `type="email"` | Email keyboard on mobile |
| Phone | `type="tel"` | Numeric keyboard |
| Number | `type="number"` | Step, min, max attributes |
| Password | `type="password"` | Show/hide toggle |
| Date | `type="date"` or date picker | Browser native or custom |
| Currency | `type="text"` | Format mask, numeric keyboard |

### Select / Dropdown

```jsx
<Select>
  <SelectTrigger aria-label="Select country">
    <SelectValue placeholder="Select a country" />
  </SelectTrigger>
  <SelectContent>
    {countries.length > 10 && (
      <SelectSearch placeholder="Search countries..." />
    )}
    <SelectGroup>
      <SelectLabel>Popular</SelectLabel>
      {popularCountries.map(c => (
        <SelectItem key={c.code} value={c.code}>{c.name}</SelectItem>
      ))}
    </SelectGroup>
    <SelectSeparator />
    <SelectGroup>
      <SelectLabel>All Countries</SelectLabel>
      {allCountries.map(c => (
        <SelectItem key={c.code} value={c.code}>{c.name}</SelectItem>
      ))}
    </SelectGroup>
  </SelectContent>
</Select>
```

**When to use which:**
| Scenario | Component |
|----------|-----------|
| ≤5 options | Radio buttons |
| 6-15 options | Select dropdown |
| >15 options | Searchable select |
| Multiple selection | Checkbox group or multi-select |

### Checkbox and Radio

```jsx
// Checkbox group with indeterminate parent
<CheckboxGroup>
  <Checkbox
    checked={allSelected}
    indeterminate={someSelected}
    onCheckedChange={toggleAll}
  >
    Select All
  </Checkbox>
  
  {options.map(opt => (
    <Checkbox
      key={opt.id}
      checked={selected.includes(opt.id)}
      onCheckedChange={() => toggle(opt.id)}
    >
      {opt.label}
    </Checkbox>
  ))}
</CheckboxGroup>

// Radio group - single selection
<RadioGroup value={size} onValueChange={setSize}>
  <RadioGroupItem value="sm" id="sm">Small</RadioGroupItem>
  <RadioGroupItem value="md" id="md">Medium</RadioGroupItem>
  <RadioGroupItem value="lg" id="lg">Large</RadioGroupItem>
</RadioGroup>
```

### Buttons

**Button Hierarchy:**
```
Primary    │ Main action, one per view
Secondary  │ Supporting actions
Outline    │ Alternative secondary
Ghost      │ Tertiary, in toolbars
Link       │ Navigation, inline actions
Destructive│ Delete, remove (with confirmation)
```

**Button with Loading State:**
```jsx
<Button disabled={isLoading} onClick={handleSubmit}>
  {isLoading ? (
    <>
      <Spinner className="mr-2 h-4 w-4" />
      Saving...
    </>
  ) : (
    'Save Changes'
  )}
</Button>
```

---

## Data Display Components

### Tables

```jsx
<Table>
  <TableHeader>
    <TableRow>
      <TableHead>
        <Checkbox checked={allSelected} onChange={selectAll} />
      </TableHead>
      <TableHead sortable sorted={sortBy === 'name'} onClick={() => sort('name')}>
        Name
      </TableHead>
      <TableHead sortable sorted={sortBy === 'date'} onClick={() => sort('date')}>
        Date
      </TableHead>
      <TableHead>Actions</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    {data.map(row => (
      <TableRow key={row.id} selected={selected.includes(row.id)}>
        <TableCell>
          <Checkbox 
            checked={selected.includes(row.id)} 
            onChange={() => toggleSelect(row.id)} 
          />
        </TableCell>
        <TableCell>{row.name}</TableCell>
        <TableCell>{formatDate(row.date)}</TableCell>
        <TableCell>
          <DropdownMenu>
            <DropdownMenuTrigger>
              <Button variant="ghost" size="sm">•••</Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent>
              <DropdownMenuItem onClick={() => edit(row)}>Edit</DropdownMenuItem>
              <DropdownMenuItem onClick={() => duplicate(row)}>Duplicate</DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem variant="destructive" onClick={() => remove(row)}>
                Delete
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </TableCell>
      </TableRow>
    ))}
  </TableBody>
</Table>

<TablePagination
  total={total}
  page={page}
  pageSize={pageSize}
  onPageChange={setPage}
  onPageSizeChange={setPageSize}
/>
```

### Cards

```jsx
<Card>
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
    <CardDescription>Supporting description</CardDescription>
    <CardAction>
      <Button variant="ghost" size="icon">
        <MoreVertical className="h-4 w-4" />
      </Button>
    </CardAction>
  </CardHeader>
  <CardContent>
    {/* Main content */}
  </CardContent>
  <CardFooter>
    <Button variant="outline">Cancel</Button>
    <Button>Save</Button>
  </CardFooter>
</Card>
```

### Badges and Tags

```jsx
// Status badges
<Badge variant="success">Active</Badge>
<Badge variant="warning">Pending</Badge>
<Badge variant="error">Failed</Badge>
<Badge variant="default">Draft</Badge>

// Removable tags
<div className="flex flex-wrap gap-2">
  {tags.map(tag => (
    <Badge key={tag} variant="secondary">
      {tag}
      <button onClick={() => removeTag(tag)} aria-label={`Remove ${tag}`}>
        <X className="h-3 w-3 ml-1" />
      </button>
    </Badge>
  ))}
</div>
```

---

## Navigation Components

### Sidebar Navigation

```jsx
<Sidebar collapsed={collapsed}>
  <SidebarHeader>
    <Logo />
    <Button variant="ghost" onClick={toggleCollapse}>
      <ChevronLeft className={cn(collapsed && 'rotate-180')} />
    </Button>
  </SidebarHeader>
  
  <SidebarContent>
    <SidebarGroup>
      <SidebarGroupLabel>Main</SidebarGroupLabel>
      <SidebarMenu>
        <SidebarMenuItem>
          <SidebarMenuButton href="/dashboard" active={path === '/dashboard'}>
            <Home className="h-4 w-4" />
            {!collapsed && <span>Dashboard</span>}
          </SidebarMenuButton>
        </SidebarMenuItem>
        
        {/* Nested navigation */}
        <SidebarMenuItem>
          <Collapsible open={projectsOpen} onOpenChange={setProjectsOpen}>
            <CollapsibleTrigger asChild>
              <SidebarMenuButton>
                <Folder className="h-4 w-4" />
                {!collapsed && (
                  <>
                    <span>Projects</span>
                    <ChevronDown className={cn(projectsOpen && 'rotate-180')} />
                  </>
                )}
              </SidebarMenuButton>
            </CollapsibleTrigger>
            <CollapsibleContent>
              <SidebarMenuSub>
                {projects.map(p => (
                  <SidebarMenuSubItem key={p.id} href={`/projects/${p.id}`}>
                    {p.name}
                  </SidebarMenuSubItem>
                ))}
              </SidebarMenuSub>
            </CollapsibleContent>
          </Collapsible>
        </SidebarMenuItem>
      </SidebarMenu>
    </SidebarGroup>
  </SidebarContent>
  
  <SidebarFooter>
    <UserMenu user={user} collapsed={collapsed} />
  </SidebarFooter>
</Sidebar>
```

### Header Navigation

```jsx
<Header>
  <HeaderLogo href="/">
    <Logo />
  </HeaderLogo>
  
  {/* Desktop nav */}
  <HeaderNav className="hidden md:flex">
    <HeaderNavItem href="/features">Features</HeaderNavItem>
    <HeaderNavItem href="/pricing">Pricing</HeaderNavItem>
    <HeaderNavItem href="/docs">Docs</HeaderNavItem>
  </HeaderNav>
  
  <HeaderActions>
    <Button variant="ghost" className="hidden md:inline-flex">Sign In</Button>
    <Button className="hidden md:inline-flex">Get Started</Button>
    
    {/* Mobile menu trigger */}
    <Sheet>
      <SheetTrigger asChild className="md:hidden">
        <Button variant="ghost" size="icon">
          <Menu className="h-5 w-5" />
        </Button>
      </SheetTrigger>
      <SheetContent side="right">
        <MobileMenu />
      </SheetContent>
    </Sheet>
  </HeaderActions>
</Header>
```

---

## Overlay Components

### Modal / Dialog

```jsx
<Dialog open={open} onOpenChange={setOpen}>
  <DialogTrigger asChild>
    <Button>Open Dialog</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Edit Profile</DialogTitle>
      <DialogDescription>
        Make changes to your profile here. Click save when done.
      </DialogDescription>
    </DialogHeader>
    
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
      
      <DialogFooter>
        <DialogClose asChild>
          <Button variant="outline">Cancel</Button>
        </DialogClose>
        <Button type="submit">Save Changes</Button>
      </DialogFooter>
    </form>
  </DialogContent>
</Dialog>
```

**Modal Sizes:**
```
sm: 400px  - Confirmations, simple forms
md: 500px  - Standard forms
lg: 600px  - Complex forms
xl: 800px  - Data-heavy content
full: 100% - Immersive views (use sparingly)
```

### Dropdown Menu

```jsx
<DropdownMenu>
  <DropdownMenuTrigger asChild>
    <Button variant="outline">
      Options <ChevronDown className="ml-2 h-4 w-4" />
    </Button>
  </DropdownMenuTrigger>
  <DropdownMenuContent align="end">
    <DropdownMenuLabel>Actions</DropdownMenuLabel>
    <DropdownMenuItem>
      <Edit className="mr-2 h-4 w-4" />
      Edit
    </DropdownMenuItem>
    <DropdownMenuItem>
      <Copy className="mr-2 h-4 w-4" />
      Duplicate
    </DropdownMenuItem>
    <DropdownMenuSeparator />
    <DropdownMenuItem variant="destructive">
      <Trash className="mr-2 h-4 w-4" />
      Delete
    </DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>
```

### Tooltip

```jsx
<Tooltip>
  <TooltipTrigger asChild>
    <Button variant="ghost" size="icon" aria-label="Settings">
      <Settings className="h-4 w-4" />
    </Button>
  </TooltipTrigger>
  <TooltipContent>
    <p>Settings</p>
  </TooltipContent>
</Tooltip>
```

---

## Layout Components

### Container

```jsx
<div className="container mx-auto px-4 sm:px-6 lg:px-8">
  {/* Content */}
</div>
```

### Grid Layouts

```jsx
// Responsive grid
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
  {items.map(item => <Card key={item.id}>{item}</Card>)}
</div>

// Dashboard layout
<div className="grid grid-cols-12 gap-4">
  <div className="col-span-12 lg:col-span-8">
    <MainContent />
  </div>
  <div className="col-span-12 lg:col-span-4">
    <Sidebar />
  </div>
</div>
```

### Page Layout Patterns

```jsx
// Standard app layout
<div className="flex h-screen">
  <aside className="w-64 border-r hidden lg:block">
    <Sidebar />
  </aside>
  
  <div className="flex-1 flex flex-col overflow-hidden">
    <header className="h-16 border-b flex items-center px-4">
      <Header />
    </header>
    
    <main className="flex-1 overflow-auto p-4 lg:p-6">
      <Outlet />
    </main>
  </div>
</div>
```
