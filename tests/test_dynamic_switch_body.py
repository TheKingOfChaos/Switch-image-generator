#!/usr/bin/env python3
"""
Test script for validating the dynamic switch body functionality.
This script tests different port configurations to ensure the switch body
width scales appropriately and maintains consistent spacing.
"""

import os
import sys
import unittest

# Add the parent directory to the path so we can import the module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme, PortStatus

class TestDynamicSwitchBody(unittest.TestCase):
    """Test cases for dynamic switch body functionality."""

    def setUp(self):
        """Set up test environment."""
        # Create output directory if it doesn't exist
        os.makedirs("output", exist_ok=True)

    def test_minimum_configuration(self):
        """Test the minimum configuration (5 regular ports, 1 SFP port)."""
        # Create a switch with minimum configuration
        generator = SwitchSVGGenerator(
            num_ports=5,
            sfp_ports=1,
            switch_name="Minimum Configuration",
            output_file="output/min_config_switch.svg"
        )
        
        # Generate the SVG
        generator.save_svg()
        
        # Verify the file was created
        self.assertTrue(os.path.exists("output/min_config_switch.svg"))
        
        # Verify the SVG content
        with open("output/min_config_switch.svg", "r") as f:
            svg_content = f.read()
            
            # Check that the SVG contains the correct number of ports
            self.assertEqual(svg_content.count('<g id="port-'), 5)
            self.assertEqual(svg_content.count('<g id="sfp-'), 1)
            
            # Check that the switch body width is appropriate
            # The width should be calculated based on the number of ports
            # For 5 ports, we expect a width of around 400-500px
            width_match = svg_content.find('width="')
            if width_match != -1:
                width_start = width_match + 7
                width_end = svg_content.find('"', width_start)
                width = int(svg_content[width_start:width_end])
                self.assertTrue(400 <= width <= 500, f"Expected width between 400-500px, got {width}px")

    def test_maximum_configuration(self):
        """Test the maximum configuration (48 regular ports, 6 SFP ports)."""
        # Create a switch with maximum configuration
        generator = SwitchSVGGenerator(
            num_ports=48,
            sfp_ports=6,
            switch_name="Maximum Configuration",
            output_file="output/max_config_switch.svg"
        )
        
        # Generate the SVG
        generator.save_svg()
        
        # Verify the file was created
        self.assertTrue(os.path.exists("output/max_config_switch.svg"))
        
        # Verify the SVG content
        with open("output/max_config_switch.svg", "r") as f:
            svg_content = f.read()
            
            # Check that the SVG contains the correct number of ports
            self.assertEqual(svg_content.count('<g id="port-'), 48)
            self.assertEqual(svg_content.count('<g id="sfp-'), 6)
            
            # Check that the switch body width is appropriate
            # The width should be calculated based on the number of ports
            # For 48 ports, we expect a width of around 1000-1500px
            width_match = svg_content.find('width="')
            if width_match != -1:
                width_start = width_match + 7
                width_end = svg_content.find('"', width_start)
                width = int(svg_content[width_start:width_end])
                self.assertTrue(1000 <= width <= 1500, f"Expected width between 1000-1500px, got {width}px")

    def test_medium_configuration(self):
        """Test a medium configuration (24 regular ports, 4 SFP ports)."""
        # Create a switch with medium configuration
        generator = SwitchSVGGenerator(
            num_ports=24,
            sfp_ports=4,
            switch_name="Medium Configuration",
            output_file="output/med_config_switch.svg"
        )
        
        # Generate the SVG
        generator.save_svg()
        
        # Verify the file was created
        self.assertTrue(os.path.exists("output/med_config_switch.svg"))
        
        # Verify the SVG content
        with open("output/med_config_switch.svg", "r") as f:
            svg_content = f.read()
            
            # Check that the SVG contains the correct number of ports
            self.assertEqual(svg_content.count('<g id="port-'), 24)
            self.assertEqual(svg_content.count('<g id="sfp-'), 4)
            
            # Check that the switch body width is appropriate
            # The width should be calculated based on the number of ports
            # For 24 ports, we expect a width of around 700-900px
            width_match = svg_content.find('width="')
            if width_match != -1:
                width_start = width_match + 7
                width_end = svg_content.find('"', width_start)
                width = int(svg_content[width_start:width_end])
                self.assertTrue(700 <= width <= 900, f"Expected width between 700-900px, got {width}px")

    def test_edge_spacing(self):
        """Test that the spacing from the edges is exactly 30px."""
        # Create a switch with a medium configuration
        generator = SwitchSVGGenerator(
            num_ports=16,
            sfp_ports=2,
            switch_name="Edge Spacing Test",
            output_file="output/edge_spacing_switch.svg"
        )
        
        # Generate the SVG
        generator.save_svg()
        
        # Verify the file was created
        self.assertTrue(os.path.exists("output/edge_spacing_switch.svg"))
        
        # Verify the SVG content
        with open("output/edge_spacing_switch.svg", "r") as f:
            svg_content = f.read()
            
            # Check that the first port starts at x=30
            first_port_x = svg_content.find('<rect x="30"')
            self.assertNotEqual(first_port_x, -1, "First port should start at x=30")
            
            # Check that the last SFP port ends at 30px from the right edge
            # This is harder to verify from the SVG content directly
            # We'll check that the SFP ports are positioned correctly
            width_match = svg_content.find('width="')
            if width_match != -1:
                width_start = width_match + 7
                width_end = svg_content.find('"', width_start)
                total_width = int(svg_content[width_start:width_end])
                
                # Find the last SFP port
                last_sfp_match = svg_content.rfind('<g id="sfp-')
                if last_sfp_match != -1:
                    # Find the x position of the last SFP port
                    rect_match = svg_content.find('<rect x="', last_sfp_match)
                    if rect_match != -1:
                        x_start = rect_match + 9
                        x_end = svg_content.find('"', x_start)
                        sfp_x = float(svg_content[x_start:x_end])
                        
                        # Find the width of the SFP port
                        width_match = svg_content.find('width="', rect_match)
                        if width_match != -1:
                            width_start = width_match + 7
                            width_end = svg_content.find('"', width_start)
                            sfp_width = float(svg_content[width_start:width_end])
                            
                            # Calculate the distance from the right edge
                            distance_from_right = total_width - (sfp_x + sfp_width) - 10  # -10 for the margin
                            self.assertAlmostEqual(distance_from_right, 30, delta=1, 
                                                  msg=f"Expected 30px from right edge, got {distance_from_right}px")

if __name__ == "__main__":
    unittest.main()
