# Troubleshooting Guide

Common issues and solutions when using the website theme generator.

## Installation Issues

### Problem: "playwright: command not found"

**Cause**: Playwright Python package is not installed.

**Solution**:
```bash
pip install playwright
```

For system-wide installation without virtual environment:
```bash
pip install playwright --break-system-packages
```

---

### Problem: "Browser executable not found"

**Cause**: Playwright is installed but the Chromium browser hasn't been downloaded.

**Solution**:
```bash
playwright install chromium
```

To install all browsers (Chromium, Firefox, WebKit):
```bash
playwright install
```

---

### Problem: "Permission denied" during installation

**Cause**: Insufficient permissions to install packages or browsers.

**Solutions**:

**macOS/Linux**:
```bash
# Use --user flag
pip install --user playwright
playwright install

# Or use sudo (not recommended)
sudo pip install playwright
sudo playwright install
```

**Windows** (run as Administrator):
```powershell
pip install playwright
playwright install
```

---

### Problem: "Python version incompatible"

**Cause**: Playwright requires Python 3.8 or higher.

**Check your version**:
```bash
python --version
# or
python3 --version
```

**Solution**: Upgrade Python to 3.8+ from [python.org](https://www.python.org/downloads/)

---

## Analysis Script Issues

### Problem: Timeout errors ("Navigation timeout exceeded")

**Cause**: Website is slow to load or has many resources.

**Solutions**:

**Increase timeout** (edit `analyze_website.py` line 163):
```python
await page.goto(url, wait_until='networkidle', timeout=60000)  # 60 seconds instead of 30
```

**Use different wait strategy**:
```python
# Instead of 'networkidle', use 'domcontentloaded' (faster but may miss dynamic content)
await page.goto(url, wait_until='domcontentloaded', timeout=30000)
```

**Check your internet connection**:
```bash
ping google.com
# Ensure you have stable internet access
```

---

### Problem: Empty or minimal color data

**Cause**: JavaScript-heavy single-page application (SPA) that renders content after page load.

**Symptoms**:
- `analysis.json` shows very few colors
- `most_common_colors` has only 1-2 entries
- Screenshots look mostly empty

**Solutions**:

**Add wait time for JavaScript rendering** (edit `analyze_website.py` after `page.goto`):
```python
await page.goto(url, wait_until='networkidle', timeout=30000)

# Add this:
await page.wait_for_timeout(3000)  # Wait 3 seconds for SPA to render
```

**Wait for specific selector** (if you know the main content selector):
```python
await page.goto(url, wait_until='networkidle')
await page.wait_for_selector('.main-content', timeout=10000)
```

**Scroll to trigger lazy loading**:
```python
# Add after page.goto
await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
await page.wait_for_timeout(2000)
```

---

### Problem: Font names are generic or show "undefined"

**Cause**: Fonts are loaded via web font services (Google Fonts, Adobe Fonts) after initial page load.

**Symptoms**:
- Fonts array shows only system fonts: `["sans-serif", "serif"]`
- Or shows fallback stacks without the actual web font

**Solutions**:

**Wait for fonts to load** (edit `analyze_website.py`):
```python
await page.goto(url, wait_until='networkidle')

# Add this:
await page.evaluate('document.fonts.ready')  # Wait for font loading
```

**Manual inspection**:
- Open the screenshot and visually identify the fonts
- Use browser DevTools on the actual site to inspect font families
- Check the site's Network tab for font file names (e.g., `Inter-Regular.woff2`)

---

### Problem: Spacing data is noisy with too many values

**Cause**: Inline styles, auto-computed values, and browser defaults create many unique spacing values.

**Symptoms**:
- `most_common_spacing` has values like `13.5px`, `17.3333px`
- Too many unique values to identify a pattern

**Solutions**:

**Round spacing values** (modify `analyze_spacing` function in `analyze_website.py`):
```python
# Round to nearest multiple of 4
def round_to_multiple(value, multiple=4):
    return multiple * round(value / multiple)

# In analyze_spacing function:
rounded_values = [round_to_multiple(px_val) for px_val in px_values]
spacing_counter = Counter(rounded_values)
```

**Filter out uncommon values**:
- Focus only on values that appear 5+ times
- Ignore outliers (extremely large or small values)

**Look for patterns** in the top 5-7 most common values:
- Often you'll see: 8, 16, 24, 32, 48
- Ignore the noise and extrapolate a sensible scale

---

### Problem: "SSL certificate verification failed"

**Cause**: Website uses self-signed certificate or there's a MITM proxy.

**Solution**:

**Disable SSL verification** (ONLY for trusted internal sites):
```python
# In analyze_website.py, modify browser launch:
browser = await p.chromium.launch(ignore_https_errors=True)
```

**Warning**: Only use this for sites you trust (e.g., internal company sites).

---

### Problem: Screenshots are blank or mostly empty

**Cause**: Content loads after screenshot is captured, or viewport is too small.

**Solutions**:

**Increase viewport size** (edit `analyze_website.py`):
```python
page = await browser.new_page()

# Add this:
await page.set_viewport_size({"width": 1920, "height": 1080})
```

**Wait longer before capturing**:
```python
await page.goto(url, wait_until='networkidle')
await page.wait_for_timeout(5000)  # Wait 5 seconds
await page.screenshot(path=screenshot_full, full_page=True)
```

**Check for lazy loading**:
```python
# Scroll to bottom to trigger lazy-loaded images
await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
await page.wait_for_timeout(2000)
await page.screenshot(path=screenshot_full, full_page=True)
```

---

## Network & Connectivity Issues

### Problem: "net::ERR_NAME_NOT_RESOLVED"

**Cause**: DNS resolution failure (invalid URL or network issue).

**Solutions**:

**Check the URL**:
- Ensure URL starts with `http://` or `https://`
- Verify the domain name is spelled correctly
- Test the URL in a regular browser first

**Check internet connection**:
```bash
ping google.com
curl https://example.com
```

**Try a different network**:
- Switch from WiFi to ethernet or vice versa
- Disable VPN if active

---

### Problem: "Error 403: Forbidden" or "Error 429: Too Many Requests"

**Cause**: Website is blocking automated access or rate limiting.

**Symptoms**:
- Analysis fails with 403 or 429 error
- Screenshot shows "Access Denied" page

**Solutions**:

**Wait and retry**:
- Website may have rate limits
- Wait 5-10 minutes before retrying

**Check robots.txt**:
```bash
curl https://example.com/robots.txt
```
- If you see `Disallow: /`, the site prohibits scraping
- Respect these directives

**Accept the limitation**:
- Some sites actively block automated access
- Use manual screenshot and color picker tools instead
- See `SECURITY.md` for ethical scraping guidelines

---

### Problem: "Error 404: Not Found"

**Cause**: URL doesn't exist or has changed.

**Solutions**:

**Verify the URL** in a browser:
- Page may have moved or been deleted
- Try the site's homepage instead

**Check for redirects**:
- Some URLs redirect to other pages
- Playwright will follow redirects automatically

---

## Data Quality Issues

### Problem: Too many neutral colors, can't identify brand colors

**Symptom**: Top 10 colors are all grays, whites, and blacks.

**Solutions**:

**Manual filtering**:
- Skip the first 5-8 colors in `most_common_colors` (usually neutrals)
- Look for the first saturated color in the list
- Examine the screenshot to identify brand colors visually

**Color picker from screenshot**:
- Open `screenshot_viewport.png` in an image editor
- Use eyedropper tool to pick brand colors directly
- Verify against analysis data for confirmation

---

### Problem: Border radius values are inconsistent

**Symptom**: `border_radius` array has values like `"8px 8px 0px 0px"`, `"16px 4px 16px 4px"`.

**Solution**:

**Look for patterns**:
- Values like `"8px 8px 0px 0px"` mean top corners are rounded (8px)
- Values like `"16px"` are consistent all around
- Group similar values: all 8px variations → small, all 16px variations → medium

**Simplify in your theme**:
- Ignore complex multi-value radius
- Focus on most common single values (4px, 8px, 16px)
- Create simple scale (sm, md, lg, full)

---

## Script Execution Issues

### Problem: "ModuleNotFoundError: No module named 'playwright'"

**Cause**: Running script with wrong Python interpreter.

**Solutions**:

**Check which Python is running**:
```bash
which python
which python3
```

**Ensure Playwright is installed for the correct Python**:
```bash
python3 -m pip install playwright
python3 scripts/analyze_website.py <url>
```

**Use virtual environment** (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install playwright
playwright install chromium
python scripts/analyze_website.py <url>
```

---

### Problem: "SyntaxError: invalid syntax" on async/await

**Cause**: Python version is too old (< 3.5).

**Solution**: Upgrade to Python 3.8+ as required by Playwright.

---

### Problem: "RuntimeError: Event loop is closed"

**Cause**: Playwright's async code conflicts with existing event loop.

**Solution**:

**Run script directly** (not in Jupyter or interactive Python):
```bash
python scripts/analyze_website.py <url>
```

**If in Jupyter notebook**, use different async approach:
```python
import nest_asyncio
nest_asyncio.apply()

await analyze_website(url)
```

---

## Output Issues

### Problem: JSON is malformed or incomplete

**Symptom**: `analysis.json` can't be opened or is missing data.

**Solutions**:

**Check for script errors**:
```bash
python scripts/analyze_website.py <url> ./output 2>&1 | tee error.log
```

**Verify output directory exists and is writable**:
```bash
mkdir -p ./output
chmod 755 ./output
```

**Re-run analysis**:
- Previous run may have been interrupted
- Delete incomplete `analysis.json` and re-run

---

### Problem: Screenshots are in wrong directory

**Cause**: Output directory path is relative, and current working directory is different.

**Solution**:

**Use absolute paths**:
```bash
python scripts/analyze_website.py https://example.com /Users/username/analysis
```

**Or change to script directory first**:
```bash
cd /path/to/website-theme-generator
python scripts/analyze_website.py <url> ./output
```

---

## Still Having Issues?

### Steps to get help:

1. **Check error messages carefully**:
   - Copy the full error text
   - Note which line of code failed

2. **Test with known-good site**:
   ```bash
   python scripts/analyze_website.py https://example.com ./test_output
   ```
   - If this works, issue is with your target URL
   - If this fails, issue is with installation/environment

3. **Verify installation**:
   ```bash
   python --version  # Should be 3.8+
   pip list | grep playwright  # Should show playwright version
   playwright --version  # Should show version number
   ```

4. **Create minimal test case**:
   - Try simplest possible usage
   - Eliminate variables one by one

5. **Check file permissions**:
   - Ensure output directory is writable
   - Check that scripts have execute permissions

6. **Review logs**:
   - Capture full output including stderr
   - Look for warnings before the error

### Reporting Bugs

If you've exhausted troubleshooting steps:

**Include this information**:
- Python version (`python --version`)
- Playwright version (`pip list | grep playwright`)
- Operating system
- Full error message and stack trace
- URL being analyzed (if public)
- Steps to reproduce
- Screenshot of terminal output

---

## Performance Tips

### Slow Analysis

**If analysis takes > 60 seconds**:

1. **Check website size**:
   - Large sites with many resources load slowly
   - E-commerce sites with many images take longer

2. **Disable full-page screenshot**:
   ```python
   # Comment out in analyze_website.py:
   # await page.screenshot(path=screenshot_full, full_page=True)
   ```
   - Full-page screenshots of long pages take time
   - Viewport screenshot is usually sufficient

3. **Use faster wait strategy**:
   ```python
   await page.goto(url, wait_until='domcontentloaded')  # Instead of 'networkidle'
   ```

4. **Skip unnecessary elements**:
   - Modify extraction functions to only query visible elements
   - Use `document.querySelector Selector('.main-content *')` instead of `document.querySelectorAll('*')`

### Memory Usage

**If browser uses too much RAM**:

1. **Close other applications**
2. **Reduce viewport size** (smaller screenshots use less memory)
3. **Analyze one site at a time** (don't run multiple instances)
4. **Restart between analyses** if doing batch processing

---

## Quick Reference

| Issue | Quick Fix |
|-------|-----------|
| Playwright not found | `pip install playwright` |
| Browser not found | `playwright install chromium` |
| Timeout error | Increase timeout in script line 163 |
| Empty colors | Add wait time after page.goto |
| Generic fonts | Add `await page.evaluate('document.fonts.ready')` |
| Noisy spacing | Round values or focus on top 5 |
| Blank screenshot | Increase viewport size, wait longer |
| 403/429 error | Wait and retry, check robots.txt |
| Wrong Python version | Use Python 3.8+ |

---

For security and privacy concerns, see `SECURITY.md`.

For comprehensive technical documentation, see `REFERENCE.md`.
