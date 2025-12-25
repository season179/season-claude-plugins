#!/usr/bin/env python3
"""
Extract design tokens from a website using Playwright.
Analyzes computed styles, colors, typography, spacing, and component patterns.
"""

import json
import sys
from collections import Counter
from playwright.sync_api import sync_playwright
import re

def extract_colors_from_styles(page):
    """Extract all colors used in the page"""
    colors = page.evaluate("""
        () => {
            const colors = new Set();
            const elements = document.querySelectorAll('*');
            
            elements.forEach(el => {
                const styles = window.getComputedStyle(el);
                
                // Extract colors from various properties
                const colorProps = [
                    'color', 'background-color', 'border-color', 
                    'border-top-color', 'border-right-color', 
                    'border-bottom-color', 'border-left-color',
                    'outline-color', 'fill', 'stroke'
                ];
                
                colorProps.forEach(prop => {
                    const value = styles.getPropertyValue(prop);
                    if (value && value !== 'transparent' && value !== 'rgba(0, 0, 0, 0)') {
                        colors.add(value);
                    }
                });
            });
            
            return Array.from(colors);
        }
    """)
    return colors

def extract_typography(page):
    """Extract typography information"""
    typography = page.evaluate("""
        () => {
            const fonts = new Set();
            const sizes = new Set();
            const weights = new Set();
            const lineHeights = new Set();
            
            const elements = document.querySelectorAll('*');
            
            elements.forEach(el => {
                const styles = window.getComputedStyle(el);
                
                const fontFamily = styles.getPropertyValue('font-family');
                const fontSize = styles.getPropertyValue('font-size');
                const fontWeight = styles.getPropertyValue('font-weight');
                const lineHeight = styles.getPropertyValue('line-height');
                
                if (fontFamily) fonts.add(fontFamily);
                if (fontSize) sizes.add(fontSize);
                if (fontWeight) weights.add(fontWeight);
                if (lineHeight && lineHeight !== 'normal') lineHeights.add(lineHeight);
            });
            
            return {
                fontFamilies: Array.from(fonts),
                fontSizes: Array.from(sizes),
                fontWeights: Array.from(weights),
                lineHeights: Array.from(lineHeights)
            };
        }
    """)
    return typography

def extract_spacing(page):
    """Extract spacing/padding/margin patterns"""
    spacing = page.evaluate("""
        () => {
            const spacings = new Set();
            const elements = document.querySelectorAll('*');
            
            elements.forEach(el => {
                const styles = window.getComputedStyle(el);
                
                const spacingProps = [
                    'padding-top', 'padding-right', 'padding-bottom', 'padding-left',
                    'margin-top', 'margin-right', 'margin-bottom', 'margin-left',
                    'gap', 'row-gap', 'column-gap'
                ];
                
                spacingProps.forEach(prop => {
                    const value = styles.getPropertyValue(prop);
                    if (value && value !== '0px' && value !== 'auto') {
                        spacings.add(value);
                    }
                });
            });
            
            return Array.from(spacings);
        }
    """)
    return spacing

def extract_border_radius(page):
    """Extract border radius values"""
    radii = page.evaluate("""
        () => {
            const radii = new Set();
            const elements = document.querySelectorAll('*');
            
            elements.forEach(el => {
                const styles = window.getComputedStyle(el);
                
                const radiusProps = [
                    'border-radius',
                    'border-top-left-radius',
                    'border-top-right-radius',
                    'border-bottom-left-radius',
                    'border-bottom-right-radius'
                ];
                
                radiusProps.forEach(prop => {
                    const value = styles.getPropertyValue(prop);
                    if (value && value !== '0px') {
                        radii.add(value);
                    }
                });
            });
            
            return Array.from(radii);
        }
    """)
    return radii

def extract_shadows(page):
    """Extract box shadow values"""
    shadows = page.evaluate("""
        () => {
            const shadows = new Set();
            const elements = document.querySelectorAll('*');
            
            elements.forEach(el => {
                const styles = window.getComputedStyle(el);
                const boxShadow = styles.getPropertyValue('box-shadow');
                
                if (boxShadow && boxShadow !== 'none') {
                    shadows.add(boxShadow);
                }
            });
            
            return Array.from(shadows);
        }
    """)
    return shadows

def extract_components(page):
    """Identify common UI component patterns"""
    components = page.evaluate("""
        () => {
            const components = [];
            
            // Look for buttons
            const buttons = document.querySelectorAll('button, [role="button"], a.btn, .button');
            if (buttons.length > 0) {
                const buttonStyles = [];
                buttons.forEach((btn, idx) => {
                    if (idx < 5) { // Sample first 5
                        const styles = window.getComputedStyle(btn);
                        buttonStyles.push({
                            backgroundColor: styles.backgroundColor,
                            color: styles.color,
                            padding: styles.padding,
                            borderRadius: styles.borderRadius,
                            fontSize: styles.fontSize,
                            fontWeight: styles.fontWeight,
                            border: styles.border
                        });
                    }
                });
                components.push({ type: 'button', count: buttons.length, samples: buttonStyles });
            }
            
            // Look for input fields
            const inputs = document.querySelectorAll('input[type="text"], input[type="email"], input[type="password"], textarea');
            if (inputs.length > 0) {
                const inputStyles = [];
                inputs.forEach((input, idx) => {
                    if (idx < 5) {
                        const styles = window.getComputedStyle(input);
                        inputStyles.push({
                            backgroundColor: styles.backgroundColor,
                            color: styles.color,
                            padding: styles.padding,
                            borderRadius: styles.borderRadius,
                            border: styles.border,
                            fontSize: styles.fontSize
                        });
                    }
                });
                components.push({ type: 'input', count: inputs.length, samples: inputStyles });
            }
            
            // Look for cards
            const cards = document.querySelectorAll('.card, [class*="card"], article');
            if (cards.length > 0) {
                const cardStyles = [];
                cards.forEach((card, idx) => {
                    if (idx < 5) {
                        const styles = window.getComputedStyle(card);
                        cardStyles.push({
                            backgroundColor: styles.backgroundColor,
                            padding: styles.padding,
                            borderRadius: styles.borderRadius,
                            boxShadow: styles.boxShadow,
                            border: styles.border
                        });
                    }
                });
                components.push({ type: 'card', count: cards.length, samples: cardStyles });
            }
            
            return components;
        }
    """)
    return components

def rgb_to_hex(rgb_string):
    """Convert rgb(r, g, b) to #rrggbb"""
    if rgb_string.startswith('#'):
        return rgb_string
    
    match = re.match(r'rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*[\d.]+)?\)', rgb_string)
    if match:
        r, g, b = map(int, match.groups())
        return f"#{r:02x}{g:02x}{b:02x}"
    return rgb_string

def normalize_colors(colors):
    """Convert all colors to hex and deduplicate"""
    hex_colors = set()
    for color in colors:
        hex_color = rgb_to_hex(color)
        hex_colors.add(hex_color)
    return sorted(list(hex_colors))

def extract_design_system(url):
    """Main function to extract design system from a URL"""
    with sync_playwright() as p:
        browser = None
        try:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Set reasonable timeout and user agent
            page.set_default_timeout(30000)
            
            try:
                page.goto(url, wait_until='networkidle', timeout=30000)
            except Exception as nav_error:
                # Fallback to domcontentloaded if networkidle fails
                try:
                    page.goto(url, wait_until='domcontentloaded', timeout=15000)
                except Exception:
                    return {
                        'error': f'Cannot access URL: {str(nav_error)}',
                        'suggestion': 'Check URL is valid and accessible'
                    }
            
            # Extract all design tokens
            colors = extract_colors_from_styles(page)
            typography = extract_typography(page)
            spacing = extract_spacing(page)
            border_radius = extract_border_radius(page)
            shadows = extract_shadows(page)
            components = extract_components(page)
            
            # Get viewport size for breakpoint reference
            viewport = page.viewport_size
            
            result = {
                'url': url,
                'colors': normalize_colors(colors),
                'typography': typography,
                'spacing': sorted(list(set(spacing))),
                'borderRadius': sorted(list(set(border_radius))),
                'shadows': list(set(shadows)),
                'components': components,
                'viewport': viewport
            }
            
            return result
            
        except Exception as e:
            return {
                'error': str(e),
                'suggestion': 'Try a different URL or check network connectivity'
            }
        finally:
            if browser:
                browser.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python extract_website_design.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    result = extract_design_system(url)
    print(json.dumps(result, indent=2))
