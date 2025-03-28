#!/usr/bin/env python3
"""
Script to fix SVG files by adding missing angle brackets.
"""

import sys
import os
import re

def fix_svg_file(svg_file):
    """
    Fix an SVG file by adding missing angle brackets.
    
    Args:
        svg_file: Path to the SVG file to fix
    """
    # Read the SVG file
    with open(svg_file, 'r') as f:
        content = f.read()
    
    # Check if the file starts with 'xml' without the opening angle bracket
    if content.startswith('xml'):
        # Add the opening angle bracket
        content = '<' + content
    
    # Check if the SVG tag is missing its opening angle bracket
    # Look for 'svg width=' without the opening angle bracket
    svg_tag_pattern = r'svg width="'
    if re.search(svg_tag_pattern, content):
        # Add the opening angle bracket before 'svg'
        content = content.replace('svg width="', '<svg width="', 1)
    
    # Check for double angle brackets (<<svg)
    if '<<svg' in content:
        # Replace <<svg with <svg
        content = content.replace('<<svg', '<svg', 1)
    
    # Write the fixed content back to a new file
    output_file = svg_file.replace('.svg', '_fixed.svg')
    with open(output_file, 'w') as f:
        f.write(content)
    
    print(f"Fixed SVG file saved to: {output_file}")
    
    # Verify the fix
    with open(output_file, 'r') as f:
        fixed_content = f.read()
    
    if fixed_content.startswith('<?xml') and '<svg' in fixed_content:
        print(f"Verification: SVG file has been fixed successfully")
    else:
        print(f"Warning: SVG file may not have been fixed correctly")
        if not fixed_content.startswith('<?xml'):
            print(f"  - XML declaration is still missing or incorrect")
        if '<svg' not in fixed_content:
            print(f"  - SVG tag is still missing or incorrect")

def main():
    """Fix SVG files specified on the command line."""
    if len(sys.argv) < 2:
        print("Usage: python fix_svg_angle_brackets.py <svg_file1> [svg_file2 ...]")
        print("Using default files: enhanced_light_switch.svg and enhanced_dark_switch.svg")
        svg_files = ["enhanced_light_switch.svg", "enhanced_dark_switch.svg"]
    else:
        svg_files = sys.argv[1:]
    
    for svg_file in svg_files:
        if os.path.exists(svg_file):
            fix_svg_file(svg_file)
        else:
            print(f"Error: File {svg_file} does not exist")
    
    # Create an HTML file to view the fixed SVG files
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fixed Switch SVG Viewer</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .svg-container {
            margin-bottom: 30px;
            border: 1px solid #ccc;
            padding: 10px;
        }
        h2 {
            margin-top: 0;
        }
        .svg-embed {
            width: 100%;
            height: 300px;
            border: 1px solid #eee;
        }
    </style>
</head>
<body>
    <h1>Fixed Switch SVG Viewer</h1>
    
    <div class="svg-container">
        <h2>Fixed Light Theme Switch</h2>
        <object class="svg-embed" type="image/svg+xml" data="enhanced_light_switch_fixed.svg">
            Your browser does not support SVG
        </object>
    </div>
    
    <div class="svg-container">
        <h2>Fixed Dark Theme Switch</h2>
        <object class="svg-embed" type="image/svg+xml" data="enhanced_dark_switch_fixed.svg">
            Your browser does not support SVG
        </object>
    </div>
</body>
</html>
"""
    
    with open("view_fixed_svg.html", 'w') as f:
        f.write(html_content)
    
    print("Created view_fixed_svg.html to view the fixed SVG files")

if __name__ == "__main__":
    main()
