---
name: website-theme-generator
description: "Extract design themes from websites using Playwright: color palettes, typography, spacing systems, and brand aesthetics. Analyzes live sites to generate design systems and style guides."
metadata:
  version: 2.0.0
  dependencies: "playwright>=1.40.0, python>=3.8"
---

# Website Theme Generator

Extract comprehensive design themes from live websites: colors, typography, spacing, and UI patterns.

## When to Use This Skill

Use when users want to:
- Extract design inspiration from existing websites
- Analyze color palettes and brand aesthetics
- Identify typography patterns and font choices
- Create design systems based on successful sites
- Generate style guides from live examples

## Prerequisites

Playwright must be installed with browser support:

```bash
pip install -r scripts/requirements.txt
playwright install chromium
```

**Troubleshooting installation**: See [resources/TROUBLESHOOTING.md](resources/TROUBLESHOOTING.md)

## Core Workflow

### Step 1: Validate the Request

**Security check** (see [resources/SECURITY.md](resources/SECURITY.md) for full guidelines):

### Step 2: Run Analysis Script

```bash
python scripts/analyze_website.py <url> <output_directory>
```

**Example:**
```bash
python scripts/analyze_website.py https://stripe.com ./stripe_analysis
```

**What this extracts:**
- Color palette (most-used colors with frequency counts)
- Typography (font families and stacks)
- Spacing system (padding/margin patterns)
- Border radius patterns
- Screenshots (full page + above-the-fold viewport)

**Output:** Creates `analysis.json` and two PNG screenshots in the output directory.

### Step 3: Review Visual Context

**Critical step** - Always view screenshots before generating the theme:

```bash
view <output_directory>/screenshot_viewport.png
view <output_directory>/screenshot_full.png
```

Visual context reveals:
- Brand personality and overall style
- Layout patterns and visual hierarchy
- Component design approaches
- Aesthetic (modern, minimal, bold, playful, etc.)

### Step 4: Examine Analysis Data

Review the extracted data:

```bash
view <output_directory>/analysis.json
```

**Key data points:**
- `colors.analysis.most_common_colors` - Top 10 colors with usage counts
- `fonts` - Detected font families
- `spacing.analysis.most_common_spacing` - Frequent spacing values
- `border_radius` - Roundness patterns

**For data structure details**: See [resources/REFERENCE.md#analysis-data-structure](resources/REFERENCE.md)

### Step 5: Generate Comprehensive Theme

Combine visual insights with data analysis to create the theme.

**Reference these guides as needed:**
- [resources/REFERENCE.md#color-selection-strategy](resources/REFERENCE.md) - How to identify primary, secondary, accent, and neutral colors
- [resources/REFERENCE.md#typography-strategy](resources/REFERENCE.md) - Font pairing principles and interpretation
- [resources/REFERENCE.md#spacing-system](resources/REFERENCE.md) - Creating spacing scales from data
- [resources/REFERENCE.md#theme-output-format](resources/REFERENCE.md) - Complete theme template

**Output the theme** using the structured format from REFERENCE.md.

## Common Issues

**Analysis fails or produces poor results?**
- Website may be JavaScript-heavy (SPA) - requires additional wait time
- Timeout errors on slow sites - increase timeout setting
- Empty color/font data - check TROUBLESHOOTING.md

**Full troubleshooting guide**: [resources/TROUBLESHOOTING.md](resources/TROUBLESHOOTING.md)

## Security & Privacy

⚠️ This skill visits live websites and captures screenshots.

**Quick guidelines:**
- Only analyze public websites
- Screenshots may contain sensitive information
- Respect robots.txt and terms of service
- Use for inspiration, not pixel-perfect copying

**Complete security guidelines**: [resources/SECURITY.md](resources/SECURITY.md)

## Additional Resources

- **[resources/REFERENCE.md](resources/REFERENCE.md)** - Comprehensive technical documentation
- **[resources/SECURITY.md](resources/SECURITY.md)** - Security and privacy guidelines
- **[resources/TROUBLESHOOTING.md](resources/TROUBLESHOOTING.md)** - Common issues and solutions

## Tips

- Analyze homepage or main landing page for best results
- Multiple pages from the same site can reveal comprehensive design systems
- Screenshots are crucial - data alone doesn't capture the full aesthetic
- Color frequency doesn't always equal importance (check visuals)
- Web fonts may load after initial extraction (see TROUBLESHOOTING.md)
