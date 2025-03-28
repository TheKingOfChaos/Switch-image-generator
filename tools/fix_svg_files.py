#!/usr/bin/env python3
"""
Script to fix SVG files with missing angle brackets in the XML declaration and SVG tag.
"""

import sys
import os

def fix_svg_file(svg_file):
    """
    Fix an SVG file by ensuring it has the correct XML declaration and SVG opening tag.
    
    Args:
        svg_file: Path to the SVG file to fix
    """
    # Read the SVG file
    with open(svg_file, 'r') as f:
        content = f.read()
    
    # Check if the file starts with the correct XML declaration
    if not content.startswith('<?xml'):
        # If it starts with 'xml' without the opening angle bracket, add it
        if content.startswith('xml'):
            content = '<' + content
    
    # Check if the SVG tag is missing its opening angle bracket
    if '<svg' not in content and 'svg' in content:
        # Replace 'svg' with '<svg' (only the first occurrence)
        content = content.replace('svg', '<svg', 1)
    
    # Ensure the SVG has a closing tag
    if not content.strip().endswith('</svg>'):
        content = content.rstrip() + '\n</svg>'
    
    # Write the fixed content back to the file
    with open(svg_file, 'w') as f:
        f.write(content)
    
    print(f"Fixed SVG file: {svg_file}")

def main():
    """Fix SVG files specified on the command line."""
    if len(sys.argv) < 2:
        print("Usage: python fix_svg_files.py <svg_file1> [svg_file2 ...]")
        print("Using default files: consistent_light_switch_enhanced.svg and consistent_dark_switch_enhanced.svg")
        svg_files = ["consistent_light_switch_enhanced.svg", "consistent_dark_switch_enhanced.svg"]
    else:
        svg_files = sys.argv[1:]
    
    for svg_file in svg_files:
        if os.path.exists(svg_file):
            fix_svg_file(svg_file)
        else:
            print(f"Error: File {svg_file} does not exist")

if __name__ == "__main__":
    main()
