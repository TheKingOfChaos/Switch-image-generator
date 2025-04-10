"""
Network Switch SVG Generator - Ports Module
----------------------------
This module contains the port generation methods for the switch SVG generator.
"""

from typing import List
import logging
from .core_base import PortStatus

# Configure logging
logger = logging.getLogger('switch_svg_generator')


def generate_ports(self, adjusted_width: int, ports_per_row: int, num_rows: int) -> List[str]:
    """
    Generate the SVG content for the switch ports.
    
    Args:
        adjusted_width: The calculated width of the SVG
        ports_per_row: Number of ports per row
        num_rows: Number of rows of ports
        
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
    sfp_spacing = 20    # Space between last regular port and first SFP port (not used in SFP-only mode)
    
    # Use the original left spacing (30px)
    start_x = start_spacing
    
    # Always add model spacing even if model is empty/basic
    # This ensures consistent spacing in all switch graphics
    # Model info would be at y=60, so start at y=70 (10px below)
    start_y = 70
    
    # Track the current port number
    port_num = 1
    
    # Generate regular RJ45 ports in a zigzag pattern (skip in SFP-only mode)
    if not self.sfp_only_mode:
        row_spacing = 4  # Use the same row spacing as defined in calculate_dimensions
        
        # Calculate how many columns we need
        # For zigzag pattern, we need twice as many columns
        ports_per_row = min(self.num_ports, 48)  # Allow up to 48 ports in zigzag (24 per row)
        num_cols = (self.num_ports + 1) // 2  # Ceiling division for odd number of ports
        
        for i in range(self.num_ports):
            # Make sure we generate exactly num_ports ports, regardless of port_start_number
            if i >= self.num_ports:
                break
                
            # Calculate row and column for zigzag pattern based on zigzag_start_position
            if self.zigzag_start_position == "top":
                # Even ports (0, 2, 4...) go in row 0 (top), odd ports (1, 3, 5...) go in row 1 (bottom)
                row = i % 2
            else:  # "bottom"
                # Even ports (0, 2, 4...) go in row 1 (bottom), odd ports (1, 3, 5...) go in row 0 (top)
                row = (i + 1) % 2
            col = i // 2
            
            # Calculate position with port grouping if enabled
            if self.port_group_size > 0 and col > 0:
                # Calculate which group this port belongs to
                # We need to use column number (not port number) for grouping
                # since we're using a zigzag pattern
                group_num = col // self.port_group_size
                
                # Add extra spacing between groups
                extra_spacing = group_num * self.port_group_spacing
                
                x = start_x + col * (self.port_width + self.port_spacing) + extra_spacing
            else:
                # Standard spacing without grouping
                x = start_x + col * (self.port_width + self.port_spacing)
                
            y = start_y + row * (self.port_height + row_spacing)
            
            color = self.get_port_color(port_num)
            
            # Create port group with tooltip
            # Adjust the displayed port number based on port_start_number
            display_port_num = i + self.port_start_number
            port_label = self.port_labels.get(port_num, str(display_port_num))
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
            if self.show_status_indicator:
                indicator_x = x + self.port_width - 5
                indicator_y = y + 5
                # Use specific colors for each status
                if status == PortStatus.UP:
                    indicator_color = "#2ecc71"  # Green for UP
                    stroke_color = "#000000"     # Black border
                elif status == PortStatus.DOWN:
                    indicator_color = "#e74c3c"  # Red for DOWN
                    stroke_color = "#000000"     # Black border
                else:  # DISABLED
                    indicator_color = "#000000"  # Black for DISABLED
                    stroke_color = "#000000"     # Black border
                
                svg.append(f'    <circle cx="{indicator_x}" cy="{indicator_y}" r="3" '
                          f'fill="{indicator_color}" stroke="{stroke_color}" stroke-width="0.5" />')
            
            svg.append(f'  </g>')
            
            port_num += 1
    
    # Generate SFP ports if requested
    if self.sfp_ports > 0:
        svg.append(f'  <!-- SFP Ports -->')
        
        # SFP ports are rotated 90 degrees (wider than tall)
        sfp_height = 20
        sfp_width = 40
        sfp_port_spacing = self.port_spacing
        
        # Calculate the position of the last regular port
        # For zigzag pattern, we need to find the rightmost port
        num_cols = (self.num_ports + 1) // 2  # Ceiling division for odd number of ports
        
        # Calculate the position of the last port, considering port grouping
        if self.port_group_size > 0 and num_cols > 0:
            # Calculate how many groups we have
            num_groups = (num_cols + self.port_group_size - 1) // self.port_group_size
            
            # Calculate extra spacing from grouping
            extra_spacing = (num_groups - 1) * self.port_group_spacing if num_groups > 0 else 0
            
            last_port_x = start_x + (num_cols - 1) * (self.port_width + self.port_spacing) + extra_spacing
        else:
            last_port_x = start_x + (num_cols - 1) * (self.port_width + self.port_spacing)
        
        # Calculate the total width available for ports (adjusted_width minus margins)
        available_width = adjusted_width - 2 * 10  # 10px margin on each side
        
        # Position SFP ports based on mode
        if self.sfp_only_mode:
            # In SFP-only mode, start SFP ports at the same position as regular ports would
            sfp_start_x = start_x
        else:
            # In normal mode, position SFP ports right after the last regular port with sfp_spacing
            sfp_start_x = last_port_x + self.port_width + sfp_spacing
        
        # Handle different SFP layouts
        if self.sfp_layout == "horizontal":
            # Place all SFP ports in a single horizontal row
            
            # Calculate how many groups we have for SFP ports
            sfp_groups = 1
            if self.sfp_group_size > 0 and self.sfp_ports > 0:
                sfp_groups = (self.sfp_ports + self.sfp_group_size - 1) // self.sfp_group_size
            
            # Calculate extra spacing from grouping
            sfp_extra_spacing = (sfp_groups - 1) * self.port_group_spacing if sfp_groups > 1 else 0
            
            # Calculate total width needed for SFP ports
            sfp_width_needed = (self.sfp_ports * sfp_width) + ((self.sfp_ports - 1) * sfp_port_spacing) + sfp_extra_spacing
            
            # Calculate the end position of the SFP ports
            sfp_end_x = sfp_start_x + sfp_width_needed
            
            # Check if this would exceed the available width
            if sfp_end_x > available_width + 10 - end_spacing:
                logger.warning(f"SFP ports would exceed available width. Adjusting switch width.")
            
            # Position SFP ports in a single row
            for i in range(self.sfp_ports):
                sfp_num = self.num_ports + i + self.port_start_number
                
                # Calculate position with SFP port grouping if enabled
                if self.sfp_group_size > 0 and i > 0:
                    # Calculate which group this SFP port belongs to
                    group_num = i // self.sfp_group_size
                    
                    # Add extra spacing between groups
                    extra_spacing = group_num * self.port_group_spacing
                    
                    sfp_x = sfp_start_x + i * (sfp_width + sfp_port_spacing) + extra_spacing
                else:
                    # Standard spacing without grouping
                    sfp_x = sfp_start_x + i * (sfp_width + sfp_port_spacing)
                
                # All SFP ports are in the same row, aligned with the bottom row of regular ports
                sfp_y = start_y + (self.port_height + 4)  # Align with bottom row
                
                # Use the VLAN color for the SFP port
                sfp_color = self.get_port_color(sfp_num)
                
                # Create SFP port group with tooltip
                sfp_label = self.port_labels.get(sfp_num, f"SFP{i}")
                vlan_id = self.port_vlan_map.get(sfp_num, 1)
                
                tooltip = f"SFP Port: {sfp_num}, Label: {sfp_label}, VLAN: {vlan_id}"
                
                svg.append(f'  <g id="sfp-{i+1}">')
                svg.append(f'    <title>{tooltip}</title>')
                
                # SFP port rectangle
                svg.append(f'    <rect x="{sfp_x}" y="{sfp_y}" width="{sfp_width}" height="{sfp_height}" '
                          f'fill="{sfp_color}" stroke="#000000" stroke-width="1" rx="2" ry="2" />')
                
                # SFP port label
                svg.append(f'    <text x="{sfp_x + sfp_width/2}" y="{sfp_y + sfp_height/2 + 4}" '
                          f'font-family="Arial" font-size="10" fill="white" '
                          f'text-anchor="middle" dominant-baseline="middle">{sfp_label}</text>')
                
                # Add status indicator for SFP ports too
                if self.show_status_indicator:
                    # Get the status for this SFP port
                    sfp_status = self.port_status_map.get(sfp_num, PortStatus.UP)
                    indicator_x = sfp_x + sfp_width - 5
                    indicator_y = sfp_y + 5
                    
                    # Always show status indicator regardless of status
                    svg.append(f'    <circle cx="{indicator_x}" cy="{indicator_y}" r="3" '
                          f'fill="{self.STATUS_COLORS[sfp_status.value]}" stroke="white" stroke-width="0.5" />')
                
                # Close the SFP port group
                svg.append(f'  </g>')
            
        else:  # Default to zigzag layout
            # Place SFP ports in a zigzag pattern (similar to regular ports)
            
            # Calculate how many columns we need for SFP ports
            sfp_cols = (self.sfp_ports + 1) // 2  # Ceiling division for odd number of SFP ports
            
            # Calculate how many groups we have for SFP ports
            sfp_groups = 1
            if self.sfp_group_size > 0 and sfp_cols > 0:
                sfp_groups = (sfp_cols + self.sfp_group_size - 1) // self.sfp_group_size
            
            # Calculate extra spacing from grouping
            sfp_extra_spacing = (sfp_groups - 1) * self.port_group_spacing if sfp_groups > 1 else 0
            
            # Calculate total width needed for SFP ports
            sfp_width_needed = (sfp_cols * sfp_width) + ((sfp_cols - 1) * sfp_port_spacing) + sfp_extra_spacing
            
            # Calculate the end position of the SFP ports
            sfp_end_x = sfp_start_x + sfp_width_needed
            
            # Check if this would exceed the available width
            if sfp_end_x > available_width + 10 - end_spacing:
                logger.warning(f"SFP ports would exceed available width. Adjusting switch width.")
            
            # Position SFP ports in a zigzag pattern
            for i in range(self.sfp_ports):
                sfp_num = self.num_ports + i + self.port_start_number
                
                # Calculate row and column for zigzag pattern based on zigzag_start_position
                if self.zigzag_start_position == "top":
                    # Even ports (0, 2, 4...) go in row 0 (top), odd ports (1, 3, 5...) go in row 1 (bottom)
                    row = i % 2
                else:  # "bottom"
                    # Even ports (0, 2, 4...) go in row 1 (bottom), odd ports (1, 3, 5...) go in row 0 (top)
                    row = (i + 1) % 2
                col = i // 2
                
                # Calculate position with SFP port grouping if enabled
                if self.sfp_group_size > 0 and col > 0:
                    # Calculate which group this SFP port belongs to
                    group_num = col // self.sfp_group_size
                    
                    # Add extra spacing between groups
                    extra_spacing = group_num * self.port_group_spacing
                    
                    sfp_x = sfp_start_x + col * (sfp_width + sfp_port_spacing) + extra_spacing
                else:
                    # Standard spacing without grouping
                    sfp_x = sfp_start_x + col * (sfp_width + sfp_port_spacing)
                
                # Position SFP ports vertically aligned with regular ports
                sfp_y = start_y + row * (self.port_height + 4)  # 4px spacing between rows
                
                # Use the VLAN color for the SFP port
                sfp_color = self.get_port_color(sfp_num)
                
                # Create SFP port group with tooltip
                # Adjust the displayed SFP port number based on port_start_number
                display_sfp_num = i + self.port_start_number
                sfp_label = self.port_labels.get(sfp_num, f"SFP{display_sfp_num}")
                vlan_id = self.port_vlan_map.get(sfp_num, 1)
                
                tooltip = f"SFP Port: {sfp_num}, Label: {sfp_label}, VLAN: {vlan_id}"
                
                svg.append(f'  <g id="sfp-{i+1}">')
                svg.append(f'    <title>{tooltip}</title>')
                
                # SFP port rectangle
                svg.append(f'    <rect x="{sfp_x}" y="{sfp_y}" width="{sfp_width}" height="{sfp_height}" '
                          f'fill="{sfp_color}" stroke="#000000" stroke-width="1" rx="2" ry="2" />')
                
                # SFP port label
                svg.append(f'    <text x="{sfp_x + sfp_width/2}" y="{sfp_y + sfp_height/2 + 4}" '
                          f'font-family="Arial" font-size="10" fill="white" '
                          f'text-anchor="middle" dominant-baseline="middle">{sfp_label}</text>')
                
                # Add status indicator for SFP ports too
                if self.show_status_indicator:
                    # Get the status for this SFP port
                    sfp_status = self.port_status_map.get(sfp_num, PortStatus.UP)
                    indicator_x = sfp_x + sfp_width - 5
                    indicator_y = sfp_y + 5
                    
                    # Always show status indicator regardless of status
                    svg.append(f'    <circle cx="{indicator_x}" cy="{indicator_y}" r="3" '
                          f'fill="{self.STATUS_COLORS[sfp_status.value]}" stroke="white" stroke-width="0.5" />')
                
                # Close the SFP port group
                svg.append(f'  </g>')
    return svg
