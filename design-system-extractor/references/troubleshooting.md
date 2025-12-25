# Troubleshooting Guide

Common errors and solutions for the Design System Extractor skill.

## Setup and Installation Errors

### Error: `ModuleNotFoundError: No module named 'playwright'`

**Cause**: Python dependencies not installed.

**Solution**:
```bash
# If in virtual environment
pip install -r scripts/requirements.txt

# If not in venv (not recommended)
pip install --user -r scripts/requirements.txt
```

### Error: `playwright._impl._errors.TargetClosedError: Browser closed`

**Cause**: Playwright browsers not installed.

**Solution**:
```bash
playwright install chromium
```

### Error: `OSError: [Errno 13] Permission denied`

**Cause**: Trying to install packages without proper permissions.

**Solution**:
1. **Recommended**: Use a virtual environment
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r scripts/requirements.txt
   ```

2. **Alternative**: Install with --user flag
   ```bash
   pip install --user -r scripts/requirements.txt
   ```

## extract_website_design.py Errors

### Error: `playwright._impl._errors.TimeoutError: Timeout 30000ms exceeded`

**Cause**: Website took too long to load or is blocking automation.

**Solution**:
1. Check if the website is accessible in your browser
2. Try a different URL or page on the same site
3. Some sites block automated browsers - try manual analysis instead

**Example recovery**:
```bash
# If stripe.com times out, try a simpler page
python scripts/extract_website_design.py https://stripe.com/about
```

### Error: `playwright._impl._errors.Error: net::ERR_NAME_NOT_RESOLVED`

**Cause**: Invalid URL or no internet connection.

**Solution**:
1. Verify the URL is correct and accessible
2. Check your internet connection
3. Ensure URL includes protocol (https://)

**Example fix**:
```bash
# Wrong
python scripts/extract_website_design.py stripe.com

# Correct
python scripts/extract_website_design.py https://stripe.com
```

### Error: `json.decoder.JSONDecodeError: Expecting value`

**Cause**: Script failed to extract valid data from website.

**Solution**:
1. Website may be JavaScript-heavy with delayed rendering
2. Try running again (some sites load inconsistently)
3. Fall back to manual analysis using screenshots

### Error: Empty JSON output `{}`

**Cause**: Website has minimal styling or uses external stylesheets not loaded.

**Solution**:
1. Verify the website renders properly in browser
2. Try a different page on the same domain
3. Extract manually from screenshots or design files

## extract_image_colors.py Errors

### Error: `FileNotFoundError: [Errno 2] No such file or directory`

**Cause**: Image file path is incorrect.

**Solution**:
1. Use absolute path: `~/Downloads/mockup.png`
2. Or relative path from current directory: `./mockup.png`
3. Verify file exists: `ls ~/Downloads/mockup.png`

**Example fix**:
```bash
# Wrong (spaces not handled)
python scripts/extract_image_colors.py ~/My Documents/mockup.png

# Correct
python scripts/extract_image_colors.py ~/Documents/mockup.png
# or
python scripts/extract_image_colors.py "$HOME/My Documents/mockup.png"
```

### Error: `PIL.UnidentifiedImageError: cannot identify image file`

**Cause**: Unsupported image format or corrupted file.

**Solution**:
1. Supported formats: PNG, JPEG, JPG, WebP, BMP, GIF
2. Convert image to PNG/JPEG using an image editor
3. Verify file isn't corrupted: `file ~/Downloads/mockup.png`

**Example**:
```bash
# If you have ImageMagick installed
convert mockup.webp mockup.png
python scripts/extract_image_colors.py mockup.png
```

### Error: `ValueError: n_samples=50 should be >= n_clusters=16`

**Cause**: Requesting more colors than pixels in image (very small image).

**Solution**:
Reduce the number of colors requested:
```bash
# Instead of 16 colors, try 8
python scripts/extract_image_colors.py small-icon.png 8 > colors.json
```

## normalize_tokens.py Errors

### Error: `json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes`

**Cause**: Invalid JSON input file from extraction step.

**Solution**:
1. Validate the JSON: `python -m json.tool extracted_data.json`
2. If validation fails, re-run the extraction script
3. Check extraction script didn't produce error messages

**Example debugging**:
```bash
# Check if JSON is valid
python -m json.tool extracted_data.json > /dev/null

# If valid, this prints nothing. If invalid, shows error location
```

### Error: `KeyError: 'colors'`

**Cause**: Extraction data is missing required fields.

**Solution**:
The normalization script expects certain fields. Create minimal valid input:
```json
{
  "colors": [],
  "typography": {},
  "spacing": [],
  "borderRadius": [],
  "shadows": []
}
```

Then re-run normalization - it will fill in defaults.

### Error: `yaml.representer.RepresenterError`

**Cause**: Data contains non-serializable objects.

**Solution**:
1. Check extracted_data.json for unusual values
2. Re-run extraction script
3. Manually edit extracted_data.json to remove problematic values

## generate_components.py Errors

### Error: `yaml.scanner.ScannerError: while scanning for the next token`

**Cause**: Invalid YAML syntax in tokens.yaml file.

**Solution**:
1. Validate YAML: `python -c "import yaml; yaml.safe_load(open('tokens.yaml'))"`
2. Check for indentation errors (use spaces, not tabs)
3. Re-run normalization script

**Example validation**:
```bash
# This command validates YAML syntax
python -c "import yaml; yaml.safe_load(open('tokens.yaml'))" && echo "✓ Valid YAML" || echo "✗ Invalid YAML"
```

### Error: `KeyError: 'colors'` or other missing token categories

**Cause**: tokens.yaml is incomplete or malformed.

**Solution**:
1. Re-run the normalization script on your extracted data
2. Ensure normalization completed successfully
3. Check tokens.yaml contains all required sections:
   - colors
   - typography
   - spacing
   - borderRadius
   - shadows

## Platform-Specific Issues

### macOS: `zsh: command not found: playwright`

**Cause**: Playwright CLI not in PATH or venv not activated.

**Solution**:
```bash
# If using venv
source venv/bin/activate

# Then try again
playwright install chromium
```

### Linux: `Error: Failed to install browsers`

**Cause**: Missing system dependencies for Chromium.

**Solution**:
```bash
# Ubuntu/Debian
sudo apt-get install -y \
  libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
  libcups2 libdrm2 libxkbcommon0 libxcomposite1 \
  libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2

# Then retry
playwright install chromium
```

### Windows: Path with spaces issues

**Cause**: Spaces in file paths not properly quoted.

**Solution**:
```bash
# Use quotes around paths
python scripts/extract_image_colors.py "C:\Users\Name\My Documents\mockup.png"
```

## General Debugging Tips

### Enable verbose output

Add `--verbose` or check script output:
```bash
# For Python scripts, run with -v flag if supported
python -v scripts/extract_website_design.py https://example.com
```

### Check versions
```bash
python --version  # Should be 3.9+
pip list | grep -E "(playwright|Pillow|numpy|scikit-learn|PyYAML)"
```

### Test with known-good inputs

Try these reliable test cases:
```bash
# Simple website (usually works)
python scripts/extract_website_design.py https://example.com

# Test image (create a simple PNG first)
python scripts/extract_image_colors.py test.png 8
```

### When all else fails

1. **Re-create virtual environment**:
   ```bash
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install -r scripts/requirements.txt
   playwright install chromium
   ```

2. **Use manual analysis**: Extract colors, typography, and spacing manually using Claude's image viewing capability and create a minimal design system using defaults from `references/design-tokens-guide.md`.

3. **Check network connectivity**: Some scripts require internet access to work properly.

## Getting Help

If you encounter an error not listed here:

1. **Check the error message carefully** - it often contains the solution
2. **Run validation steps** - Validate JSON/YAML at each stage
3. **Try with simpler inputs** - Use example.com or a simple PNG
4. **Check your environment** - Ensure Python 3.9+, dependencies installed
5. **Use manual fallback** - Create design tokens manually using reference guides
