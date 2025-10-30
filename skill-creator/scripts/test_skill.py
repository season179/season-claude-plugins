#!/usr/bin/env python3
"""
Skill Testing Helper

Generates test prompts and provides a testing checklist for Claude Code skills.
Helps verify that skills are invoked correctly and produce expected results.

Usage:
    python test_skill.py <skill-directory>

Example:
    python test_skill.py ../my-skill
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Dict


class SkillTester:
    """Generates test cases for skills"""

    def __init__(self, skill_path: Path):
        self.skill_path = skill_path
        self.skill_md_path = skill_path / "Skill.md"
        self.metadata = {}
        self.content = ""

    def load_skill(self) -> bool:
        """Load and parse the skill file"""
        if not self.skill_md_path.exists():
            print(f"❌ Skill.md not found in {self.skill_path}", file=sys.stderr)
            return False

        try:
            self.content = self.skill_md_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"❌ Failed to read Skill.md: {e}", file=sys.stderr)
            return False

        self._parse_metadata()
        return True

    def _parse_metadata(self):
        """Parse YAML frontmatter"""
        if not self.content.startswith('---'):
            return

        parts = self.content.split('---', 2)
        if len(parts) < 3:
            return

        yaml_content = parts[1].strip()
        for line in yaml_content.split('\n'):
            line = line.strip()
            if not line or line.startswith('#') or ':' not in line:
                continue

            key, value = line.split(':', 1)
            self.metadata[key.strip()] = value.strip()

    def generate_test_prompts(self) -> List[Dict[str, str]]:
        """Generate test prompts based on the skill description"""
        prompts = []

        if 'description' not in self.metadata:
            return prompts

        description = self.metadata['description']
        name = self.metadata.get('name', 'Skill')

        # Extract action verbs from description
        action_verbs = [
            'analyze', 'analyzes', 'generate', 'generates', 'create', 'creates',
            'build', 'builds', 'test', 'tests', 'validate', 'validates',
            'refactor', 'refactors', 'optimize', 'optimizes', 'scan', 'scans',
            'review', 'reviews', 'format', 'formats', 'convert', 'converts'
        ]

        found_verbs = [verb for verb in action_verbs if verb.lower() in description.lower()]

        # Extract domain/technology keywords
        domain_keywords = self._extract_keywords(description)

        # Generate direct prompts
        if found_verbs:
            base_verb = found_verbs[0].rstrip('s')  # Remove 's' for imperative form
            prompts.append({
                'type': 'direct',
                'prompt': f"{base_verb.capitalize()} {domain_keywords[0] if domain_keywords else 'this'}",
                'should_match': True,
                'reason': 'Direct match with skill description action'
            })

        # Generate synonym prompts
        if domain_keywords:
            prompts.append({
                'type': 'synonym',
                'prompt': f"Help me with {domain_keywords[0]}",
                'should_match': True,
                'reason': 'Uses domain keyword from description'
            })

        # Generate specific prompts based on description
        prompts.extend(self._generate_specific_prompts(description, domain_keywords))

        # Generate negative test cases
        prompts.extend(self._generate_negative_prompts(domain_keywords))

        return prompts

    def _extract_keywords(self, description: str) -> List[str]:
        """Extract important keywords from description"""
        # Common technical keywords
        tech_words = [
            'python', 'javascript', 'java', 'code', 'api', 'database', 'sql',
            'html', 'css', 'react', 'node', 'docker', 'kubernetes', 'aws',
            'test', 'security', 'performance', 'documentation', 'git'
        ]

        found = []
        desc_lower = description.lower()
        for word in tech_words:
            if word in desc_lower:
                found.append(word)

        return found

    def _generate_specific_prompts(self, description: str, keywords: List[str]) -> List[Dict[str, str]]:
        """Generate specific test prompts"""
        prompts = []

        # Pattern-based generation
        if 'security' in description.lower():
            prompts.append({
                'type': 'specific',
                'prompt': f"Check my {keywords[0] if keywords else 'code'} for security issues",
                'should_match': True,
                'reason': 'Security-related request'
            })

        if any(word in description.lower() for word in ['generate', 'create', 'build']):
            prompts.append({
                'type': 'specific',
                'prompt': f"Create a {keywords[0] if keywords else 'file'} for me",
                'should_match': True,
                'reason': 'Generation request'
            })

        if 'documentation' in description.lower() or 'docs' in description.lower():
            prompts.append({
                'type': 'specific',
                'prompt': "Write documentation for this",
                'should_match': True,
                'reason': 'Documentation request'
            })

        if any(word in description.lower() for word in ['test', 'testing']):
            prompts.append({
                'type': 'specific',
                'prompt': f"Write tests for my {keywords[0] if keywords else 'code'}",
                'should_match': True,
                'reason': 'Testing request'
            })

        return prompts

    def _generate_negative_prompts(self, keywords: List[str]) -> List[Dict[str, str]]:
        """Generate prompts that should NOT match"""
        prompts = []

        # Generic unrelated prompts
        unrelated = [
            "What's the weather today?",
            "Tell me a joke",
            "Explain quantum physics",
            "How do I cook pasta?"
        ]

        for prompt_text in unrelated[:2]:  # Include 2 negative cases
            prompts.append({
                'type': 'negative',
                'prompt': prompt_text,
                'should_match': False,
                'reason': 'Unrelated to skill domain'
            })

        # Domain-adjacent but different intent
        if keywords:
            prompts.append({
                'type': 'negative',
                'prompt': f"What is {keywords[0]}?",
                'should_match': False,
                'reason': 'Informational query, not action request'
            })

        return prompts

    def print_test_plan(self):
        """Print comprehensive test plan"""
        print(f"\n{'='*70}")
        print(f"Test Plan for: {self.metadata.get('name', self.skill_path.name)}")
        print(f"{'='*70}\n")

        # Metadata summary
        print("📋 Skill Metadata")
        print(f"  Name: {self.metadata.get('name', 'N/A')}")
        print(f"  Description: {self.metadata.get('description', 'N/A')}")
        print(f"  Version: {self.metadata.get('version', 'N/A')}")
        print()

        # Pre-upload checklist
        print("✅ Pre-Upload Checklist")
        print("  [ ] Skill.md has clear instructions")
        print("  [ ] All file references are valid")
        print("  [ ] Scripts work independently (if applicable)")
        print("  [ ] Examples are included")
        print("  [ ] Description is specific and action-oriented")
        print("  [ ] Name is descriptive and under 64 chars")
        print("  [ ] Run validate_skill.py with no errors")
        print("  [ ] ZIP file created with package_skill.py")
        print()

        # Generated test prompts
        prompts = self.generate_test_prompts()
        if prompts:
            print("🧪 Test Prompts")
            print("\nPositive Tests (should invoke skill):")
            for i, prompt_data in enumerate([p for p in prompts if p['should_match']], 1):
                print(f"\n  {i}. \"{prompt_data['prompt']}\"")
                print(f"     Type: {prompt_data['type']}")
                print(f"     Why: {prompt_data['reason']}")

            print("\nNegative Tests (should NOT invoke skill):")
            for i, prompt_data in enumerate([p for p in prompts if not p['should_match']], 1):
                print(f"\n  {i}. \"{prompt_data['prompt']}\"")
                print(f"     Type: {prompt_data['type']}")
                print(f"     Why: {prompt_data['reason']}")
            print()

        # Post-upload checklist
        print("✅ Post-Upload Checklist")
        print("  [ ] Skill uploaded successfully")
        print("  [ ] Skill enabled in Settings > Capabilities")
        print("  [ ] All positive test prompts invoke the skill")
        print("  [ ] All negative test prompts do NOT invoke the skill")
        print("  [ ] Claude follows the instructions correctly")
        print("  [ ] Output quality meets expectations")
        print("  [ ] Edge cases handled appropriately")
        print()

        # Testing tips
        print("💡 Testing Tips")
        print("  • Test with varied phrasings of the same request")
        print("  • Check Claude's reasoning for why it chose the skill")
        print("  • Verify the skill doesn't trigger on unrelated prompts")
        print("  • Test with and without domain keywords")
        print("  • Try implicit vs explicit requests")
        print("  • Test edge cases and error scenarios")
        print()

        # Iteration guidance
        print("🔄 If Tests Fail")
        print("\n  Skill not invoked when expected:")
        print("    → Make description more specific")
        print("    → Add action verbs and domain keywords")
        print("    → Include synonyms in description")
        print()
        print("  Skill invoked when it shouldn't be:")
        print("    → Narrow description scope")
        print("    → Add domain-specific qualifiers")
        print("    → Remove generic terms")
        print()
        print("  Instructions not followed correctly:")
        print("    → Break down complex steps")
        print("    → Add more examples")
        print("    → Clarify ambiguous instructions")
        print("    → Move detailed info to REFERENCE.md")
        print()

        print(f"{'='*70}\n")

    def generate_test_script(self) -> str:
        """Generate a test script template"""
        prompts = self.generate_test_prompts()
        positive = [p for p in prompts if p['should_match']]
        negative = [p for p in prompts if not p['should_match']]

        script = f"""# Test Script for {self.metadata.get('name', 'Skill')}

## Test Session: {self.metadata.get('name', 'Skill')}

Date: ___________
Tester: ___________

### Positive Tests (Should invoke skill)

"""
        for i, p in enumerate(positive, 1):
            script += f"""{i}. **Prompt:** "{p['prompt']}"
   - [ ] Skill invoked
   - [ ] Instructions followed correctly
   - [ ] Output quality good
   - **Notes:** ___________________________________________

"""

        script += """### Negative Tests (Should NOT invoke skill)

"""
        for i, p in enumerate(negative, 1):
            script += f"""{i}. **Prompt:** "{p['prompt']}"
   - [ ] Skill NOT invoked
   - [ ] Correct alternative used (if any)
   - **Notes:** ___________________________________________

"""

        script += """### Overall Assessment

- [ ] All positive tests passed
- [ ] All negative tests passed
- [ ] Instructions are clear and followed
- [ ] No unexpected invocations
- [ ] Quality meets expectations

### Issues Found:

1. ___________________________________________
2. ___________________________________________
3. ___________________________________________

### Next Steps:

- [ ] Description changes needed
- [ ] Instruction improvements needed
- [ ] Examples to add
- [ ] Ready for production use
"""

        return script


def main():
    parser = argparse.ArgumentParser(
        description='Generate test plan for a Claude Code skill',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  python test_skill.py my-skill
  python test_skill.py my-skill --output test-plan.md

Generates:
  - Test prompts (positive and negative cases)
  - Pre-upload checklist
  - Post-upload checklist
  - Testing tips and iteration guidance
        """
    )

    parser.add_argument(
        'skill_directory',
        help='Path to the skill directory containing Skill.md'
    )

    parser.add_argument(
        '--output', '-o',
        help='Save test script to file (markdown format)'
    )

    args = parser.parse_args()

    skill_path = Path(args.skill_directory).resolve()

    if not skill_path.exists() or not skill_path.is_dir():
        print(f"❌ Invalid skill directory: {skill_path}", file=sys.stderr)
        return 1

    print(f"🧪 Generating test plan for: {skill_path}")

    tester = SkillTester(skill_path)
    if not tester.load_skill():
        return 1

    tester.print_test_plan()

    # Optionally save test script
    if args.output:
        output_path = Path(args.output)
        script = tester.generate_test_script()
        output_path.write_text(script, encoding='utf-8')
        print(f"📝 Test script saved to: {output_path}")
        print()

    return 0


if __name__ == '__main__':
    sys.exit(main())
