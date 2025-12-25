#!/bin/bash
# Setup script for Design System Extractor skill
# Installs all required dependencies using best practices

echo "🎨 Setting up Design System Extractor..."
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found"
    echo "   Please install Python 3.9 or later"
    exit 1
fi

echo "✓ Python 3 found ($(python3 --version))"
echo ""

# Get the directory where the script is located
SCRIPT_DIR="$(dirname "$0")"
REQUIREMENTS_FILE="$SCRIPT_DIR/requirements.txt"

# Check if we're in a virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Not running in a virtual environment"
    echo ""
    echo "It's strongly recommended to use a virtual environment to avoid conflicts."
    echo ""
    echo "To create and activate a virtual environment:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
    echo "  bash $0"
    echo ""

    read -p "Continue installing without virtual environment? [y/N] " -n 1 -r
    echo

    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled. Please create a virtual environment first."
        exit 0
    fi

    echo ""
    echo "📦 Installing Python dependencies globally..."

    # Try different installation methods in order of safety
    if pip3 install -r "$REQUIREMENTS_FILE" 2>/dev/null; then
        echo "✓ Installed using pip3"
    elif pip3 install --user -r "$REQUIREMENTS_FILE" 2>/dev/null; then
        echo "✓ Installed using pip3 --user"
    elif pip3 install --break-system-packages -r "$REQUIREMENTS_FILE" 2>/dev/null; then
        echo "⚠️  Installed using --break-system-packages (not recommended)"
        echo "   Consider using a virtual environment in the future"
    else
        echo "❌ Failed to install Python dependencies"
        echo "   Please try creating a virtual environment:"
        echo "     python3 -m venv venv"
        echo "     source venv/bin/activate"
        echo "     pip install -r $REQUIREMENTS_FILE"
        exit 1
    fi
else
    echo "✓ Virtual environment detected: $VIRTUAL_ENV"
    echo ""
    echo "📦 Installing Python dependencies..."

    if pip install -r "$REQUIREMENTS_FILE"; then
        echo "✓ Python dependencies installed"
    else
        echo "❌ Failed to install Python dependencies"
        echo "   Check the error message above and try:"
        echo "     pip install --upgrade pip"
        echo "     pip install -r $REQUIREMENTS_FILE"
        exit 1
    fi
fi

echo ""
echo "🌐 Installing Playwright browsers..."

if playwright install chromium; then
    echo "✓ Playwright browsers installed"
else
    echo "❌ Failed to install Playwright browsers"
    echo "   Try manually: playwright install chromium"
    exit 1
fi

echo ""
echo "✅ Setup complete! You can now use the Design System Extractor skill."
echo ""
echo "Test extraction with:"
echo "  python $SCRIPT_DIR/extract_website_design.py https://example.com"
echo ""

if [ -z "$VIRTUAL_ENV" ]; then
    echo "💡 Tip: For future use, consider setting up a virtual environment"
    echo "   to keep your system Python clean and organized."
fi
