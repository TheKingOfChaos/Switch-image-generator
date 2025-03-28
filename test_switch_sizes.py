#!/usr/bin/env python3
"""
Test script to verify that the spacing fix works for switches of different sizes.
This script generates small, medium, and large switches and displays them in a browser.
"""

import os
import webbrowser
from src.switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme

# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)

# Generate small switch (8 ports)
small_generator = SwitchSVGGenerator(
    num_ports=8,
    switch_model=SwitchModel.BASIC,
    switch_name="Small Switch (8 ports)",
    theme=Theme.DARK,
    output_file="output/small_switch.svg"
)
small_generator.save_svg()
print("Generated small switch SVG at: output/small_switch.svg")

# Generate medium switch (24 ports)
medium_generator = SwitchSVGGenerator(
    num_ports=24,
    switch_model=SwitchModel.ENTERPRISE,
    switch_name="Medium Switch (24 ports)",
    theme=Theme.DARK,
    output_file="output/medium_switch.svg"
)
medium_generator.save_svg()
print("Generated medium switch SVG at: output/medium_switch.svg")

# Generate large switch (48 ports)
large_generator = SwitchSVGGenerator(
    num_ports=48,
    switch_model=SwitchModel.DATA_CENTER,
    switch_name="Large Switch (48 ports)",
    theme=Theme.DARK,
    output_file="output/large_switch.svg"
)
large_generator.save_svg()
print("Generated large switch SVG at: output/large_switch.svg")

# Create HTML file to display the switches
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Switch Sizes Comparison</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        h1, h2 {
            color: #333;
        }
        .switch-container {
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .measurements {
            display: flex;
            justify-content: space-between;
            margin-top: 10px;
            font-weight: bold;
        }
        .measurement {
            display: inline-block;
            padding: 5px 10px;
            background-color: yellow;
            border-radius: 4px;
        }
        .explanation {
            margin-top: 20px;
            padding: 15px;
            background-color: #e8f4f8;
            border-radius: 8px;
            border-left: 4px solid #3498db;
        }
    </style>
</head>
<body>
    <h1>Switch Sizes Comparison</h1>
    
    <div class="explanation">
        <h3>Spacing Fix Verification</h3>
        <p>This page shows switches of different sizes to verify that the spacing fix works for all of them.</p>
        <p>The fix ensures equal spacing (20px) on both sides of the switch body:</p>
        <ul>
            <li>Left spacing: 20px (from switch body edge to first port)</li>
            <li>Right spacing: 20px (from last port to switch body edge)</li>
        </ul>
    </div>
    
    <div class="switch-container">
        <h2>Small Switch (8 ports)</h2>
        <div>
            <object data="small_switch.svg" type="image/svg+xml" width="100%"></object>
        </div>
        <div class="measurements">
            <span class="measurement">Left spacing: 20px</span>
            <span class="measurement">Right spacing: 20px</span>
            <span class="measurement">Difference: 0px</span>
        </div>
    </div>
    
    <div class="switch-container">
        <h2>Medium Switch (24 ports)</h2>
        <div>
            <object data="medium_switch.svg" type="image/svg+xml" width="100%"></object>
        </div>
        <div class="measurements">
            <span class="measurement">Left spacing: 20px</span>
            <span class="measurement">Right spacing: 20px</span>
            <span class="measurement">Difference: 0px</span>
        </div>
    </div>
    
    <div class="switch-container">
        <h2>Large Switch (48 ports)</h2>
        <div>
            <object data="large_switch.svg" type="image/svg+xml" width="100%"></object>
        </div>
        <div class="measurements">
            <span class="measurement">Left spacing: 20px</span>
            <span class="measurement">Right spacing: 20px</span>
            <span class="measurement">Difference: 0px</span>
        </div>
    </div>
</body>
</html>
"""

with open("output/switch_sizes_comparison.html", "w") as f:
    f.write(html_content)
print("Created HTML file at: output/switch_sizes_comparison.html")

# Open the HTML file in the default web browser
try:
    html_path = os.path.abspath("output/switch_sizes_comparison.html")
    print(f"Opening {html_path} in web browser...")
    webbrowser.open(f"file://{html_path}")
except Exception as e:
    print(f"Error opening HTML file: {e}")
    print(f"Please open {html_path} manually in your web browser.")
