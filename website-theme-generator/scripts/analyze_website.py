#!/usr/bin/env python3
"""
Website Design Analyzer using Playwright
Visits a website, captures screenshots, and extracts design information.
"""

import sys
import json
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
import re
from collections import Counter

async def extract_colors_from_computed_styles(page):
    """Extract colors from computed styles of various elements"""
    colors = await page.evaluate("""
        () => {
            const colors = new Set();
            const elements = document.querySelectorAll('*');
            
            elements.forEach(el => {
                const styles = window.getComputedStyle(el);
                
                // Extract colors
                ['color', 'backgroundColor', 'borderColor', 'borderTopColor', 
                 'borderRightColor', 'borderBottomColor', 'borderLeftColor'].forEach(prop => {
                    const value = styles[prop];
                    if (value && value !== 'rgba(0, 0, 0, 0)' && value !== 'transparent') {
                        colors.add(value);
                    }
                });
            });
            
            return Array.from(colors);
        }
    """)
    return colors

async def extract_fonts(page):
    """Extract font families used on the page"""
    fonts = await page.evaluate("""
        () => {
            const fonts = new Set();
            const elements = document.querySelectorAll('*');
            
            elements.forEach(el => {
                const styles = window.getComputedStyle(el);
                const fontFamily = styles.fontFamily;
                if (fontFamily) {
                    fonts.add(fontFamily);
                }
            });
            
            return Array.from(fonts);
        }
    """)
    return fonts

async def extract_spacing_patterns(page):
    """Extract common spacing patterns (margins, padding)"""
    spacing = await page.evaluate("""
        () => {
            const spacings = [];
            const elements = document.querySelectorAll('*');
            
            elements.forEach(el => {
                const styles = window.getComputedStyle(el);
                ['marginTop', 'marginRight', 'marginBottom', 'marginLeft',
                 'paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft'].forEach(prop => {
                    const value = styles[prop];
                    if (value && value !== '0px') {
                        spacings.push(value);
                    }
                });
            });
            
            return spacings;
        }
    """)
    return spacing

async def extract_border_radius(page):
    """Extract border radius values"""
    radii = await page.evaluate("""
        () => {
            const radii = new Set();
            const elements = document.querySelectorAll('*');
            
            elements.forEach(el => {
                const styles = window.getComputedStyle(el);
                const radius = styles.borderRadius;
                if (radius && radius !== '0px') {
                    radii.add(radius);
                }
            });
            
            return Array.from(radii);
        }
    """)
    return radii

def rgb_to_hex(rgb_str):
    """Convert rgb/rgba string to hex"""
    match = re.match(r'rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*[\d.]+)?\)', rgb_str)
    if match:
        r, g, b = match.groups()
        return f"#{int(r):02x}{int(g):02x}{int(b):02x}"
    return rgb_str

def analyze_colors(colors):
    """Analyze and categorize colors"""
    hex_colors = []
    for color in colors:
        if color.startswith('rgb'):
            hex_colors.append(rgb_to_hex(color))
        elif color.startswith('#'):
            hex_colors.append(color)
    
    # Count occurrences
    color_counter = Counter(hex_colors)
    most_common = color_counter.most_common(10)
    
    return {
        'total_unique_colors': len(hex_colors),
        'most_common_colors': [{'color': color, 'count': count} for color, count in most_common]
    }

def analyze_spacing(spacing_values):
    """Analyze spacing patterns"""
    # Extract numeric values
    px_values = []
    for value in spacing_values:
        match = re.match(r'([\d.]+)px', value)
        if match:
            px_values.append(float(match.group(1)))
    
    if not px_values:
        return {}
    
    spacing_counter = Counter(px_values)
    most_common = spacing_counter.most_common(10)
    
    return {
        'most_common_spacing': [{'value': f"{value}px", 'count': count} for value, count in most_common]
    }

async def analyze_website(url, output_dir=None):
    """Main function to analyze a website"""
    if output_dir is None:
        output_dir = Path.cwd()
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        try:
            print(f"Visiting {url}...")
            await page.goto(url, wait_until='networkidle', timeout=30000)
            
            # Take screenshots
            screenshot_full = output_dir / "screenshot_full.png"
            screenshot_viewport = output_dir / "screenshot_viewport.png"
            
            await page.screenshot(path=screenshot_full, full_page=True)
            await page.screenshot(path=screenshot_viewport, full_page=False)
            print(f"Screenshots saved to {output_dir}")
            
            # Extract design information
            print("Extracting design information...")
            colors = await extract_colors_from_computed_styles(page)
            fonts = await extract_fonts(page)
            spacing = await extract_spacing_patterns(page)
            border_radii = await extract_border_radius(page)
            
            # Get page title
            title = await page.title()
            
            # Analyze the data
            color_analysis = analyze_colors(colors)
            spacing_analysis = analyze_spacing(spacing)
            
            # Compile results
            results = {
                'url': url,
                'title': title,
                'colors': {
                    'raw_colors': colors[:50],  # Limit to first 50
                    'analysis': color_analysis
                },
                'fonts': fonts,
                'spacing': {
                    'raw_spacing': spacing[:50],  # Limit to first 50
                    'analysis': spacing_analysis
                },
                'border_radius': border_radii,
                'screenshots': {
                    'full_page': str(screenshot_full),
                    'viewport': str(screenshot_viewport)
                }
            }
            
            # Save results
            results_file = output_dir / "analysis.json"
            with open(results_file, 'w') as f:
                json.dump(results, f, indent=2)
            
            print(f"Analysis complete! Results saved to {results_file}")
            return results
            
        except Exception as e:
            print(f"Error analyzing website: {e}", file=sys.stderr)
            raise
        finally:
            await browser.close()

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_website.py <url> [output_directory]")
        sys.exit(1)
    
    url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    asyncio.run(analyze_website(url, output_dir))

if __name__ == "__main__":
    main()
