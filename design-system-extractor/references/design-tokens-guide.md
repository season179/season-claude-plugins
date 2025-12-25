# Design Tokens Reference Guide

## Contents
- Color token structure (primary, semantic, neutral)
- Typography scale (font families, sizes, weights, line heights, letter spacing)
- Spacing scale (4px-based system)
- Other design tokens (border radius, shadows, breakpoints, transitions, z-index)
- Component pattern examples
- Common patterns for interactive states and text hierarchy

## Color Token Structure

```yaml
colors:
  # Primary colors - main brand colors
  primary:
    50: "#f0f9ff"
    100: "#e0f2fe"
    200: "#bae6fd"
    300: "#7dd3fc"
    400: "#38bdf8"
    500: "#0ea5e9"  # Base primary
    600: "#0284c7"
    700: "#0369a1"
    800: "#075985"
    900: "#0c4a6e"
    950: "#082f49"
  
  # Semantic colors - purpose-driven
  semantic:
    success: "#10b981"
    warning: "#f59e0b"
    error: "#ef4444"
    info: "#3b82f6"
  
  # Neutral colors - grays and backgrounds
  neutral:
    white: "#ffffff"
    black: "#000000"
    50: "#fafafa"
    100: "#f5f5f5"
    200: "#e5e5e5"
    300: "#d4d4d4"
    400: "#a3a3a3"
    500: "#737373"
    600: "#525252"
    700: "#404040"
    800: "#262626"
    900: "#171717"
    950: "#0a0a0a"
```

## Typography Scale

```yaml
typography:
  fontFamilies:
    sans: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    serif: "'Merriweather', Georgia, serif"
    mono: "'JetBrains Mono', 'Courier New', monospace"
  
  fontSizes:
    xs: "0.75rem"      # 12px
    sm: "0.875rem"     # 14px
    base: "1rem"       # 16px
    lg: "1.125rem"     # 18px
    xl: "1.25rem"      # 20px
    "2xl": "1.5rem"    # 24px
    "3xl": "1.875rem"  # 30px
    "4xl": "2.25rem"   # 36px
    "5xl": "3rem"      # 48px
    "6xl": "3.75rem"   # 60px
    "7xl": "4.5rem"    # 72px
    "8xl": "6rem"      # 96px
    "9xl": "8rem"      # 128px
  
  fontWeights:
    thin: "100"
    extralight: "200"
    light: "300"
    normal: "400"
    medium: "500"
    semibold: "600"
    bold: "700"
    extrabold: "800"
    black: "900"
  
  lineHeights:
    none: "1"
    tight: "1.25"
    snug: "1.375"
    normal: "1.5"
    relaxed: "1.625"
    loose: "2"
  
  letterSpacing:
    tighter: "-0.05em"
    tight: "-0.025em"
    normal: "0"
    wide: "0.025em"
    wider: "0.05em"
    widest: "0.1em"
```

## Spacing Scale

```yaml
spacing:
  0: "0"
  px: "1px"
  0.5: "0.125rem"   # 2px
  1: "0.25rem"      # 4px
  1.5: "0.375rem"   # 6px
  2: "0.5rem"       # 8px
  2.5: "0.625rem"   # 10px
  3: "0.75rem"      # 12px
  3.5: "0.875rem"   # 14px
  4: "1rem"         # 16px
  5: "1.25rem"      # 20px
  6: "1.5rem"       # 24px
  7: "1.75rem"      # 28px
  8: "2rem"         # 32px
  9: "2.25rem"      # 36px
  10: "2.5rem"      # 40px
  11: "2.75rem"     # 44px
  12: "3rem"        # 48px
  14: "3.5rem"      # 56px
  16: "4rem"        # 64px
  20: "5rem"        # 80px
  24: "6rem"        # 96px
  28: "7rem"        # 112px
  32: "8rem"        # 128px
  36: "9rem"        # 144px
  40: "10rem"       # 160px
  44: "11rem"       # 176px
  48: "12rem"       # 192px
  52: "13rem"       # 208px
  56: "14rem"       # 224px
  60: "15rem"       # 240px
  64: "16rem"       # 256px
  72: "18rem"       # 288px
  80: "20rem"       # 320px
  96: "24rem"       # 384px
```

## Other Design Tokens

```yaml
borderRadius:
  none: "0"
  sm: "0.125rem"    # 2px
  base: "0.25rem"   # 4px
  md: "0.375rem"    # 6px
  lg: "0.5rem"      # 8px
  xl: "0.75rem"     # 12px
  "2xl": "1rem"     # 16px
  "3xl": "1.5rem"   # 24px
  full: "9999px"

shadows:
  sm: "0 1px 2px 0 rgb(0 0 0 / 0.05)"
  base: "0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)"
  md: "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)"
  lg: "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)"
  xl: "0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)"
  "2xl": "0 25px 50px -12px rgb(0 0 0 / 0.25)"
  inner: "inset 0 2px 4px 0 rgb(0 0 0 / 0.05)"
  none: "0 0 #0000"

breakpoints:
  sm: "640px"
  md: "768px"
  lg: "1024px"
  xl: "1280px"
  "2xl": "1536px"

transitions:
  duration:
    fast: "150ms"
    base: "300ms"
    slow: "500ms"
  easing:
    linear: "linear"
    in: "cubic-bezier(0.4, 0, 1, 1)"
    out: "cubic-bezier(0, 0, 0.2, 1)"
    inOut: "cubic-bezier(0.4, 0, 0.2, 1)"

zIndex:
  0: "0"
  10: "10"
  20: "20"
  30: "30"
  40: "40"
  50: "50"
  auto: "auto"
```

## Component Pattern Examples

### Button Variants

```typescript
// Solid button (primary style)
className: "bg-primary-600 hover:bg-primary-700 text-white"

// Outline button
className: "border-2 border-primary-600 text-primary-600 hover:bg-primary-50"

// Ghost button
className: "text-primary-600 hover:bg-primary-50"

// Sizes
small: "px-3 py-1.5 text-sm"
medium: "px-4 py-2 text-base"
large: "px-6 py-3 text-lg"
```

### Common Patterns

**Card elevation:**
```
low: shadow-sm
medium: shadow-md
high: shadow-lg
```

**Interactive states:**
```
hover: brightness-110 scale-105
active: brightness-90 scale-95
disabled: opacity-50 cursor-not-allowed
focus: ring-2 ring-primary-500 ring-offset-2
```

**Text hierarchy:**
```
heading: font-bold tracking-tight
subheading: font-semibold
body: font-normal leading-relaxed
caption: text-sm text-neutral-600
```
