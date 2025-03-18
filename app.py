#!/usr/bin/env python3
"""
Image Converter Web Application

A web interface for the image converter utility, allowing users to upload images,
select output formats, and download the converted images.
"""

import os
import uuid
import time
from flask import Flask, render_template, request, send_file, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from img_converter import convert_image

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'converted'
ALLOWED_EXTENSIONS = {'heic', 'jpg', 'jpeg', 'png', 'bmp', 'tiff', 'gif'}
OUTPUT_FORMATS = {'jpg': 'JPEG', 'jpeg': 'JPEG', 'png': 'PNG', 'bmp': 'BMP', 'tiff': 'TIFF', 'gif': 'GIF'}

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB max upload size

def allowed_file(filename):
    """Check if the file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html', output_formats=OUTPUT_FORMATS)

@app.route('/convert', methods=['POST'])
def convert():
    """Handle image conversion"""
    # Check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        try:
            # Generate unique filenames
            original_extension = os.path.splitext(file.filename)[1].lower()
            unique_id = str(uuid.uuid4())
            
            # Secure the filename
            secure_name = secure_filename(file.filename)
            base_name = os.path.splitext(secure_name)[0]
            
            # Save the uploaded file
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{base_name}_{unique_id}{original_extension}")
            file.save(input_path)
            
            # Get the output format
            output_format = request.form.get('output_format', 'jpg')
            if output_format not in OUTPUT_FORMATS:
                output_format = 'jpg'  # Default to jpg if invalid format
            
            # Create output path
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{base_name}_{unique_id}.{output_format}")
            
            # Add a small delay to ensure file is saved properly
            time.sleep(0.5)
            
            # Convert the image
            convert_image(input_path, output_path)
            
            # Return the converted file for download
            return send_file(
                output_path, 
                as_attachment=True, 
                download_name=f"{base_name}.{output_format}",
                mimetype=f"image/{output_format}"
            )
        except Exception as e:
            app.logger.error(f"Error converting image: {str(e)}")
            flash(f"Error converting image: {str(e)}")
            return redirect(url_for('index'))
        finally:
            # Clean up files after sending
            try:
                if os.path.exists(input_path):
                    os.remove(input_path)
                if os.path.exists(output_path):
                    os.remove(output_path)
            except Exception as e:
                app.logger.error(f"Error cleaning up files: {str(e)}")
                pass  # Ignore cleanup errors
    else:
        flash('File type not allowed. Supported formats: HEIC, JPG, JPEG, PNG, BMP, TIFF, GIF')
        return redirect(url_for('index'))

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    flash('File too large (max 32MB)')
    return redirect(url_for('index')), 413

@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors"""
    return render_template('index.html', output_formats=OUTPUT_FORMATS, error="Page not found"), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    app.logger.error(f"Server error: {str(error)}")
    return render_template('index.html', output_formats=OUTPUT_FORMATS, error="Server error occurred. Please try again."), 500

if __name__ == '__main__':
    # Make the server accessible from any device on the network
    # Using port 8080 instead of 5000 to avoid conflicts with AirPlay Receiver on macOS
    app.run(debug=True, host='0.0.0.0', port=8080) 