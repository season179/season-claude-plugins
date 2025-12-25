
================================================================================
// Button.tsx
================================================================================
import React from 'react';

interface ButtonProps {{
  variant?: 'solid' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  className?: string;
}}

export const Button: React.FC<ButtonProps> = ({{
  variant = 'solid',
  size = 'md',
  children,
  onClick,
  disabled = false,
  className = '',
}}) => {{
  const baseStyles = 'rounded-md font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2';
  
  const variantStyles = {{
    solid: 'bg-primary-600 hover:bg-primary-700 text-white focus:ring-primary-500',
    outline: 'border-2 border-primary-600 text-primary-600 hover:bg-primary-50 focus:ring-primary-500 bg-white',
    ghost: 'text-primary-600 hover:bg-primary-50 focus:ring-primary-500',
  }};
  
  const sizeStyles = {{
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  }};
  
  const disabledStyles = disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer';
  
  return (
    <button
      onClick={{onClick}}
      disabled={{disabled}}
      className={{`${{baseStyles}} ${{variantStyles[variant]}} ${{sizeStyles[size]}} ${{disabledStyles}} ${{className}}`}}
      aria-disabled={{disabled}}
    >
      {{children}}
    </button>
  );
}};

// Usage examples:
// <Button>Click me</Button>
// <Button variant="outline" size="lg">Large outline button</Button>
// <Button variant="ghost" disabled>Disabled ghost button</Button>


================================================================================
// Input.tsx
================================================================================
import React from 'react';

interface InputProps {{
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
}}

export const Input: React.FC<InputProps> = ({{
  label,
  error,
  helperText,
  type = 'text',
  placeholder,
  value,
  onChange,
  disabled = false,
  required = false,
  className = '',
}}) => {{
  const baseStyles = 'w-full px-3 py-2 border rounded-md text-base transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500';
  const errorStyles = error ? 'border-error bg-error/5' : 'border-neutral-300 focus:border-primary-500';
  const disabledStyles = disabled ? 'opacity-50 cursor-not-allowed bg-neutral-100' : 'bg-white';
  
  return (
    <div className={{`space-y-1 ${{className}}`}}>
      {{label && (
        <label className="block text-sm font-medium text-neutral-700">
          {{label}}
          {{required && <span className="text-error ml-1">*</span>}}
        </label>
      )}}
      <input
        type={{type}}
        value={{value}}
        onChange={{onChange}}
        placeholder={{placeholder}}
        disabled={{disabled}}
        required={{required}}
        className={{`${{baseStyles}} ${{errorStyles}} ${{disabledStyles}}`}}
        aria-invalid={{!!error}}
        aria-describedby={{error ? 'input-error' : helperText ? 'input-helper' : undefined}}
      />
      {{error && (
        <p id="input-error" className="text-sm text-error">
          {{error}}
        </p>
      )}}
      {{helperText && !error && (
        <p id="input-helper" className="text-sm text-neutral-600">
          {{helperText}}
        </p>
      )}}
    </div>
  );
}};

// Usage examples:
// <Input label="Email" type="email" placeholder="you@example.com" />
// <Input label="Password" type="password" error="Password is required" required />


================================================================================
// Card.tsx
================================================================================
import React from 'react';

interface CardProps {{
  children: React.ReactNode;
  elevation?: 'low' | 'medium' | 'high';
  padding?: 'none' | 'sm' | 'md' | 'lg';
  className?: string;
}}

export const Card: React.FC<CardProps> = ({{
  children,
  elevation = 'medium',
  padding = 'md',
  className = '',
}}) => {{
  const baseStyles = 'rounded-lg bg-white border border-neutral-200';
  
  const elevationStyles = {{
    low: 'shadow-sm',
    medium: 'shadow-md',
    high: 'shadow-lg',
  }};
  
  const paddingStyles = {{
    none: 'p-0',
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
  }};
  
  return (
    <div className={{`${{baseStyles}} ${{elevationStyles[elevation]}} ${{paddingStyles[padding]}} ${{className}}`}}>
      {{children}}
    </div>
  );
}};

// Usage examples:
// <Card elevation="high" padding="lg">
//   <h3>Card Title</h3>
//   <p>Card content goes here</p>
// </Card>


================================================================================
// Badge.tsx
================================================================================
import React from 'react';

interface BadgeProps {{
  children: React.ReactNode;
  variant?: 'success' | 'warning' | 'error' | 'info' | 'neutral';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}}

export const Badge: React.FC<BadgeProps> = ({{
  children,
  variant = 'neutral',
  size = 'md',
  className = '',
}}) => {{
  const baseStyles = 'inline-flex items-center font-medium rounded-full';
  
  const variantStyles = {{
    success: 'bg-success/10 text-success',
    warning: 'bg-warning/10 text-warning',
    error: 'bg-error/10 text-error',
    info: 'bg-info/10 text-info',
    neutral: 'bg-neutral-100 text-neutral-700',
  }};
  
  const sizeStyles = {{
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-2.5 py-1 text-sm',
    lg: 'px-3 py-1.5 text-base',
  }};
  
  return (
    <span className={{`${{baseStyles}} ${{variantStyles[variant]}} ${{sizeStyles[size]}} ${{className}}`}}>
      {{children}}
    </span>
  );
}};

// Usage examples:
// <Badge variant="success">Active</Badge>
// <Badge variant="error" size="lg">Critical</Badge>


================================================================================
// Checkbox.tsx
================================================================================
import React from 'react';

interface CheckboxProps {{
  label?: string;
  checked?: boolean;
  onChange?: (checked: boolean) => void;
  disabled?: boolean;
  error?: string;
  className?: string;
}}

export const Checkbox: React.FC<CheckboxProps> = ({{
  label,
  checked = false,
  onChange,
  disabled = false,
  error,
  className = '',
}}) => {{
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {{
    onChange?.(e.target.checked);
  }};
  
  return (
    <div className={{`space-y-1 ${{className}}`}}>
      <label className={{`flex items-center space-x-2 ${{disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}}`}}>
        <input
          type="checkbox"
          checked={{checked}}
          onChange={{handleChange}}
          disabled={{disabled}}
          className="w-4 h-4 rounded border-neutral-300 text-primary-600 focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:cursor-not-allowed"
          aria-invalid={{!!error}}
        />
        {{label && <span className="text-sm text-neutral-700">{{label}}</span>}}
      </label>
      {{error && (
        <p className="text-sm text-error ml-6">{{error}}</p>
      )}}
    </div>
  );
}};

// Usage examples:
// <Checkbox label="I agree to the terms" checked={{agreed}} onChange={{setAgreed}} />
// <Checkbox label="Subscribe to newsletter" disabled />


================================================================================
// Alert.tsx
================================================================================
import React from 'react';

interface AlertProps {{
  variant?: 'success' | 'warning' | 'error' | 'info';
  title?: string;
  message: string;
  dismissible?: boolean;
  onDismiss?: () => void;
  className?: string;
}}

export const Alert: React.FC<AlertProps> = ({{
  variant = 'info',
  title,
  message,
  dismissible = false,
  onDismiss,
  className = '',
}}) => {{
  const baseStyles = 'rounded-lg p-4 border';
  
  const variantStyles = {{
    success: 'bg-success/10 border-success/30 text-success',
    warning: 'bg-warning/10 border-warning/30 text-warning',
    error: 'bg-error/10 border-error/30 text-error',
    info: 'bg-info/10 border-info/30 text-info',
  }};
  
  return (
    <div className={{`${{baseStyles}} ${{variantStyles[variant]}} ${{className}}`}} role="alert">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          {{title && <h4 className="font-semibold mb-1">{{title}}</h4>}}
          <p className="text-sm">{{message}}</p>
        </div>
        {{dismissible && (
          <button
            onClick={{onDismiss}}
            className="ml-4 text-current opacity-70 hover:opacity-100 focus:outline-none"
            aria-label="Dismiss alert"
          >
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </button>
        )}}
      </div>
    </div>
  );
}};

// Usage examples:
// <Alert variant="success" message="Your changes have been saved!" />
// <Alert variant="error" title="Error" message="Something went wrong" dismissible onDismiss={{handleDismiss}} />


================================================================================
// tokens.ts
================================================================================
// Design Tokens
// Auto-generated from design system extraction

export const tokens = {
  "colors": {
    "primary": {
      "500": "#003561",
      "50": "#00569e",
      "100": "#005297",
      "200": "#004b89",
      "300": "#00437c",
      "400": "#003c6e",
      "600": "#002b4f",
      "700": "#00223e",
      "800": "#00182d",
      "900": "#000f1c",
      "950": "#000a13"
    },
    "semantic": {
      "success": "#10b981",
      "warning": "#f59e0b",
      "error": "#ef4444",
      "info": "#3b82f6"
    },
    "neutral": {
      "white": "#ffffff",
      "50": "#fafafa",
      "100": "#f5f5f5",
      "200": "#e5e5e5",
      "300": "#d4d4d4",
      "400": "#a3a3a3",
      "500": "#737373",
      "600": "#525252",
      "700": "#404040",
      "800": "#262626",
      "900": "#171717",
      "950": "#0a0a0a",
      "black": "#000000"
    }
  },
  "typography": {
    "fontFamilies": {
      "sans": "canada-type-gibson, Arial, sans-serif",
      "serif": "'Merriweather', Georgia, serif",
      "mono": "'JetBrains Mono', 'Courier New', monospace"
    },
    "fontSizes": {
      "xs": "0.75rem",
      "sm": "0.875rem",
      "base": "1rem",
      "lg": "1.125rem",
      "xl": "1.25rem",
      "2xl": "1.5rem",
      "3xl": "1.875rem",
      "4xl": "2.25rem",
      "5xl": "3rem",
      "6xl": "3.75rem",
      "7xl": "4.5rem",
      "8xl": "6rem",
      "9xl": "8rem"
    },
    "fontWeights": {
      "thin": "100",
      "extralight": "200",
      "light": "300",
      "normal": "400",
      "medium": "500",
      "semibold": "600",
      "bold": "700",
      "extrabold": "800",
      "black": "900"
    },
    "lineHeights": {
      "none": "1",
      "tight": "1.25",
      "snug": "1.375",
      "normal": "1.5",
      "relaxed": "1.625",
      "loose": "2"
    }
  },
  "spacing": {
    "0": "0",
    "0.125": "0.125rem",
    "0.25": "0.25rem",
    "0.5": "0.5rem",
    "0.75": "0.75rem",
    "1": "1rem",
    "1.25": "1.25rem",
    "1.5": "1.5rem",
    "1.75": "1.75rem",
    "2": "2rem",
    "2.25": "2.25rem",
    "2.5": "2.5rem",
    "3": "3rem",
    "4": "4rem",
    "12": "12rem"
  },
  "borderRadius": {
    "none": "0",
    "sm": "0.125rem",
    "base": "0.25rem",
    "md": "0.375rem",
    "lg": "0.5rem",
    "xl": "0.75rem",
    "2xl": "1rem",
    "3xl": "1.5rem",
    "full": "9999px"
  },
  "shadows": {
    "sm": "0 1px 2px 0 rgb(0 0 0 / 0.05)",
    "base": "0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)",
    "md": "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
    "lg": "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)",
    "xl": "0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)",
    "2xl": "0 25px 50px -12px rgb(0 0 0 / 0.25)",
    "inner": "inset 0 2px 4px 0 rgb(0 0 0 / 0.05)",
    "none": "0 0 #0000"
  },
  "breakpoints": {
    "sm": "640px",
    "md": "768px",
    "lg": "1024px",
    "xl": "1280px",
    "2xl": "1536px"
  },
  "transitions": {
    "duration": {
      "fast": "150ms",
      "base": "300ms",
      "slow": "500ms"
    },
    "easing": {
      "linear": "linear",
      "in": "cubic-bezier(0.4, 0, 1, 1)",
      "out": "cubic-bezier(0, 0, 0.2, 1)",
      "inOut": "cubic-bezier(0.4, 0, 0.2, 1)"
    }
  },
  "zIndex": {
    "0": "0",
    "10": "10",
    "20": "20",
    "30": "30",
    "40": "40",
    "50": "50",
    "auto": "auto"
  }
};

export type ColorScale = typeof tokens.colors.primary;
export type SpacingValue = keyof typeof tokens.spacing;
export type FontSize = keyof typeof tokens.typography.fontSizes;

