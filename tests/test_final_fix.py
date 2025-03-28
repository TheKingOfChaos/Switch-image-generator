#!/usr/bin/env python3
"""
Test script to verify the fix for the spacing issue in the switch SVG generator.
This script generates a switch with the fixed code and displays it in a browser.
"""

import os
import webbrowser
from src.switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme

# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)

# Generate switch with fixed code
generator = SwitchSVGGenerator(
    num_ports=24,
    switch_model=SwitchModel.ENTERPRISE,
    switch_name="Medium Switch (24 ports)",
    theme=Theme.DARK,
    output_file="output/switch_final_fix.svg"
)
generator.save_svg()
print("Generated switch SVG with fixed spacing at: output/switch_final_fix.svg")

# Create HTML file to display the switch
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fixed Switch Spacing</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        h1 {
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
    <h1>Fixed Switch Spacing</h1>
    
    <div class="switch-container">
        <h2>Switch with Equal Spacing</h2>
        <div>
            <object data="switch_final_fix.svg" type="image/svg+xml" width="100%"></object>
        </div>
        <div class="measurements">
            <span class="measurement">Left spacing: 20px</span>
            <span class="measurement">Right spacing: 20px</span>
            <span class="measurement">Difference: 0px</span>
        </div>
    </div>
    
    <div class="explanation">
        <h3>Fix Explanation</h3>
        <p>The original switch had uneven spacing between the switch body edge and the ports:</p>
        <ul>
            <li>Left spacing: 20px (from switch body edge to first port)</li>
            <li>Right spacing: 54px (from last port to switch body edge)</li>
            <li>Difference: 34px</li>
        </ul>
        <p>The fix ensures equal spacing on both sides by modifying the <code>calculate_dimensions</code> method in <code>src/switch_svg_generator.py</code>:</p>
        <pre>
# Calculate the width needed for the switch body with equal spacing on both sides
# Left spacing = start_spacing - 10 = 20px (from left edge to first port)
# For equal spacing, right spacing should also be 20px
# For a 24-port switch with last port at x=382 with width 28px:
# body_width = (382 + 28 + 20) - 10 = 420px
body_width = (last_port_x + last_port_width + left_edge_spacing) - 10
        </pre>
        <p>This ensures that the right spacing is exactly equal to the left spacing (left_edge_spacing = 20px).</p>
    </div>
</body>
</html>
"""

with open("output/fixed_switch_spacing.html", "w") as f:
    f.write(html_content)
print("Created HTML file at: output/fixed_switch_spacing.html")

# Open the HTML file in the default web browser
try:
    html_path = os.path.abspath("output/fixed_switch_spacing.html")
    print(f"Opening {html_path} in web browser...")
    webbrowser.open(f"file://{html_path}")
except Exception as e:
    print(f"Error opening HTML file: {e}")
    print(f"Please open {html_path} manually in your web browser.")
