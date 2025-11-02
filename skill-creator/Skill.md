---
name: skill-creator
description: Creates and debugs Claude Code skills. Validates frontmatter, checks ZIP structure, packages correctly, provides templates, and ensures best practices for skill invocation.
---

# Skill Creator

A comprehensive tool for creating high-quality Claude Code custom skills. This skill provides templates, validation, packaging automation, and best practices to help you build effective skills quickly.

## Communication Style
- Be concise - provide only essential information
- Avoid verbose explanations unless explicitly requested
- Focus on actionable steps and key details

## When to Use This Skill

Use this skill when you need to:
- **Create a new Claude Code skill** from scratch
- **Debug why a skill isn't being invoked** properly
- **Validate skill structure and metadata** before uploading
- **Package skills correctly** into ZIP format for Claude Code
- **Fix frontmatter errors** or invalid field configurations
- **Learn best practices** for skill descriptions and organization

Also useful when improving existing skills or understanding skill architecture.

## Common Gotchas

**Before you start, avoid these common mistakes:**

1. **Invalid top-level fields** - Never use `version`, `author`, or `dependencies` at the top level
   - ❌ `version: 1.0.0` (top level)
   - ✅ `metadata:` with `version: 1.0.0` nested inside
   - Or document in README.md instead

2. **Wrong ZIP structure** - The ZIP must contain the skill folder as root
   - ✅ `skill-name.zip` → `skill-name/` → `Skill.md`
   - ❌ `skill-name.zip` → `Skill.md` (missing folder wrapper)
   - Use `package_skill.py` to ensure correct structure

3. **Generic descriptions won't trigger** - Be specific with action verbs
   - ❌ "Helps with code" or "A useful tool"
   - ✅ "Analyzes Python code for security vulnerabilities and suggests fixes"

4. **Name format must be lowercase-with-hyphens**
   - ❌ `Python Analyzer`, `API_Helper`, `My Skill!`
   - ✅ `python-analyzer`, `api-helper`, `my-skill`
   - The validator will auto-suggest corrections

5. **Description length limit** - Maximum 200 characters
   - Keep it concise and action-focused
   - Every word should earn its place

## Quick Start Guide

### Creating a Basic Skill

1. **Start with a template**: Use the basic skill template from `resources/templates/basic-skill.md`
2. **Fill in metadata**: Set your skill's name and description (name max 64 chars, description max 200 chars)
3. **Write instructions**: Add clear markdown instructions for Claude
4. **Validate**: Run `python scripts/validate_skill.py <skill-path>`
5. **Package**: Run `python scripts/package_skill.py <skill-path>`

### Creating an Advanced Skill

For skills with helper scripts and resources:
1. Use the advanced template from `resources/templates/advanced-skill.md`
2. Add your Python/JavaScript scripts to the skill directory
3. Include reference documents in a `resources/` subdirectory
4. Specify dependencies in the YAML frontmatter
5. Validate and package using the provided scripts

## Key Components

### 1. Skill.md Structure

Every skill needs a `Skill.md` file with YAML frontmatter:

```yaml
---
name: your-skill-name
description: Clear purpose and use cases (max 200 chars)
---
```

**Critical Requirements**:
- **name**: Must be lowercase letters, numbers, and hyphens only (max 64 chars)
  - ✅ Good: `python-security-analyzer`, `api-doc-generator`, `n8n-workflow-builder`
  - ❌ Bad: `Python Security Analyzer`, `API_Doc_Generator`, `My Skill!`
- **description**: Determines when Claude invokes your skill - be specific and action-oriented

**Optional fields** you can add:
- `license`: Specify the license (e.g., "MIT")
- `allowed-tools`: Array of tools the skill can use
- `metadata`: Object for version, author, dependencies, etc.

### 2. File Organization

```
your-skill/
├── Skill.md              # Required: Main skill definition
├── resources/            # Optional: Additional documentation
│   └── REFERENCE.md
└── scripts/              # Optional: Helper scripts
    └── helper.py
```

### 3. Packaging Format

The ZIP must have the skill folder as root:
```
your-skill.zip
└── your-skill/
    ├── Skill.md
    └── ...
```

## Writing Effective Descriptions

Your description (max 200 chars) should:
- ✅ Be specific about what the skill does
- ✅ Include key trigger words (e.g., "analyze", "generate", "validate")
- ✅ Mention the domain or use case
- ❌ Be too generic or vague
- ❌ Include unnecessary words

**Examples:**

Good: "Analyzes Python code for security vulnerabilities, suggests fixes, and generates secure code alternatives."

Bad: "A helpful tool for code stuff."

## Best Practices

1. **Single Responsibility**: Each skill should focus on one workflow or domain
2. **Clear Instructions**: Write step-by-step instructions in the markdown body
3. **Include Examples**: Show Claude how to use resources or run scripts
4. **Track Versions**: Use metadata to track versions with semantic versioning (1.0.0, 1.1.0, etc.)
5. **Test Thoroughly**: Test with multiple prompts before and after uploading
6. **Reference Resources**: For extensive info, use separate REFERENCE.md files

## Available Tools

### Validation Script
```bash
python scripts/validate_skill.py <skill-directory>
```
Checks:
- YAML frontmatter validity
- Required fields presence
- Description length (≤200 chars)
- Name length (≤64 chars)
- File structure correctness

### Packaging Script
```bash
python scripts/package_skill.py <skill-directory>
```
Creates a properly formatted ZIP file ready for upload.

### Testing Helper
```bash
python scripts/test_skill.py <skill-directory>
```
Generates test prompts and validation checklist.

## Troubleshooting

**Skill not being invoked?**
- Make your description more specific with action verbs
- Include domain keywords that match your use case
- Test with more varied prompts

**Packaging errors?**
- Ensure Skill.md is in the root of your skill folder
- Check that ZIP has skill folder as root (not nested)
- Verify all file references in Skill.md are valid

**Validation failures?**
- Check YAML syntax (use `---` delimiters)
- Verify description is under 200 characters
- Ensure name is under 64 characters
- Confirm required fields are present

## Reference Documentation

For comprehensive details, see:
- `resources/REFERENCE.md` - In-depth guide covering all aspects
- `resources/templates/` - Ready-to-use templates
- `resources/examples/` - Working skill examples

## Workflow Overview

1. **Plan**: Define what your skill will do (single, focused workflow)
2. **Template**: Start from basic or advanced template
3. **Develop**: Write instructions, add scripts/resources if needed
4. **Validate**: Check structure and metadata
5. **Test**: Try multiple prompts to verify invocation
6. **Package**: Create ZIP file
7. **Upload**: Add to Claude Code via Settings > Capabilities
8. **Iterate**: Refine description based on testing

Remember: Skills can't explicitly reference each other, but Claude can use multiple skills together automatically based on their descriptions.
