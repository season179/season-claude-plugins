#!/usr/bin/env python3
"""
Skill Validation Tool

Validates a Claude Code skill directory for correctness and best practices.

Checks:
- Skill.md file exists
- YAML frontmatter is valid
- Required fields are present
- Field length constraints
- File references are valid
- Best practices adherence

Usage:
    python validate_skill.py <skill-directory>

Example:
    python validate_skill.py ../my-skill
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple


class ValidationIssue:
    """Represents a validation issue"""

    def __init__(self, level: str, message: str, suggestion: str = None):
        self.level = level  # 'error', 'warning', 'info'
        self.message = message
        self.suggestion = suggestion

    def __str__(self):
        icon = {'error': '❌', 'warning': '⚠️ ', 'info': 'ℹ️ '}[self.level]
        result = f"{icon} {self.message}"
        if self.suggestion:
            result += f"\n   💡 {self.suggestion}"
        return result


class SkillValidator:
    """Validates Claude Code skills"""

    def __init__(self, skill_path: Path):
        self.skill_path = skill_path
        self.issues: List[ValidationIssue] = []
        self.skill_md_path = skill_path / "Skill.md"
        self.metadata = {}
        self.content = ""

    def validate(self) -> bool:
        """
        Run all validations.

        Returns:
            True if no errors found, False otherwise
        """
        self._check_skill_md_exists()

        if not self.skill_md_path.exists():
            return False

        self._read_skill_file()
        self._validate_yaml_frontmatter()
        self._validate_required_fields()
        self._validate_field_lengths()
        self._validate_description_quality()
        self._validate_dependencies()
        self._validate_file_references()
        self._check_best_practices()

        return not any(issue.level == 'error' for issue in self.issues)

    def _check_skill_md_exists(self):
        """Check if Skill.md file exists"""
        if not self.skill_md_path.exists():
            self.issues.append(ValidationIssue(
                'error',
                f"Skill.md not found in {self.skill_path}",
                "Create a Skill.md file with YAML frontmatter"
            ))

    def _read_skill_file(self):
        """Read the Skill.md file"""
        try:
            self.content = self.skill_md_path.read_text(encoding='utf-8')
        except Exception as e:
            self.issues.append(ValidationIssue(
                'error',
                f"Failed to read Skill.md: {e}"
            ))

    def _validate_yaml_frontmatter(self):
        """Validate YAML frontmatter exists and is properly formatted"""
        if not self.content:
            return

        # Check for frontmatter delimiters
        if not self.content.startswith('---'):
            self.issues.append(ValidationIssue(
                'error',
                "Skill.md must start with YAML frontmatter (---)",
                "Add --- at the beginning of the file followed by metadata fields"
            ))
            return

        # Extract frontmatter
        parts = self.content.split('---', 2)
        if len(parts) < 3:
            self.issues.append(ValidationIssue(
                'error',
                "YAML frontmatter not properly closed with ---",
                "Ensure you have --- before and after the metadata"
            ))
            return

        yaml_content = parts[1].strip()

        # Parse YAML manually (simple key: value format)
        for line in yaml_content.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            if ':' not in line:
                self.issues.append(ValidationIssue(
                    'warning',
                    f"Invalid YAML line (missing colon): {line}",
                    "Use format: key: value"
                ))
                continue

            key, value = line.split(':', 1)
            self.metadata[key.strip()] = value.strip()

    def _validate_required_fields(self):
        """Validate required metadata fields are present"""
        required = ['name', 'description']

        for field in required:
            if field not in self.metadata or not self.metadata[field]:
                self.issues.append(ValidationIssue(
                    'error',
                    f"Required field '{field}' is missing or empty",
                    f"Add '{field}: <value>' to the YAML frontmatter"
                ))

    def _validate_field_lengths(self):
        """Validate field length constraints"""
        if 'name' in self.metadata:
            name = self.metadata['name']
            name_len = len(name)
            if name_len > 64:
                self.issues.append(ValidationIssue(
                    'error',
                    f"Name exceeds 64 characters (current: {name_len})",
                    "Shorten the skill name to 64 characters or less"
                ))
            elif name_len > 50:
                self.issues.append(ValidationIssue(
                    'warning',
                    f"Name is quite long ({name_len} chars, max 64)",
                    "Consider shortening for better readability"
                ))

        if 'description' in self.metadata:
            desc = self.metadata['description']
            desc_len = len(desc)
            if desc_len > 200:
                self.issues.append(ValidationIssue(
                    'error',
                    f"Description exceeds 200 characters (current: {desc_len})",
                    "Shorten the description to 200 characters or less"
                ))
            elif desc_len > 180:
                self.issues.append(ValidationIssue(
                    'warning',
                    f"Description is near the limit ({desc_len}/200 chars)",
                    "Consider condensing if possible"
                ))
            elif desc_len < 50:
                self.issues.append(ValidationIssue(
                    'warning',
                    f"Description is quite short ({desc_len} chars)",
                    "Add more details to help Claude understand when to invoke this skill"
                ))

    def _validate_description_quality(self):
        """Check description quality and best practices"""
        if 'description' not in self.metadata:
            return

        desc = self.metadata['description'].lower()

        # Check for action verbs
        action_verbs = [
            'analyze', 'generate', 'create', 'build', 'test', 'validate',
            'refactor', 'optimize', 'scan', 'review', 'format', 'convert',
            'transform', 'deploy', 'monitor', 'detect', 'identify', 'suggest'
        ]

        has_action_verb = any(verb in desc for verb in action_verbs)
        if not has_action_verb:
            self.issues.append(ValidationIssue(
                'warning',
                "Description lacks specific action verbs",
                "Start with action verbs like 'Analyzes', 'Generates', 'Refactors' for better matching"
            ))

        # Check for generic phrases
        generic_phrases = [
            'helps with', 'tool for', 'assistant for', 'useful for',
            'helps you', 'works with'
        ]

        has_generic = any(phrase in desc for phrase in generic_phrases)
        if has_generic:
            self.issues.append(ValidationIssue(
                'info',
                "Description contains generic phrases",
                "Be more specific about what the skill does"
            ))

        # Check if description is too vague
        vague_words = ['various', 'stuff', 'things', 'something']
        has_vague = any(word in desc for word in vague_words)
        if has_vague:
            self.issues.append(ValidationIssue(
                'warning',
                "Description contains vague terms",
                "Be specific about what the skill operates on"
            ))

    def _validate_dependencies(self):
        """Validate dependencies are not in top-level frontmatter"""
        if 'dependencies' in self.metadata:
            self.issues.append(ValidationIssue(
                'error',
                "Dependencies field is not allowed at top level",
                "Document dependencies in your README, requirements.txt, or in metadata field"
            ))

        if 'version' in self.metadata:
            self.issues.append(ValidationIssue(
                'error',
                "Version field is not allowed at top level",
                "Use metadata.version instead or track versions in your README"
            ))

        if 'author' in self.metadata:
            self.issues.append(ValidationIssue(
                'error',
                "Author field is not allowed at top level",
                "Use metadata.author instead if you want to track authorship"
            ))

    def _validate_file_references(self):
        """Validate that referenced files exist"""
        if not self.content:
            return

        # Find markdown links and file references
        # Pattern: `path/to/file.ext` or [text](path/to/file.ext)
        inline_code_pattern = r'`([^`]+\.[a-z]+)`'
        markdown_link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'

        referenced_files = set()

        # Find inline code references
        for match in re.finditer(inline_code_pattern, self.content):
            file_ref = match.group(1)
            if '/' in file_ref:  # Likely a file path
                referenced_files.add(file_ref)

        # Find markdown links
        for match in re.finditer(markdown_link_pattern, self.content):
            file_ref = match.group(2)
            if not file_ref.startswith(('http://', 'https://', '#')):
                referenced_files.add(file_ref)

        # Check if referenced files exist
        for file_ref in referenced_files:
            file_path = self.skill_path / file_ref
            if not file_path.exists():
                self.issues.append(ValidationIssue(
                    'warning',
                    f"Referenced file not found: {file_ref}",
                    f"Create the file or remove the reference"
                ))

    def _check_best_practices(self):
        """Check adherence to best practices"""
        if not self.content:
            return

        # Check if there's content after frontmatter
        parts = self.content.split('---', 2)
        if len(parts) >= 3:
            body = parts[2].strip()
            if not body:
                self.issues.append(ValidationIssue(
                    'warning',
                    "Skill.md has no content after frontmatter",
                    "Add instructions, examples, and guidance for Claude"
                ))
            elif len(body) < 200:
                self.issues.append(ValidationIssue(
                    'info',
                    "Skill.md has minimal content",
                    "Consider adding more detailed instructions and examples"
                ))

        # Check for examples in content
        if 'example' not in self.content.lower():
            self.issues.append(ValidationIssue(
                'info',
                "No examples found in Skill.md",
                "Adding examples helps Claude understand how to use the skill"
            ))

    def print_report(self):
        """Print validation report"""
        errors = [i for i in self.issues if i.level == 'error']
        warnings = [i for i in self.issues if i.level == 'warning']
        infos = [i for i in self.issues if i.level == 'info']

        print(f"\n{'='*60}")
        print(f"Validation Report: {self.skill_path.name}")
        print(f"{'='*60}\n")

        if not self.issues:
            print("✅ All checks passed! The skill looks great.\n")
            return

        if errors:
            print(f"Errors ({len(errors)}):")
            for issue in errors:
                print(f"  {issue}\n")

        if warnings:
            print(f"Warnings ({len(warnings)}):")
            for issue in warnings:
                print(f"  {issue}\n")

        if infos:
            print(f"Suggestions ({len(infos)}):")
            for issue in infos:
                print(f"  {issue}\n")

        print(f"{'='*60}")
        print(f"Summary: {len(errors)} errors, {len(warnings)} warnings, {len(infos)} suggestions")
        print(f"{'='*60}\n")

        if errors:
            print("❌ Validation failed. Please fix errors before packaging.\n")
        elif warnings:
            print("⚠️  Validation passed with warnings. Consider addressing them.\n")
        else:
            print("✅ Validation passed. Ready to package!\n")


def main():
    parser = argparse.ArgumentParser(
        description='Validate a Claude Code skill',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  python validate_skill.py my-skill
  python validate_skill.py ../path/to/skill

Checks performed:
  - Skill.md file exists
  - Valid YAML frontmatter
  - Required fields present
  - Field length constraints
  - Description quality
  - File references validity
  - Best practices adherence
        """
    )

    parser.add_argument(
        'skill_directory',
        help='Path to the skill directory containing Skill.md'
    )

    parser.add_argument(
        '--strict',
        action='store_true',
        help='Treat warnings as errors'
    )

    args = parser.parse_args()

    skill_path = Path(args.skill_directory).resolve()

    if not skill_path.exists():
        print(f"❌ Directory not found: {skill_path}", file=sys.stderr)
        return 1

    if not skill_path.is_dir():
        print(f"❌ Path is not a directory: {skill_path}", file=sys.stderr)
        return 1

    print(f"🔍 Validating skill: {skill_path}")

    validator = SkillValidator(skill_path)
    is_valid = validator.validate()
    validator.print_report()

    # Return appropriate exit code
    if not is_valid:
        return 1
    elif args.strict and any(i.level == 'warning' for i in validator.issues):
        return 1
    else:
        return 0


if __name__ == '__main__':
    sys.exit(main())
