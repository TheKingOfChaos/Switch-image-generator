#!/usr/bin/env python3
"""
Test script to compare the original spacing with the fixed spacing.
This script generates switches with both the original and fixed spacing and creates a comparison HTML file.
"""

import os
import webbrowser
from src.switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme, PortStatus

def generate_original_spacing_switch(num_ports, output_file):
    """Generate a switch with the original spacing."""
    # Create a switch with the specified number of ports
    generator = SwitchSVGGenerator(
        num_ports=num_ports,
        switch_model=SwitchModel.ENTERPRISE,
        switch_name=f"{num_ports}-Port Switch (Original Spacing)",
        theme=Theme.DARK,
        output_file=output_file
    )
    
    # Calculate dimensions to initialize body_width and actual_body_width
    generator.calculate_dimensions()
    
    # Modify the body_width calculation to simulate the original spacing issue
    # This is done by using the actual_body_width instead of body_width
    generator.body_width = generator.actual_body_width - 20
    
    # Save the SVG
    generator.save_svg()
    
    return output_file

def generate_fixed_spacing_switch(num_ports, output_file):
    """Generate a switch with the fixed spacing."""
    # Create a switch with the specified number of ports
    generator = SwitchSVGGenerator(
        num_ports=num_ports,
        switch_model=SwitchModel.ENTERPRISE,
        switch_name=f"{num_ports}-Port Switch (Fixed Spacing)",
        theme=Theme.DARK,
        output_file=output_file
    )
    
    # Save the SVG
    generator.save_svg()
    
    return output_file

def create_html_comparison(original_files, fixed_files):
    """Create an HTML file to compare the original and fixed spacing."""
    html_file = "output/spacing_comparison.html"
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Switch Spacing Comparison</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1, h2 { color: #333; }
            .comparison-container { display: flex; margin-bottom: 40px; }
            .switch-container { flex: 1; margin-right: 20px; }
            .switch-title { font-size: 18px; font-weight: bold; margin-bottom: 10px; }
            .switch-image { border: 1px solid #ccc; }
            .highlight-spacing { 
                background-color: rgba(255, 255, 0, 0.3); 
                position: absolute; 
                height: 100px; 
                width: 20px; 
                z-index: 10;
            }
            .left-spacing { left: 10px; }
            .right-spacing-original { right: 10px; width: 106px; }
            .right-spacing-fixed { right: 10px; width: 20px; }
            .port-count { font-size: 24px; font-weight: bold; margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <h1>Switch Spacing Comparison: Original vs. Fixed</h1>
        <p>This page compares switches with the original spacing issue (uneven spacing) and the fixed spacing (equal spacing on both sides).</p>
        <p>The yellow highlight shows the spacing between the switch edge and the ports.</p>
    """
    
    # Sort files by port count
    port_counts = [8, 16, 24, 48]
    
    for port_count in port_counts:
        original_file = next((f for f in original_files if f"{port_count}-port" in f.lower()), None)
        fixed_file = next((f for f in fixed_files if f"{port_count}-port" in f.lower()), None)
        
        if original_file and fixed_file:
            html_content += f"""
            <div class="port-count">{port_count}-Port Switch</div>
            <div class="comparison-container">
                <div class="switch-container">
                    <div class="switch-title">Original Spacing</div>
                    <div class="switch-image" style="position: relative;">
                        <div class="highlight-spacing left-spacing"></div>
                        <div class="highlight-spacing right-spacing-original"></div>
                        <img src="{original_file}" alt="Original Spacing" />
                    </div>
                </div>
                <div class="switch-container">
                    <div class="switch-title">Fixed Spacing</div>
                    <div class="switch-image" style="position: relative;">
                        <div class="highlight-spacing left-spacing"></div>
                        <div class="highlight-spacing right-spacing-fixed"></div>
                        <img src="{fixed_file}" alt="Fixed Spacing" />
                    </div>
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
    """Generate switches with original and fixed spacing and create a comparison HTML file."""
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    # Test switches with different numbers of ports
    port_counts = [8, 16, 24, 48]
    original_files = []
    fixed_files = []
    
    print("Generating switches for comparison:")
    print("----------------------------------")
    
    for num_ports in port_counts:
        # Generate original spacing switch
        original_file = f"output/original_spacing_{num_ports}_ports.svg"
        generate_original_spacing_switch(num_ports, original_file)
        original_files.append(original_file)
        print(f"Generated {num_ports}-port switch with original spacing: {original_file}")
        
        # Generate fixed spacing switch
        fixed_file = f"output/fixed_spacing_{num_ports}_ports.svg"
        generate_fixed_spacing_switch(num_ports, fixed_file)
        fixed_files.append(fixed_file)
        print(f"Generated {num_ports}-port switch with fixed spacing: {fixed_file}")
    
    # Create HTML comparison file
    html_file = create_html_comparison(original_files, fixed_files)
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
