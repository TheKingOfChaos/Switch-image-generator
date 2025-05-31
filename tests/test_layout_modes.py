#!/usr/bin/env python3
"""
Test Layout Modes
----------------
This script tests the different layout modes available in the SwitchSVGGenerator.
It creates two switches: one with the zigzag layout and one with the single row layout,
and verifies that they are generated correctly.
"""

import sys
import os
import unittest

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme, LayoutMode

class TestLayoutModes(unittest.TestCase):
    """Test case for layout modes in SwitchSVGGenerator."""
    
    def setUp(self):
        """Set up test environment."""
        # Create output directory if it doesn't exist
        os.makedirs(os.path.join(os.path.dirname(__file__), 'output'), exist_ok=True)
    
    def test_zigzag_layout(self):
        """Test that zigzag layout generates correctly."""
        output_file = os.path.join(os.path.dirname(__file__), 'output', 'test_zigzag_layout.svg')
        
        # Create a switch with zigzag layout
        switch = SwitchSVGGenerator(
            num_ports=24,
            switch_model=SwitchModel.ENTERPRISE,
            switch_name="Zigzag Layout Test",
            sfp_ports=2,
            output_file=output_file,
            layout_mode=LayoutMode.ZIGZAG
        )
        
        # Generate and save the SVG
        switch.save_svg()
        
        # Verify that the file was created
        self.assertTrue(os.path.exists(output_file), "Zigzag layout SVG file was not created")
        
        # Read the file and verify it contains zigzag pattern indicators
        with open(output_file, 'r') as f:
            content = f.read()
            # In zigzag layout, ports are placed in two rows
            # Check for ports in both rows by looking at their y-coordinates
            self.assertIn('y="70"', content, "No ports found in top row")
            # Check for ports in bottom row, but exclude SFP ports which might be at y="102"
            # Instead, look for regular ports which would be at y="102"
            self.assertIn('<rect x="', content, "No ports found")
            # Verify that at least one port is in the bottom row
            self.assertIn('y="102"', content, "No ports found in bottom row")
    
    def test_single_row_layout(self):
        """Test that single row layout generates correctly."""
        output_file = os.path.join(os.path.dirname(__file__), 'output', 'test_single_row_layout.svg')
        
        # Create a switch with single row layout
        switch = SwitchSVGGenerator(
            num_ports=24,
            switch_model=SwitchModel.ENTERPRISE,
            switch_name="Single Row Layout Test",
            sfp_ports=2,
            output_file=output_file,
            layout_mode=LayoutMode.SINGLE_ROW
        )
        
        # Generate and save the SVG
        switch.save_svg()
        
        # Verify that the file was created
        self.assertTrue(os.path.exists(output_file), "Single row layout SVG file was not created")
        
        # Read the file and verify it contains single row pattern indicators
        with open(output_file, 'r') as f:
            content = f.read()
            # In single row layout, all ports should have the same y-coordinate
            # Count occurrences of the y-coordinate for the first row
            top_row_count = content.count('y="70"')
            # Verify that we have at least 24 ports (the number of normal ports) in the top row
            self.assertGreaterEqual(top_row_count, 24, "Not all ports are in a single row")
            # Verify that we don't have ports in the bottom row (which would be at y="102")
            bottom_row_count = content.count('y="102"')
            self.assertEqual(bottom_row_count, 0, "Found ports in bottom row, should be single row layout")

if __name__ == "__main__":
    unittest.main()
