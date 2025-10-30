#!/usr/bin/env python3
"""
Check installed OpenAI SDK version and provide upgrade guidance.

This script helps users verify their OpenAI SDK installation and provides
information about available updates.

Usage:
    python check_openai_version.py
"""

import sys
import subprocess
from typing import Optional


def get_installed_version() -> Optional[str]:
    """Get the currently installed OpenAI SDK version."""
    try:
        import openai
        return openai.__version__
    except ImportError:
        return None
    except AttributeError:
        return "unknown"


def get_latest_version() -> Optional[str]:
    """Get the latest available version from PyPI."""
    try:
        result = subprocess.run(
            ["pip", "index", "versions", "openai"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            # Parse output to find latest version
            for line in result.stdout.split('\n'):
                if 'Available versions:' in line or 'LATEST:' in line:
                    # Extract version number
                    parts = line.split()
                    for part in parts:
                        if part[0].isdigit():
                            return part.rstrip(',')

            # Fallback: try first line after "Available versions:"
            lines = result.stdout.split('\n')
            for i, line in enumerate(lines):
                if 'Available versions:' in line and i + 1 < len(lines):
                    versions = lines[i + 1].strip().split(',')
                    if versions:
                        return versions[0].strip()
        return None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None


def check_python_version() -> tuple[bool, str]:
    """Check if Python version is 3.11+."""
    version_info = sys.version_info
    version_str = f"{version_info.major}.{version_info.minor}.{version_info.micro}"

    is_compatible = version_info.major == 3 and version_info.minor >= 11

    return is_compatible, version_str


def main():
    """Main execution function."""
    print("=" * 60)
    print("OpenAI SDK Version Check")
    print("=" * 60)
    print()

    # Check Python version
    python_compatible, python_version = check_python_version()
    print(f"Python Version: {python_version}")

    if not python_compatible:
        print("⚠️  WARNING: This skill targets Python 3.11+")
        print("   You may encounter compatibility issues with older versions.")
        print()
    else:
        print("✅ Python version compatible (3.11+)")
        print()

    # Check OpenAI SDK installation
    installed_version = get_installed_version()

    if installed_version is None:
        print("❌ OpenAI SDK not installed")
        print()
        print("To install:")
        print("    pip install openai")
        print()
        print("For development:")
        print("    pip install openai[datalib]")
        print()
        return 1

    print(f"✅ OpenAI SDK installed: v{installed_version}")
    print()

    # Check for updates
    print("Checking for updates...")
    latest_version = get_latest_version()

    if latest_version is None:
        print("⚠️  Could not check for latest version")
        print("   Run manually: pip index versions openai")
    else:
        print(f"Latest available: v{latest_version}")

        if installed_version == "unknown":
            print("⚠️  Cannot compare versions (version detection failed)")
        elif installed_version != latest_version:
            print()
            print("📦 Update available!")
            print(f"   Current: v{installed_version}")
            print(f"   Latest:  v{latest_version}")
            print()
            print("To upgrade:")
            print("    pip install --upgrade openai")
        else:
            print("✅ You have the latest version!")

    print()
    print("-" * 60)
    print("Additional Information:")
    print("-" * 60)
    print()
    print("Documentation:")
    print("  • API Reference: https://platform.openai.com/docs/api-reference")
    print("  • Python SDK: https://github.com/openai/openai-python")
    print()
    print("Useful commands:")
    print("  • Show details: pip show openai")
    print("  • List versions: pip index versions openai")
    print("  • Force reinstall: pip install --force-reinstall openai")
    print()
    print("Remember: Always check latest documentation!")
    print("  The API evolves rapidly - verify syntax before implementing.")
    print()

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
