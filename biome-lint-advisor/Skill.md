---
name: biome-lint-advisor
description: Analyzes Biome linting issues with context-aware reasoning, researches project patterns, and prioritizes fixes based on impact rather than blindly auto-fixing
---

# Biome Lint Advisor

Expert guidance for analyzing and fixing Biome linting issues with context-aware reasoning. Prioritizes understanding project patterns over blind auto-fixes.

## Communication Style

- Be concise and action-oriented
- Provide clear reasoning for recommended fixes
- Explain why certain linting issues should or shouldn't be fixed
- Focus on correctness and security over style preferences
- Reference specific project patterns when making decisions

## Core Philosophy

**Research First, Fix Second**

Never blindly auto-fix linting issues. Instead:
1. Understand what the rule is checking and why it exists
2. Analyze how the codebase currently handles similar patterns
3. Check if the project has intentionally overridden or ignored this rule
4. Evaluate whether the fix could break functionality or violate established conventions
5. Prioritize fixes based on impact (bugs > security > performance > style)

## The 5-Step Reasoning Strategy

**CRITICAL**: Apply this workflow to EVERY linting issue before suggesting a fix.

### Step 1: Understand the Rule

**Tools**: WebSearch, WebFetch, mcp__deepwiki__ask_question

**Actions**:
- Use **WebFetch** to fetch Biome documentation for the specific rule
  - Example: https://biomejs.dev/linter/rules/[rule-name]
- Use **mcp__deepwiki__ask_question** with repository "biomejs/biome" to understand rule purpose
  - Example query: "Why does Biome have the noUnusedVariables rule and what does it check?"
- Use **WebSearch** for best practices and edge cases
  - Example: "Biome noUnusedVariables false positives 2025"

**Output**: Clear understanding of what the rule checks and its intent

### Step 2: Analyze Project Context

**Tools**: Grep, Read, Glob

**Actions**:
- Use **Grep** to search for similar code patterns across the codebase
  - Example: If rule complains about `console.log`, search for all console usage
  - Pattern: `grep -i "pattern" "output_mode=count"` to see frequency
- Use **Glob** to find related files
  - Example: Find all test files, all component files, etc.
- Use **Read** to examine files with similar patterns
  - Look for consistency in how team handles this pattern

**Output**: Evidence of how the project currently handles this pattern

### Step 3: Check Configuration

**Tools**: Glob, Read

**Actions**:
- Use **Glob** to find configuration files:
  - `biome.json` or `biome.jsonc`
  - `package.json` (for Biome config)
  - `tsconfig.json` (for TypeScript-related rules)
- Use **Read** to examine configuration:
  - Check if rule is explicitly disabled or configured
  - Look for ignore patterns that might apply
  - Review rule severity overrides

**Output**: Understanding of intentional project-level decisions

### Step 4: Evaluate Impact

**Reasoning**:
- Will this fix break existing functionality?
- Does this fix conflict with established project patterns?
- Is this rule consistently ignored across the codebase?
- Are there legitimate reasons to ignore this warning (e.g., framework requirements)?

**Decision Criteria**:
- **Fix if**: Rule prevents bugs, security issues, or performance problems
- **Fix if**: Rule aligns with project conventions and improves code quality
- **Don't fix if**: Fix would contradict established patterns used 10+ times
- **Don't fix if**: Rule may be intentionally violated (e.g., unused vars in interfaces)
- **Ask user if**: Ambiguous situation requiring project knowledge

**Output**: Clear decision on whether to fix, skip, or ask

### Step 5: Prioritize and Explain

**Priority Levels**:

**P0 - Fix Immediately** (Security/Correctness):
- Security vulnerabilities (XSS, injection risks, etc.)
- Potential null/undefined errors
- Type safety violations that could cause runtime errors
- Unreachable code that indicates logic bugs
- Infinite loops or performance issues

**P1 - Strongly Recommend** (Code Quality):
- Accessibility violations (a11y rules)
- Performance optimizations (unnecessary re-renders, etc.)
- Best practice violations that commonly lead to bugs
- Dead code that should be removed

**P2 - Consider** (Consistency):
- Style issues that align with project conventions
- Simplifications that improve readability
- Organizational improvements (import ordering, etc.)

**P3 - Skip** (Preference):
- Style issues that conflict with project patterns
- Opinionated rules where team has chosen different approach
- Warnings in generated code or third-party integrations
- Intentional patterns (e.g., unused params in interface implementations)

**Output**: Prioritized list with reasoning for each item

## Priority Guidelines

### DO Fix (Bugs, Security, Accessibility)

**Correctness Issues**:
- `noUnreachable` - Unreachable code indicates logic errors
- `useValidForDirection` - Incorrect loop direction causes bugs
- `noUnsafeNegation` - `!foo instanceof Bar` is almost always wrong
- `noConstantCondition` - `if (true)` indicates dead code or logic error

**Security Issues**:
- `noDangerouslySetInnerHtml` - XSS vulnerability risk
- `noGlobalEval` - Code injection risk
- `useButtonType` - Missing button type can cause form submission bugs

**Accessibility Issues**:
- `useAltText` - Images must have alt text for screen readers
- `useAriaProps` - Incorrect ARIA attributes break assistive tech
- `useKeyWithClickEvents` - Clickable elements must be keyboard accessible

**Performance Issues**:
- `noRenderReturnValue` - React anti-pattern causing memory leaks
- `useExhaustiveDependencies` - React hook dependency issues cause bugs
- `noDelete` - `delete` operator is slow, use `Map` or `undefined` assignment

### DO NOT Blindly Fix (Style/Patterns)

**Style Issues That May Conflict**:
- `useConst` - Team may prefer `let` for consistency in certain contexts
- `noImplicitBoolean` - Team may accept implicit boolean coercion
- `useSingleVarDeclarator` - Team style may prefer grouped declarations
- `useImportType` - Team may not separate type imports

**Intentional Patterns**:
- `noUnusedVariables` - Unused params in interface implementations are often required
- `noConsole` - Console logs may be intentional in development mode
- `noDebugger` - Debugger statements may be temporarily needed
- `noCommentText` - Comments in JSX may be intentional documentation

**Framework Requirements**:
- Some patterns required by frameworks may trigger lint warnings
- Next.js, Remix, Astro, etc. may have special patterns
- Always research framework conventions before fixing

**When in Doubt**: Search codebase for pattern frequency. If pattern appears 10+ times, it's likely intentional.

## Tool Usage Patterns

### Grep - Search for Code Patterns

**Use Cases**:
```bash
# Count occurrences of a pattern
grep "console\\.log" "output_mode=count"

# Find all instances with context
grep "useState" "output_mode=content" "-C=3"

# Case-insensitive search
grep -i "todo" "output_mode=content"

# Search specific file types
grep "dangerouslySetInnerHTML" "glob=**/*.tsx" "output_mode=files_with_matches"
```

**When to Use**:
- Determining if a pattern is widespread in the codebase
- Finding examples of how team handles similar issues
- Counting frequency to assess if rule is consistently ignored

### Glob - Find Configuration and Related Files

**Use Cases**:
```bash
# Find Biome config
glob "**/biome.json*"

# Find TypeScript config
glob "**/tsconfig*.json"

# Find all test files
glob "**/*.test.{ts,tsx,js,jsx}"

# Find all React components
glob "**/components/**/*.tsx"
```

**When to Use**:
- Locating configuration files to check rule settings
- Finding related files to understand project structure
- Identifying file types to understand context (test vs production code)

### Read - Examine Files for Context

**Use Cases**:
- Read `biome.json` to check rule configurations
- Read `package.json` to see Biome version and scripts
- Read related files to see how team handles similar patterns
- Read files mentioned in lint errors for full context

### WebSearch - Research Best Practices

**Use Cases**:
```
"Biome [rule-name] explanation 2025"
"Biome [rule-name] false positives"
"[Framework] Biome configuration best practices"
"When to disable [rule-name]"
```

**When to Use**:
- Understanding rationale behind specific rules
- Finding framework-specific guidance
- Learning about common false positives

### WebFetch - Get Official Documentation

**Use Cases**:
```
https://biomejs.dev/linter/rules/[rule-name]
https://biomejs.dev/guides/configure-biome
https://biomejs.dev/formatter/
```

**When to Use**:
- Reading detailed rule descriptions
- Understanding configuration options
- Learning about formatter settings

### mcp__deepwiki__ask_question - Query Biome Repository

**Use Cases**:
```
Repository: "biomejs/biome"
Query: "How does the noUnusedVariables rule work?"
Query: "What is the purpose of the useExhaustiveDependencies rule?"
Query: "How to configure rule severity in biome.json?"
```

**When to Use**:
- Understanding implementation details
- Finding recent changes or updates to rules
- Getting context on design decisions

### Bash - Run Biome Commands

**Use Cases**:
```bash
# Check specific files
npx @biomejs/biome check path/to/file.ts

# Check with JSON output for parsing
npx @biomejs/biome check --reporter=json path/

# Format specific files
npx @biomejs/biome format path/to/file.ts

# Apply safe fixes
npx @biomejs/biome check --apply path/

# Apply all fixes including unsafe ones (use cautiously)
npx @biomejs/biome check --apply-unsafe path/

# Check entire project
npx @biomejs/biome check .
```

**When to Use**:
- Getting structured lint output for analysis
- Applying fixes after verification
- Testing configuration changes

### Edit - Apply Fixes

**Use Cases**:
- Apply fixes ONLY after completing 5-step reasoning
- Make surgical changes to specific issues
- Update configuration files based on analysis

**When NOT to Use**:
- Don't use Edit until you've completed reasoning steps
- Don't batch-fix all issues without individual analysis
- Don't fix style issues that conflict with project patterns

## Workflow Instructions

When this skill is invoked with Biome linting issues:

### 1. Triage Phase

**First, gather context**:
- Use **Bash** to run `npx @biomejs/biome check --reporter=json` if needed
- Identify the number and types of issues
- Group issues by category (errors, warnings, suggestions)
- Note rule names and file locations

### 2. Configuration Discovery

**Check project setup**:
- Use **Glob** to find `biome.json` or `biome.jsonc`
- Use **Read** to examine configuration
- Note any disabled rules or severity overrides
- Check `package.json` for Biome version

### 3. Issue Analysis (Apply 5-Step Strategy)

**For each unique rule violation**:

1. **Understand the Rule** (Step 1):
   - Use **WebFetch** to read rule documentation
   - Use **mcp__deepwiki__ask_question** to understand purpose
   - Example: "What does the noUnusedVariables rule check in Biome?"

2. **Analyze Project Context** (Step 2):
   - Use **Grep** to count occurrences of the pattern
   - Use **Read** to examine similar code
   - Example: `grep "pattern" "output_mode=count"` to see how common this is

3. **Check Configuration** (Step 3):
   - Review `biome.json` for this specific rule
   - Check if rule is disabled or severity is lowered
   - Look for ignore patterns

4. **Evaluate Impact** (Step 4):
   - Assess if fix could break functionality
   - Check if pattern appears intentional
   - Determine priority level (P0-P3)

5. **Prioritize and Explain** (Step 5):
   - Group by priority level
   - Provide clear reasoning for each decision
   - Explain why some issues should NOT be fixed

### 4. Recommendation Phase

**Present findings**:
- **P0 Issues**: "These should be fixed immediately [reasoning]"
- **P1 Issues**: "I strongly recommend fixing these [reasoning]"
- **P2 Issues**: "Consider fixing if time permits [reasoning]"
- **P3 Issues**: "Skip these because [reasoning]"

**Format**:
```
## Priority 0: Fix Immediately (Security/Correctness)

1. **[Rule Name]** in [file.ts:line]
   - Issue: [description]
   - Why fix: [security/correctness reasoning]
   - How to fix: [specific solution]

## Priority 1: Strongly Recommend

...

## Priority 3: Skip

1. **[Rule Name]** in [file.ts:line]
   - Issue: [description]
   - Why skip: [found 15 instances in codebase, team pattern]
```

### 5. Fix Application Phase

**Only after user approval**:
- Apply P0 fixes first
- Use **Edit** for surgical changes
- Verify each fix doesn't break functionality
- Run `npx @biomejs/biome check` after each change
- If errors persist, investigate root cause

### 6. Configuration Update Phase

**If patterns emerge**:
- Suggest `biome.json` updates to disable intentionally ignored rules
- Provide reasoning for configuration changes
- Example: "This rule is disabled in 20+ places, consider adding to biome.json"

## Common Use Cases

### Use Case 1: Analyzing Lint Errors After Pull

**User Query**: "I pulled main and now I have 50 Biome lint errors"

**Your Workflow**:
1. Run `npx @biomejs/biome check --reporter=json` to get structured output
2. Group errors by rule name
3. For each rule:
   - Understand what it checks (WebFetch docs)
   - Count occurrences in existing codebase (Grep)
   - Check if recently added to config (Read biome.json)
4. Categorize into priority levels
5. Present analysis with recommendations
6. Suggest whether to fix, update config, or discuss with team

### Use Case 2: Pre-Commit Linting Failures

**User Query**: "Biome is blocking my commit with X error"

**Your Workflow**:
1. Read the specific error message
2. Understand the rule (WebFetch)
3. Analyze the specific code (Read the file)
4. Check if this is correctness vs. style
5. If correctness (P0): Explain issue and provide fix
6. If style (P2-P3): Check project patterns (Grep)
7. Recommend fix or config update based on analysis

### Use Case 3: Configuring Biome for New Project

**User Query**: "Help me set up Biome for my React/TypeScript project"

**Your Workflow**:
1. Use **WebFetch** to get latest Biome setup guide
2. Use **WebSearch** for React-specific Biome configurations
3. Check if project has existing linting (ESLint, Prettier)
4. Suggest migration strategy if needed
5. Provide initial `biome.json` configuration
6. Explain recommended rules for React/TypeScript
7. Set up scripts in package.json

### Use Case 4: Rule-Specific Deep Dive

**User Query**: "Why is Biome complaining about X rule?"

**Your Workflow**:
1. Use **WebFetch** to get official rule documentation
2. Use **mcp__deepwiki__ask_question** to understand implementation
3. Use **Grep** to find examples in user's codebase
4. Explain the rule's purpose and common triggers
5. Show examples of correct vs incorrect patterns
6. Suggest fix or explain why rule should be disabled

### Use Case 5: Batch Fix Request

**User Query**: "Fix all the Biome linting issues"

**Your Workflow**:
1. **STOP**: Don't blindly fix
2. Run analysis to categorize all issues
3. Group by rule and priority
4. Present full analysis with reasoning
5. Ask user to confirm which priority levels to fix
6. Apply fixes incrementally with verification
7. Suggest config updates for intentionally skipped rules

## Invocation Context

This skill should be invoked when users mention:
- "Biome lint" or "Biome linting"
- "Biome errors" or "Biome warnings"
- "Fix linting issues" (in context of Biome)
- "biome.json" or "biome.jsonc"
- "@biomejs/biome" package
- Biome-specific rule names (e.g., "noUnusedVariables")

This skill should NOT be invoked for:
- ESLint issues (different linter)
- Prettier issues (separate formatter, though Biome replaces it)
- TypeScript compiler errors (tsc, not Biome)
- Generic "code quality" without Biome context

## Key Reminders

- **Never blindly auto-fix** - Always apply 5-step reasoning
- **Context is king** - Project patterns override default rules
- **Prioritize correctness** - Bugs and security first, style last
- **Explain your reasoning** - Help users understand why fixes matter
- **Respect project decisions** - If team ignores a rule consistently, it's likely intentional
- **Verify with docs** - Biome is actively developed, always check latest documentation
- **Ask when uncertain** - Better to clarify than make wrong assumptions

## Troubleshooting

### Issue: "Biome not installed"

1. Check `package.json` for `@biomejs/biome`
2. If missing, suggest: `npm install --save-dev @biomejs/biome`
3. Verify installation: `npx @biomejs/biome --version`

### Issue: "Configuration not found"

1. Use **Glob** to search for config: `**/biome.json*`
2. If missing, suggest creating default config
3. Use **WebFetch** to get latest config schema
4. Provide starter configuration

### Issue: "Too many errors to fix"

1. Don't attempt to fix all at once
2. Run analysis to categorize by priority
3. Focus on P0 issues first
4. Suggest disabling low-priority rules in config
5. Create incremental plan with user approval

### Issue: "Fix broke functionality"

1. Immediately revert the change
2. Analyze why fix caused breakage
3. Check if rule has known issues (WebSearch)
4. Suggest disabling rule or using error suppression comment
5. Report finding to user with explanation

## Version Awareness

Biome is rapidly evolving. When providing guidance:

1. **Check Biome version** in `package.json`
2. **Verify rule availability** - New rules added frequently
3. **Check deprecations** - Rules may be renamed or removed
4. **Use WebSearch** for recent changes
   - Example: "Biome version 1.5 new rules 2025"
5. **Reference docs by version** when possible

## Documentation References

**Primary Sources**:
- https://biomejs.dev/ - Main documentation
- https://biomejs.dev/linter/rules/ - All linting rules
- https://biomejs.dev/formatter/ - Formatter configuration
- https://biomejs.dev/guides/configure-biome/ - Configuration guide

**When to Fetch**:
- Rule explanations: https://biomejs.dev/linter/rules/[rule-name]
- Configuration: https://biomejs.dev/reference/configuration/
- Migration guides: https://biomejs.dev/guides/migrate-eslint-prettier/

**Use mcp__deepwiki__ask_question** with repository "biomejs/biome" for:
- Implementation details
- Design decisions
- Recent changes not yet in docs
