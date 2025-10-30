---
name: skill-creator
description: Creates, validates, and packages Claude Code custom skills using templates, automation scripts, and best practices guidance.
---

# Skill Creator

A comprehensive tool for creating high-quality Claude Code custom skills. This skill provides templates, validation, packaging automation, and best practices to help you build effective skills quickly.

## What This Skill Does

This skill helps you:
- **Scaffold new skills** with proper structure and metadata
- **Validate skill definitions** before packaging
- **Package skills correctly** into ZIP files
- **Write effective descriptions** that help Claude invoke your skills at the right time
- **Follow best practices** for skill organization and testing

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
name: Your Skill Name (max 64 chars)
description: Clear purpose and use cases (max 200 chars)
---
```

**Critical**: The description field determines when Claude invokes your skill. Make it specific and action-oriented.

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
