# Utility Suite

A collection of practical tools for everyday use, designed to simplify common tasks.

## Image Converter

A robust tool to convert images across various formats, with special support for iPhone HEIC images.

### Features

- Convert between multiple image formats
- Support for HEIC format from iPhones and other devices
- Available as both CLI and web interface
- Preserves image quality during conversion
- Handles transparency correctly when converting to formats without alpha channel support
- Simple, intuitive web UI for easy image conversion

### Supported Formats

- **Input**: HEIC, JPG, JPEG, PNG, BMP, TIFF, GIF
- **Output**: JPG, JPEG, PNG, BMP, TIFF, GIF

## Getting Started

### Prerequisites

#### System Dependencies for HEIC Support

- **macOS**: `brew install libheif`
- **Ubuntu/Debian**: `sudo apt-get install libheif-dev`

#### Python Dependencies

Install all required dependencies:

```bash
pip install -r requirements.txt
```

### Usage

#### Web Interface (Recommended)

Start the web server:

```bash
python app.py
```

Then open your browser and navigate to:
```
http://localhost:8080
```

The web interface allows you to:
1. Upload an image
2. Select the desired output format
3. Convert and download the converted image

![Web Interface Screenshot](https://via.placeholder.com/800x450.png?text=Image+Converter+Web+UI)

#### Command Line Interface

For batch processing or automation, you can use the CLI:

```bash
python img_converter.py --input <input_image_path> --output <output_image_path>
```

Example:
```bash
python img_converter.py --input photo.heic --output photo.jpg
```

## Project Structure

- `img_converter.py` - Core image conversion functionality
- `app.py` - Web server for the UI interface
- `templates/` - HTML templates for the web interface
- `static/` - CSS, JavaScript, and other static assets
- `uploads/` - Temporary storage for uploaded images (auto-created)
- `converted/` - Temporary storage for converted images (auto-created)

## Future Enhancements

- Batch conversion support
- Image resizing and optimization options
- Additional image formats
- Dark mode UI

## License

This project is licensed under the terms of the license included in the repository.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.