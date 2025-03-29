#!/usr/bin/env python3
"""
Network Switch Generator
-----------------------
Main script to generate network switch SVG visualizations with configurable layouts.

This script provides a convenient entry point to the configurable switch generator.
"""

import sys
import os

# Add the src directory to the Python path
src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_dir)

# Import the main function from the configurable switch generator
try:
    # Try direct import first (when run from project root)
    from src.configurable_switch_generator import main as generator_main
except ImportError:
    # Fall back to regular import (when src is in path)
    from configurable_switch_generator import main as generator_main

if __name__ == "__main__":
    # Run the configurable switch generator
    generator_main()
