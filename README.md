# Claude Skills Repository

A comprehensive collection of custom skills for Claude Code, starting with the Skill Creator - a meta-skill that helps you build more skills.

## What Are Claude Code Skills?

Claude Code skills are reusable tools that extend Claude's capabilities for specific workflows. Each skill:
- Contains instructions Claude follows when invoked
- Is automatically selected based on its description
- Can include helper scripts and reference materials
- Works seamlessly with other skills

## Available Skills

### 1. Skill Creator

**Expert tool for creating, validating, and packaging Claude Code custom skills.**

The Skill Creator skill includes:
- Templates for basic and advanced skills
- Validation tools to check structure and metadata
- Packaging automation for correct ZIP format
- Testing helpers to verify skill behavior
- Comprehensive best practices guide
- Working examples

[View Documentation](skill-creator/README.md)

**Quick Start:**
```bash
# Validate a skill
python skill-creator/scripts/validate_skill.py my-skill/

# Package for upload
python skill-creator/scripts/package_skill.py my-skill/

# Generate test plan
python skill-creator/scripts/test_skill.py my-skill/
```

### 2. n8n Workflow Builder

**Helps build n8n workflows by selecting optimal nodes, configuring them correctly, and providing up-to-date documentation.**

This skill:
- Always fetches the latest n8n documentation
- Recommends the best nodes for your workflow requirements
- Provides detailed configuration instructions
- Includes n8n expression syntax guidance
- Suggests workflow patterns and best practices

**Package**: [n8n-workflow-builder.zip](n8n-workflow-builder.zip)

**Usage**: Just ask about building n8n workflows, and the skill will automatically be invoked!

## Repository Structure

```
claude-skills/
├── README.md                    # This file
└── skill-creator/               # Skill Creator skill
    ├── Skill.md                 # Main skill definition
    ├── README.md                # Skill documentation
    ├── resources/               # Templates, examples, reference
    │   ├── REFERENCE.md         # Comprehensive guide
    │   ├── templates/           # Starting templates
    │   │   ├── basic-skill.md
    │   │   ├── advanced-skill.md
    │   │   └── metadata-examples.md
    │   └── examples/            # Working examples
    │       ├── example-simple.md
    │       └── example-advanced.md
    └── scripts/                 # Automation tools
        ├── validate_skill.py    # Validation tool
        ├── package_skill.py     # Packaging tool
        └── test_skill.py        # Testing helper
```

## Getting Started

### Using Skills

1. **Download the skill** you want to use
2. **Package it** (if not already packaged):
   ```bash
   python skill-creator/scripts/package_skill.py skill-name/
   ```
3. **Upload to Claude Code**:
   - Open Claude Code Settings > Capabilities
   - Upload the ZIP file
   - Enable the skill

### Creating New Skills

Use the Skill Creator skill:

1. **Start from a template**:
   ```bash
   cp skill-creator/resources/templates/basic-skill.md my-skill/Skill.md
   ```

2. **Edit the skill**:
   - Fill in YAML frontmatter (name in lowercase-with-hyphens, description)
   - Add instructions for Claude
   - Include examples

3. **Validate**:
   ```bash
   python skill-creator/scripts/validate_skill.py my-skill/
   ```

4. **Package**:
   ```bash
   python skill-creator/scripts/package_skill.py my-skill/
   ```

5. **Test** after uploading to Claude Code

## Skill Requirements

Every Claude Code skill must have:

- **Skill.md file** with YAML frontmatter
- **name** field: lowercase-with-hyphens format only (max 64 chars)
  - ✅ Valid: `my-awesome-skill`, `python-analyzer`, `api-helper`
  - ❌ Invalid: `My Awesome Skill`, `my_skill`, `MySkill`
- **description** field: specific, action-oriented (max 200 chars)

**Minimal Example:**
```yaml
---
name: my-awesome-skill
description: Does specific things with particular technologies and use cases.
---

# My Awesome Skill

When this skill is invoked:
1. Do this
2. Then this
3. Finally this
```

**With Optional Fields:**
```yaml
---
name: my-awesome-skill
description: Does specific things with particular technologies and use cases.
license: MIT
metadata:
  version: 1.0.0
  author: Your Name
---
```

## Best Practices

1. **Single Responsibility**: Each skill should focus on one workflow
2. **Clear Descriptions**: Use action verbs and domain keywords
3. **Specific Instructions**: Provide step-by-step guidance
4. **Include Examples**: Show expected behavior
5. **Validate First**: Always run validation before packaging
6. **Test Thoroughly**: Test with multiple prompts

## Tools

### Validation Tool

Checks skill structure, metadata, and best practices:

```bash
python skill-creator/scripts/validate_skill.py <skill-directory>
```

Validates:
- Skill.md exists and is valid
- YAML frontmatter correct
- Name format (lowercase-with-hyphens only)
- Required fields present
- Field length constraints
- Description quality
- File references
- No invalid top-level fields (version, author, dependencies)

### Packaging Tool

Creates properly formatted ZIP files:

```bash
python skill-creator/scripts/package_skill.py <skill-directory> [--output name.zip]
```

Ensures correct structure:
```
skill-name.zip
└── skill-name/
    ├── Skill.md
    └── ...
```

### Testing Tool

Generates test plans and prompts:

```bash
python skill-creator/scripts/test_skill.py <skill-directory> [--output test-plan.md]
```

Provides:
- Test prompts (positive and negative)
- Pre/post-upload checklists
- Testing tips
- Iteration guidance

## Contributing Skills

Want to add your skill to this repository?

1. **Create your skill** using the Skill Creator
2. **Validate** with the validation tool
3. **Test thoroughly**
4. **Document** with a README
5. **Submit** via pull request

Include:
- Skill directory with all files
- README with usage instructions
- Examples (if applicable)
- Version history

## Resources

### Documentation

- **Skill Creator Reference**: [skill-creator/resources/REFERENCE.md](skill-creator/resources/REFERENCE.md)
- **Official Docs**: [Claude Code Skills Documentation](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)

### Templates

- **Basic Skill**: [skill-creator/resources/templates/basic-skill.md](skill-creator/resources/templates/basic-skill.md)
- **Advanced Skill**: [skill-creator/resources/templates/advanced-skill.md](skill-creator/resources/templates/advanced-skill.md)
- **Metadata Examples**: [skill-creator/resources/templates/metadata-examples.md](skill-creator/resources/templates/metadata-examples.md)

### Examples

- **Simple Skill**: [skill-creator/resources/examples/example-simple.md](skill-creator/resources/examples/example-simple.md) (Git commit message writer)
- **Advanced Skill**: [skill-creator/resources/examples/example-advanced.md](skill-creator/resources/examples/example-advanced.md) (Python code analyzer)

## Requirements

- Python 3.8+ (for automation scripts)
- Claude Code (to use the skills)

## Common Issues

### Skill Not Invoked

Make description more specific with action verbs and domain keywords.

### Validation Errors

Common issues:
- **Name format**: Must be lowercase-with-hyphens only
- **Invalid fields**: `version`, `author`, `dependencies` not allowed at top level (use `metadata` instead)
- **YAML syntax**: Check delimiters (`---`) and proper formatting
- **Field lengths**: Name max 64 chars, description max 200 chars

### Packaging Issues

Use `package_skill.py` to ensure correct ZIP structure.

See the [Comprehensive Reference](skill-creator/resources/REFERENCE.md) for detailed troubleshooting.

## Future Skills

This repository will grow with more skills:

- Code analyzers for different languages
- Documentation generators
- Testing assistants
- Refactoring tools
- DevOps helpers
- Security scanners

## License

MIT License - Free to use and modify

## Support

For help:
1. Check the [Comprehensive Reference](skill-creator/resources/REFERENCE.md)
2. Review [examples](skill-creator/resources/examples/)
3. Run validation tools
4. Open an issue

## Changelog

### 1.1.0 (2025-10-30)
- Added n8n Workflow Builder skill
- Fixed name format validation (must be lowercase-with-hyphens)
- Updated validator to catch invalid top-level fields
- Corrected all templates and documentation
- Improved error messages with auto-suggestions

### 1.0.0 (2025-01-30)
- Initial release
- Added Skill Creator skill
- Validation, packaging, and testing tools
- Templates and examples
- Comprehensive documentation

---

Built with Claude Code | [Documentation](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
