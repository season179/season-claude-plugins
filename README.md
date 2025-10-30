# Claude Skills Repository

A comprehensive collection of custom skills for Claude Code, starting with the Skill Creator - a meta-skill that helps you build more skills.

## What Are Claude Code Skills?

Claude Code skills are reusable tools that extend Claude's capabilities for specific workflows. Each skill:
- Contains instructions Claude follows when invoked
- Is automatically selected based on its description
- Can include helper scripts and reference materials
- Works seamlessly with other skills

## Available Skills

### Skill Creator

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
   - Fill in YAML frontmatter (name, description, version)
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
- **name** field (max 64 characters)
- **description** field (max 200 characters)

Example:
```yaml
---
name: My Awesome Skill
description: Does specific things with particular technologies and use cases.
version: 1.0.0
---

# Instructions for Claude

When this skill is invoked:
1. Do this
2. Then this
3. Finally this
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
- Required fields present
- Field length constraints
- Description quality
- File references

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

Check YAML syntax, field lengths, and required fields.

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

### 1.0.0 (2025-01-30)
- Initial release
- Added Skill Creator skill
- Validation, packaging, and testing tools
- Templates and examples
- Comprehensive documentation

---

Built with Claude Code | [Documentation](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
