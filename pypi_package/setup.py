from setuptools import setup, find_packages

setup(
    name="switch_svg_generator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pillow",  # For text width calculations
    ],
    entry_points={
        "console_scripts": [
            "switch-svg-generator=switch_svg_generator.cli:main",
        ],
    },
    python_requires=">=3.6",
)
