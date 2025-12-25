---
name: designing-web-app-ux
description: Expert guidance for building web application user interfaces with excellent user experience. Use when designing UI layouts, implementing user flows, creating accessible interfaces, building responsive designs, handling form interactions, designing navigation systems, or implementing feedback patterns. Triggers on requests involving dashboards, admin panels, SaaS interfaces, data-heavy apps, multi-step forms, complex navigation, or any web app requiring thoughtful UX decisions.
---

# Web App UI/UX Design

Build web applications with excellent user experience through proven patterns, accessibility standards, and modern interaction design.

## Core UX Principles

**User-Centered Design**
- Understand user goals before implementation
- Reduce cognitive load—users shouldn't think about how to use the interface
- Provide immediate, clear feedback for every action
- Design for error recovery, not just error prevention

**Information Architecture**
- Group related functionality logically
- Use progressive disclosure—show what's needed, hide complexity
- Maintain consistent patterns throughout the application
- Prioritize scannability over reading

## Reference Files

Read these based on specific needs:

**For user flows, state management, or complex interactions**: See [references/ux-patterns.md](references/ux-patterns.md)
- Use when: implementing wizards, handling loading/error/empty states, designing confirmation flows

**For component implementation details**: See [references/ui-components.md](references/ui-components.md)
- Use when: building forms, tables, navigation, modals, or layout structures

**For accessibility and WCAG compliance**: See [references/accessibility.md](references/accessibility.md)
- Use when: implementing keyboard navigation, screen reader support, or auditing for a11y

**For responsive design and mobile patterns**: See [references/responsive.md](references/responsive.md)
- Use when: adapting layouts for mobile, implementing touch interactions, or choosing breakpoints

## Design Workflow

### Step 1: Define User Context

Before implementing, establish:
```
User Context:
- Primary user goal: [what they want to accomplish]
- Entry point: [how they arrive at this interface]
- Success metric: [how they know they succeeded]
- Error scenarios: [what could go wrong]
```

### Step 2: Choose Interaction Model

Select the appropriate pattern based on task type:

| Task Type | Pattern | Example |
|-----------|---------|---------|
| Data entry | Form with validation | User registration, settings |
| Data viewing | Table/list with filters | Admin panel, dashboard |
| Navigation | Hierarchical/flat nav | App shell, wizard |
| Selection | Checkbox/radio/dropdown | Preferences, filters |
| Creation | Multi-step wizard | Onboarding, checkout |

### Step 3: Apply Feedback Patterns

Every user action needs feedback:

```
Action → Immediate Feedback → State Change → Confirmation

Examples:
- Button click → Loading state → Success/error → Toast notification
- Form submit → Disable + spinner → Redirect → Success message
- Delete action → Confirm modal → Progress → Undo option
```

## Critical Patterns

### Loading States

Never leave users wondering if something is happening:

```jsx
// GOOD: Skeleton loading preserves layout
<div className="space-y-4">
  {isLoading ? (
    <>
      <Skeleton className="h-12 w-full" />
      <Skeleton className="h-12 w-full" />
    </>
  ) : (
    data.map(item => <DataRow key={item.id} {...item} />)
  )}
</div>

// BAD: Spinner with layout shift
{isLoading ? <Spinner /> : <DataList />}
```

### Empty States

Empty states are opportunities, not dead ends:

```jsx
// GOOD: Actionable empty state
<EmptyState
  icon={<DocumentIcon />}
  title="No documents yet"
  description="Create your first document to get started"
  action={<Button onClick={createDoc}>Create Document</Button>}
/>

// BAD: Just text
<p>No documents found.</p>
```

### Error Handling

Errors should guide recovery:

```jsx
// GOOD: Specific, actionable error
<Alert variant="error">
  <AlertTitle>Unable to save changes</AlertTitle>
  <AlertDescription>
    Your session expired. <Button variant="link" onClick={reauth}>Sign in again</Button> to continue.
  </AlertDescription>
</Alert>

// BAD: Generic error
<Alert>Something went wrong. Please try again.</Alert>
```

### Form Design

Forms are the most critical UX element in web apps:

```jsx
// GOOD: Inline validation with clear feedback
<FormField>
  <Label htmlFor="email">Email address</Label>
  <Input
    id="email"
    type="email"
    aria-describedby="email-error"
    aria-invalid={errors.email ? "true" : "false"}
  />
  {errors.email && (
    <FormError id="email-error">{errors.email}</FormError>
  )}
</FormField>

// Validation timing:
// - Validate on blur for long fields
// - Validate on change after first error
// - Validate all on submit
```

## Component Guidelines

### Buttons

```
Primary button: One per view, main action
Secondary button: Supporting actions
Destructive button: Irreversible actions (always confirm)
Ghost/link button: Tertiary actions

Button states: default → hover → active → disabled → loading
Always disable during async operations to prevent double-submit
```

### Tables

```
Required: Sortable columns, pagination or virtual scroll for >50 rows
Recommended: Column resize, row selection, bulk actions
Optional: Column reorder, row expansion, inline edit

Mobile: Transform to cards or use horizontal scroll with frozen first column
```

### Navigation

```
Top nav: Global navigation, user menu, search
Side nav: Feature/section navigation, collapsible for space
Breadcrumbs: Deep hierarchies (>2 levels)
Tabs: Related content at same hierarchy level
```

### Modals and Dialogs

```
Use modals for:
- Confirmations requiring user decision
- Forms that don't need full page
- Quick actions without context switch

Don't use modals for:
- Complex multi-step processes (use pages)
- Content that needs comparison with background
- Frequent operations (use inline editing)

Always: Focus trap, ESC to close, click-outside to close
```

## Responsive Breakpoints

Standard breakpoints (Tailwind convention):
```css
sm: 640px   /* Large phones */
md: 768px   /* Tablets */
lg: 1024px  /* Laptops */
xl: 1280px  /* Desktops */
2xl: 1536px /* Large screens */
```

Mobile-first implementation:
```jsx
// Base: Mobile styles
// sm: Enhance for larger
<div className="
  flex flex-col gap-4          /* Mobile: stack */
  sm:flex-row sm:gap-6         /* Tablet+: horizontal */
  lg:gap-8                     /* Desktop: more space */
">
```

## Accessibility Essentials

**Keyboard Navigation**
- All interactive elements focusable with Tab
- Focus order matches visual order
- Focus visible (never `outline: none` without replacement)
- ESC closes modals/dropdowns

**Screen Readers**
- Images have alt text (or `alt=""` for decorative)
- Forms have associated labels
- Error messages announced via `aria-live`
- Dynamic content uses appropriate ARIA roles

**Visual**
- 4.5:1 contrast for normal text, 3:1 for large text
- Color not sole indicator of state
- Animations respect `prefers-reduced-motion`

## Performance Considerations

**Perceived Performance**
- Show skeleton screens, not spinners
- Optimistic UI updates for low-risk operations
- Progressive loading for data-heavy views

**Actual Performance**
- Lazy load below-fold content and routes
- Virtual scroll for lists >100 items
- Debounce search inputs (300ms typical)
- Cache API responses when appropriate

## Anti-Patterns to Avoid

- **Layout shift** — Reserve space for async content
- **Mystery meat navigation** — Icons need labels or tooltips
- **Disabled without explanation** — Explain why actions are unavailable
- **Infinite nesting** — Max 3 levels for any hierarchy
- **Modal inception** — Never open a modal from a modal
- **Form without feedback** — Always show validation state
- **Hidden scroll** — Make scrollable areas obvious
- **Unexpected navigation** — Warn before leaving with unsaved changes

## Framework-Specific Notes

**React**
- Use controlled components for forms
- Implement error boundaries for graceful degradation
- Consider React Query/SWR for server state

**Vue**
- Use v-model with validation libraries
- Leverage computed properties for derived UI state
- Consider Pinia for complex state

**Vanilla/HTML**
- Progressive enhancement: works without JS
- Use `<dialog>` for native modal behavior
- Leverage CSS `:has()` for parent selectors
