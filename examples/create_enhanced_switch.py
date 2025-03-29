#!/usr/bin/env python3
"""
Script to create a new SVG file with an enhanced legend.
This script creates a completely new SVG file from scratch.
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.switch_svg_generator import SwitchSVGGenerator, Theme, SwitchModel, PortStatus

def create_enhanced_switch(theme=Theme.DARK):
    """
    Create a switch SVG with an enhanced legend.
    
    Args:
        theme: The theme to use (Theme.DARK or Theme.LIGHT)
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
    
    # Create a switch with enhanced legend
    switch = SwitchSVGGenerator(
        num_ports=48,
        switch_width=800,
        switch_height=130,  # Fixed height for all switches
        output_file=f"enhanced_{theme.value}_switch.svg",
        switch_model=SwitchModel.ENTERPRISE,
        switch_name=f"Enhanced {theme.value.capitalize()} Theme Switch",
        theme=theme,
        port_vlan_map=port_vlan_map,
        port_status_map=port_status_map,
        port_labels=port_labels,
        legend_spacing=30  # Increase spacing between switch and legend for better visibility
    )
    
    # Generate and save the SVG
    switch.save_svg()
    print(f"Created enhanced_{theme.value}_switch.svg")
    
    # Verify that the SVG file has the correct XML declaration and SVG opening tag
    with open(f"enhanced_{theme.value}_switch.svg", 'r') as f:
        content = f.read()
    
    if not content.startswith('<?xml'):
        print(f"Warning: SVG file does not start with XML declaration")
    if '<svg' not in content:
        print(f"Warning: SVG file does not contain SVG tag")
    
    return f"enhanced_{theme.value}_switch.svg"

def main():
    """Create enhanced switches with both themes."""
    light_file = create_enhanced_switch(Theme.LIGHT)
    dark_file = create_enhanced_switch(Theme.DARK)
    
    print(f"\nCreated enhanced switches with both themes:")
    print(f"- {light_file}")
    print(f"- {dark_file}")
    
    # Update the HTML viewer to include the new SVG files
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enhanced Switch SVG Viewer</title>
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
    <h1>Enhanced Switch SVG Viewer</h1>
    
    <div class="svg-container">
        <h2>Enhanced Light Theme Switch</h2>
        <object class="svg-embed" type="image/svg+xml" data="enhanced_light_switch.svg">
            Your browser does not support SVG
        </object>
    </div>
    
    <div class="svg-container">
        <h2>Enhanced Dark Theme Switch</h2>
        <object class="svg-embed" type="image/svg+xml" data="enhanced_dark_switch.svg">
            Your browser does not support SVG
        </object>
    </div>
</body>
</html>
"""
    
    with open("view_enhanced_svg.html", 'w') as f:
        f.write(html_content)
    
    print("Created view_enhanced_svg.html to view the enhanced switches")

if __name__ == "__main__":
    main()
