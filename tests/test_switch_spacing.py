#!/usr/bin/env python3
"""
Test script to demonstrate the spacing issue in the switch SVG generator.
This script generates two switches:
1. Original switch with uneven spacing
2. Fixed switch with equal spacing on both sides

It also creates an HTML file that shows both switches side by side with measurements.
"""

import os
from src.switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme

# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)

# Generate original switch
original_generator = SwitchSVGGenerator(
    num_ports=24,
    switch_model=SwitchModel.ENTERPRISE,
    switch_name="Medium Switch (24 ports)",
    theme=Theme.DARK,
    output_file="output/switch_original.svg"
)
original_generator.save_svg()
print("Generated original switch SVG at: output/switch_original.svg")

# Create a custom subclass that overrides the generate_switch_body method
class FixedSpacingSwitchGenerator(SwitchSVGGenerator):
    def generate_switch_body(self, adjusted_width, adjusted_height):
        svg = []
        svg.append(f'  <!-- Switch body -->')
        
        # Use the switch_height for the body height
        body_height = self.switch_height - 20  # -20 for the margins (10px top and bottom)
        
        # Calculate exact body width for equal spacing
        # First port is at x=30, last port (port-24) is at x=382 with width 28px
        # Left spacing = 30 - 10 = 20px
        # For right spacing to be 20px, body width should be (382 + 28 + 20) - 10 = 420px
        body_width = 420
            
        svg.append(f'  <rect x="10" y="10" width="{body_width}" height="{body_height}" '
                  f'rx="10" ry="10" fill="{self.switch_body_color}" '
                  f'stroke="{self.switch_body_border_color}" stroke-width="{self.switch_body_border_width}" />')
        return svg

# Generate fixed switch
fixed_generator = FixedSpacingSwitchGenerator(
    num_ports=24,
    switch_model=SwitchModel.ENTERPRISE,
    switch_name="Medium Switch (24 ports)",
    theme=Theme.DARK,
    output_file="output/switch_fixed.svg"
)
fixed_generator.save_svg()
print("Generated fixed switch SVG at: output/switch_fixed.svg")

# Create HTML file to compare both switches
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Switch Spacing Comparison</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
        }
        .comparison {
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .switch-container {
            position: relative;
            margin-bottom: 20px;
        }
        .measurement {
            display: flex;
            justify-content: space-between;
            margin-top: 10px;
            font-weight: bold;
        }
        .measurement span {
            display: inline-block;
            padding: 5px 10px;
            background-color: yellow;
            border-radius: 4px;
        }
        .difference {
            text-align: right;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>Switch Spacing Comparison</h1>
    
    <div class="comparison">
        <h2>Original Switch (Uneven Spacing)</h2>
        <div class="switch-container">
            <object data="switch_original.svg" type="image/svg+xml" width="100%"></object>
        </div>
        <div class="measurement">
            <span>Left spacing: 20px</span>
            <span>Right spacing: 54px</span>
            <span class="difference">Difference: 34px</span>
        </div>
    </div>
    
    <div class="comparison">
        <h2>Fixed Switch (Balanced Spacing)</h2>
        <div class="switch-container">
            <object data="switch_fixed.svg" type="image/svg+xml" width="100%"></object>
        </div>
        <div class="measurement">
            <span>Left spacing: 20px</span>
            <span>Right spacing: 20px</span>
            <span class="difference">Difference: 0px</span>
        </div>
    </div>
</body>
</html>
"""

with open("output/switch_spacing_comparison.html", "w") as f:
    f.write(html_content)
print("Created comparison HTML at: output/switch_spacing_comparison.html")

print("\nTo view the comparison, open output/switch_spacing_comparison.html in a web browser.")
print("You can also examine the SVG files directly to see the difference in the switch body width.")
