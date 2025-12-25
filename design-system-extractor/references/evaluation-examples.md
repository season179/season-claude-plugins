# Evaluation Examples

Test scenarios to validate the Design System Extractor skill. Use these to ensure the skill works correctly across different input types.

## Scenario 1: Website Extraction (Stripe.com)

### Input

**User request**: "Extract the design system from https://stripe.com"

**Source type**: Live website URL

### Expected Process

1. ✓ Execute `extract_website_design.py` with the URL
2. ✓ Validate JSON output contains colors, typography, spacing
3. ✓ Execute `normalize_tokens.py` on extracted data
4. ✓ Validate YAML output is properly formatted
5. ✓ Execute `generate_components.py` to create React components
6. ✓ Combine into final markdown file: `stripe-design-system.md`

### Success Criteria

**Extracted data must include**:
- Colors: Primary brand colors (purple/blue shades), neutral grays, semantic colors
- Typography: Multiple font sizes (14px-48px range), font weights (400, 500, 600), Inter or similar sans-serif
- Spacing: Various padding/margin values
- Border radius: Rounded corners (4px, 8px, etc.)
- Shadows: Box shadows for elevation

**Normalized tokens must have**:
- Complete color scales (50-950) for primary colors
- Full typography scale (xs through 9xl)
- Spacing scale in rem units (0.25rem, 0.5rem, 1rem, etc.)
- No missing or undefined values

**Generated components must include**:
- Button with variants (solid, outline, ghost)
- Input with label and error states
- Card component
- TypeScript interfaces for all props
- Usage examples in comments

**Final output**:
- Single markdown file under 2000 lines
- Three main sections: Instructions, Design Tokens (YAML), Components (TypeScript)
- No hardcoded values in components (all reference tokens)
- Valid YAML and TypeScript syntax

### Common Pitfalls

- ❌ Timeout errors: Stripe is a complex site, may need retry
- ❌ Missing brand colors: Script should capture purple/blue brand colors
- ❌ Incomplete scales: Normalization might not generate full 50-950 range
- ✓ Check that semantic colors (success, error) are included

---

## Scenario 2: Screenshot Analysis (Figma Mockup)

### Input

**User request**: "Extract the design system from this Figma mockup screenshot"

**Source type**: PNG/JPEG screenshot of a design mockup showing UI components (buttons, inputs, cards)

**Test file**: Create a mockup with:
- 3-4 distinct brand colors
- 2 font sizes (heading and body)
- Button component in 2 states (normal and hover)
- Input field with label
- Card with padding and shadow

### Expected Process

1. ✓ Execute `extract_image_colors.py` with image path and 12-16 colors
2. ✓ Validate JSON contains dominant colors with hex codes
3. ✓ Manually analyze typography and spacing using Claude's image viewing
4. ✓ Create `extracted_data.json` combining color extraction + manual analysis
5. ✓ Execute `normalize_tokens.py` on combined data
6. ✓ Execute `generate_components.py`
7. ✓ Create final markdown file: `custom-design-system.md`

### Success Criteria

**Color extraction must identify**:
- 3-4 primary brand colors accurately
- Neutral grays/whites/blacks
- Color categorization (primary vs neutral vs accents)

**Manual analysis must capture**:
- At least 2 font sizes
- Font weight if visible (normal, bold)
- Approximate spacing values (8px, 16px, 24px common increments)
- Border radius if components have rounded corners
- Shadow intensity if present

**Normalized output must**:
- Generate complete color scales even from limited input colors
- Fill in missing typography values with sensible defaults
- Create full spacing scale based on observed values

**Quality checks**:
- Color extraction captures actual brand colors (not noise)
- Typography scale makes sense (not just random sizes)
- Components use extracted tokens, not made-up values

### Common Pitfalls

- ❌ Too many/too few colors extracted: Adjust number parameter (8-16 range)
- ❌ Background colors dominate: Script might extract white/gray as "primary"
- ❌ Unable to determine exact font sizes: Use rough estimates (16px, 18px, 24px)
- ✓ It's okay to use defaults for missing information

---

## Scenario 3: Text Description (Minimal Brand Requirements)

### Input

**User request**: "Create a design system for a SaaS product with these brand colors: #3B82F6 (primary blue), #10B981 (success green), #EF4444 (error red). Use Inter font. Make it clean and modern."

**Source type**: Text description with minimal specifications

### Expected Process

1. ✓ No extraction scripts needed (no visual source)
2. ✓ Ask clarifying questions:
   - Preferred spacing philosophy? (compact, normal, spacious)
   - Button style preference? (rounded, sharp corners)
   - Shadow style? (flat, subtle elevation, strong elevation)
3. ✓ Create minimal `extracted_data.json` with user-specified values:
   ```json
   {
     "colors": ["#3B82F6", "#10B981", "#EF4444", "#6B7280"],
     "typography": {
       "fontFamilies": ["Inter"],
       "fontSizes": [16, 18, 24, 32]
     },
     "spacing": [4, 8, 16, 24, 32],
     "borderRadius": [4, 8],
     "shadows": ["0 1px 3px rgba(0,0,0,0.1)"]
   }
   ```
4. ✓ Execute `normalize_tokens.py` (fills in complete system)
5. ✓ Execute `generate_components.py`
6. ✓ Create final markdown: `saas-design-system.md`

### Success Criteria

**Clarification questions asked**:
- Spacing scale preference
- Component style preferences (rounded vs sharp)
- Any other brand colors beyond the 3 specified

**Minimal data creation**:
- Uses exact colors provided (#3B82F6, #10B981, #EF4444)
- Includes Inter font family
- Has reasonable defaults for missing values

**Normalized tokens must**:
- Generate full 50-950 scale from #3B82F6 primary
- Create neutral scale (grays) even if not specified
- Semantic colors map correctly (success → #10B981, error → #EF4444)
- Complete typography scale based on minimal input

**Generated components**:
- Reflect "clean and modern" aesthetic in code comments
- Use the specified brand colors appropriately
- Include all standard components even with minimal input

### Common Pitfalls

- ❌ Not asking clarifying questions: User only gave 3 colors, ask about neutrals
- ❌ Making assumptions: Don't guess brand direction without asking
- ❌ Over-specifying: User said "clean and modern", don't add complex patterns
- ✓ Default to industry standards when user doesn't specify

### Example Dialog

**Good approach**:
> I'll create a design system with your brand colors. A few questions:
> 1. For neutral colors (grays, blacks), should I use blue-tinted grays or pure grays?
> 2. Spacing preference: compact (4px base) or spacious (8px base)?
> 3. Any additional accent colors needed?

**Bad approach**:
> (Silently creates design system without clarification, makes random choices)

---

## Testing the Skill

### Quick Validation Checklist

For each scenario, verify:

- [ ] Skill activates on relevant trigger phrases
- [ ] Correct scripts are executed in correct order
- [ ] Validation commands run between steps
- [ ] Error handling works (test with invalid URL, missing file)
- [ ] Final output is single markdown file
- [ ] YAML syntax is valid (`python -c "import yaml; yaml.safe_load(open('file.yaml'))"`)
- [ ] Components reference tokens, not hardcoded values
- [ ] Documentation is clear and actionable

### Performance Benchmarks

**Scenario 1 (Website)**:
- Extraction: 10-30 seconds
- Normalization: < 1 second
- Component generation: < 1 second
- Total: ~1-2 minutes

**Scenario 2 (Screenshot)**:
- Color extraction: 2-5 seconds
- Manual analysis: 1-2 minutes (Claude reviewing image)
- Normalization: < 1 second
- Component generation: < 1 second
- Total: ~2-3 minutes

**Scenario 3 (Text)**:
- Clarifying questions: 30 seconds
- Manual data creation: 1 minute
- Normalization: < 1 second
- Component generation: < 1 second
- Total: ~2 minutes

### Regression Testing

Re-run these scenarios after making changes to:
- Extraction scripts
- Normalization logic
- Component templates
- SKILL.md instructions

Ensure outputs remain consistent and high-quality.
