#!/usr/bin/env python3
"""
Script to fix the legend visibility issue in switch SVG files.
This script:
1. Generates switch SVGs with consistent dimensions and enhanced legend
2. Fixes any issues with the SVG files (missing angle brackets)
3. Creates an HTML file to view the result
"""

import sys
import os
import re

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.switch_svg_generator import SwitchSVGGenerator, Theme, SwitchModel, PortStatus

def create_switch_with_enhanced_legend(theme=Theme.DARK, output_file=None):
    """
    Create a switch SVG with an enhanced legend.
    
    Args:
        theme: The theme to use (Theme.DARK or Theme.LIGHT)
        output_file: Optional custom output file name
    
    Returns:
        Path to the generated SVG file
    """
    # Define VLAN assignments
    port_vlan_map = {
        1: 10,   # Port 1 on VLAN 10
        2: 10,   # Port 2 on VLAN 10
        3: 20,   # Port 3 on VLAN 20
        4: 20,   # Port 4 on VLAN 20
        5: 30,   # Port 5 on VLAN 30
        6: 30,   # Port 6 on VLAN 30
    }
    
    # Define port statuses
    port_status_map = {
        4: PortStatus.DOWN,      # Port 4 is down
        8: PortStatus.DISABLED,  # Port 8 is disabled
    }
    
    # Define custom port labels
    port_labels = {
        1: "WAN",
        2: "DMZ",
        3: "SRV1",
        4: "SRV2",
    }
    
    # Set default output file name if not provided
    if output_file is None:
        output_file = f"switch_with_visible_legend_{theme.value}.svg"
    
    # Create a switch with enhanced legend
    switch = SwitchSVGGenerator(
        num_ports=48,
        switch_width=800,
        switch_height=130,  # Fixed height for all switches
        output_file=output_file,
        switch_model=SwitchModel.ENTERPRISE,
        switch_name=f"Switch with Visible Legend ({theme.value.capitalize()})",
        theme=theme,
        port_vlan_map=port_vlan_map,
        port_status_map=port_status_map,
        port_labels=port_labels,
        legend_position="outside",
        legend_spacing=30  # Increase spacing between switch and legend for better visibility
    )
    
    # Generate and save the SVG
    switch.save_svg()
    print(f"Created {output_file}")
    
    return output_file

def fix_svg_file(svg_file):
    """
    Fix an SVG file by adding missing angle brackets.
    
    Args:
        svg_file: Path to the SVG file to fix
    
    Returns:
        Path to the fixed SVG file
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
    
    # Write the fixed content back to the same file
    with open(svg_file, 'w') as f:
        f.write(content)
    
    print(f"Fixed SVG file: {svg_file}")
    
    # Verify the fix
    with open(svg_file, 'r') as f:
        fixed_content = f.read()
    
    if fixed_content.startswith('<?xml') and '<svg' in fixed_content:
        print(f"Verification: SVG file has been fixed successfully")
    else:
        print(f"Warning: SVG file may not have been fixed correctly")
        if not fixed_content.startswith('<?xml'):
            print(f"  - XML declaration is still missing or incorrect")
        if '<svg' not in fixed_content:
            print(f"  - SVG tag is still missing or incorrect")
    
    return svg_file

def create_html_viewer(svg_files):
    """
    Create an HTML file to view the SVG files.
    
    Args:
        svg_files: List of SVG files to include in the viewer
    
    Returns:
        Path to the HTML file
    """
    # Create HTML content
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Switch SVG Viewer</title>
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
    <h1>Switch SVG Viewer</h1>
"""
    
    # Add a container for each SVG file
    for svg_file in svg_files:
        # Extract theme from filename
        theme = "Light" if "light" in svg_file.lower() else "Dark"
        
        html_content += f"""    
    <div class="svg-container">
        <h2>{theme} Theme Switch</h2>
        <object class="svg-embed" type="image/svg+xml" data="{svg_file}">
            Your browser does not support SVG
        </object>
    </div>
"""
    
    # Close HTML
    html_content += """</body>
</html>
"""
    
    # Write HTML to file
    html_file = "view_switches.html"
    with open(html_file, 'w') as f:
        f.write(html_content)
    
    print(f"Created {html_file} to view the SVG files")
    
    return html_file

def main():
    """Create switches with visible legends and view them in a browser."""
    # Create switches with enhanced legends
    light_file = create_switch_with_enhanced_legend(Theme.LIGHT)
    dark_file = create_switch_with_enhanced_legend(Theme.DARK)
    
    # Fix any issues with the SVG files
    light_file = fix_svg_file(light_file)
    dark_file = fix_svg_file(dark_file)
    
    # Create HTML viewer
    html_file = create_html_viewer([light_file, dark_file])
    
    print("\nSummary:")
    print("1. Created switch SVGs with enhanced legends")
    print("2. Fixed any issues with the SVG files")
    print("3. Created an HTML file to view the result")
    print(f"\nTo view the switches, open {html_file} in a web browser")

if __name__ == "__main__":
    main()
