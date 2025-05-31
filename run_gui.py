#!/usr/bin/env python3
"""
Script to run the Network Switch SVG Generator GUI.
This script checks for required dependencies and installs them if needed.
"""

import os
import sys
import subprocess
import importlib.util

def check_module(module_name):
    """Check if a Python module is installed."""
    return importlib.util.find_spec(module_name) is not None

def install_requirements():
    """Install required packages from requirements_gui.txt."""
    print("Installing required dependencies...")
    requirements_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'requirements_gui.txt')
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_file])
        print("Dependencies installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def check_dependencies():
    """Check if all required dependencies are installed."""
    required_modules = ['PIL', 'cairosvg', 'tkinter']
    missing_modules = []
    
    for module in required_modules:
        if not check_module(module):
            missing_modules.append(module)
    
    if missing_modules:
        print(f"Missing required modules: {', '.join(missing_modules)}")
        return False
    
    return True

def run_gui():
    """Run the GUI application."""
    gui_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gui.py')
    
    try:
        subprocess.check_call([sys.executable, gui_script])
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running GUI: {e}")
        return False
    except KeyboardInterrupt:
        print("\nGUI terminated by user.")
        return True

def main():
    """Main function to check dependencies and run the GUI."""
    print("Network Switch SVG Generator GUI")
    print("================================")
    
    # Check if dependencies are installed
    if not check_dependencies():
        print("Some dependencies are missing. Attempting to install...")
        if not install_requirements():
            print("Failed to install dependencies. Please install them manually:")
            print("  pip install -r requirements_gui.txt")
            return 1
    
    # Run the GUI
    print("Starting GUI...")
    if not run_gui():
        print("Failed to run the GUI. Please check the error messages above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
