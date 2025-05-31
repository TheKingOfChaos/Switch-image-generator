#!/usr/bin/env python3
"""
Graphical User Interface for the Network Switch SVG Generator.
This GUI allows users to configure and generate SVG visualizations of network switches.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tempfile
import webbrowser
import logging
import threading
from io import BytesIO
import base64
from PIL import Image, ImageTk

# Add the src directory to the Python path
src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_dir)

# Import the switch generator
try:
    from src.switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme, PortStatus, LayoutMode
except ImportError:
    try:
        from switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme, PortStatus, LayoutMode
    except ImportError:
        print("Error: Could not import SwitchSVGGenerator. Make sure the src directory is in your Python path.")
        sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Try to import cairosvg for SVG to PNG conversion
try:
    import cairosvg
    HAS_CAIROSVG = True
except ImportError:
    HAS_CAIROSVG = False
    logger.warning("cairosvg not found. SVG preview will be disabled.")

class SwitchGeneratorGUI:
    """GUI for the Network Switch SVG Generator."""
    
    def __init__(self, root):
        """Initialize the GUI."""
        self.root = root
        self.root.title("Network Switch SVG Generator")
        self.root.geometry("1000x800")
        self.root.minsize(800, 600)
        
        # Set up the main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create the configuration frame (left side)
        self.config_frame = ttk.LabelFrame(self.main_frame, text="Configuration", padding="10")
        self.config_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5, pady=5)
        
        # Create the preview frame (right side)
        self.preview_frame = ttk.LabelFrame(self.main_frame, text="Preview", padding="10")
        self.preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Initialize variables
        self.layout_mode = tk.StringVar(value="zigzag")
        self.sfp_only_mode = tk.BooleanVar(value=False)
        self.num_ports = tk.IntVar(value=24)
        self.num_sfp_ports = tk.IntVar(value=2)
        self.sfp_layout = tk.StringVar(value="zigzag")
        self.theme = tk.StringVar(value="dark")
        self.switch_model = tk.StringVar(value="enterprise")
        self.switch_name = tk.StringVar(value="")
        self.output_file = tk.StringVar(value="switch.svg")
        
        # Create the configuration widgets
        self.create_config_widgets()
        
        # Create the preview widgets
        self.create_preview_widgets()
        
        # Create the action buttons
        self.create_action_buttons()
        
        # Set up event bindings
        self.setup_bindings()
        
        # Generate initial preview
        self.generate_preview()
    
    def create_config_widgets(self):
        """Create the configuration widgets."""
        # Layout mode
        ttk.Label(self.config_frame, text="Layout Mode:").grid(row=0, column=0, sticky=tk.W, pady=5)
        layout_combo = ttk.Combobox(self.config_frame, textvariable=self.layout_mode, 
                                    values=["zigzag", "single_row"], state="readonly")
        layout_combo.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # SFP-only mode
        ttk.Label(self.config_frame, text="SFP-Only Mode:").grid(row=1, column=0, sticky=tk.W, pady=5)
        sfp_only_check = ttk.Checkbutton(self.config_frame, variable=self.sfp_only_mode)
        sfp_only_check.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Number of ports
        ttk.Label(self.config_frame, text="Number of Ports:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ports_spinbox = ttk.Spinbox(self.config_frame, from_=1, to=48, textvariable=self.num_ports, width=5)
        ports_spinbox.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Number of SFP ports
        ttk.Label(self.config_frame, text="Number of SFP Ports:").grid(row=3, column=0, sticky=tk.W, pady=5)
        sfp_ports_spinbox = ttk.Spinbox(self.config_frame, from_=0, to=32, textvariable=self.num_sfp_ports, width=5)
        sfp_ports_spinbox.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # SFP layout
        ttk.Label(self.config_frame, text="SFP Layout:").grid(row=4, column=0, sticky=tk.W, pady=5)
        sfp_layout_combo = ttk.Combobox(self.config_frame, textvariable=self.sfp_layout, 
                                       values=["zigzag", "horizontal"], state="readonly")
        sfp_layout_combo.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Theme
        ttk.Label(self.config_frame, text="Theme:").grid(row=5, column=0, sticky=tk.W, pady=5)
        theme_combo = ttk.Combobox(self.config_frame, textvariable=self.theme, 
                                  values=["dark", "light"], state="readonly")
        theme_combo.grid(row=5, column=1, sticky=tk.W, pady=5)
        
        # Switch model
        ttk.Label(self.config_frame, text="Switch Model:").grid(row=6, column=0, sticky=tk.W, pady=5)
        model_combo = ttk.Combobox(self.config_frame, textvariable=self.switch_model, 
                                  values=["basic", "enterprise", "data_center", "stackable"], state="readonly")
        model_combo.grid(row=6, column=1, sticky=tk.W, pady=5)
        
        # Switch name
        ttk.Label(self.config_frame, text="Switch Name:").grid(row=7, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(self.config_frame, textvariable=self.switch_name, width=20)
        name_entry.grid(row=7, column=1, sticky=tk.W, pady=5)
        
        # Output file
        ttk.Label(self.config_frame, text="Output File:").grid(row=8, column=0, sticky=tk.W, pady=5)
        file_frame = ttk.Frame(self.config_frame)
        file_frame.grid(row=8, column=1, sticky=tk.W, pady=5)
        file_entry = ttk.Entry(file_frame, textvariable=self.output_file, width=15)
        file_entry.pack(side=tk.LEFT)
        browse_button = ttk.Button(file_frame, text="Browse", command=self.browse_output_file)
        browse_button.pack(side=tk.LEFT, padx=5)
    
    def create_preview_widgets(self):
        """Create the preview widgets."""
        # Create a canvas for the preview
        self.preview_canvas = tk.Canvas(self.preview_frame, bg="white", highlightthickness=0)
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create a label for the preview status
        self.preview_status = ttk.Label(self.preview_frame, text="No preview available")
        self.preview_status.pack(fill=tk.X, pady=5)
    
    def create_action_buttons(self):
        """Create the action buttons."""
        # Create a frame for the buttons
        button_frame = ttk.Frame(self.main_frame, padding="10")
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        # Generate preview button
        generate_button = ttk.Button(button_frame, text="Generate Preview", command=self.generate_preview)
        generate_button.pack(side=tk.LEFT, padx=5)
        
        # Save SVG button
        save_button = ttk.Button(button_frame, text="Save SVG", command=self.save_svg)
        save_button.pack(side=tk.LEFT, padx=5)
        
        # Open in browser button
        open_button = ttk.Button(button_frame, text="Open in Browser", command=self.open_in_browser)
        open_button.pack(side=tk.LEFT, padx=5)
    
    def setup_bindings(self):
        """Set up event bindings."""
        # Update constraints when layout mode changes
        self.layout_mode.trace_add("write", self.update_constraints)
        
        # Update constraints when SFP-only mode changes
        self.sfp_only_mode.trace_add("write", self.update_constraints)
        
        # Update the initial constraints
        self.update_constraints()
    
    def update_constraints(self, *args):
        """Update the constraints based on the current configuration."""
        layout = self.layout_mode.get()
        sfp_only = self.sfp_only_mode.get()
        
        # Get the spinbox widgets
        ports_spinbox = self.config_frame.winfo_children()[5]
        sfp_ports_spinbox = self.config_frame.winfo_children()[7]
        
        if sfp_only:
            # Disable regular ports for SFP-only mode
            ports_spinbox.configure(state="disabled")
            self.num_ports.set(0)
            
            # Set SFP port limits for SFP-only mode
            sfp_ports_spinbox.configure(from_=4, to=32)
            if self.num_sfp_ports.get() < 4:
                self.num_sfp_ports.set(4)
        else:
            # Enable regular ports
            ports_spinbox.configure(state="normal")
            
            if layout == "single_row":
                # Set limits for single row layout
                ports_spinbox.configure(from_=1, to=24)
                sfp_ports_spinbox.configure(from_=0, to=2)
                
                # Adjust values if they exceed the limits
                if self.num_ports.get() > 24:
                    self.num_ports.set(24)
                if self.num_sfp_ports.get() > 2:
                    self.num_sfp_ports.set(2)
            else:  # zigzag layout
                # Set limits for zigzag layout
                ports_spinbox.configure(from_=1, to=48)
                sfp_ports_spinbox.configure(from_=0, to=6)
                
                # Adjust values if they exceed the limits
                if self.num_ports.get() > 48:
                    self.num_ports.set(48)
                if self.num_sfp_ports.get() > 6:
                    self.num_sfp_ports.set(6)
    
    def browse_output_file(self):
        """Open a file dialog to select the output file."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".svg",
            filetypes=[("SVG files", "*.svg"), ("All files", "*.*")],
            initialfile=self.output_file.get()
        )
        if filename:
            self.output_file.set(filename)
    
    def generate_preview(self):
        """Generate a preview of the switch."""
        try:
            # Update the preview status
            self.preview_status.config(text="Generating preview...")
            self.root.update_idletasks()
            
            # Create a temporary file for the SVG
            with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as temp_file:
                temp_svg_path = temp_file.name
            
            # Generate the switch SVG
            switch = self.create_switch_generator(temp_svg_path)
            switch.save_svg()
            
            # Convert SVG to PNG for preview
            if HAS_CAIROSVG:
                # Use cairosvg to convert SVG to PNG
                png_data = cairosvg.svg2png(url=temp_svg_path, scale=1.0)
                
                # Load the PNG data into a PIL Image
                image = Image.open(BytesIO(png_data))
                
                # Resize the image to fit the canvas
                canvas_width = self.preview_canvas.winfo_width()
                canvas_height = self.preview_canvas.winfo_height()
                
                # Calculate the scaling factor to fit the image in the canvas
                image_width, image_height = image.size
                scale_width = canvas_width / image_width if image_width > 0 else 1
                scale_height = canvas_height / image_height if image_height > 0 else 1
                scale = min(scale_width, scale_height, 1.0)  # Don't scale up
                
                # Resize the image
                new_width = int(image_width * scale)
                new_height = int(image_height * scale)
                if new_width > 0 and new_height > 0:
                    image = image.resize((new_width, new_height), Image.LANCZOS)
                
                # Convert the PIL Image to a Tkinter PhotoImage
                photo = ImageTk.PhotoImage(image)
                
                # Clear the canvas
                self.preview_canvas.delete("all")
                
                # Display the image on the canvas
                self.preview_canvas.create_image(
                    canvas_width // 2, canvas_height // 2, 
                    image=photo, anchor=tk.CENTER
                )
                
                # Keep a reference to the photo to prevent garbage collection
                self.preview_canvas.image = photo
                
                # Update the preview status
                self.preview_status.config(text=f"Preview generated ({image_width}x{image_height})")
            else:
                # If cairosvg is not available, show a message
                self.preview_canvas.delete("all")
                self.preview_canvas.create_text(
                    self.preview_canvas.winfo_width() // 2,
                    self.preview_canvas.winfo_height() // 2,
                    text="Preview not available (cairosvg not installed)",
                    fill="black"
                )
                self.preview_status.config(text="Preview not available (cairosvg not installed)")
            
            # Clean up the temporary file
            try:
                os.unlink(temp_svg_path)
            except:
                pass
        
        except Exception as e:
            # Show the error message
            self.preview_canvas.delete("all")
            self.preview_canvas.create_text(
                self.preview_canvas.winfo_width() // 2,
                self.preview_canvas.winfo_height() // 2,
                text=f"Error generating preview:\n{str(e)}",
                fill="red"
            )
            self.preview_status.config(text=f"Error: {str(e)}")
            logger.error(f"Error generating preview: {e}", exc_info=True)
    
    def save_svg(self):
        """Save the switch SVG to a file."""
        try:
            # Get the output file path
            output_file = self.output_file.get()
            
            # Create the switch generator
            switch = self.create_switch_generator(output_file)
            
            # Save the SVG
            switch.save_svg()
            
            # Show a success message
            messagebox.showinfo("Success", f"SVG saved to {output_file}")
        
        except Exception as e:
            # Show an error message
            messagebox.showerror("Error", f"Failed to save SVG: {str(e)}")
            logger.error(f"Error saving SVG: {e}", exc_info=True)
    
    def open_in_browser(self):
        """Save the SVG and open it in a web browser."""
        try:
            # Get the output file path
            output_file = self.output_file.get()
            
            # Create the switch generator
            switch = self.create_switch_generator(output_file)
            
            # Save the SVG
            switch.save_svg()
            
            # Open the SVG in a web browser
            webbrowser.open(f"file://{os.path.abspath(output_file)}")
        
        except Exception as e:
            # Show an error message
            messagebox.showerror("Error", f"Failed to open SVG in browser: {str(e)}")
            logger.error(f"Error opening SVG in browser: {e}", exc_info=True)
    
    def create_switch_generator(self, output_file):
        """Create a SwitchSVGGenerator with the current configuration."""
        # Get the configuration values
        layout_mode_str = self.layout_mode.get()
        sfp_only_mode = self.sfp_only_mode.get()
        num_ports = self.num_ports.get()
        num_sfp_ports = self.num_sfp_ports.get()
        sfp_layout = self.sfp_layout.get()
        theme_str = self.theme.get()
        switch_model_str = self.switch_model.get()
        switch_name = self.switch_name.get()
        
        # Convert string values to enum values
        layout_mode = LayoutMode.SINGLE_ROW if layout_mode_str == "single_row" else LayoutMode.ZIGZAG
        theme = Theme.LIGHT if theme_str == "light" else Theme.DARK
        
        # Convert switch model string to enum value
        switch_model_map = {
            "basic": SwitchModel.BASIC,
            "enterprise": SwitchModel.ENTERPRISE,
            "data_center": SwitchModel.DATA_CENTER,
            "stackable": SwitchModel.STACKABLE
        }
        switch_model = switch_model_map.get(switch_model_str, SwitchModel.ENTERPRISE)
        
        # Create the switch generator
        if sfp_only_mode:
            # Create an SFP-only switch
            switch = SwitchSVGGenerator(
                sfp_ports=num_sfp_ports,
                sfp_only_mode=True,
                sfp_layout=sfp_layout,
                switch_model=switch_model,
                switch_name=switch_name if switch_name else None,
                theme=theme,
                output_file=output_file
            )
        else:
            # Create a regular switch
            switch = SwitchSVGGenerator(
                num_ports=num_ports,
                sfp_ports=num_sfp_ports,
                layout_mode=layout_mode,
                sfp_layout=sfp_layout,
                switch_model=switch_model,
                switch_name=switch_name if switch_name else None,
                theme=theme,
                output_file=output_file
            )
        
        return switch

def main():
    """Main function to run the GUI."""
    root = tk.Tk()
    app = SwitchGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
