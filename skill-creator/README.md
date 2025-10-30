# Skill Creator

Expert tool for creating, validating, and packaging Claude Code custom skills with templates, best practices, and automation scripts.

## Overview

Skill Creator is a comprehensive skill that helps you build high-quality Claude Code skills quickly and correctly. It includes:

- **Templates** for basic and advanced skills
- **Validation** to check structure and metadata
- **Packaging** automation for correct ZIP format
- **Testing** helpers to verify skill behavior
- **Best practices** guide and examples

## Quick Start

### Using the Skill

Once uploaded to Claude Code, invoke this skill by asking:

- "Help me create a new Claude skill"
- "I want to build a skill for [purpose]"
- "Validate my skill structure"
- "How do I package my skill?"

The skill will guide you through creating, validating, and packaging your custom skill.

### Manual Usage

You can also use the included tools directly:

#### 1. Create a Skill

Start with a template:
```bash
cp resources/templates/basic-skill.md my-new-skill/Skill.md
```

Edit the YAML frontmatter and add your instructions.

#### 2. Validate Your Skill

```bash
python scripts/validate_skill.py my-new-skill/
```

This checks:
- Skill.md exists and is valid
- YAML frontmatter is correct
- Required fields present
- Description and name length
- File references validity

#### 3. Package Your Skill

```bash
python scripts/package_skill.py my-new-skill/
```

Creates `my-new-skill.zip` ready for upload.

#### 4. Generate Test Plan

```bash
python scripts/test_skill.py my-new-skill/
```

Generates test prompts and checklists.

## What's Included

### Templates

- **basic-skill.md** - Simple skill with instructions only
- **advanced-skill.md** - Full-featured skill with scripts and resources
- **metadata-examples.md** - YAML frontmatter examples

### Examples

- **example-simple.md** - Git commit message writer (simple skill)
- **example-advanced.md** - Python code analyzer (complex skill with scripts)

### Scripts

- **validate_skill.py** - Validates skill structure and metadata
- **package_skill.py** - Creates properly formatted ZIP files
- **test_skill.py** - Generates test plans and prompts

### Documentation

- **REFERENCE.md** - Comprehensive guide covering all aspects of skill creation
- **Skill.md** - Quick-start guide and instructions

## Skill Requirements

Every Claude Code skill needs:

1. **Skill.md file** with YAML frontmatter
2. **name** field (max 64 chars)
3. **description** field (max 200 chars)

Optional but recommended:
- **version** for tracking iterations
- **dependencies** for scripts
- **resources/** for additional documentation
- **scripts/** for helper scripts

## File Structure

```
skill-name/
├── Skill.md              # Required: Main skill definition
├── README.md             # Optional: Documentation
├── resources/            # Optional: Additional docs
│   ├── REFERENCE.md
│   └── examples/
└── scripts/              # Optional: Helper scripts
    ├── helper.py
    └── requirements.txt
```

## ZIP Packaging

Skills must be packaged with the skill folder as root:

```
skill-name.zip
└── skill-name/
    ├── Skill.md
    └── ...
```

Use `package_skill.py` to ensure correct structure.

## Best Practices

1. **Single Responsibility** - One skill, one workflow
2. **Clear Description** - Use action verbs and domain keywords
3. **Specific Instructions** - Step-by-step guidance for Claude
4. **Include Examples** - Show expected behavior
5. **Validate Before Upload** - Run validation script
6. **Test Thoroughly** - Test positive and negative cases

## Common Issues

### Skill Not Invoked

**Problem:** Claude doesn't use your skill when expected

**Solutions:**
- Make description more specific
- Add action verbs (analyze, generate, etc.)
- Include domain keywords
- Test with varied phrasings

### Validation Errors

**Problem:** Validation script reports errors

**Common fixes:**
- Ensure `---` delimiters around YAML
- Check description length (≤200 chars)
- Verify all required fields present
- Fix file references

### Packaging Errors

**Problem:** ZIP file doesn't work

**Solution:**
- Use `package_skill.py` script
- Verify structure: `skill-name.zip/skill-name/Skill.md`
- Don't nest extra folders

## Dependencies

Scripts require Python 3.8+. No additional packages needed for the core tools.

## Version

Current version: 1.0.0

## Contributing

To improve this skill:
1. Test with your use cases
2. Report issues or suggestions
3. Share successful skill examples
4. Contribute additional templates

## Resources

- [Claude Code Documentation](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
- See `resources/REFERENCE.md` for comprehensive guide
- Check `resources/examples/` for working examples
- Review `resources/templates/` for starting points

## License

MIT License - Feel free to use and modify

## Support

For issues or questions:
1. Check `resources/REFERENCE.md`
2. Run validation script
3. Review examples
4. Test with provided test script
