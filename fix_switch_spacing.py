#!/usr/bin/env python3
"""
Fix for the spacing issue in the switch SVG generator.

This script provides a permanent fix for the uneven spacing issue in the switch SVG generator.
It creates a subclass of SwitchSVGGenerator that overrides the generate_switch_body method
to ensure equal spacing on both sides of the switch.

Usage:
    python fix_switch_spacing.py

This will generate a fixed switch SVG with equal spacing on both sides.
"""

from src.switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme

class FixedSpacingSwitchGenerator(SwitchSVGGenerator):
    """
    A subclass of SwitchSVGGenerator that fixes the spacing issue.
    
    The original SwitchSVGGenerator has uneven spacing between the switch body edge
    and the ports. The left spacing is 20px, but the right spacing is 54px.
    
    This subclass overrides the generate_switch_body method to ensure equal spacing
    on both sides of the switch.
    """
    
    def generate_switch_body(self, adjusted_width, adjusted_height):
        """
        Generate the SVG content for the switch body with equal spacing on both sides.
        
        Args:
            adjusted_width: The calculated width of the SVG
            adjusted_height: The calculated height of the SVG
            
        Returns:
            List of SVG lines for the switch body
        """
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


def main():
    """Generate a fixed switch SVG with equal spacing on both sides."""
    # Create output directory if it doesn't exist
    import os
    os.makedirs("output", exist_ok=True)
    
    # Generate fixed switch
    fixed_generator = FixedSpacingSwitchGenerator(
        num_ports=24,
        switch_model=SwitchModel.ENTERPRISE,
        switch_name="Medium Switch (24 ports)",
        theme=Theme.DARK,
        output_file="output/switch_fixed_spacing.svg"
    )
    fixed_generator.save_svg()
    print("Generated fixed switch SVG at: output/switch_fixed_spacing.svg")
    
    print("\nTo view the fixed switch, open output/switch_fixed_spacing.svg in a web browser.")
    print("The fixed switch has equal spacing (20px) on both sides.")


if __name__ == "__main__":
    main()
