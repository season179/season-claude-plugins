# CLAUDE.md

Guidance for Claude Code when working with this plugin marketplace repository.

## Repository Structure

```
season-claude-plugins/
├── .claude-plugin/
│   └── marketplace.json    # Plugin registry
├── <plugin-name>/
│   ├── SKILL.md            # Plugin definition (required)
│   └── references/         # Supporting docs (optional)
└── README.md               # User-facing docs
```

## Plugin Format

Each plugin requires a `SKILL.md` (or `Skill.md`) with YAML frontmatter:

```yaml
---
name: plugin-name          # Required: lowercase-with-hyphens only
description: Brief desc    # Required: max 200 chars, triggers invocation
---

# Plugin Title

Instructions for Claude when this plugin is invoked.
```

**Name validation**: `^[a-z0-9-]+$` (no spaces, underscores, or capitals)

## Adding a Plugin

1. Create folder: `new-plugin-name/`
2. Add `SKILL.md` with frontmatter
3. Add entry to [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json):
   ```json
   {
     "name": "new-plugin-name",
     "source": "./new-plugin-name",
     "description": "...",
     "author": { "name": "Season Saw" },
     "keywords": ["..."],
     "category": "..."
   }
   ```

## Modifying Plugins

- Edit the `SKILL.md` in the plugin folder
- Update `marketplace.json` if name/description changes
- Keep README.md plugin list in sync

## Categories

Used in marketplace.json: `ai`, `design`, `developer-tools`, `automation`, `observability`, `architecture`, `productivity`, `documentation`

## Reference

- [Plugin Marketplaces Docs](https://code.claude.com/docs/en/plugin-marketplaces)
- [README.md](README.md) - Plugin list for users
