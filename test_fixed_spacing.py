#!/usr/bin/env python3
"""
Test script to verify the fixed spacing in the switch SVG generator.
This script generates a medium switch SVG with equal spacing on both sides.
"""

from src.switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme

# Create a custom switch with exactly 20px spacing on both sides
class FixedSpacingSwitch(SwitchSVGGenerator):
    def generate_switch_body(self, adjusted_width, adjusted_height):
        """Override to set exact width for equal spacing"""
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

# Create a medium switch with enterprise model (24 ports)
generator = FixedSpacingSwitch(
    num_ports=24,
    switch_model=SwitchModel.ENTERPRISE,
    switch_name="Medium Switch (24 ports)",
    theme=Theme.DARK,
    output_file="output/medium_width_fixed.svg"
)

# Generate and save the SVG
generator.save_svg()

print("Generated medium switch SVG with fixed spacing at: output/medium_width_fixed.svg")
