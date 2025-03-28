#!/usr/bin/env python3
"""
Test script to verify that the default parameters in the SwitchSVGGenerator
now use consistent dimensions and have a visible legend.
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.switch_svg_generator import SwitchSVGGenerator, Theme, SwitchModel, PortStatus

def main():
    """Create test switches using default parameters."""
    
    # Example 1: Light theme switch with default parameters
    light_switch = SwitchSVGGenerator(
        num_ports=48,
        output_file="default_light_switch.svg",
        switch_model=SwitchModel.ENTERPRISE,
        switch_name="Default Light Theme Switch",
        theme=Theme.LIGHT
    )
    light_switch.save_svg()
    print("Created default_light_switch.svg")
    
    # Example 2: Dark theme switch with default parameters
    dark_switch = SwitchSVGGenerator(
        num_ports=48,
        output_file="default_dark_switch.svg",
        switch_model=SwitchModel.ENTERPRISE,
        switch_name="Default Dark Theme Switch",
        theme=Theme.DARK
    )
    dark_switch.save_svg()
    print("Created default_dark_switch.svg")
    
    print("\nBoth switches have been generated with default parameters.")
    print("The switch body height should be 130px for both themes.")
    print("The legend should be positioned outside the switch body in both cases.")
    print("The legend spacing should be 30px for better visibility.")

    # Create HTML viewer
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Default Switch SVG Viewer</title>
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
    <h1>Default Switch SVG Viewer</h1>
    
    <div class="svg-container">
        <h2>Light Theme Switch (Default Parameters)</h2>
        <object class="svg-embed" type="image/svg+xml" data="default_light_switch.svg">
            Your browser does not support SVG
        </object>
    </div>
    
    <div class="svg-container">
        <h2>Dark Theme Switch (Default Parameters)</h2>
        <object class="svg-embed" type="image/svg+xml" data="default_dark_switch.svg">
            Your browser does not support SVG
        </object>
    </div>
</body>
</html>
"""
    
    with open("view_default_switches.html", 'w') as f:
        f.write(html_content)
    
    print("Created view_default_switches.html to view the switches")

if __name__ == "__main__":
    main()
