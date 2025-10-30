---
name: Python Code Analyzer
description: Analyzes Python code for complexity, quality metrics, security issues, and generates improvement reports.
version: 1.0.0
dependencies: python>=3.8, radon>=5.1.0, bandit>=1.7.0, pylint>=2.15.0
---

# Python Code Analyzer

Comprehensive Python code analysis tool that evaluates code quality, complexity, security, and provides actionable improvement recommendations.

## Purpose

Provides deep analysis of Python codebases:
- Complexity metrics (cyclomatic, cognitive, maintainability)
- Code quality scoring
- Security vulnerability detection
- Style and convention compliance
- Performance bottleneck identification

## Prerequisites

Install required dependencies:
```bash
pip install radon>=5.1.0 bandit>=1.7.0 pylint>=2.15.0
```

Or use the requirements file:
```bash
cd scripts && pip install -r requirements.txt
```

## Core Workflow

### Phase 1: Initial Analysis

1. **Identify target files**
   - Ask user which files or directories to analyze
   - Support glob patterns: `src/**/*.py`
   - Exclude test files and migrations by default (unless requested)

2. **Run complexity analysis**
   ```bash
   python scripts/analyze_complexity.py <path-to-code>
   ```

   This generates:
   - Cyclomatic complexity per function
   - Maintainability index per module
   - Cognitive complexity scores

3. **Run security scan**
   ```bash
   python scripts/security_scan.py <path-to-code>
   ```

   Identifies:
   - SQL injection risks
   - Hard-coded secrets
   - Insecure cryptography
   - Command injection vulnerabilities

### Phase 2: Detailed Assessment

1. **Analyze results from scripts**
   - Complexity scores > 10: Flag for refactoring
   - Maintainability < 20: Critical improvement needed
   - Security issues: Prioritize by severity (High, Medium, Low)

2. **Identify patterns**
   - Common anti-patterns
   - Repeated code smells
   - Architecture issues

3. **Generate metrics summary**
   - Overall quality score (0-100)
   - Number of issues by category
   - Comparison to industry standards

### Phase 3: Recommendations

1. **Prioritize improvements**
   - Critical: Security High + Complexity > 15
   - High: Security Medium + Maintainability < 20
   - Medium: Complexity 10-15 + Quality issues
   - Low: Style and convention improvements

2. **Provide specific refactoring suggestions**
   - Extract complex functions
   - Reduce nesting depth
   - Apply design patterns
   - Improve error handling

3. **Generate action plan**
   - Numbered list of improvements
   - Estimated effort (quick wins vs. major refactors)
   - Expected impact on quality metrics

## Using Helper Scripts

### Script 1: `analyze_complexity.py`

**Purpose:** Calculates complexity metrics for Python code

**Usage:**
```bash
python scripts/analyze_complexity.py <path> [--threshold 10] [--output json]
```

**Options:**
- `--threshold N`: Alert on complexity > N (default: 10)
- `--output FORMAT`: Output format: text, json, html (default: json)
- `--exclude PATTERN`: Exclude files matching pattern

**Output:**
```json
{
  "files": [
    {
      "path": "module.py",
      "functions": [
        {
          "name": "complex_function",
          "complexity": 15,
          "maintainability": 18.5
        }
      ]
    }
  ],
  "summary": {
    "average_complexity": 7.2,
    "high_complexity_count": 3
  }
}
```

### Script 2: `security_scan.py`

**Purpose:** Scans for security vulnerabilities

**Usage:**
```bash
python scripts/security_scan.py <path> [--severity low] [--output json]
```

**Options:**
- `--severity LEVEL`: Minimum severity to report (low, medium, high)
- `--output FORMAT`: Output format (default: json)
- `--config FILE`: Custom bandit config

**Output:**
```json
{
  "vulnerabilities": [
    {
      "file": "auth.py",
      "line": 45,
      "severity": "HIGH",
      "issue": "Hardcoded password",
      "recommendation": "Use environment variables or secrets manager"
    }
  ]
}
```

### Script 3: `quality_report.py`

**Purpose:** Generates comprehensive HTML report

**Usage:**
```bash
python scripts/quality_report.py <complexity-json> <security-json> --output report.html
```

Combines all analysis into a visual dashboard with charts and recommendations.

## Interpreting Metrics

### Cyclomatic Complexity
- **1-5**: Simple, easy to maintain
- **6-10**: Moderate complexity, acceptable
- **11-15**: High complexity, consider refactoring
- **16+**: Very high, refactor immediately

### Maintainability Index
- **85-100**: Highly maintainable
- **65-84**: Moderately maintainable
- **20-64**: Low maintainability
- **0-19**: Critical, very hard to maintain

### Security Severity
- **High**: Immediate action required
- **Medium**: Fix in next sprint
- **Low**: Address when convenient

## Example Analysis Session

### User Request:
"Analyze my Python backend code for issues"

### Response Steps:

1. **Request clarification**:
   "I'll analyze your Python code. Which directory should I examine? (e.g., `src/`, `app/`, entire project)"

2. **Run analysis** (after user specifies):
   ```bash
   python scripts/analyze_complexity.py src/
   python scripts/security_scan.py src/
   ```

3. **Present findings**:
   ```
   📊 Code Analysis Results

   Overall Quality Score: 72/100 (Good)

   Complexity Issues:
   - 3 functions with high complexity (>10)
   - Average complexity: 6.8 (acceptable)

   Security Issues:
   - 1 HIGH severity: Hard-coded API key (auth.py:23)
   - 2 MEDIUM severity: SQL injection risks (database.py:45, 67)
   - 3 LOW severity: Weak cryptography usage

   Top Priority Improvements:
   1. Remove hardcoded API key, use environment variables
   2. Use parameterized queries for SQL statements
   3. Refactor process_order() function (complexity: 16)
   ```

4. **Provide specific recommendations**:
   ```python
   # Current (auth.py:23):
   API_KEY = "sk_live_abc123..."

   # Recommended:
   import os
   API_KEY = os.environ.get("API_KEY")
   if not API_KEY:
       raise ValueError("API_KEY environment variable not set")
   ```

5. **Generate action plan**:
   ```
   Action Plan (Prioritized):

   🔴 Critical (Do immediately):
   1. Fix hardcoded credentials - 15 min
   2. Fix SQL injection vulnerabilities - 30 min

   🟡 High Priority (This sprint):
   3. Refactor complex functions - 2 hours
   4. Add input validation - 1 hour

   🟢 Medium Priority (Next sprint):
   5. Improve error handling - 1 hour
   6. Add type hints - 2 hours
   ```

## Troubleshooting

### Issue: Scripts fail to run

**Solution:**
```bash
# Verify Python version
python --version  # Should be >= 3.8

# Reinstall dependencies
pip install -r scripts/requirements.txt

# Check file permissions
chmod +x scripts/*.py
```

### Issue: False positives in security scan

**Solution:**
- Create `.bandit` config file to exclude specific checks
- Use inline comments to suppress warnings:
  ```python
  # nosec - False positive, input is validated
  ```

### Issue: Analysis takes too long

**Solution:**
- Analyze specific directories instead of entire codebase
- Exclude test files and migrations:
  ```bash
  python scripts/analyze_complexity.py src/ --exclude "*/tests/*,*/migrations/*"
  ```

## Advanced Features

### Custom Thresholds

Create a `.analyzer-config.json`:
```json
{
  "complexity_threshold": 12,
  "maintainability_threshold": 25,
  "exclude_patterns": ["*/tests/*", "*/venv/*"]
}
```

### CI/CD Integration

Use in continuous integration:
```yaml
# .github/workflows/code-quality.yml
- name: Analyze Code Quality
  run: |
    python scripts/analyze_complexity.py src/ --threshold 10
    python scripts/security_scan.py src/ --severity medium
```

Fails build if thresholds exceeded.

### Historical Tracking

Track metrics over time:
```bash
python scripts/analyze_complexity.py src/ --output metrics.json
# Commit metrics.json to track improvements
```

## Limitations

- **Python-specific**: Only analyzes Python code
- **Static analysis**: Can't detect runtime issues
- **False positives**: Security scan may flag safe code
- **Large codebases**: May be slow on 10,000+ files

For other languages, consider language-specific tools.

## Reference Materials

For detailed information, see:
- `resources/complexity-guide.md` - Understanding complexity metrics
- `resources/security-checklist.md` - Security best practices
- `resources/refactoring-patterns.md` - Common refactoring strategies

## Version History

### 1.0.0 (2025-01-15)
- Initial release
- Complexity analysis with radon
- Security scanning with bandit
- HTML report generation
- Priority-based recommendations
