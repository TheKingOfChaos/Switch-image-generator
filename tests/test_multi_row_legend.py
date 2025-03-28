#!/usr/bin/env python3
"""
Test script for validating the multi-row legend functionality.
This script tests that legend items wrap to multiple rows when they exceed the switch width.
"""

import os
import sys
import unittest

# Add the parent directory to the path so we can import the module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme, PortStatus

class TestMultiRowLegend(unittest.TestCase):
    """Test cases for multi-row legend functionality."""

    def setUp(self):
        """Set up test environment."""
        # Create output directory if it doesn't exist
        os.makedirs("output", exist_ok=True)

    def test_many_vlans(self):
        """Test that legend items wrap to multiple rows when there are many VLANs."""
        # Create a switch with many VLANs
        # We'll create a port-VLAN map with 15 different VLANs
        port_vlan_map = {}
        for i in range(1, 16):
            port_vlan_map[i] = i * 10  # VLANs 10, 20, 30, ..., 150
        
        # Create custom VLAN colors
        vlan_colors = {}
        for vlan_id in port_vlan_map.values():
            # Generate a color based on the VLAN ID
            r = (vlan_id * 13) % 256
            g = (vlan_id * 17) % 256
            b = (vlan_id * 23) % 256
            vlan_colors[vlan_id] = f"#{r:02x}{g:02x}{b:02x}"
        
        # Create a switch with many VLANs
        generator = SwitchSVGGenerator(
            num_ports=15,
            sfp_ports=1,
            switch_name="Many VLANs Test",
            port_vlan_map=port_vlan_map,
            vlan_colors=vlan_colors,
            output_file="output/many_vlans_switch.svg"
        )
        
        # Generate the SVG
        generator.save_svg()
        
        # Verify the file was created
        self.assertTrue(os.path.exists("output/many_vlans_switch.svg"))
        
        # Verify the SVG content
        with open("output/many_vlans_switch.svg", "r") as f:
            svg_content = f.read()
            
            # Count the total number of legend items (rect elements)
            legend_item_count = svg_content.count('<rect x="')
            
            # We should have at least 15 legend items (one for each VLAN)
            self.assertGreaterEqual(legend_item_count, 15, 
                                   f"Expected at least 15 legend items, got {legend_item_count}")
            
            # Check that we have multiple rows of legend items by looking for different y-coordinates
            # Get all the y-coordinates used for legend items
            import re
            y_coords = re.findall(r'<rect x="\d+" y="(\d+)"', svg_content)
            unique_y_coords = set(y_coords)
            
            # We should have at least 2 different y-coordinates (2 rows)
            self.assertGreaterEqual(len(unique_y_coords), 2, 
                                   f"Expected at least 2 rows, got {len(unique_y_coords)} rows with y-coords: {unique_y_coords}")

    def test_long_vlan_names(self):
        """Test that legend items wrap to multiple rows when VLAN names are long."""
        # Create a switch with a few VLANs but with long names
        port_vlan_map = {
            1: 10,  # Administration
            2: 20,  # Very Long VLAN Name That Will Wrap
            3: 30,  # Another Very Long VLAN Name That Will Definitely Wrap
            4: 40,  # Yet Another Very Long VLAN Name
            5: 50,  # One More Very Long VLAN Name
        }
        
        # Create custom VLAN names
        vlan_names = {
            10: "Administration Department",
            20: "Very Long VLAN Name That Will Wrap To Multiple Lines",
            30: "Another Very Long VLAN Name That Will Definitely Wrap To Multiple Lines",
            40: "Yet Another Very Long VLAN Name That Will Wrap To Multiple Lines",
            50: "One More Very Long VLAN Name That Will Wrap To Multiple Lines",
        }
        
        # Create a switch with long VLAN names
        # We'll use a small switch width to force wrapping
        generator = SwitchSVGGenerator(
            num_ports=5,
            sfp_ports=1,
            switch_name="Long VLAN Names Test",
            switch_width=400,  # Small width to force wrapping
            port_vlan_map=port_vlan_map,
            output_file="output/long_vlan_names_switch.svg"
        )
        
        # Inject the custom VLAN names
        # This is a bit of a hack, but it's the easiest way to test this
        generator.vlan_names = vlan_names
        
        # Generate the SVG
        generator.save_svg()
        
        # Verify the file was created
        self.assertTrue(os.path.exists("output/long_vlan_names_switch.svg"))
        
        # Verify the SVG content
        with open("output/long_vlan_names_switch.svg", "r") as f:
            svg_content = f.read()
            
            # Check that we have multiple rows of legend items
            # The first row should start at y=170
            first_row = svg_content.find('<rect x="30" y="170"')
            self.assertNotEqual(first_row, -1, "First row of legend items not found")
            
            # There should be at least one more row of legend items
            # The second row should start at y=195 (170 + 25)
            second_row = svg_content.find('<rect x="30" y="195"')
            self.assertNotEqual(second_row, -1, "Second row of legend items not found")

    def test_narrow_switch(self):
        """Test that legend items wrap to multiple rows when the switch is narrow."""
        # Create a switch with a narrow width and multiple VLANs to force wrapping
        port_vlan_map = {
            1: 10,  # VLAN 10
            2: 20,  # VLAN 20
            3: 30,  # VLAN 30
            4: 40,  # VLAN 40
            5: 50,  # VLAN 50
            6: 60,  # VLAN 60
            7: 70,  # VLAN 70
            8: 80,  # VLAN 80
        }
        
        generator = SwitchSVGGenerator(
            num_ports=8,
            sfp_ports=1,
            switch_name="Narrow Switch Test",
            switch_width=200,  # Extremely narrow width to force wrapping
            port_vlan_map=port_vlan_map,
            output_file="output/narrow_switch.svg"
        )
        
        # Generate the SVG
        generator.save_svg()
        
        # Verify the file was created
        self.assertTrue(os.path.exists("output/narrow_switch.svg"))
        
        # Verify the SVG content
        with open("output/narrow_switch.svg", "r") as f:
            svg_content = f.read()
            
            # Check that we have multiple rows of legend items by looking for different y-coordinates
            # Get all the y-coordinates used for legend items
            import re
            y_coords = re.findall(r'<rect x="\d+" y="(\d+)"', svg_content)
            unique_y_coords = set(y_coords)
            
            # We should have at least 2 different y-coordinates (2 rows)
            self.assertGreaterEqual(len(unique_y_coords), 2, 
                                   f"Expected at least 2 rows, got {len(unique_y_coords)} rows with y-coords: {unique_y_coords}")

if __name__ == "__main__":
    unittest.main()
