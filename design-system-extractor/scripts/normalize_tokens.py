#!/usr/bin/env python3
"""
Normalize and organize extracted design tokens into a standardized YAML structure.
Takes raw extraction data and produces clean, organized design token definitions.
"""

import json
import sys
import yaml
import re
from collections import defaultdict

def px_to_rem(px_value, base=16):
    """Convert px to rem"""
    if isinstance(px_value, str):
        match = re.match(r'([\d.]+)px', px_value)
        if match:
            px = float(match.group(1))
            return f"{px / base}rem"
    return px_value

def normalize_spacing_scale(spacing_values):
    """Normalize spacing values to a standard scale"""
    # Convert all to rem and deduplicate
    rem_values = set()
    for val in spacing_values:
        rem_val = px_to_rem(val)
        if rem_val.endswith('rem'):
            rem_values.add(float(rem_val.replace('rem', '')))
    
    # Create standard scale (multiples of 0.25rem = 4px)
    standard_scale = [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1, 1.25, 1.5, 1.75, 2, 
                      2.25, 2.5, 2.75, 3, 3.5, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 20, 24]
    
    # Find closest matches from extracted values
    used_values = {}
    for rem in sorted(rem_values):
        # Find closest standard value
        closest = min(standard_scale, key=lambda x: abs(x - rem))
        if closest not in used_values:
            used_values[closest] = f"{closest}rem"
    
    # Ensure we have a basic scale
    basic_scale = {
        0: "0",
        0.125: "0.125rem",  # 2px
        0.25: "0.25rem",    # 4px
        0.5: "0.5rem",      # 8px
        0.75: "0.75rem",    # 12px
        1: "1rem",          # 16px
        1.5: "1.5rem",      # 24px
        2: "2rem",          # 32px
        3: "3rem",          # 48px
        4: "4rem",          # 64px
    }
    
    # Merge with extracted values
    final_scale = {**basic_scale, **used_values}
    
    # Convert to named scale (0.5 -> "0.5", 1 -> "1", etc.)
    named_scale = {}
    for key, value in sorted(final_scale.items()):
        if key == 0:
            named_scale["0"] = "0"
        elif key < 1:
            # Use decimal notation for sub-1 values
            named_scale[str(key)] = value
        else:
            # Use integer notation for >= 1 values
            named_scale[str(int(key)) if key == int(key) else str(key)] = value
    
    return named_scale

def normalize_typography(typography):
    """Normalize typography to standard scales"""
    
    # Standard font size scale
    font_sizes = {
        "xs": "0.75rem",    # 12px
        "sm": "0.875rem",   # 14px
        "base": "1rem",     # 16px
        "lg": "1.125rem",   # 18px
        "xl": "1.25rem",    # 20px
        "2xl": "1.5rem",    # 24px
        "3xl": "1.875rem",  # 30px
        "4xl": "2.25rem",   # 36px
        "5xl": "3rem",      # 48px
        "6xl": "3.75rem",   # 60px
        "7xl": "4.5rem",    # 72px
        "8xl": "6rem",      # 96px
        "9xl": "8rem"       # 128px
    }
    
    # Standard font weights
    font_weights = {
        "thin": "100",
        "extralight": "200",
        "light": "300",
        "normal": "400",
        "medium": "500",
        "semibold": "600",
        "bold": "700",
        "extrabold": "800",
        "black": "900"
    }
    
    # Standard line heights
    line_heights = {
        "none": "1",
        "tight": "1.25",
        "snug": "1.375",
        "normal": "1.5",
        "relaxed": "1.625",
        "loose": "2"
    }
    
    # Process font families
    font_families = {}
    if 'fontFamilies' in typography and typography['fontFamilies']:
        # Take the most common sans-serif
        for family in typography['fontFamilies']:
            if 'sans' not in font_families and any(x in family.lower() for x in ['sans', 'helvetica', 'arial', 'inter']):
                font_families['sans'] = family
            if 'serif' not in font_families and 'serif' in family.lower() and 'sans' not in family.lower():
                font_families['serif'] = family
            if 'mono' not in font_families and any(x in family.lower() for x in ['mono', 'courier', 'code', 'console']):
                font_families['mono'] = family
    
    # Defaults if not found
    if 'sans' not in font_families:
        font_families['sans'] = "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    if 'serif' not in font_families:
        font_families['serif'] = "'Merriweather', Georgia, serif"
    if 'mono' not in font_families:
        font_families['mono'] = "'JetBrains Mono', 'Courier New', monospace"
    
    return {
        'fontFamilies': font_families,
        'fontSizes': font_sizes,
        'fontWeights': font_weights,
        'lineHeights': line_heights
    }

def normalize_border_radius(radius_values):
    """Normalize border radius values"""
    standard_radii = {
        "none": "0",
        "sm": "0.125rem",   # 2px
        "base": "0.25rem",  # 4px
        "md": "0.375rem",   # 6px
        "lg": "0.5rem",     # 8px
        "xl": "0.75rem",    # 12px
        "2xl": "1rem",      # 16px
        "3xl": "1.5rem",    # 24px
        "full": "9999px"
    }
    return standard_radii

def normalize_shadows(shadow_values):
    """Normalize shadow values"""
    # If we have extracted shadows, categorize them by size
    # Otherwise, use standard shadows
    standard_shadows = {
        "sm": "0 1px 2px 0 rgb(0 0 0 / 0.05)",
        "base": "0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)",
        "md": "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
        "lg": "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)",
        "xl": "0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)",
        "2xl": "0 25px 50px -12px rgb(0 0 0 / 0.25)",
        "inner": "inset 0 2px 4px 0 rgb(0 0 0 / 0.05)",
        "none": "0 0 #0000"
    }
    return standard_shadows

def normalize_colors(colors):
    """Organize colors into primary, neutral, and semantic categories"""
    
    # Default semantic colors
    semantic_colors = {
        "success": "#10b981",
        "warning": "#f59e0b",
        "error": "#ef4444",
        "info": "#3b82f6"
    }
    
    # If we have extracted colors, try to find primary
    primary_scale = {}
    neutral_scale = {}
    
    if isinstance(colors, list) and colors:
        # Simple approach: first non-grayscale color is primary
        # Group grayscale colors separately
        chromatic = [c for c in colors if not is_grayscale_hex(c)]
        grayscale = [c for c in colors if is_grayscale_hex(c)]
        
        if chromatic:
            # Use first chromatic color as primary base
            primary_scale = generate_color_scale_from_hex(chromatic[0])
        
        if grayscale:
            neutral_scale = generate_grayscale_scale()
    
    # Ensure we have basic colors
    if not primary_scale:
        primary_scale = generate_color_scale_from_hex("#3b82f6")  # Default blue
    
    if not neutral_scale:
        neutral_scale = generate_grayscale_scale()
    
    return {
        "primary": primary_scale,
        "semantic": semantic_colors,
        "neutral": neutral_scale
    }

def is_grayscale_hex(hex_color):
    """Check if hex color is grayscale"""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return abs(r - g) < 15 and abs(g - b) < 15 and abs(r - b) < 15

def generate_color_scale_from_hex(base_hex):
    """Generate 50-950 color scale from a base color"""
    def hex_to_rgb(h):
        h = h.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_hex(r, g, b):
        return f"#{int(r):02x}{int(g):02x}{int(b):02x}"
    
    base_rgb = hex_to_rgb(base_hex)
    
    scale = {}
    scale["500"] = base_hex  # Base color at 500
    
    # Generate lighter variants
    for step in [50, 100, 200, 300, 400]:
        factor = 1 + ((500 - step) / 500) * 0.7
        new_rgb = tuple(min(255, c * factor) for c in base_rgb)
        scale[str(step)] = rgb_to_hex(*new_rgb)
    
    # Generate darker variants
    for step in [600, 700, 800, 900, 950]:
        factor = 1 - ((step - 500) / 450) * 0.8
        new_rgb = tuple(max(0, c * factor) for c in base_rgb)
        scale[str(step)] = rgb_to_hex(*new_rgb)
    
    return scale

def generate_grayscale_scale():
    """Generate standard grayscale palette"""
    return {
        "white": "#ffffff",
        "50": "#fafafa",
        "100": "#f5f5f5",
        "200": "#e5e5e5",
        "300": "#d4d4d4",
        "400": "#a3a3a3",
        "500": "#737373",
        "600": "#525252",
        "700": "#404040",
        "800": "#262626",
        "900": "#171717",
        "950": "#0a0a0a",
        "black": "#000000"
    }

def normalize_design_tokens(extracted_data):
    """Main function to normalize all design tokens"""
    
    tokens = {}
    
    # Colors
    colors = extracted_data.get('colors', [])
    tokens['colors'] = normalize_colors(colors)
    
    # Typography
    typography = extracted_data.get('typography', {})
    tokens['typography'] = normalize_typography(typography)
    
    # Spacing
    spacing = extracted_data.get('spacing', [])
    tokens['spacing'] = normalize_spacing_scale(spacing)
    
    # Border Radius
    border_radius = extracted_data.get('borderRadius', [])
    tokens['borderRadius'] = normalize_border_radius(border_radius)
    
    # Shadows
    shadows = extracted_data.get('shadows', [])
    tokens['shadows'] = normalize_shadows(shadows)
    
    # Breakpoints
    tokens['breakpoints'] = {
        "sm": "640px",
        "md": "768px",
        "lg": "1024px",
        "xl": "1280px",
        "2xl": "1536px"
    }
    
    # Transitions
    tokens['transitions'] = {
        "duration": {
            "fast": "150ms",
            "base": "300ms",
            "slow": "500ms"
        },
        "easing": {
            "linear": "linear",
            "in": "cubic-bezier(0.4, 0, 1, 1)",
            "out": "cubic-bezier(0, 0, 0.2, 1)",
            "inOut": "cubic-bezier(0.4, 0, 0.2, 1)"
        }
    }
    
    # Z-index
    tokens['zIndex'] = {
        "0": "0",
        "10": "10",
        "20": "20",
        "30": "30",
        "40": "40",
        "50": "50",
        "auto": "auto"
    }
    
    return tokens

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python normalize_tokens.py <extracted_data.json>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    with open(input_file, 'r') as f:
        extracted_data = json.load(f)
    
    normalized_tokens = normalize_design_tokens(extracted_data)
    
    # Output as YAML
    print(yaml.dump(normalized_tokens, default_flow_style=False, sort_keys=False))
