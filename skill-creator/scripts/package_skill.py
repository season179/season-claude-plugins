#!/usr/bin/env python3
"""
Skill Packaging Tool

Packages a Claude Code skill directory into a correctly formatted ZIP file.
The ZIP structure places the skill folder as the root.

Usage:
    python package_skill.py <skill-directory> [--output <output-path>]

Example:
    python package_skill.py ../my-skill
    python package_skill.py ../my-skill --output my-skill-v1.0.0.zip
"""

import argparse
import os
import sys
import zipfile
from pathlib import Path


def validate_skill_directory(skill_path: Path) -> tuple[bool, str]:
    """
    Validates that the directory is a valid skill directory.

    Args:
        skill_path: Path to the skill directory

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not skill_path.exists():
        return False, f"Directory does not exist: {skill_path}"

    if not skill_path.is_dir():
        return False, f"Path is not a directory: {skill_path}"

    skill_md = skill_path / "Skill.md"
    if not skill_md.exists():
        return False, f"Skill.md not found in {skill_path}"

    if not skill_md.is_file():
        return False, f"Skill.md is not a file: {skill_md}"

    return True, ""


def create_skill_zip(skill_path: Path, output_path: Path) -> bool:
    """
    Creates a ZIP file with the correct structure for Claude Code skills.

    Structure:
        skill-name.zip
        └── skill-name/
            ├── Skill.md
            └── ...

    Args:
        skill_path: Path to the skill directory
        output_path: Path where the ZIP file should be created

    Returns:
        True if successful, False otherwise
    """
    skill_name = skill_path.name

    try:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Walk through all files in the skill directory
            for root, dirs, files in os.walk(skill_path):
                # Calculate the relative path from the skill directory
                rel_dir = Path(root).relative_to(skill_path.parent)

                for file in files:
                    # Skip hidden files and system files
                    if file.startswith('.') or file == '.DS_Store':
                        continue

                    file_path = Path(root) / file
                    # Archive name maintains the skill folder as root
                    arcname = rel_dir / file

                    zipf.write(file_path, arcname)
                    print(f"  Added: {arcname}")

        return True

    except Exception as e:
        print(f"❌ Error creating ZIP file: {e}", file=sys.stderr)
        return False


def get_output_path(skill_path: Path, output_arg: str = None) -> Path:
    """
    Determines the output path for the ZIP file.

    Args:
        skill_path: Path to the skill directory
        output_arg: Optional output path specified by user

    Returns:
        Path where the ZIP file should be created
    """
    if output_arg:
        output_path = Path(output_arg)
    else:
        # Default: skill-name.zip in the current directory
        skill_name = skill_path.name
        output_path = Path.cwd() / f"{skill_name}.zip"

    # Ensure .zip extension
    if not output_path.suffix == '.zip':
        output_path = output_path.with_suffix('.zip')

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Package a Claude Code skill into a ZIP file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python package_skill.py my-skill
  python package_skill.py my-skill --output my-skill-v1.0.0.zip
  python package_skill.py ../path/to/skill --output dist/skill.zip

The ZIP structure will be:
  skill-name.zip
  └── skill-name/
      ├── Skill.md
      └── ...
        """
    )

    parser.add_argument(
        'skill_directory',
        help='Path to the skill directory containing Skill.md'
    )

    parser.add_argument(
        '--output', '-o',
        help='Output path for the ZIP file (default: skill-name.zip in current directory)'
    )

    parser.add_argument(
        '--force', '-f',
        action='store_true',
        help='Overwrite existing ZIP file without prompting'
    )

    args = parser.parse_args()

    # Convert to Path object and resolve to absolute path
    skill_path = Path(args.skill_directory).resolve()

    print(f"📦 Packaging skill from: {skill_path}")

    # Validate the skill directory
    is_valid, error_msg = validate_skill_directory(skill_path)
    if not is_valid:
        print(f"❌ Validation failed: {error_msg}", file=sys.stderr)
        return 1

    print("✅ Skill directory validated")

    # Determine output path
    output_path = get_output_path(skill_path, args.output)

    # Check if output file already exists
    if output_path.exists() and not args.force:
        response = input(f"⚠️  {output_path} already exists. Overwrite? (y/N): ")
        if response.lower() not in ['y', 'yes']:
            print("❌ Cancelled")
            return 0

    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Create the ZIP file
    print(f"\n📝 Creating ZIP file: {output_path}")
    success = create_skill_zip(skill_path, output_path)

    if success:
        file_size = output_path.stat().st_size
        print(f"\n✅ Successfully packaged skill!")
        print(f"📄 Output: {output_path}")
        print(f"📊 Size: {file_size:,} bytes ({file_size / 1024:.1f} KB)")
        print(f"\n💡 Next steps:")
        print(f"   1. Upload {output_path.name} to Claude Code")
        print(f"   2. Enable the skill in Settings > Capabilities")
        print(f"   3. Test with various prompts")
        return 0
    else:
        return 1


if __name__ == '__main__':
    sys.exit(main())
