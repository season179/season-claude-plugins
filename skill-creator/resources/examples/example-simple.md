---
name: Git Commit Message Writer
description: Generates clear, conventional commit messages following best practices and team standards.
version: 1.0.0
---

# Git Commit Message Writer

This skill helps write standardized, informative Git commit messages following conventional commit format and best practices.

## Purpose

Ensures consistent, meaningful commit messages across the codebase that:
- Follow conventional commit format
- Clearly describe what changed and why
- Are searchable and useful for git history
- Enable automated changelog generation

## Instructions

When writing a commit message:

1. **Analyze the changes**: Review what files were modified and the nature of changes
   - New features
   - Bug fixes
   - Documentation updates
   - Refactoring
   - Performance improvements
   - Breaking changes

2. **Determine the type**: Use conventional commit types
   - `feat`: New feature
   - `fix`: Bug fix
   - `docs`: Documentation changes
   - `style`: Code style changes (formatting, missing semi-colons, etc.)
   - `refactor`: Code refactoring
   - `perf`: Performance improvements
   - `test`: Adding or updating tests
   - `chore`: Maintenance tasks, dependency updates

3. **Structure the message**:
   ```
   <type>(<scope>): <subject>

   <body>

   <footer>
   ```

4. **Write the subject line**:
   - Start with type and optional scope: `feat(auth):` or `fix:`
   - Use imperative mood: "add" not "added" or "adds"
   - Keep under 50 characters
   - Don't end with a period
   - Be specific and descriptive

5. **Add body if needed** (optional but recommended for non-trivial changes):
   - Explain what and why, not how
   - Wrap at 72 characters
   - Separate from subject with blank line
   - Can use bullet points with `-` or `*`

6. **Add footer if applicable**:
   - Reference issues: `Fixes #123` or `Closes #456`
   - Note breaking changes: `BREAKING CHANGE: description`

## Examples

### Simple Feature Addition

```
feat(auth): add password reset functionality

Allow users to reset their forgotten passwords via email.
Includes rate limiting to prevent abuse.

Closes #245
```

### Bug Fix

```
fix(api): prevent null pointer exception in user lookup

Handle case where user ID doesn't exist in database.
Returns 404 instead of 500 error.

Fixes #312
```

### Documentation Update

```
docs(readme): update installation instructions

Add troubleshooting section for common setup issues
and clarify Python version requirements.
```

### Refactoring

```
refactor(database): simplify query builder logic

Extract common query patterns into reusable methods.
No functional changes to API.
```

### Breaking Change

```
feat(api): change response format to JSON:API spec

Update all API responses to follow JSON:API specification
for better consistency and tooling support.

BREAKING CHANGE: Response structure has changed. Clients
must update to parse new format. Migration guide in docs.

Closes #567
```

## Key Points

- **Be specific**: "fix login bug" → "fix(auth): prevent session timeout on refresh"
- **Use imperative mood**: "add feature" not "added feature"
- **Explain why**: Don't just describe what changed, explain the motivation
- **Reference issues**: Always link to related issues or tickets
- **Keep subject short**: Under 50 chars for better readability in git log
- **Wrap body**: At 72 chars for terminal compatibility

## Anti-Patterns to Avoid

❌ "Fixed stuff"
❌ "WIP"
❌ "Update file.js"
❌ "Various changes"
❌ "fix bugs"

✅ "fix(parser): handle malformed JSON input"
✅ "feat(ui): add dark mode toggle to settings"
✅ "refactor(api): extract validation to middleware"

## Tips

- Review `git diff --staged` before writing
- Think about someone reading this in 6 months
- Consider changelog generation tools
- Be consistent with team conventions
- Use scope to indicate affected area
