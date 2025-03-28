#!/usr/bin/env python3
"""
Script to enhance the visibility of the legend in switch SVG files.
This script modifies existing SVG files to make the legend more prominent.
"""

import re
import sys

def enhance_legend(svg_file):
    """
    Enhance the visibility of the legend in an SVG file.
    
    Args:
        svg_file: Path to the SVG file to modify
    """
    # Read the SVG file
    with open(svg_file, 'r') as f:
        svg_content = f.read()
    
    # Check if the file starts with XML declaration and SVG tag
    xml_decl = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
    svg_start = '<svg'
    
    if not svg_content.startswith(xml_decl):
        print(f"Warning: SVG file {svg_file} does not start with XML declaration")
        if not svg_content.startswith(svg_start):
            print(f"Error: SVG file {svg_file} does not start with SVG tag")
            return
    
    # Find the SVG dimensions
    width_match = re.search(r'<svg width="(\d+)" height="(\d+)"', svg_content)
    if not width_match:
        print(f"Error: Could not find SVG dimensions in {svg_file}")
        return
    
    width = int(width_match.group(1))
    height = int(width_match.group(2))
    
    # Find the legend section
    legend_match = re.search(r'(<!-- Legend -->.*?)<g id="port-1">', svg_content, re.DOTALL)
    if not legend_match:
        # Try another pattern if the first one doesn't match
        legend_match = re.search(r'(<!-- Legend -->.*?)$', svg_content, re.DOTALL)
        if not legend_match:
            print(f"Error: Could not find legend section in {svg_file}")
            return
    
    # Extract the theme color (text color)
    text_color_match = re.search(r'font-family="Arial" font-size="16" fill="(#[0-9a-fA-F]+)"', svg_content)
    if not text_color_match:
        print(f"Warning: Could not determine text color in {svg_file}, using default")
        text_color = "#000000"
    else:
        text_color = text_color_match.group(1)
    
    # Extract the background color
    bg_color_match = re.search(r'<rect x="0" y="0" width="\d+" height="\d+" fill="(#[0-9a-fA-F]+)" />', svg_content)
    if not bg_color_match:
        print(f"Warning: Could not determine background color in {svg_file}, using default")
        bg_color = "#ffffff"
    else:
        bg_color = bg_color_match.group(1)
    
    # Determine contrasting color for legend background
    # If background is light, use a slightly darker shade; if dark, use a slightly lighter shade
    if bg_color.lower() in ["#ffffff", "#d3d3d3", "#f0f0f0", "#e0e0e0"]:
        # Light background - use a slightly darker shade
        legend_bg_color = "#c0c0c0"
    else:
        # Dark background - use a slightly lighter shade
        legend_bg_color = "#4a5c70"
    
    # Create enhanced legend section
    # 1. Add a background rectangle for the legend
    # 2. Increase the font size for better visibility
    # 3. Add a border around the legend
    
    # Find all legend items
    legend_items = re.findall(r'<rect x="(\d+)" y="(\d+)" width="10" height="10" fill="([^"]+)" />\s*<text x="[^"]+" y="[^"]+" font-family="Arial" font-size="10" fill="[^"]+">([^<]+)</text>', svg_content)
    
    if not legend_items:
        print(f"Error: Could not find legend items in {svg_file}")
        return
    
    # Calculate legend dimensions
    legend_width = 600  # Fixed width for the legend
    legend_height = 60  # Fixed height for the legend
    legend_x = (width - legend_width) // 2  # Center horizontally
    legend_y = 160  # Fixed position below the switch
    
    # Create new legend section
    new_legend = f"""  <!-- Enhanced Legend -->
  <rect x="{legend_x}" y="{legend_y}" width="{legend_width}" height="{legend_height}" fill="{legend_bg_color}" rx="5" ry="5" stroke="{text_color}" stroke-width="1" />
  <text x="{legend_x + 10}" y="{legend_y + 20}" font-family="Arial" font-size="14" font-weight="bold" fill="{text_color}">Legend:</text>
"""
    
    # Add legend items in a horizontal layout
    item_spacing = legend_width // (len(legend_items) + 1)
    for i, (_, _, color, label) in enumerate(legend_items):
        item_x = legend_x + (i + 1) * item_spacing - 50  # Distribute evenly
        item_y = legend_y + 40  # Fixed vertical position
        
        new_legend += f"""  <rect x="{item_x}" y="{item_y - 10}" width="15" height="15" fill="{color}" stroke="{text_color}" stroke-width="0.5" />
  <text x="{item_x + 20}" y="{item_y}" font-family="Arial" font-size="12" fill="{text_color}">{label}</text>
"""
    
    # Replace the old legend section with the new one
    if legend_match:
        old_legend = legend_match.group(1)
        svg_content = svg_content.replace(old_legend, new_legend)
        
    # Ensure the SVG has a closing tag
    if not svg_content.strip().endswith('</svg>'):
        svg_content = svg_content.rstrip() + '\n</svg>'
    
    # Write the modified SVG file
    output_file = svg_file.replace('.svg', '_enhanced.svg')
    
    # Create a completely new SVG file with the correct XML declaration and SVG tag
    with open(svg_file, 'r') as f:
        original_content = f.read()
    
    # Extract the SVG attributes
    svg_attrs_match = re.search(r'<svg\s+([^>]+)>', original_content)
    if not svg_attrs_match:
        print(f"Error: Could not extract SVG attributes from {svg_file}")
        return
    
    svg_attrs = svg_attrs_match.group(1)
    
    # Create the new SVG content with the correct XML declaration and SVG tag
    new_svg_content = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg {svg_attrs}>
{svg_content.split('<svg ' + svg_attrs + '>', 1)[1] if '<svg ' + svg_attrs + '>' in svg_content else svg_content.split('<svg', 1)[1].split('>', 1)[1]}"""
    
    with open(output_file, 'w') as f:
        f.write(new_svg_content)
    
    print(f"Enhanced legend saved to {output_file}")

def main():
    """Process SVG files to enhance legend visibility."""
    if len(sys.argv) < 2:
        print("Usage: python enhance_legend_visibility.py <svg_file1> [svg_file2 ...]")
        print("Using default files: consistent_light_switch.svg and consistent_dark_switch.svg")
        svg_files = ["consistent_light_switch.svg", "consistent_dark_switch.svg"]
    else:
        svg_files = sys.argv[1:]
    
    for svg_file in svg_files:
        enhance_legend(svg_file)

if __name__ == "__main__":
    main()
