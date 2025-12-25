---
name: design-system-extractor
description: Extracts design tokens (colors, typography, spacing) and components from websites, screenshots, or descriptions into production-ready documentation. Use when creating design systems or documenting visual patterns.
---

# Design System Extractor

Extract and document design systems from any source into production-ready markdown files with design tokens and component libraries.

## Prerequisites

**Recommended**: Use a virtual environment to avoid system conflicts:

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install playwright==1.56.0 Pillow==12.0.0 numpy==2.3.5 scikit-learn==1.7.2 PyYAML==6.0.3
playwright install chromium
```

Or use the provided setup script (guides you through venv setup):

```bash
bash scripts/setup.sh
```

**Environment**: This skill requires network access and is designed for claude.ai. API environments without network access are not supported.

## Model Compatibility

- **Tested with**: Claude Sonnet 3.5 and 4.5
- **Recommended**: Claude Sonnet (best balance of speed and quality)
- **Haiku**: Works but may need more explicit guidance on error recovery steps
- **Opus**: Produces high-quality documentation but may be overly verbose

## Workflow Overview

Copy this checklist and track progress:

```
Design System Extraction Progress:
- [ ] Step 1: Extract raw data from source
- [ ] Step 2: Normalize design tokens
- [ ] Step 3: Generate component library
- [ ] Step 4: Create final documentation
```

This skill uses executable scripts for deterministic extraction:

1. **Extract Raw Data** → Run extraction scripts on source
2. **Normalize Tokens** → Process raw data into standard format  
3. **Generate Components** → Create React/TypeScript library
4. **Output Documentation** → Produce single markdown file

## Step 1: Extract Raw Design Data

Use the appropriate extraction script based on input type:

### From Website URLs

**Execute `scripts/extract_website_design.py` to extract design tokens:**

```bash
python scripts/extract_website_design.py <url> > extracted_data.json
```

**Do not read the script** - execute it directly. The script:
- Launches a headless browser with Playwright
- Analyzes computed styles of all elements
- Extracts colors, typography, spacing, border radius, shadows
- Identifies component patterns (buttons, inputs, cards)
- Returns structured JSON data

**Example:**
```bash
python scripts/extract_website_design.py https://stripe.com > stripe_design.json
```

The script outputs JSON with:
- `colors`: Array of all colors found (in various formats)
- `typography`: Font families, sizes, weights, line heights
- `spacing`: Padding/margin/gap values used
- `borderRadius`: Border radius values
- `shadows`: Box shadow definitions
- `components`: Identified UI components with their styles

### From Screenshots/Images

**Execute `scripts/extract_image_colors.py` to extract color palettes:**

```bash
python scripts/extract_image_colors.py <image_path> [num_colors] > color_data.json
```

**Do not read the script** - execute it directly. The script:
- Uses K-means clustering to find dominant colors
- Categorizes colors as primary, grayscale, or accents
- Generates color scales (50-950) from primary colors
- Returns color frequency and brightness analysis

**Example:**
```bash
# Using home directory (works on macOS and Linux)
python scripts/extract_image_colors.py ~/Downloads/mockup.png 16 > colors.json

# Or using relative path
python scripts/extract_image_colors.py ./mockup.png 16 > colors.json
```

For full design system extraction from screenshots:
1. Run color extraction script
2. Manually analyze typography, spacing from the image using Claude's image viewing capability
3. Combine into extracted_data.json format

### From Text Descriptions

When user provides requirements without visual source:
- Ask clarifying questions about brand colors, typography, spacing philosophy
- Create a minimal extracted_data.json with user specifications
- Use defaults from `references/design-tokens-guide.md` for missing values

### ✓ Step 1 Validation

Before proceeding to Step 2, verify:
- [ ] Extraction script completed without errors
- [ ] JSON output is valid: `python -m json.tool extracted_data.json > /dev/null`
- [ ] File contains expected fields: colors, typography, spacing
- [ ] Color values are in valid format (hex, rgb, or color names)
- [ ] At least some data was extracted (file is not empty)

## Step 2: Normalize Design Tokens

**Execute `scripts/normalize_tokens.py` to convert raw data into normalized tokens:**

```bash
python scripts/normalize_tokens.py extracted_data.json > tokens.yaml
```

**Do not read the script** - execute it directly. The script automatically:
- **Normalizes colors** into primary, neutral, and semantic categories
- **Generates complete color scales** (50-950) from extracted base colors
- **Standardizes spacing** to a consistent 4px-based scale in rem units
- **Organizes typography** into standard size/weight/line-height scales
- **Creates standard border radius, shadow, and transition tokens**
- **Outputs properly formatted YAML** ready for documentation

The script handles:
- Converting px to rem (base 16px)
- Deduplicating similar values
- Filling gaps in extracted scales
- Applying design system best practices from `references/design-tokens-guide.md`

**What the script produces:**

```yaml
colors:
  primary:
    50: "#f0f9ff"
    # ... full 50-950 scale
  semantic:
    success: "#10b981"
    error: "#ef4444"
  neutral:
    # ... grayscale palette

typography:
  fontFamilies:
    sans: "'Inter', sans-serif"
  fontSizes:
    xs: "0.75rem"
    # ... xs through 9xl

spacing:
  0: "0"
  1: "0.25rem"  # 4px
  # ... full scale

# ... all other tokens
```

**When extraction data is incomplete:**
The script fills in sensible defaults, ensuring you always get a complete, production-ready token system even from partial data.

### ✓ Step 2 Validation

Before proceeding to Step 3, verify:
- [ ] Normalization script completed successfully
- [ ] YAML output is valid: `python -c "import yaml; yaml.safe_load(open('tokens.yaml'))" && echo "✓ Valid"`
- [ ] Color scales are complete (check for 50, 100, 200...950 values)
- [ ] Typography includes xs through 9xl sizes
- [ ] Spacing scale is in rem units
- [ ] No undefined or null values in critical sections

## Step 3: Generate Component Library

**Execute `scripts/generate_components.py` to create React/TypeScript components:**

```bash
python scripts/generate_components.py tokens.yaml
```

**Do not read the script** - execute it directly. The script generates production-ready components:
- **Button** - Multiple variants (solid, outline, ghost) and sizes
- **Input** - With label, error states, validation
- **Card** - Container with elevation options
- **Badge** - Status indicators with semantic variants
- **Checkbox** - Boolean input with proper accessibility
- **Alert** - Feedback messages with dismissible option

Each component includes:
- Full TypeScript interface with prop types
- Default values for optional props
- Variant styling using design token references
- Size options (sm, md, lg)
- Disabled state handling
- Accessibility attributes (ARIA, roles, focus management)
- Usage examples in comments

**The script outputs component code** that can be copied directly into the final documentation.

For reference on component patterns and best practices, see `references/component-patterns.md`.

### ✓ Step 3 Validation

Before proceeding to Step 4, verify:
- [ ] Component generation script ran successfully
- [ ] All components have TypeScript interfaces
- [ ] Components reference design tokens (no hardcoded #hex or px values)
- [ ] Each component includes size variants (sm, md, lg)
- [ ] Accessibility attributes are present (ARIA labels, roles)
- [ ] Code includes usage examples in comments

## Step 4: Generate Complete Documentation

Now create the final design system markdown file by combining all sections:

### Structure

Use the template from `assets/design-system-template.md` as a guide. The output file should have:

1. **Instructions Section**
   - Overview of the design system
   - Installation and setup (npm/yarn)
   - How to use design tokens in CSS, React, Tailwind
   - Component usage examples
   - Best practices and customization

2. **Design Tokens Section**
   - Insert the complete YAML from `tokens.yaml`
   - Wrap in proper YAML code blocks
   - Add explanatory comments where helpful

3. **Component Library Section**
   - Insert each component from the generation script
   - Include full TypeScript implementation
   - Add usage examples for each component
   - Group logically (inputs, feedback, layout, etc.)

### File Output

Save the final design system to `./[name]-design-system.md` (current directory) where `[name]` is:
- Domain name from URL (e.g., "stripe" from stripe.com)
- Brand name if specified by user
- "custom" as fallback

Alternatively, use an absolute path like `~/Documents/[name]-design-system.md` for specific locations.

**Complete example workflow:**

```bash
# 1. Extract from website
python scripts/extract_website_design.py https://example.com > raw_data.json

# 2. Validate extraction (check file is valid JSON)
python -m json.tool raw_data.json > /dev/null && echo "✓ Valid JSON" || echo "✗ Invalid JSON - retry extraction"

# 3. Normalize tokens
python scripts/normalize_tokens.py raw_data.json > tokens.yaml

# 4. Validate YAML (check file is valid YAML)
python -c "import yaml; yaml.safe_load(open('tokens.yaml'))" && echo "✓ Valid YAML" || echo "✗ Invalid YAML"

# 5. Generate components
python scripts/generate_components.py tokens.yaml

# 6. Combine into final markdown (done by Claude)
```

**Feedback loop**: If validation fails at any step, review error messages and retry the failed step before continuing.

### ✓ Step 4 Final Validation

Before delivering the final design system, verify:
- [ ] Single markdown file created with appropriate name
- [ ] File size is reasonable (typically 500-2000 lines)
- [ ] Three main sections present: Instructions, Design Tokens, Components
- [ ] YAML syntax is valid (can be parsed without errors)
- [ ] TypeScript code is syntactically correct
- [ ] All color scales complete (50-950)
- [ ] Typography scale comprehensive (xs-9xl)
- [ ] Components reference tokens, not hardcoded values
- [ ] Usage examples included for key components
- [ ] Installation instructions are clear

## Important: Script Execution Strategy

### When to Run Scripts

**ALWAYS run extraction scripts** for:
- Website URLs (use `extract_website_design.py`)
- Image files with clear UI elements (use `extract_image_colors.py`)

Scripts provide deterministic, accurate extraction that's more reliable than manual analysis.

### When to Use Manual Analysis

Use Claude's image viewing and manual analysis when:
- Images are low quality or unclear
- User provides only text descriptions
- Scripts fail or return errors

### Handling Script Errors

If scripts fail, see `references/troubleshooting.md` for detailed error solutions. Quick fixes:

1. **Network errors** (website extraction) → Check connectivity, try different URL
2. **File not found** (image extraction) → Use absolute paths, verify file exists
3. **Module errors** → Ensure dependencies installed: `pip install -r scripts/requirements.txt`
4. **Invalid JSON/YAML** → Run validation: `python -m json.tool file.json`
5. **Timeout errors** → Website may block automation, try manual analysis

See [troubleshooting.md](references/troubleshooting.md) for complete error reference with examples.

### Optimizing Token Generation

The normalization script (`normalize_tokens.py`) is **deterministic and should always be run** even if you manually create the extracted_data.json. It ensures:
- Consistent naming conventions
- Complete scales (no gaps)
- Proper unit conversions (px to rem)
- Valid YAML output

## Quality Assurance

Quality checks are integrated into each workflow step (see ✓ Step 1-4 Validation sections above). Use the step-by-step validation checklists to ensure quality throughout the process, not just at the end.

For comprehensive testing scenarios, see `references/evaluation-examples.md`.

## Tips for Best Results

**When analyzing designs:**
- Look for repeated patterns (they become tokens)
- Group similar values (create scales)
- Identify component variations (become props)
- Note interactive states (hover, focus, active, disabled)

**When creating tokens:**
- Prefer semantic naming over descriptive (`colors.semantic.error` vs `colors.red`)
- Create complete scales even if source doesn't show all values
- Use industry-standard conventions (like 50-950 for colors)
- Include reasonable defaults for missing information

**When building components:**
- Start simple, add complexity as needed
- Compose larger components from smaller ones
- Keep components focused (single responsibility)
- Make common cases easy, complex cases possible

**When writing documentation:**
- Write for developers who are new to the design system
- Include concrete examples, not just descriptions
- Explain the "why" behind design decisions
- Make it easy to find what you need quickly

## Additional References

- `references/design-tokens-guide.md` - Comprehensive token examples and structure
- `references/component-patterns.md` - React component patterns and TypeScript best practices
- `references/troubleshooting.md` - Error solutions with concrete examples
- `references/evaluation-examples.md` - Test scenarios to validate skill functionality
- `assets/design-system-template.md` - Output structure template

Read these files when you need detailed examples or are unsure about structure.
