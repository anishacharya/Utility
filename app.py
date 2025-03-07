#!/usr/bin/env python3
"""
Image Converter Web Application

A web interface for the image converter utility, allowing users to upload images,
select output formats, and download the converted images.
"""

import os
import uuid
from flask import Flask, render_template, request, send_file, redirect, url_for, flash
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
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html', output_formats=OUTPUT_FORMATS)

@app.route('/convert', methods=['POST'])
def convert():
    # Check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    
    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
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
        
        try:
            # Convert the image
            convert_image(input_path, output_path)
            
            # Return the converted file for download
            return send_file(output_path, as_attachment=True, download_name=f"{base_name}.{output_format}")
        except Exception as e:
            flash(f"Error converting image: {str(e)}")
            return redirect(url_for('index'))
        finally:
            # Clean up files after sending
            try:
                if os.path.exists(input_path):
                    os.remove(input_path)
                if os.path.exists(output_path):
                    os.remove(output_path)
            except:
                pass  # Ignore cleanup errors
    else:
        flash('File type not allowed')
        return redirect(url_for('index'))

@app.errorhandler(413)
def request_entity_too_large(error):
    flash('File too large (max 16MB)')
    return redirect(url_for('index')), 413

if __name__ == '__main__':
    # Make the server accessible from any device on the network
    app.run(debug=True, host='0.0.0.0', port=5000) 