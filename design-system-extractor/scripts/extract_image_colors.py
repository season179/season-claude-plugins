#!/usr/bin/env python3
"""
Extract color palette from an image (screenshot, design mockup, etc.)
Uses K-means clustering to find dominant colors.
"""

import sys
import json
import os
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter

def rgb_to_hex(rgb):
    """Convert RGB tuple to hex string"""
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def hex_to_rgb(hex_color):
    """Convert hex string to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def calculate_brightness(rgb):
    """Calculate perceived brightness of a color (0-255)"""
    # Using perceived brightness formula
    r, g, b = rgb
    return (0.299 * r + 0.587 * g + 0.114 * b)

def is_grayscale(rgb, threshold=15):
    """Check if a color is grayscale (low saturation)"""
    r, g, b = rgb
    return abs(r - g) < threshold and abs(g - b) < threshold and abs(r - b) < threshold

def extract_colors_from_image(image_path, num_colors=16, sample_fraction=0.1):
    """
    Extract dominant colors from an image.
    """
    try:
        # Validate file exists
        if not os.path.exists(image_path):
            return {
                'error': f'File not found: {image_path}',
                'suggestion': 'Check the file path is correct'
            }
        
        # Load and resize image for faster processing
        try:
            img = Image.open(image_path)
        except Exception as e:
            return {
                'error': f'Cannot open image: {str(e)}',
                'suggestion': 'Ensure file is a valid image format (PNG, JPG, etc.)'
            }
        
        img = img.convert('RGB')
        
        # Sample pixels for performance
        width, height = img.size
        max_dimension = 800
        if width > max_dimension or height > max_dimension:
            ratio = min(max_dimension / width, max_dimension / height)
            new_size = (int(width * ratio), int(height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Get pixel data
        pixels = np.array(img)
        pixels = pixels.reshape(-1, 3)
        
        # Sample pixels
        if sample_fraction < 1.0:
            sample_size = int(len(pixels) * sample_fraction)
            indices = np.random.choice(len(pixels), sample_size, replace=False)
            pixels = pixels[indices]
        
        # Remove pure black and pure white (often backgrounds)
        pixels = pixels[~((pixels == [0, 0, 0]).all(axis=1) | (pixels == [255, 255, 255]).all(axis=1))]
        
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init=10)
        kmeans.fit(pixels)
        
        # Get cluster centers (dominant colors)
        colors = kmeans.cluster_centers_
        
        # Get cluster sizes (color frequency)
        labels = kmeans.labels_
        label_counts = Counter(labels)
        
        # Sort colors by frequency
        color_freq = []
        for i in range(num_colors):
            color = colors[i]
            count = label_counts[i]
            percentage = (count / len(labels)) * 100
            
            color_freq.append({
                'rgb': [int(c) for c in color],
                'hex': rgb_to_hex(color),
                'percentage': round(percentage, 2),
                'brightness': round(calculate_brightness(color), 2),
                'is_grayscale': is_grayscale(color)
            })
        
        # Sort by percentage
        color_freq.sort(key=lambda x: x['percentage'], reverse=True)
        
        # Categorize colors
        categorized = categorize_colors(color_freq)
        
        return {
            'total_colors': num_colors,
            'all_colors': color_freq,
            'categorized': categorized
        }
        
    except Exception as e:
        return {'error': str(e)}

def categorize_colors(colors):
    """Categorize colors into primary, neutral, and accent"""
    
    grayscale = []
    chromatic = []
    
    for color in colors:
        if color['is_grayscale']:
            grayscale.append(color)
        else:
            chromatic.append(color)
    
    # Sort grayscale by brightness
    grayscale.sort(key=lambda x: x['brightness'])
    
    # Identify potential primary color (most common chromatic color)
    primary_candidates = [c for c in chromatic if c['percentage'] > 5]
    primary = primary_candidates[0] if primary_candidates else (chromatic[0] if chromatic else None)
    
    # Other chromatic colors are accents
    accents = [c for c in chromatic if c != primary]
    
    return {
        'primary': primary,
        'grayscale': grayscale,
        'accents': accents
    }

def generate_color_scale(base_hex, name="primary"):
    """Generate a color scale (50-950) from a base color"""
    base_rgb = hex_to_rgb(base_hex)
    base_brightness = calculate_brightness(base_rgb)
    
    # Generate lighter and darker variants
    scale = {}
    
    # 500 is the base color
    scale[500] = base_hex
    
    # Generate lighter variants (50-400)
    for step in [50, 100, 200, 300, 400]:
        factor = 1 + ((500 - step) / 500) * 0.7  # Lighten
        new_rgb = tuple(min(255, int(c * factor)) for c in base_rgb)
        scale[step] = rgb_to_hex(new_rgb)
    
    # Generate darker variants (600-950)
    for step in [600, 700, 800, 900, 950]:
        factor = 1 - ((step - 500) / 450) * 0.8  # Darken
        new_rgb = tuple(max(0, int(c * factor)) for c in base_rgb)
        scale[step] = rgb_to_hex(new_rgb)
    
    return scale

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python extract_image_colors.py <image_path> [num_colors]")
        sys.exit(1)
    
    image_path = sys.argv[1]
    num_colors = int(sys.argv[2]) if len(sys.argv) > 2 else 16
    
    result = extract_colors_from_image(image_path, num_colors)
    
    # If successful, also generate color scales for primary colors
    if 'error' not in result and result['categorized']['primary']:
        primary_hex = result['categorized']['primary']['hex']
        result['color_scales'] = {
            'primary': generate_color_scale(primary_hex, 'primary')
        }
    
    print(json.dumps(result, indent=2))
