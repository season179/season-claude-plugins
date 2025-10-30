# Skill Metadata Examples

This document provides examples of well-crafted YAML frontmatter for different types of skills.

## Basic Skill (Minimal)

```yaml
---
name: Code Reviewer
description: Reviews code for quality, suggests improvements, and identifies potential bugs.
---
```

## With Version

```yaml
---
name: API Documentation Generator
description: Generates comprehensive API docs from OpenAPI specs with examples and error codes.
version: 1.0.0
---
```

## With Python Dependencies

```yaml
---
name: Data Analyzer
description: Analyzes CSV/JSON datasets, generates statistics, visualizations, and insights.
version: 1.2.0
dependencies: python>=3.8, pandas>=1.5.0, matplotlib>=3.5.0, numpy>=1.20.0
---
```

## With JavaScript/Node Dependencies

```yaml
---
name: Web Performance Auditor
description: Audits web applications for performance issues and generates optimization reports.
version: 2.0.0
dependencies: node>=18.0.0, puppeteer>=19.0.0, lighthouse>=10.0.0
---
```

## Domain-Specific Examples

### Security Analysis

```yaml
---
name: Python Security Scanner
description: Scans Python code for security vulnerabilities, insecure patterns, and suggests fixes.
version: 1.0.0
dependencies: python>=3.8, bandit>=1.7.0
---
```

### Code Generation

```yaml
---
name: REST API Generator
description: Generates complete REST API implementations with tests, docs, and validation from specs.
version: 1.1.0
---
```

### Testing

```yaml
---
name: Test Suite Builder
description: Creates comprehensive test suites with unit, integration, and e2e tests for applications.
version: 1.0.0
---
```

### Refactoring

```yaml
---
name: Legacy Code Modernizer
description: Refactors legacy JavaScript to modern ES6+, improves patterns, optimizes performance.
version: 1.5.0
dependencies: node>=16.0.0
---
```

### Documentation

```yaml
---
name: Technical Writer Assistant
description: Transforms code and specs into clear technical documentation with examples and diagrams.
version: 1.0.0
---
```

### Database

```yaml
---
name: SQL Query Optimizer
description: Analyzes SQL queries for performance, suggests indexes, and rewrites for optimization.
version: 2.1.0
dependencies: python>=3.8, sqlparse>=0.4.0
---
```

### DevOps

```yaml
---
name: CI/CD Pipeline Builder
description: Designs and generates CI/CD pipelines for GitHub Actions, GitLab CI, and Jenkins.
version: 1.0.0
---
```

### Machine Learning

```yaml
---
name: ML Model Trainer
description: Trains ML models, performs hyperparameter tuning, and generates evaluation reports.
version: 1.0.0
dependencies: python>=3.9, scikit-learn>=1.0.0, tensorflow>=2.10.0
---
```

## Description Writing Patterns

### Pattern 1: Action + Target + Detail

```yaml
description: Analyzes [target] for [issues], identifies [specifics], and [outcome].
```

**Examples:**
- "Analyzes Python code for PEP 8 violations, identifies style issues, and suggests auto-fixes."
- "Analyzes Dockerfile for best practices, identifies security risks, and recommends improvements."

### Pattern 2: Generates/Creates + What + With What

```yaml
description: Generates [output] from [input] with [features].
```

**Examples:**
- "Generates React components from Figma designs with TypeScript, tests, and storybook stories."
- "Generates database schemas from ER diagrams with migrations, seeds, and documentation."

### Pattern 3: Domain + Multiple Actions

```yaml
description: [Domain expertise] that [action 1], [action 2], and [action 3].
```

**Examples:**
- "Kubernetes expert that deploys applications, manages clusters, and troubleshoots issues."
- "AWS architect that designs infrastructures, optimizes costs, and ensures security compliance."

### Pattern 4: Transforms/Converts + From X to Y

```yaml
description: Converts [source] to [target] while [considerations].
```

**Examples:**
- "Converts REST APIs to GraphQL schemas while preserving semantics and adding optimizations."
- "Converts legacy SQL to modern ORM models while maintaining data integrity and relationships."

## Field Length Guidelines

### Name Examples by Length

**Short (20-30 chars):**
- "Code Analyzer" (13)
- "API Generator" (13)
- "Test Builder" (12)

**Medium (30-45 chars):**
- "Python Security Vulnerability Scanner" (39)
- "REST API Documentation Generator" (33)
- "Legacy JavaScript Modernizer" (29)

**Long (45-64 chars, max):**
- "Machine Learning Model Training and Evaluation Assistant" (57)
- "Enterprise Microservices Architecture Design Tool" (50)

### Description Examples by Length

**Short (100-120 chars):**
```yaml
description: Analyzes code for bugs and suggests fixes. (44)
```

**Medium (120-160 chars):**
```yaml
description: Analyzes Python code for security vulnerabilities, identifies risks, and suggests specific remediation steps. (120)
```

**Long (160-200 chars, max):**
```yaml
description: Generates comprehensive REST API implementations from OpenAPI specs including endpoints, validation, error handling, tests, and interactive documentation. (171)
```

## Common Mistakes to Avoid

### ❌ Too Vague

```yaml
name: Helper Tool
description: Helps with various tasks.
```

**Why it's bad:** No specific domain or action

**✅ Better:**
```yaml
name: Python Debugging Assistant
description: Debugs Python code by analyzing stack traces, identifying root causes, and suggesting fixes.
```

### ❌ Too Generic

```yaml
name: Code Tool
description: Works with code to make it better.
```

**Why it's bad:** Could apply to anything

**✅ Better:**
```yaml
name: Code Performance Optimizer
description: Optimizes code performance by identifying bottlenecks, suggesting algorithms, and profiling results.
```

### ❌ Missing Key Information

```yaml
name: API Thing
description: Does API stuff with documentation.
```

**Why it's bad:** Unclear what it does or when to use it

**✅ Better:**
```yaml
name: OpenAPI Documentation Generator
description: Generates interactive API documentation from OpenAPI specs with examples, authentication guides, and SDKs.
```

### ❌ Too Long (exceeds limits)

```yaml
name: Super Advanced Machine Learning Model Training and Deployment Assistant (OVER 64!)
description: This amazing tool helps you with all your machine learning needs including training models using various algorithms, deploying to production environments, monitoring performance, and much more with comprehensive features. (OVER 200!)
```

**✅ Better:**
```yaml
name: ML Training and Deployment Assistant
description: Trains ML models with hyperparameter tuning, deploys to production, monitors performance, and generates evaluation reports.
```

## Version Format Examples

### Semantic Versioning

```yaml
version: 1.0.0        # Initial release
version: 1.1.0        # Added features (backwards compatible)
version: 1.1.1        # Bug fix
version: 2.0.0        # Breaking changes
version: 2.1.0        # New features in v2
```

### When to Increment

**MAJOR (X.0.0):**
- Complete rewrite
- Breaking changes to structure
- Incompatible with previous version

**MINOR (1.X.0):**
- New features added
- New scripts or resources
- Backwards compatible changes

**PATCH (1.0.X):**
- Bug fixes
- Documentation updates
- Minor clarifications

## Dependencies Format Examples

### Python Packages

```yaml
# Single package
dependencies: python>=3.8

# Multiple packages
dependencies: python>=3.8, pandas>=1.5.0, numpy>=1.20.0

# Exact versions
dependencies: python==3.10, pandas==1.5.3

# Mixed
dependencies: python>=3.8, pandas>=1.5.0, requests==2.28.0
```

### JavaScript/Node Packages

```yaml
# Node version
dependencies: node>=18.0.0

# With packages
dependencies: node>=18.0.0, axios>=1.0.0, lodash>=4.17.21

# Exact versions
dependencies: node==18.12.0, express==4.18.2
```

### No Dependencies

```yaml
# Just omit the field entirely
---
name: Simple Skill
description: Does something without external packages.
version: 1.0.0
---

# Or use an empty string (not recommended)
dependencies: ""
```

## Complete Examples

### Example 1: Simple Documentation Skill

```yaml
---
name: README Generator
description: Generates comprehensive README files with badges, usage examples, and contribution guidelines.
version: 1.0.0
---
```

### Example 2: Script-Based Analysis Skill

```yaml
---
name: Code Complexity Analyzer
description: Analyzes code complexity metrics, identifies high-complexity functions, and suggests refactoring strategies.
version: 1.2.0
dependencies: python>=3.8, radon>=5.1.0, mccabe>=0.7.0
---
```

### Example 3: Multi-Language Tool

```yaml
---
name: Polyglot Code Formatter
description: Formats code across multiple languages following language-specific style guides and best practices.
version: 2.0.0
dependencies: python>=3.8, black>=23.0.0, node>=16.0.0, prettier>=2.8.0
---
```
