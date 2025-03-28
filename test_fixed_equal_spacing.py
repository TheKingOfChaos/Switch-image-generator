#!/usr/bin/env python3
"""
Test script to generate switches with equal spacing on both sides.
This script generates switches of different sizes and saves them to the output directory.
"""

import os
import webbrowser
from src.switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme, PortStatus

def generate_switch(num_ports, output_file):
    """Generate a switch with the specified number of ports."""
    # Create a switch with the specified number of ports
    generator = SwitchSVGGenerator(
        num_ports=num_ports,
        switch_model=SwitchModel.ENTERPRISE,
        switch_name=f"{num_ports}-Port Switch (Equal Spacing)",
        theme=Theme.DARK,
        output_file=output_file
    )
    
    # Save the SVG
    generator.save_svg()
    
    return output_file

def create_html_comparison(output_files):
    """Create an HTML file to compare the switches."""
    html_file = "output/equal_spacing_comparison.html"
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Switch Equal Spacing Comparison</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #333; }
            .switch-container { margin-bottom: 30px; }
            .switch-title { font-size: 18px; font-weight: bold; margin-bottom: 10px; }
            .switch-image { border: 1px solid #ccc; }
        </style>
    </head>
    <body>
        <h1>Switch Equal Spacing Comparison</h1>
        <p>This page shows switches of different sizes with equal spacing on both sides.</p>
    """
    
    for file in output_files:
        switch_name = os.path.basename(file).replace(".svg", "")
        html_content += f"""
        <div class="switch-container">
            <div class="switch-title">{switch_name}</div>
            <div class="switch-image">
                <img src="{file}" alt="{switch_name}" />
            </div>
        </div>
        """
    
    html_content += """
    </body>
    </html>
    """
    
    with open(html_file, "w") as f:
        f.write(html_content)
    
    return html_file

def main():
    """Generate switches of different sizes and create a comparison HTML file."""
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    # Test switches with different numbers of ports
    port_counts = [8, 16, 24, 48]
    output_files = []
    
    print("Generating switches with equal spacing:")
    print("--------------------------------------")
    
    for num_ports in port_counts:
        output_file = f"output/equal_spacing_{num_ports}_ports.svg"
        generate_switch(num_ports, output_file)
        output_files.append(output_file)
        print(f"Generated {num_ports}-port switch: {output_file}")
    
    # Create HTML comparison file
    html_file = create_html_comparison(output_files)
    print(f"\nCreated comparison HTML file: {html_file}")
    
    # Open the HTML file in the default web browser
    try:
        abs_path = os.path.abspath(html_file)
        file_url = f"file://{abs_path}"
        print(f"Opening {file_url} in browser...")
        webbrowser.open(file_url)
    except Exception as e:
        print(f"Error opening HTML file in browser: {e}")

if __name__ == "__main__":
    main()
