# Network Switch SVG Generator GUI

This document provides information on using the graphical user interface (GUI) for the Network Switch SVG Generator.

## Installation

The GUI requires the following dependencies:

- Python 3.6 or higher
- Tkinter (usually included with Python)
- Pillow (PIL) for image processing
- cairosvg for SVG to PNG conversion

You can install the required dependencies using the provided `run_gui.py` script, which will automatically check and install the necessary packages:

```bash
./run_gui.py
```

Alternatively, you can install the dependencies manually:

```bash
pip install -r requirements_gui.txt
```

## Running the GUI

There are two ways to run the GUI:

1. Using the `run_gui.py` script (recommended for first-time users):

```bash
./run_gui.py
```

2. Directly running the GUI script (if dependencies are already installed):

```bash
./gui.py
```

## Using the GUI

The GUI is divided into three main sections:

1. **Configuration** - Where you set the parameters for the switch
2. **Preview** - Where you see a real-time preview of the switch
3. **Action Buttons** - For generating, saving, and previewing the SVG

### Configuration Options

- **Layout Mode**: Choose between "zigzag" (double row) or "single_row" layout
- **SFP-Only Mode**: Toggle to create a switch with only SFP ports (no regular ports)
- **Number of Ports**: Set the number of regular ports (1-24 for single row, 1-48 for zigzag)
- **Number of SFP Ports**: Set the number of SFP ports (limits depend on layout mode)
- **SFP Layout**: Choose between "zigzag" or "horizontal" layout for SFP ports
- **Theme**: Choose between "dark" or "light" color theme
- **Switch Model**: Select the switch model type
- **Switch Name**: Enter a custom name for the switch (optional)
- **Output File**: Specify the filename for the SVG output

### Action Buttons

- **Generate Preview**: Updates the preview with the current configuration
- **Save SVG**: Saves the SVG file to the specified output file
- **Open in Browser**: Saves the SVG file and opens it in the default web browser

### Dynamic Constraints

The GUI dynamically adjusts the available options based on your selections:

- When "single_row" layout is selected, the maximum number of ports is limited to 24 and SFP ports to 2
- When "zigzag" layout is selected, the maximum number of ports is 48 and SFP ports is 6
- When "SFP-Only Mode" is enabled, regular ports are disabled and SFP ports must be between 4 and 32

## Examples

### Creating a Single Row Switch

1. Select "single_row" from the Layout Mode dropdown
2. Set Number of Ports to 24
3. Set Number of SFP Ports to 2
4. Choose your preferred theme
5. Click "Generate Preview" to see the switch
6. Enter an output filename
7. Click "Save SVG" to save the file

### Creating an SFP-Only Switch

1. Check the "SFP-Only Mode" checkbox
2. Set Number of SFP Ports to a value between 4 and 32
3. Choose your preferred SFP Layout
4. Click "Generate Preview" to see the switch
5. Enter an output filename
6. Click "Save SVG" to save the file

## Troubleshooting

### Preview Not Showing

If the preview doesn't appear, check that:

1. You have all the required dependencies installed
2. The configuration values are within valid ranges
3. There's enough memory available for image processing

### Error Messages

The GUI will display error messages in the preview area if there are issues with:

- Invalid configuration values
- Problems generating the SVG
- Issues converting the SVG to PNG for preview

### Dependencies Issues

If you encounter dependency-related errors:

1. Try running with the `run_gui.py` script which handles dependencies
2. Manually install the required packages:
   ```bash
   pip install Pillow cairosvg
   ```
3. Ensure Tkinter is installed with your Python distribution
