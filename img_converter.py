#!/usr/bin/env python3
"""
Image Format Converter CLI

A robust command-line tool to convert images across various formats, specifically designed to handle images 
from different devices including iPhone (HEIC format).

Supported formats:
    - Input: HEIC, JPG, JPEG, PNG, BMP, TIFF, GIF
    - Output: JPG, JPEG, PNG, BMP, TIFF, GIF

Prerequisites:
    Install system dependencies for HEIC:
    - macOS: brew install libheif
    - Ubuntu: sudo apt-get install libheif-dev

    Python Dependencies:
    pip install pillow pillow-heif

Usage:
    python img_converter.py --input <input_image_path> --output <output_image_path>

Example:
    python img_converter.py --input photo.heic --output photo.jpg
"""

import argparse
import os
from PIL import Image
import pillow_heif

# Register HEIF support with PIL
pillow_heif.register_heif_opener()

def validate_format(path, supported_formats):
    ext = os.path.splitext(path.lower())[1]
    if ext not in supported_formats:
        raise ValueError(f"Unsupported file format: {ext}. Supported formats are {', '.join(supported_formats)}")

def convert_image(input_path: str, output_path: str):
    """
    Convert an image from one format to another.
    
    Args:
        input_path: Path to the input image file
        output_path: Path for the output image file
    """
    input_ext = os.path.splitext(input_path.lower())[1]
    output_ext = os.path.splitext(output_path.lower())[1]
    
    # Open the image based on its format
    img = Image.open(input_path)
    
    # Convert to RGB if saving to a format that doesn't support alpha
    if output_ext in ['.jpg', '.jpeg'] and img.mode == 'RGBA':
        # Create a white background
        background = Image.new('RGB', img.size, (255, 255, 255))
        # Paste the image on the background
        background.paste(img, mask=img.split()[3])  # 3 is the alpha channel
        img = background
    
    # Save the image based on the output format
    if output_ext == '.heic':
        # Special handling for HEIC output
        heif_file = pillow_heif.HeifFile()
        heif_file.add_from_pillow(img)
        heif_file.save(output_path)
    else:
        # Standard save for other formats
        img.save(output_path, quality=95)  # Higher quality for JPG/JPEG
    
    # Close the image
    img.close()
    
    print(f"Successfully converted '{input_path}' to '{output_path}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Image Format Converter CLI with HEIC support",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('-i', '--input', required=True, help="Path to the input image file")
    parser.add_argument('-o', '--output', required=True, help="Path for the output image file")

    args = parser.parse_args()

    # Define supported formats once
    supported_formats = ['.heic', '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']

    if not os.path.exists(args.input):
        raise FileNotFoundError(f"Input file '{args.input}' does not exist.")

    validate_format(args.input, supported_formats)
    validate_format(args.output, supported_formats)

    convert_image(args.input, args.output)