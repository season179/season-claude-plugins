# Component Library Patterns

## Contents
- React component structure and basic examples
- Common component patterns (Input, Card, Badge, Select, Modal, Checkbox, Alert)
- TypeScript best practices (extending HTML attributes, polymorphic components)
- Accessibility patterns (keyboard navigation, ARIA attributes, focus management)
- Responsive design patterns
- Component organization structure

## React Component Structure

### Basic Button Component Example

```tsx
import React from 'react';

interface ButtonProps {
  variant?: 'solid' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  className?: string;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'solid',
  size = 'md',
  children,
  onClick,
  disabled = false,
  className = '',
}) => {
  const baseStyles = 'rounded-md font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2';
  
  const variantStyles = {
    solid: 'bg-primary-600 hover:bg-primary-700 text-white focus:ring-primary-500',
    outline: 'border-2 border-primary-600 text-primary-600 hover:bg-primary-50 focus:ring-primary-500',
    ghost: 'text-primary-600 hover:bg-primary-50 focus:ring-primary-500',
  };
  
  const sizeStyles = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  };
  
  const disabledStyles = disabled ? 'opacity-50 cursor-not-allowed' : '';
  
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${disabledStyles} ${className}`}
    >
      {children}
    </button>
  );
};

// Usage examples:
// <Button>Click me</Button>
// <Button variant="outline" size="lg">Large outline button</Button>
// <Button variant="ghost" disabled>Disabled ghost button</Button>
```

## Common Component Patterns

### Input Component

```tsx
interface InputProps {
  label?: string;
  error?: string;
  helperText?: string;
  type?: 'text' | 'email' | 'password' | 'number';
  placeholder?: string;
  value?: string;
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
  disabled?: boolean;
  required?: boolean;
  className?: string;
}
```

### Card Component

```tsx
interface CardProps {
  children: React.ReactNode;
  elevation?: 'low' | 'medium' | 'high';
  padding?: 'none' | 'sm' | 'md' | 'lg';
  className?: string;
}
```

### Badge Component

```tsx
interface BadgeProps {
  children: React.ReactNode;
  variant?: 'success' | 'warning' | 'error' | 'info' | 'neutral';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}
```

### Select/Dropdown Component

```tsx
interface SelectProps {
  label?: string;
  options: Array<{ value: string; label: string }>;
  value?: string;
  onChange?: (value: string) => void;
  placeholder?: string;
  error?: string;
  disabled?: boolean;
  className?: string;
}
```

### Modal Component

```tsx
interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  className?: string;
}
```

### Checkbox Component

```tsx
interface CheckboxProps {
  label?: string;
  checked?: boolean;
  onChange?: (checked: boolean) => void;
  disabled?: boolean;
  error?: string;
  className?: string;
}
```

### Alert/Toast Component

```tsx
interface AlertProps {
  variant?: 'success' | 'warning' | 'error' | 'info';
  title?: string;
  message: string;
  dismissible?: boolean;
  onDismiss?: () => void;
  className?: string;
}
```

## TypeScript Best Practices

### Extending HTML Attributes

```tsx
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'solid' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
}

// Allows all standard button props (onClick, type, disabled, etc.)
```

### Using Design Tokens in Components

```tsx
// Import design tokens from a central file
import { colors, spacing, borderRadius, shadows } from './tokens';

// Reference tokens in component styles
const cardStyles = {
  padding: spacing[4],
  borderRadius: borderRadius.lg,
  boxShadow: shadows.md,
  backgroundColor: colors.neutral.white,
};
```

### Polymorphic Components

```tsx
type ButtonAsButton = {
  as?: 'button';
} & React.ButtonHTMLAttributes<HTMLButtonElement>;

type ButtonAsLink = {
  as: 'a';
  href: string;
} & React.AnchorHTMLAttributes<HTMLAnchorElement>;

type ButtonProps = (ButtonAsButton | ButtonAsLink) & {
  variant?: 'solid' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
};

// Allows: <Button>Click</Button> or <Button as="a" href="/path">Link</Button>
```

## Accessibility Patterns

### Keyboard Navigation

```tsx
// Add keyboard support
onKeyDown={(e) => {
  if (e.key === 'Enter' || e.key === ' ') {
    onClick?.();
  }
}}
```

### ARIA Attributes

```tsx
aria-label="Close modal"
aria-disabled={disabled}
aria-expanded={isOpen}
aria-controls="menu-items"
role="button"
tabIndex={0}
```

### Focus Management

```tsx
// Focus visible styles
className="focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"

// Skip to main content
<a href="#main" className="sr-only focus:not-sr-only">Skip to main content</a>
```

## Responsive Design Patterns

```tsx
// Tailwind-style responsive classes
className="text-sm md:text-base lg:text-lg"
className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3"
className="hidden md:block"

// CSS-in-JS approach
const responsiveStyles = {
  '@media (min-width: 768px)': {
    fontSize: '1rem',
  },
  '@media (min-width: 1024px)': {
    fontSize: '1.125rem',
  },
};
```

## Component Organization

```
components/
├── Button/
│   ├── Button.tsx
│   ├── Button.types.ts
│   └── index.ts
├── Input/
│   ├── Input.tsx
│   ├── Input.types.ts
│   └── index.ts
└── Card/
    ├── Card.tsx
    ├── Card.types.ts
    └── index.ts
```
