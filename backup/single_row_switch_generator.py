#!/usr/bin/env python3
"""
Single Row Switch SVG Generator
------------------------------
This script extends the SwitchSVGGenerator to create a switch with ports in a single row
rather than the default zigzag pattern.
"""

from src.switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme, PortStatus

class SingleRowSwitchGenerator(SwitchSVGGenerator):
    """Extended generator that places all ports in a single row."""
    
    def generate_ports(self, adjusted_width: int, ports_per_row: int, num_rows: int) -> list:
        """
        Override the port generation to place all ports in a single row.
        
        Args:
            adjusted_width: The calculated width of the SVG
            ports_per_row: Number of ports per row (ignored in this implementation)
            num_rows: Number of rows of ports (ignored in this implementation)
            
        Returns:
            List of SVG lines for the ports
        """
        svg = []
        svg.append(f'  <!-- Switch ports -->')
        
        # Get port shape attributes
        port_shape_attrs = self.get_port_shape_attributes()
        
        # Define spacing constants
        start_spacing = 30  # Space from start of switch to first port
        end_spacing = 30    # Space from last SFP port to end of switch
        sfp_spacing = 20    # Space between last regular port and first SFP port
        
        # Calculate starting positions
        start_x = start_spacing
        start_y = 90  # Center the ports vertically in the switch
        
        # Generate regular RJ45 ports in a single row
        for port_num in range(1, self.num_ports + 1):
            # Calculate position
            x = start_x + (port_num - 1) * (self.port_width + self.port_spacing)
            y = start_y
            
            color = self.get_port_color(port_num)
            
            # Create port group with tooltip
            port_label = self.port_labels.get(port_num, str(port_num))
            status = self.port_status_map.get(port_num, PortStatus.UP)
            vlan_id = self.port_vlan_map.get(port_num, 1)
            
            tooltip = f"Port: {port_num}, Label: {port_label}, Status: {status.value}, VLAN: {vlan_id}"
            
            svg.append(f'  <g id="port-{port_num}">')
            svg.append(f'    <title>{tooltip}</title>')
            
            # Port rectangle
            svg.append(f'    <rect x="{x}" y="{y}" width="{self.port_width}" height="{self.port_height}" '
                      f'fill="{color}" stroke="#000000" stroke-width="1" '
                      f'rx="{port_shape_attrs["rx"]}" ry="{port_shape_attrs["ry"]}" />')
            
            # Port label - centered inside the port rectangle
            text_x = x + (self.port_width // 2)
            text_y = y + (self.port_height // 2) + 4  # Adjusted to center vertically
            svg.append(f'    <text x="{text_x}" y="{text_y}" font-family="Arial" font-size="10" '
                      f'fill="white" text-anchor="middle" dominant-baseline="middle">{port_label}</text>')
            
            # Status indicator (small circle in corner if enabled)
            if self.show_status_indicator and status != PortStatus.UP:
                indicator_x = x + self.port_width - 5
                indicator_y = y + 5
                svg.append(f'    <circle cx="{indicator_x}" cy="{indicator_y}" r="3" '
                          f'fill="{self.STATUS_COLORS[status]}" stroke="white" stroke-width="0.5" />')
            
            svg.append(f'  </g>')
        
        # Generate SFP ports if requested
        if self.sfp_ports > 0:
            svg.append(f'  <!-- SFP Ports -->')
            
            # SFP ports are wider than tall
            sfp_height = 20
            sfp_width = 40
            
            # Calculate the position of the last regular port
            last_port_x = start_x + (self.num_ports - 1) * (self.port_width + self.port_spacing)
            
            # Position SFP ports starting sfp_spacing from the last regular port
            sfp_start_x = last_port_x + self.port_width + sfp_spacing
            sfp_start_y = start_y + (self.port_height - sfp_height) // 2  # Center SFP ports vertically with regular ports
            
            # Place SFP ports in a single row
            for i in range(self.sfp_ports):
                sfp_x = sfp_start_x + i * (sfp_width + self.port_spacing)
                sfp_y = sfp_start_y
                
                sfp_num = self.num_ports + i + 1
                
                # SFP ports are typically for uplinks, so use a different color
                sfp_color = "#3498db"  # Blue
                
                # Create SFP port group with tooltip
                sfp_label = self.port_labels.get(sfp_num, f"SFP{i+1}")
                
                tooltip = f"SFP Port: {sfp_num}, Label: {sfp_label}"
                
                svg.append(f'  <g id="sfp-{i+1}">')
                svg.append(f'    <title>{tooltip}</title>')
                
                # SFP port rectangle
                svg.append(f'    <rect x="{sfp_x}" y="{sfp_y}" width="{sfp_width}" height="{sfp_height}" '
                          f'fill="{sfp_color}" stroke="#000000" stroke-width="1" rx="2" ry="2" />')
                
                # SFP port label
                svg.append(f'    <text x="{sfp_x + sfp_width/2}" y="{sfp_y + sfp_height/2 + 4}" '
                          f'font-family="Arial" font-size="10" fill="white" '
                          f'text-anchor="middle" dominant-baseline="middle">{sfp_label}</text>')
                
                svg.append(f'  </g>')
        
        return svg
