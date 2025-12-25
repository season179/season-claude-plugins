# Accessibility Reference

## Contents
- WCAG Quick Reference
- Keyboard Navigation
- Screen Reader Support
- Visual Accessibility
- ARIA Patterns
- Testing Checklist

---

## WCAG Quick Reference

### Levels at a Glance

| Level | Requirement | Impact |
|-------|-------------|--------|
| A | Minimum accessibility | Legal baseline |
| AA | Standard accessibility | **Target for most apps** |
| AAA | Enhanced accessibility | Specialized use cases |

### Critical WCAG 2.1 AA Requirements

**Perceivable**
- 1.1.1: Non-text content has text alternatives
- 1.4.3: Contrast ratio ≥4.5:1 (normal text), ≥3:1 (large text)
- 1.4.4: Text resizable to 200% without loss of content

**Operable**
- 2.1.1: All functionality via keyboard
- 2.4.3: Focus order matches visual flow
- 2.4.7: Focus indicator visible

**Understandable**
- 3.1.1: Page language defined
- 3.3.1: Errors identified and described
- 3.3.2: Labels or instructions for inputs

**Robust**
- 4.1.2: Name, role, value for custom components

---

## Keyboard Navigation

### Focus Management

```css
/* Visible focus states */
.focus-visible:outline-2
.focus-visible:outline-offset-2
.focus-visible:outline-primary

/* Never do this */
button { outline: none; } /* BAD */

/* Custom focus ring */
button:focus-visible {
  outline: 2px solid var(--focus-color);
  outline-offset: 2px;
}
```

### Tab Order

```jsx
// Natural tab order follows DOM
<form>
  <input type="text" />     {/* Tab 1 */}
  <input type="email" />    {/* Tab 2 */}
  <button type="submit" />  {/* Tab 3 */}
</form>

// Override only when necessary
<div tabIndex={0}>Focusable div</div>
<div tabIndex={-1}>Programmatically focusable only</div>

// Skip to main content
<a href="#main" className="sr-only focus:not-sr-only">
  Skip to main content
</a>
```

### Focus Trapping

Required for modals and dropdowns:

```jsx
function Modal({ children, open, onClose }) {
  const modalRef = useFocusTrap(open);
  
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') onClose();
    };
    if (open) document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [open, onClose]);
  
  return open ? (
    <div ref={modalRef} role="dialog" aria-modal="true">
      {children}
    </div>
  ) : null;
}
```

### Common Keyboard Patterns

| Component | Keys |
|-----------|------|
| Button | Enter, Space |
| Link | Enter |
| Checkbox | Space |
| Radio | Arrow keys |
| Select/Dropdown | Arrow keys, Enter, Escape |
| Modal | Escape to close |
| Tab list | Arrow keys, Home, End |
| Menu | Arrow keys, Enter, Escape |

---

## Screen Reader Support

### Semantic HTML

Always use semantic HTML before ARIA:

```jsx
// GOOD: Semantic HTML
<button onClick={handleClick}>Save</button>
<nav aria-label="Main">...</nav>
<main>...</main>

// BAD: div soup with ARIA
<div role="button" tabIndex={0} onClick={handleClick}>Save</div>
```

### Landmarks

```jsx
<header role="banner">
  <nav role="navigation" aria-label="Main">...</nav>
</header>

<main role="main">
  <section aria-labelledby="section-title">
    <h2 id="section-title">Section Title</h2>
  </section>
</main>

<aside role="complementary">...</aside>
<footer role="contentinfo">...</footer>
```

### Announcing Dynamic Content

```jsx
// Live regions for dynamic updates
<div aria-live="polite" aria-atomic="true">
  {message}
</div>

// Assertive for errors
<div role="alert" aria-live="assertive">
  {errorMessage}
</div>

// Status messages
<div role="status" aria-live="polite">
  Saving... / Saved successfully
</div>
```

### Form Accessibility

```jsx
<div className="form-field">
  <label htmlFor="email">
    Email address
    <span aria-hidden="true">*</span>
    <span className="sr-only">(required)</span>
  </label>
  
  <input
    id="email"
    type="email"
    required
    aria-required="true"
    aria-invalid={!!error}
    aria-describedby={`${error ? 'email-error' : ''} email-hint`.trim()}
  />
  
  <p id="email-hint" className="text-muted">
    We'll never share your email.
  </p>
  
  {error && (
    <p id="email-error" role="alert" className="text-error">
      {error}
    </p>
  )}
</div>
```

---

## Visual Accessibility

### Color Contrast

Minimum contrast ratios (WCAG AA):
```
Normal text (<18px or <14px bold): 4.5:1
Large text (≥18px or ≥14px bold): 3:1
UI components and graphics: 3:1
```

### Color Independence

Never use color alone to convey information:

```jsx
// BAD: Color only
<span className={status === 'error' ? 'text-red' : 'text-green'}>
  {status}
</span>

// GOOD: Color + icon + text
<span className={statusStyles[status]}>
  <StatusIcon status={status} aria-hidden="true" />
  <span>{statusLabels[status]}</span>
</span>
```

### Motion and Animation

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## ARIA Patterns

### Toggle Button

```jsx
<button aria-pressed={isPressed} onClick={toggle}>
  {isPressed ? 'On' : 'Off'}
</button>
```

### Tabs

```jsx
<div role="tablist" aria-label="Account settings">
  <button
    role="tab"
    aria-selected={activeTab === 'profile'}
    aria-controls="panel-profile"
    id="tab-profile"
    tabIndex={activeTab === 'profile' ? 0 : -1}
  >
    Profile
  </button>
</div>

<div
  role="tabpanel"
  id="panel-profile"
  aria-labelledby="tab-profile"
  hidden={activeTab !== 'profile'}
>
  Profile content...
</div>
```

### Disclosure (Accordion)

```jsx
<button
  aria-expanded={isOpen}
  aria-controls="section-content"
  onClick={() => setIsOpen(!isOpen)}
>
  Section Title
</button>

<div id="section-content" hidden={!isOpen}>
  Section content...
</div>
```

---

## Testing Checklist

### Automated Testing

```
Tools:
- axe DevTools (browser extension)
- Lighthouse accessibility audit
- eslint-plugin-jsx-a11y (React)
- Pa11y (CLI)
```

### Manual Testing Checklist

**Keyboard**
- [ ] All interactive elements reachable with Tab
- [ ] Buttons activate with Enter and Space
- [ ] Modals/dropdowns close with Escape
- [ ] Focus visible on all elements
- [ ] No keyboard traps

**Screen Reader** (NVDA, VoiceOver, JAWS)
- [ ] Page title announced on load
- [ ] Headings create logical outline
- [ ] Images have meaningful alt text
- [ ] Forms have associated labels
- [ ] Errors announced when they appear

**Visual**
- [ ] Content readable at 200% zoom
- [ ] No horizontal scroll at 320px width
- [ ] Contrast ratios meet AA standards
- [ ] Color not sole indicator of state
- [ ] Focus indicator visible

### Quick Audit Commands

```javascript
// Check for missing alt text
document.querySelectorAll('img:not([alt])');

// Check for missing form labels
document.querySelectorAll('input:not([aria-label]):not([aria-labelledby])');

// Check for missing button text
document.querySelectorAll('button:empty:not([aria-label])');
```
