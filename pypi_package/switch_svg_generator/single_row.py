"""
Network Switch SVG Generator - Single Row Module
----------------------------
This module provides a specialized generator for single row switches.
"""

from typing import Dict, Optional
from .core import SwitchSVGGenerator, PortStatus, SwitchModel, Theme, PortShape


class SingleRowSwitchGenerator(SwitchSVGGenerator):
    """
    A specialized generator for single row switches with optional SFP ports.
    
    This class extends SwitchSVGGenerator to create a single row switch layout
    with up to 24 normal ports and 2 SFP ports.
    """
    
    def __init__(
        self,
        num_ports: int = 24,
        sfp_ports: int = 0,
        switch_width: int = 800,
        switch_height: int = 130,
        port_width: int = 28,
        port_height: int = 28,
        port_spacing: int = 4,
        vlan_colors: Optional[Dict[int, str]] = None,
        port_vlan_map: Optional[Dict[int, int]] = None,
        port_status_map: Optional[Dict[int, PortStatus]] = None,
        port_labels: Optional[Dict[int, str]] = None,
        output_file: str = "single_row_switch.svg",
        switch_model: SwitchModel = SwitchModel.BASIC,
        model_name: str = "",
        switch_name: str = "",
        theme: Theme = Theme.LIGHT,
        port_shape: PortShape = PortShape.SQUARE,
        show_status_indicator: bool = True,
        port_group_size: int = 0,
        port_group_spacing: int = 7,
        port_start_number: int = 1,
    ):
        """
        Initialize a single row switch generator.
        
        Args:
            num_ports: Number of normal ports (1-24)
            sfp_ports: Number of SFP ports (0-2)
            switch_width: Width of the switch in pixels
            switch_height: Height of the switch in pixels
            port_width: Width of each port in pixels
            port_height: Height of each port in pixels
            port_spacing: Spacing between ports in pixels
            vlan_colors: Dictionary mapping VLAN IDs to color codes
            port_vlan_map: Dictionary mapping port numbers to VLAN IDs
            port_status_map: Dictionary mapping port numbers to their status
            port_labels: Dictionary mapping port numbers to custom labels
            output_file: Path to save the SVG file
            switch_model: The model of the switch to render
            switch_name: Custom name for the switch
            theme: Color theme to use (dark or light)
            port_shape: Shape of the ports (square, rounded, circular)
            show_status_indicator: Whether to show port status indicators
            port_group_size: Number of ports per group (0 means no grouping)
            port_group_spacing: Additional spacing between port groups in pixels
            port_start_number: Starting port number (0 or 1)
        """
        # Validate inputs for single row switch
        if num_ports < 1 or num_ports > 24:
            raise ValueError("Number of ports must be between 1 and 24 for a single row switch")
        
        if sfp_ports < 0 or sfp_ports > 2:
            raise ValueError("Number of SFP ports must be between 0 and 2 for a single row switch")
        
        # Set default switch name if not provided
        if not switch_name:
            if sfp_ports > 0:
                switch_name = f"{num_ports}-Port Switch with {sfp_ports} SFP (Single Row)"
            else:
                switch_name = f"{num_ports}-Port Switch (Single Row)"
        
        # Initialize the parent class with single row configuration
        super().__init__(
            num_ports=num_ports,
            switch_width=switch_width,
            switch_height=switch_height,
            port_width=port_width,
            port_height=port_height,
            port_spacing=port_spacing,
            vlan_colors=vlan_colors,
            port_vlan_map=port_vlan_map,
            port_status_map=port_status_map,
            port_labels=port_labels,
            output_file=output_file,
            switch_model=switch_model,
            model_name=model_name,
            switch_name=switch_name,
            theme=theme,
            port_shape=port_shape,
            show_status_indicator=show_status_indicator,
            sfp_ports=sfp_ports,
            sfp_layout="horizontal",  # Force horizontal layout for SFP ports in single row
            port_group_size=port_group_size,
            port_group_spacing=port_group_spacing,
            sfp_only_mode=False,  # Never use SFP-only mode for single row
            port_start_number=port_start_number,
            zigzag_start_position="top",  # Not used in single row, but required
        )
