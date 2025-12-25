# Responsive Design Reference

## Contents
- Breakpoint Strategy
- Mobile-First Patterns
- Component Adaptations
- Touch Interactions
- Common Layouts

---

## Breakpoint Strategy

### Standard Breakpoints

```css
/* Tailwind defaults */
sm: 640px   /* Large phones, landscape */
md: 768px   /* Tablets */
lg: 1024px  /* Laptops, small desktops */
xl: 1280px  /* Desktops */
2xl: 1536px /* Large screens */

@media (min-width: 640px) { /* sm */ }
@media (min-width: 768px) { /* md */ }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }
```

### Content-Based Breakpoints

Prefer content-based over device-based:

```css
.card-grid {
  grid-template-columns: 1fr;
}

@media (min-width: 500px) {
  .card-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
```

### Container Queries (Modern)

```css
.card-container {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .card {
    display: flex;
    flex-direction: row;
  }
}
```

---

## Mobile-First Patterns

### CSS Mobile-First

```css
/* Base: mobile styles */
.component {
  display: flex;
  flex-direction: column;
  padding: 1rem;
}

/* Enhance for larger screens */
@media (min-width: 768px) {
  .component {
    flex-direction: row;
    padding: 2rem;
  }
}
```

### Tailwind Mobile-First

```jsx
<div className="
  flex flex-col gap-4          // Mobile: stacked
  sm:flex-row sm:gap-6         // sm+: horizontal
  md:gap-8                     // md+: more gap
  lg:max-w-4xl lg:mx-auto      // lg+: constrained
">
```

---

## Component Adaptations

### Navigation

```jsx
<header className="flex items-center justify-between p-4">
  <Logo />
  
  {/* Desktop nav */}
  <nav className="hidden md:flex items-center gap-6">
    <NavLink href="/features">Features</NavLink>
    <NavLink href="/pricing">Pricing</NavLink>
  </nav>
  
  {/* Mobile menu trigger */}
  <Sheet>
    <SheetTrigger asChild className="md:hidden">
      <Button variant="ghost" size="icon">
        <Menu className="h-6 w-6" />
      </Button>
    </SheetTrigger>
    <SheetContent side="left">
      <nav className="flex flex-col gap-4 mt-8">
        <NavLink href="/features">Features</NavLink>
        <NavLink href="/pricing">Pricing</NavLink>
      </nav>
    </SheetContent>
  </Sheet>
</header>
```

### Tables

```jsx
// Option 1: Horizontal scroll
<div className="overflow-x-auto">
  <table className="min-w-[600px]">...</table>
</div>

// Option 2: Transform to cards on mobile
<div className="hidden md:block">
  <Table data={data} columns={columns} />
</div>

<div className="md:hidden space-y-4">
  {data.map(row => (
    <Card key={row.id}>
      <dl className="divide-y">
        {columns.map(col => (
          <div key={col.key} className="flex justify-between py-2">
            <dt className="font-medium text-muted-foreground">{col.header}</dt>
            <dd>{row[col.key]}</dd>
          </div>
        ))}
      </dl>
    </Card>
  ))}
</div>
```

### Modals

```jsx
// Full-screen on mobile, centered modal on desktop
<DialogContent className="
  fixed inset-0 w-full h-full
  sm:inset-auto sm:w-[500px] sm:h-auto sm:rounded-lg
  sm:top-1/2 sm:left-1/2 sm:-translate-x-1/2 sm:-translate-y-1/2
">
```

### Forms

```jsx
// Stack labels on mobile, inline on desktop
<FormField className="
  flex flex-col gap-2
  sm:flex-row sm:items-center
">
  <Label className="sm:w-32">Email</Label>
  <Input className="flex-1" type="email" />
</FormField>

// Full-width buttons on mobile
<div className="flex flex-col sm:flex-row gap-2">
  <Button className="w-full sm:w-auto">Submit</Button>
  <Button variant="outline" className="w-full sm:w-auto">Cancel</Button>
</div>
```

### Cards/Grids

```jsx
<div className="
  grid gap-4
  grid-cols-1
  sm:grid-cols-2
  lg:grid-cols-3
  xl:grid-cols-4
">
  {items.map(item => <Card key={item.id} {...item} />)}
</div>
```

---

## Touch Interactions

### Touch Targets

Minimum touch target: 44x44px (WCAG), 48x48px (recommended)

```jsx
<Button className="min-h-[44px] min-w-[44px] p-3">
  <Icon />
</Button>

// Expand touch area beyond visual bounds
<a href="/link" className="relative inline-block p-2 -m-2">
  Link text
</a>
```

### Swipe Gestures

```jsx
import { useSwipeable } from 'react-swipeable';

function SwipeableCard({ onDelete, children }) {
  const [offset, setOffset] = useState(0);
  
  const handlers = useSwipeable({
    onSwiping: (e) => setOffset(e.deltaX),
    onSwipedLeft: () => onDelete(),
    onSwiped: () => setOffset(0),
  });
  
  return (
    <div {...handlers} className="relative overflow-hidden">
      <div style={{ transform: `translateX(${offset}px)` }}>
        {children}
      </div>
      <div className="absolute right-0 inset-y-0 bg-red-500 flex items-center px-4">
        Delete
      </div>
    </div>
  );
}
```

---

## Common Layouts

### App Shell (Dashboard)

```jsx
<div className="h-screen flex flex-col">
  {/* Mobile header */}
  <header className="lg:hidden h-14 border-b flex items-center px-4">
    <MobileMenuTrigger />
    <Logo />
    <UserMenu />
  </header>
  
  <div className="flex-1 flex overflow-hidden">
    {/* Sidebar */}
    <aside className="hidden lg:flex lg:w-64 lg:flex-col lg:border-r">
      <Sidebar />
    </aside>
    
    {/* Main content */}
    <main className="flex-1 overflow-auto p-4 lg:p-6">
      <Outlet />
    </main>
  </div>
</div>
```

### Marketing Page

```jsx
<div className="min-h-screen">
  <header className="sticky top-0 z-50 bg-background/95 backdrop-blur">
    <div className="container flex h-14 items-center">
      <ResponsiveNav />
    </div>
  </header>
  
  <section className="py-12 md:py-24 lg:py-32">
    <div className="container text-center">
      <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold">
        Hero Title
      </h1>
    </div>
  </section>
  
  <section className="py-12 bg-muted">
    <div className="container">
      <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
        {features.map(f => <FeatureCard key={f.id} {...f} />)}
      </div>
    </div>
  </section>
</div>
```

### Split View

```jsx
<div className="h-screen flex flex-col lg:flex-row">
  {/* List panel */}
  <div className={cn(
    "lg:w-80 lg:border-r flex-shrink-0",
    selectedItem ? "hidden lg:block" : "flex-1 lg:flex-none"
  )}>
    <ItemList items={items} selected={selectedItem} onSelect={setSelectedItem} />
  </div>
  
  {/* Detail panel */}
  <div className={cn(
    "flex-1",
    selectedItem ? "block" : "hidden lg:block"
  )}>
    {selectedItem ? (
      <ItemDetail item={selectedItem} onBack={() => setSelectedItem(null)} />
    ) : (
      <EmptyState>Select an item</EmptyState>
    )}
  </div>
</div>
```

---

## Performance Tips

### Responsive Images

```jsx
<img
  src="/image-400.jpg"
  srcSet="
    /image-400.jpg 400w,
    /image-800.jpg 800w,
    /image-1200.jpg 1200w
  "
  sizes="
    (max-width: 640px) 100vw,
    (max-width: 1024px) 50vw,
    33vw
  "
  alt="Description"
  loading="lazy"
/>
```

### Conditional Loading

```jsx
const HeavyChart = dynamic(() => import('./HeavyChart'), {
  loading: () => <ChartSkeleton />,
  ssr: false,
});

function Dashboard() {
  const isMobile = useMediaQuery('(max-width: 768px)');
  
  return (
    <div>
      {isMobile ? <SimpleStats /> : <HeavyChart />}
    </div>
  );
}
```
