import sys
import os
import unittest

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme, PortStatus

class TestExactWidth(unittest.TestCase):
    def test_small_config_width(self):
        """Test that a small configuration has the exact width needed for the ports."""
        # Create a small configuration with 8 regular ports and 2 SFP ports
        generator = SwitchSVGGenerator(
            num_ports=8,
            sfp_ports=2,
            switch_model=SwitchModel.ENTERPRISE,
            theme=Theme.DARK,
            output_file="../output/exact_width_small.svg"
        )
        
        # Generate the SVG
        generator.save_svg()
        
        # Read the SVG file
        with open("../output/exact_width_small.svg", "r") as f:
            svg_content = f.read()
        
        # Check that the SVG width is exactly what's needed
        # For 8 regular ports (4 columns) and 2 SFP ports (1 column):
        # 30 (start spacing) + 4 * (28 + 4) (regular ports) + 20 (sfp spacing) + 1 * 40 (sfp ports) + 20 (margins) = 238px
        # The SVG width should be around 238px, and the switch body width should be around 218px
        
        # Extract the SVG width from the content
        import re
        svg_width_match = re.search(r'<svg width="(\d+)"', svg_content)
        self.assertIsNotNone(svg_width_match, "SVG width not found")
        svg_width = int(svg_width_match.group(1))
        
        # Extract the switch body width from the content
        body_width_match = re.search(r'<rect x="10" y="10" width="(\d+)"', svg_content)
        self.assertIsNotNone(body_width_match, "Switch body width not found")
        body_width = int(body_width_match.group(1))
        
        # Check that the widths are close to the expected values
        # Allow for some variation due to rounding and other factors
        self.assertLessEqual(abs(svg_width - 238), 20, f"SVG width {svg_width} is not close to expected 238px")
        self.assertLessEqual(abs(body_width - 218), 20, f"Switch body width {body_width} is not close to expected 218px")
        
        # Check that the last SFP port is close to the right edge of the switch body
        # The last SFP port should end at around 30 + 4 * (28 + 4) + 20 + 40 = 178px
        # The switch body width should be around 178px
        # So the gap should be minimal
        
        # Extract the last SFP port position from the content
        sfp_pos_match = re.search(r'<rect x="(\d+)" y="\d+" width="40" height="20".*SFP2', svg_content, re.DOTALL)
        self.assertIsNotNone(sfp_pos_match, "Last SFP port position not found")
        sfp_pos = int(sfp_pos_match.group(1))
        
        # Calculate the gap between the end of the last SFP port and the right edge of the switch body
        gap = body_width - (sfp_pos + 40)
        
        # Check that the gap is minimal (less than 20px)
        self.assertLessEqual(gap, 20, f"Gap between last SFP port and right edge is {gap}px, expected less than 20px")

if __name__ == '__main__':
    unittest.main()
