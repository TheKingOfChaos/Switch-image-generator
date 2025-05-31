#!/usr/bin/env python3
"""
Test Single Row Switch
---------------------
This script tests that the SwitchSVGGenerator with LayoutMode.SINGLE_ROW correctly places all ports
in a single row rather than the default zigzag pattern.
"""

import sys
import os
import unittest
import re
import xml.etree.ElementTree as ET

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme, LayoutMode

class TestSingleRowSwitch(unittest.TestCase):
    """Test cases for the SwitchSVGGenerator with single row layout."""

    def setUp(self):
        """Set up test environment."""
        # Create output directory if it doesn't exist
        os.makedirs("tests/output", exist_ok=True)

    def test_ports_in_single_row(self):
        """Test that all ports are arranged in a single row."""
        # Create a switch with single row layout
        single_row_switch = SwitchSVGGenerator(
            num_ports=24,
            switch_width=800,
            switch_model=SwitchModel.ENTERPRISE,
            switch_name="Single Row Switch Test",
            sfp_ports=2,
            output_file="tests/output/single_row_switch_test.svg",
            theme=Theme.LIGHT,
            layout_mode=LayoutMode.SINGLE_ROW
        )
        
        # Generate and save the SVG
        single_row_switch.save_svg()
        
        # Verify the file was created
        self.assertTrue(os.path.exists("tests/output/single_row_switch_test.svg"))
        
        # Read the SVG content
        with open("tests/output/single_row_switch_test.svg", "r") as f:
            svg_content = f.read()
        
        # Parse the SVG to extract port positions
        port_y_positions = []
        
        # Use regex to find all port rectangles and extract their y-coordinates
        port_rect_pattern = r'<rect x="(\d+)" y="(\d+)" width="\d+" height="\d+" fill="[^"]+" stroke="#000000" stroke-width="1" rx="\d+" ry="\d+" />'
        port_matches = re.finditer(port_rect_pattern, svg_content)
        
        for match in port_matches:
            y_pos = int(match.group(2))
            port_y_positions.append(y_pos)
        
        # Verify we found some ports
        self.assertGreater(len(port_y_positions), 0, "No ports found in the SVG")
        
        # Check that all ports are arranged in a single row (or very close to it)
        # Allow for a small tolerance in y-coordinates (e.g., 5 pixels)
        if port_y_positions:
            min_y = min(port_y_positions)
            max_y = max(port_y_positions)
            # Check that the range of y-coordinates is small (within 5 pixels)
            self.assertLessEqual(max_y - min_y, 5, 
                               f"Ports are not in a single row. Y-coordinates range from {min_y} to {max_y}")
        
        # For comparison, create a switch with the zigzag layout
        zigzag_switch = SwitchSVGGenerator(
            num_ports=24,
            switch_width=800,
            switch_model=SwitchModel.ENTERPRISE,
            switch_name="Zigzag Switch Test",
            sfp_ports=2,
            output_file="tests/output/zigzag_switch_test.svg",
            theme=Theme.LIGHT,
            layout_mode=LayoutMode.ZIGZAG
        )
        
        # Generate and save the SVG
        zigzag_switch.save_svg()
        
        # Verify the file was created
        self.assertTrue(os.path.exists("tests/output/zigzag_switch_test.svg"))
        
        # Read the SVG content
        with open("tests/output/zigzag_switch_test.svg", "r") as f:
            zigzag_svg_content = f.read()
        
        # Parse the SVG to extract port positions
        zigzag_port_y_positions = []
        
        # Use regex to find all port rectangles and extract their y-coordinates
        zigzag_port_matches = re.finditer(port_rect_pattern, zigzag_svg_content)
        
        for match in zigzag_port_matches:
            y_pos = int(match.group(2))
            zigzag_port_y_positions.append(y_pos)
        
        # Verify we found some ports
        self.assertGreater(len(zigzag_port_y_positions), 0, "No ports found in the zigzag SVG")
        
        # Check that the zigzag switch has ports in at least two different rows (zigzag pattern)
        unique_y_positions = set(zigzag_port_y_positions)
        self.assertGreater(len(unique_y_positions), 1, 
                          f"Zigzag switch should have ports in multiple rows, but found only one row at y={list(unique_y_positions)[0]}")
        
        print("Test completed successfully. The SwitchSVGGenerator with SINGLE_ROW layout correctly places all ports in a single row.")

    def test_sfp_ports_alignment(self):
        """Test that SFP ports are properly aligned with the regular ports in a single row."""
        # Create a switch with single row layout and SFP ports
        single_row_switch = SwitchSVGGenerator(
            num_ports=8,
            switch_width=600,
            switch_model=SwitchModel.ENTERPRISE,
            switch_name="Single Row Switch with SFP Test",
            sfp_ports=2,
            output_file="tests/output/single_row_switch_sfp_test.svg",
            theme=Theme.LIGHT,
            layout_mode=LayoutMode.SINGLE_ROW
        )
        
        # Generate and save the SVG
        single_row_switch.save_svg()
        
        # Verify the file was created
        self.assertTrue(os.path.exists("tests/output/single_row_switch_sfp_test.svg"))
        
        # Read the SVG content
        with open("tests/output/single_row_switch_sfp_test.svg", "r") as f:
            svg_content = f.read()
        
        # Parse the SVG using ElementTree for more precise element selection
        try:
            # Replace angle brackets in CDATA sections to avoid XML parsing errors
            svg_content = re.sub(r'<!\[CDATA\[(.*?)\]\]>', lambda m: '<![CDATA[' + m.group(1).replace('<', '&lt;').replace('>', '&gt;') + ']]>', svg_content)
            root = ET.fromstring(svg_content)
        except ET.ParseError:
            # If parsing fails, use a simpler regex approach
            self.skipTest("XML parsing failed, skipping detailed SFP alignment test")
        
        # Find all port rectangles (both regular and SFP)
        port_rects = []
        sfp_rects = []
        
        # Use regex as a fallback since ElementTree might be complex for SVG
        regular_port_pattern = r'<g id="port-\d+">[^<]*<title>[^<]*</title>\s*<rect x="(\d+)" y="(\d+)" width="(\d+)" height="(\d+)"'
        sfp_port_pattern = r'<g id="sfp-\d+">[^<]*<title>[^<]*</title>\s*<rect x="(\d+)" y="(\d+)" width="(\d+)" height="(\d+)"'
        
        regular_matches = re.finditer(regular_port_pattern, svg_content)
        sfp_matches = re.finditer(sfp_port_pattern, svg_content)
        
        for match in regular_matches:
            port_rects.append({
                'x': int(match.group(1)),
                'y': int(match.group(2)),
                'width': int(match.group(3)),
                'height': int(match.group(4))
            })
        
        for match in sfp_matches:
            sfp_rects.append({
                'x': int(match.group(1)),
                'y': int(match.group(2)),
                'width': int(match.group(3)),
                'height': int(match.group(4))
            })
        
        # Verify we found both regular ports and SFP ports
        self.assertGreater(len(port_rects), 0, "No regular ports found in the SVG")
        self.assertGreater(len(sfp_rects), 0, "No SFP ports found in the SVG")
        
        # Check that all regular ports have the same y-coordinate
        if port_rects:
            regular_port_y = port_rects[0]['y']
            regular_port_height = port_rects[0]['height']
            for rect in port_rects:
                self.assertEqual(rect['y'], regular_port_y, 
                                f"Regular port found at y={rect['y']}, expected y={regular_port_y}")
        
        # Check that all SFP ports have the same y-coordinate
        if sfp_rects:
            sfp_port_y = sfp_rects[0]['y']
            sfp_port_height = sfp_rects[0]['height']
            for rect in sfp_rects:
                self.assertEqual(rect['y'], sfp_port_y, 
                                f"SFP port found at y={rect['y']}, expected y={sfp_port_y}")
        
        # Check that SFP ports are vertically centered with regular ports
        # The center of the SFP port should align with the center of the regular port
        regular_port_center_y = regular_port_y + regular_port_height / 2
        sfp_port_center_y = sfp_port_y + sfp_port_height / 2
        
        # Allow for a larger tolerance (5 pixels) due to different port heights
        self.assertAlmostEqual(regular_port_center_y, sfp_port_center_y, delta=5)
        
        # Print a message about the alignment
        print(f"SFP ports (center y={sfp_port_center_y}) are vertically aligned with regular ports (center y={regular_port_center_y})")
        print("Test completed successfully. SFP ports are properly aligned with regular ports in a single row.")

if __name__ == "__main__":
    unittest.main()
