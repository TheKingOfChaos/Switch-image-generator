#!/usr/bin/env python3
"""
Single Row Switch SVG Generator
------------------------------
This script extends the SwitchSVGGenerator to create a switch with ports in a single row
rather than the default zigzag pattern.

DEPRECATED: This module is kept for backward compatibility.
            New code should use SwitchSVGGenerator with layout_mode=LayoutMode.SINGLE_ROW instead.
"""

import sys
import os
import warnings

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.dirname(current_dir))  # Add parent directory too

# Try different import approaches to handle both direct and relative imports
try:
    # Try direct import first (when run from project root)
    from src.switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme, PortStatus, LayoutMode
except ImportError:
    # Fall back to regular import (when src is in path)
    from switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme, PortStatus, LayoutMode

class SingleRowSwitchGenerator(SwitchSVGGenerator):
    """
    Extended generator that places all ports in a single row.
    
    DEPRECATED: This class is kept for backward compatibility.
                New code should use SwitchSVGGenerator with layout_mode=LayoutMode.SINGLE_ROW instead.
    """
    
    def __init__(self, **kwargs):
        """
        Initialize the single row switch generator.
        
        Args:
            **kwargs: All arguments are passed to the parent class
        """
        # Show deprecation warning
        warnings.warn(
            "SingleRowSwitchGenerator is deprecated. "
            "Use SwitchSVGGenerator with layout_mode=LayoutMode.SINGLE_ROW instead.",
            DeprecationWarning,
            stacklevel=2
        )
        
        # Force single row layout mode
        kwargs['layout_mode'] = LayoutMode.SINGLE_ROW
        
        # Initialize the parent class with single row layout
        super().__init__(**kwargs)
