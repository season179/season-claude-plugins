# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a Claude Code skills development repository containing:
1. **skill-creator** - A meta-skill for creating, validating, and packaging Claude Code skills
2. **n8n-workflow-builder** - A skill for building n8n automation workflows
3. Development tools for the skill creation lifecycle

## Critical Skill Format Requirements

When creating or modifying skills in this repository, these rules are **enforced by Claude Code**:

### YAML Frontmatter Rules

**Allowed top-level fields:**
- `name` (required) - Must be lowercase-with-hyphens format only (e.g., `my-skill-name`)
- `description` (required) - Max 200 characters, action-oriented
- `license` (optional)
- `allowed-tools` (optional array)
- `metadata` (optional object)

**Invalid top-level fields** (will cause upload errors):
- `version` - Use `metadata.version` instead
- `author` - Use `metadata.author` instead
- `dependencies` - Document in README or `metadata.dependencies`

### Name Format Validation

The `name` field uses regex: `^[a-z0-9-]+$`

✅ Valid: `python-analyzer`, `api-helper`, `n8n-workflow-builder`
❌ Invalid: `Python Analyzer`, `api_helper`, `MySkill`

The validator auto-suggests corrections (converts to lowercase, replaces underscores/spaces with hyphens).

## Development Workflow

### Creating a New Skill

```bash
# 1. Copy template
cp skill-creator/resources/templates/basic-skill.md new-skill-name/Skill.md

# 2. Edit the Skill.md with correct frontmatter

# 3. Validate (catches format errors early)
python skill-creator/scripts/validate_skill.py new-skill-name/

# 4. Package for upload
python skill-creator/scripts/package_skill.py new-skill-name/
```

### Testing Changes to skill-creator

When modifying the skill-creator tools:

```bash
# Test validation logic
python skill-creator/scripts/validate_skill.py skill-creator/

# Test packaging
python skill-creator/scripts/package_skill.py skill-creator/

# Test against a malformed skill (should fail)
python skill-creator/scripts/validate_skill.py test-skill-with-errors/
```

### Modifying Existing Skills

```bash
# Always validate after changes
python skill-creator/scripts/validate_skill.py n8n-workflow-builder/

# Re-package if validation passes
python skill-creator/scripts/package_skill.py n8n-workflow-builder/
```

## Architecture Overview

### Three-Script System

The skill-creator uses three Python scripts that work together:

1. **validate_skill.py** (lines 152-177)
   - Validates name format with regex and auto-suggestion
   - Checks for invalid top-level fields (version, author, dependencies)
   - Validates description length and quality
   - Returns errors before packaging

2. **package_skill.py**
   - Creates ZIP with skill folder as root (required structure)
   - Runs validation first to prevent packaging invalid skills
   - Output: `skill-name.zip` containing `skill-name/Skill.md`

3. **test_skill.py**
   - Generates test prompts based on skill description
   - Creates validation checklist for manual testing

### Validator Evolution

The validator has been updated to catch common Claude Code upload errors:
- Name format checking (added in validate_skill.py:159-164)
- Top-level field validation (added in validate_skill.py:238-259)
- Auto-suggestion for name format (validate_skill.py:201-212)

## Package Structure Requirements

ZIP files must have this exact structure:
```
skill-name.zip
└── skill-name/
    └── Skill.md
```

NOT:
```
skill-name.zip
└── Skill.md  # Missing folder wrapper - will fail
```

The `package_skill.py` script enforces this automatically.

## Working with Templates

Templates live in `skill-creator/resources/templates/`:
- **basic-skill.md** - Minimal skill (instructions only)
- **advanced-skill.md** - Full skill with scripts/resources

When updating templates:
1. Ensure name uses lowercase-with-hyphens format
2. Don't use invalid top-level fields
3. Update both templates if changing frontmatter structure

## Updating Documentation

When modifying skill requirements:
1. Update `skill-creator/Skill.md` (quick reference)
2. Update `skill-creator/resources/REFERENCE.md` (comprehensive guide)
3. Update `README.md` (repository overview)
4. Update templates in `resources/templates/`
5. Update validator logic in `scripts/validate_skill.py`

These must stay synchronized to prevent confusion.

## Git Workflow

The repository uses simple main branch workflow. When making changes:

```bash
# Check status
git status

# Commit skill updates
git add .
git commit -m "Update skill-creator validator to catch X"

# No need to push unless sharing with others
```

## n8n-workflow-builder Skill

This skill uses MCP tools to stay current:
- `WebSearch` - Finds latest n8n documentation
- `mcp__deepwiki__ask_question` - Queries n8n repository ("n8n-io/n8n")

When updating this skill, the description determines when it's invoked. Current trigger phrases:
- "n8n workflow"
- "n8n nodes"
- "workflow automation" (may overlap with other skills)
