# Claude Skills: Comprehensive Reference Guide

This document provides in-depth information about creating, structuring, and optimizing Claude Code custom skills.

## Table of Contents

1. [Understanding Skills](#understanding-skills)
2. [Structure & Metadata](#structure--metadata)
3. [Writing Effective Descriptions](#writing-effective-descriptions)
4. [File Organization](#file-organization)
5. [Advanced Features](#advanced-features)
6. [Testing & Iteration](#testing--iteration)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

## Understanding Skills

### What Are Skills?

Claude Code skills are reusable tools that extend Claude's capabilities for specific workflows. Each skill:
- Contains instructions that Claude follows when invoked
- Is automatically selected based on its description
- Can include helper scripts and reference materials
- Works alongside other skills seamlessly

### When to Create a Skill

Create a skill when you have:
- A **repeatable workflow** you use frequently
- **Domain-specific knowledge** Claude should apply
- **Complex multi-step processes** that need guidance
- **Specialized tools or scripts** that need context

### When NOT to Create a Skill

Avoid creating skills for:
- One-time tasks or ad-hoc requests
- General-purpose capabilities Claude already has
- Tasks requiring real-time interaction or decision-making
- Workflows that change frequently

## Structure & Metadata

### Required File Structure

Every skill MUST have this minimum structure:

```
skill-name/
└── Skill.md
```

The `Skill.md` file must begin with YAML frontmatter.

### YAML Frontmatter

#### Required Fields

```yaml
---
name: skill-name-here
description: What this skill does and when to use it.
---
```

**name** (required)
- Type: String
- Format: **lowercase letters, numbers, and hyphens only**
- Max length: 64 characters
- Purpose: Unique identifier for the skill
- Examples: `python-security-analyzer`, `api-doc-generator`, `code-reviewer`
- Invalid: `Python Security`, `API_Generator`, `My Skill!`
- Note: You can use a human-readable title in the markdown heading (# Your Skill Title)

**description** (required)
- Type: String
- Max length: 200 characters
- Purpose: **This is how Claude decides when to invoke your skill**
- Critical: Must be specific and action-oriented
- Examples: See "Writing Effective Descriptions" section

#### Optional Fields

```yaml
---
name: advanced-skill
description: Does amazing things.
license: MIT
allowed-tools:
  - WebSearch
  - WebFetch
metadata:
  version: 1.0.0
  author: Your Name
---
```

**license** (optional)
- Type: String
- Purpose: Specify the license for your skill
- Examples: "MIT", "Apache-2.0", "GPL-3.0"

**allowed-tools** (optional)
- Type: Array of strings
- Purpose: Specify which tools the skill is allowed to use
- Examples: WebSearch, WebFetch, Bash, Read, Write, etc.

**metadata** (optional)
- Type: Object
- Purpose: Store additional metadata about the skill
- Common fields:
  - `version`: Semantic versioning (e.g., "1.0.0")
  - `author`: Creator of the skill
  - `dependencies`: Required packages (document in skill body or README)
  - Any other custom metadata you want to track

### Markdown Body

After the frontmatter, include:

1. **Overview**: What the skill does
2. **Instructions**: Step-by-step guidance for Claude
3. **Examples**: Sample inputs/outputs
4. **File References**: How to use included resources
5. **Script Usage**: How to invoke helper scripts

Example structure:

```markdown
---
name: my-skill
description: Does specific things.
---

# My Skill

This skill helps with [specific task].

## Instructions

When invoked:
1. First, do this
2. Then, do that
3. Finally, check this

## Using Resources

Reference the detailed information in `resources/REFERENCE.md` when...

## Running Scripts

Execute `scripts/helper.py` to...
```

## Writing Effective Descriptions

The description is THE MOST IMPORTANT part of your skill. Claude uses it to decide when to invoke your skill.

### Anatomy of a Good Description

**Formula**: [Action verb] + [What it affects] + [Optional: how/why/when]

### ✅ Good Examples

1. **Specific with clear trigger words:**
   > "Analyzes Python codebases for security vulnerabilities, identifies risks, and suggests remediation steps."

2. **Domain and action clear:**
   > "Generates comprehensive API documentation from OpenAPI/Swagger specs with examples and error codes."

3. **Multiple related actions:**
   > "Refactors JavaScript code for performance, converts to modern ES6+ syntax, and optimizes bundle size."

4. **Clear use case:**
   > "Reviews pull requests for code quality, tests coverage, and suggests improvements following team standards."

### ❌ Bad Examples

1. **Too generic:**
   > "A helpful tool for working with code."
   - Why: No specific action, could apply to anything

2. **Too vague:**
   > "Helps improve your programs."
   - Why: No domain, no specific trigger

3. **Missing action:**
   > "Tool for databases."
   - Why: What does it DO with databases?

4. **Overly broad:**
   > "Complete solution for all your development needs."
   - Why: Skills should be focused, not comprehensive

### Description Writing Checklist

- [ ] Contains specific action verbs (analyze, generate, refactor, validate, etc.)
- [ ] Mentions the domain or technology (Python, API, database, etc.)
- [ ] Under 200 characters
- [ ] Would trigger on relevant user prompts
- [ ] Wouldn't trigger on irrelevant prompts
- [ ] Distinguishes this skill from others

### Testing Your Description

Ask yourself:
1. If I said "[task]", would this description match? (Should match)
2. If I said "[unrelated task]", would this description match? (Should NOT match)

Example:
- Skill: "Analyzes Python code for security vulnerabilities"
- Prompt: "Check my Python app for security issues" → ✅ Should match
- Prompt: "Write me a Python script" → ❌ Should NOT match

## File Organization

### Minimal Skill (Documentation Only)

```
simple-skill/
└── Skill.md
```

Best for:
- Instruction-only skills
- Knowledge or guidelines
- Simple workflows without code

### Standard Skill (With Resources)

```
standard-skill/
├── Skill.md
└── resources/
    ├── REFERENCE.md      # Detailed documentation
    ├── guidelines.md     # Additional guidelines
    └── examples.md       # More examples
```

Best for:
- Skills with extensive documentation
- Complex procedures needing reference
- Skills with multiple sub-workflows

### Advanced Skill (With Scripts)

```
advanced-skill/
├── Skill.md
├── resources/
│   └── REFERENCE.md
└── scripts/
    ├── analyzer.py
    ├── generator.js
    └── requirements.txt
```

Best for:
- Skills that need computation
- Data processing or transformation
- Integration with external tools
- Complex validation or analysis

### Full-Featured Skill

```
full-skill/
├── Skill.md
├── README.md            # Skill documentation for users
├── resources/
│   ├── REFERENCE.md     # Comprehensive guide
│   ├── templates/       # Reusable templates
│   │   └── template.md
│   └── examples/        # Working examples
│       └── example.json
├── scripts/
│   ├── main.py
│   ├── utils.py
│   ├── requirements.txt
│   └── package.json
└── tests/               # Optional: test files
    └── test_main.py
```

## Advanced Features

### Using Helper Scripts

#### Python Scripts

**In Skill.md:**
```markdown
To analyze the code, run:
```bash
cd scripts && python analyzer.py <file-path>
```

Check `scripts/requirements.txt` for dependencies.
```

**Dependencies documentation:**
Document required packages in your skill's markdown body, README, or in a `requirements.txt` file:
```
# scripts/requirements.txt
pandas>=1.5.0
numpy>=1.20.0
requests>=2.28.0
```

You can also document dependencies in metadata:
```yaml
---
name: my-skill
description: Does things.
metadata:
  dependencies: "python>=3.8, pandas>=1.5.0, numpy>=1.20.0"
---
```

#### JavaScript/Node.js Scripts

**In Skill.md:**
```markdown
To process the data, run:
```bash
cd scripts && node processor.js <input-file>
```

Install dependencies: `npm install`
```

**Dependencies documentation:**
Include a `package.json` file in your scripts directory or document in metadata:
```yaml
---
name: my-skill
description: Does things.
metadata:
  dependencies: "node>=18.0.0, axios>=1.0.0, lodash>=4.17.0"
---
```

### Using Reference Materials

Reference documents provide Claude with extensive information without cluttering Skill.md.

**Best practices:**
1. Keep Skill.md concise (overview + instructions)
2. Move detailed documentation to resources/REFERENCE.md
3. Reference the document explicitly in Skill.md:
   ```markdown
   For detailed information about [topic], see `resources/REFERENCE.md`.
   ```

### Multi-File Skills

For complex skills with multiple components:

```
complex-skill/
├── Skill.md             # Main instructions
├── resources/
│   ├── REFERENCE.md     # General reference
│   ├── api-guide.md     # Specific topic guide
│   ├── patterns.md      # Patterns and examples
│   └── troubleshooting.md
```

Reference specific files in instructions:
```markdown
- For API usage, see `resources/api-guide.md`
- For common patterns, see `resources/patterns.md`
- If issues arise, check `resources/troubleshooting.md`
```

## Testing & Iteration

### Pre-Upload Testing

#### 1. Validate Structure
```bash
python validate_skill.py your-skill/
```

Check:
- [ ] YAML frontmatter is valid
- [ ] Required fields present
- [ ] Description ≤ 200 chars
- [ ] Name ≤ 64 chars
- [ ] File references are valid

#### 2. Review Clarity

Ask someone to:
- Read your Skill.md
- Explain what the skill does
- Suggest when they'd use it

If they're confused, clarify your instructions.

#### 3. Test Example Prompts

Create 5-10 prompts that should trigger your skill:
- Vary the wording
- Use synonyms
- Try different phrasings

Example for "Python Security Analyzer":
- "Check my Python code for security issues"
- "Scan this script for vulnerabilities"
- "Is my Python app secure?"
- "Find security problems in this code"

### Post-Upload Testing

#### 1. Enable the Skill
Settings > Capabilities > Enable your skill

#### 2. Test with Real Prompts
Try your prepared test prompts and observe:
- Does Claude invoke the skill?
- Does it use it correctly?
- Are the outputs as expected?

#### 3. Review Claude's Reasoning
Check if Claude explains why it chose your skill. This reveals:
- What triggered the invocation
- How Claude interpreted the description
- Whether the match was appropriate

#### 4. Test Edge Cases

**Positive tests** (should invoke):
- Direct requests matching description
- Synonymous phrasings
- Implicit requests (e.g., "Is this code safe?" for security skill)

**Negative tests** (should NOT invoke):
- Unrelated requests
- Partially related but different domain
- General requests that don't need the skill

### Iteration Based on Testing

**If skill isn't invoked when it should be:**
- Add more trigger words to description
- Make description more specific to the use case
- Include synonyms or related terms

**If skill is invoked when it shouldn't be:**
- Narrow the description
- Remove generic terms
- Add domain-specific qualifiers

**If instructions are unclear:**
- Add more examples
- Break down complex steps
- Reference additional documentation

## Best Practices

### 1. Single Responsibility Principle

**Do:**
- "Analyzes Python code for security vulnerabilities"
- "Generates API documentation from OpenAPI specs"

**Don't:**
- "Complete development toolkit for all languages and tasks"

### 2. Clear and Actionable Instructions

**Do:**
```markdown
When analyzing code:
1. Read the provided code files
2. Identify security vulnerabilities using common patterns
3. Categorize by severity (Critical, High, Medium, Low)
4. Suggest specific remediation steps
5. Provide code examples for fixes
```

**Don't:**
```markdown
Look at the code and find problems.
```

### 3. Progressive Disclosure

**Skill.md:** Quick overview + basic instructions
**resources/REFERENCE.md:** Detailed information + edge cases
**resources/examples/:** Working examples

### 4. Version Control

Use semantic versioning in metadata:
```yaml
---
name: my-skill
description: Does things.
metadata:
  version: 1.0.0
---
```

Version numbering:
- **MAJOR** (1.0.0 → 2.0.0): Breaking changes to structure or behavior
- **MINOR** (1.0.0 → 1.1.0): New features, backwards compatible
- **PATCH** (1.0.0 → 1.0.1): Bug fixes, clarifications

### 5. Documentation

Include a README.md with:
- What the skill does
- How to use it
- Dependencies and setup
- Example prompts
- Changelog

### 6. Naming Conventions

**Files:**
- Skill.md (exactly this name and case)
- Use lowercase with hyphens: `my-skill/`
- Scripts: descriptive names like `analyzer.py`, not `script1.py`

**Metadata:**
- name: lowercase-with-hyphens format (max 64 chars)
- description: Action-oriented, specific (max 200 chars)
- metadata.version: Semantic versioning if tracking versions
- license: Standard license identifiers (MIT, Apache-2.0, etc.)

## Troubleshooting

### Skill Not Being Invoked

**Problem:** Skill never triggers when expected

**Solutions:**
1. Make description more specific with action verbs
2. Include keywords that match typical user prompts
3. Test with varied phrasings
4. Ensure description isn't too narrow or too broad
5. Check that skill is enabled in Settings

### Skill Invoked at Wrong Times

**Problem:** Skill triggers when it shouldn't

**Solutions:**
1. Narrow description scope
2. Add domain-specific qualifiers
3. Remove generic terms
4. Test negative cases

### Packaging Errors

**Problem:** ZIP file doesn't work when uploaded

**Solutions:**
1. Ensure structure is: `skill-name.zip/skill-name/Skill.md`
2. NOT: `skill-name.zip/Skill.md` (missing folder)
3. NOT: `skill-name.zip/parent/skill-name/Skill.md` (extra nesting)
4. Use provided `package_skill.py` script for correct structure

### Validation Failures

**Problem:** Validator reports errors

**Common issues:**
- Missing `---` delimiters around YAML
- Name contains uppercase letters, spaces, or special characters (must be lowercase-with-hyphens)
- Description exceeds 200 characters
- Name exceeds 64 characters
- Invalid YAML syntax (check indentation, colons, quotes)
- File references pointing to non-existent files

### Script Execution Issues

**Problem:** Helper scripts fail to run

**Solutions:**
1. Verify dependencies are listed in frontmatter
2. Check file paths in instructions
3. Ensure scripts have correct permissions
4. Test scripts independently before packaging
5. Include error handling in scripts

### Claude Not Following Instructions

**Problem:** Skill invokes but Claude doesn't follow the workflow

**Solutions:**
1. Break instructions into numbered steps
2. Use clear, imperative language
3. Provide examples of expected behavior
4. Move complex details to REFERENCE.md
5. Test instructions with varied inputs

## Additional Resources

### Example Skills to Study

Look at well-designed skills in the community:
- Simple instruction-only skills
- Skills with helper scripts
- Multi-file reference skills

### Community Best Practices

- Keep skills focused and specific
- Test extensively before sharing
- Version your skills properly
- Document dependencies clearly
- Include helpful examples

### Getting Help

- Review this reference guide
- Check the troubleshooting section
- Test with validation scripts
- Iterate based on feedback

## Quick Reference Card

### File Must-Haves
- [ ] Skill.md with YAML frontmatter
- [ ] name field (≤64 chars)
- [ ] description field (≤200 chars)
- [ ] Clear instructions in markdown body

### Description Checklist
- [ ] Specific action verbs
- [ ] Domain/technology mentioned
- [ ] Under 200 characters
- [ ] Distinguishes from other skills
- [ ] Matches expected user prompts

### Pre-Upload Checklist
- [ ] Structure validated
- [ ] Metadata correct
- [ ] File references valid
- [ ] Instructions clear
- [ ] Example prompts tested
- [ ] Packaged correctly

### Post-Upload Checklist
- [ ] Skill enabled
- [ ] Positive test cases pass
- [ ] Negative test cases pass
- [ ] Claude's reasoning makes sense
- [ ] Outputs are correct
- [ ] Documentation is clear
