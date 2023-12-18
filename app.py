from flask import Flask, request, jsonify
import os
from tqdm import tqdm

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    # Allow all file formats
    return True

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        file_size = int(request.headers['Content-Length'])
        file_format = file.filename.rsplit('.', 1)[1].lower()
        print(f"File Properties:\n  - Name: {file.filename}\n  - Size: {file_size} bytes\n  - Format: {file_format}")

        # Set up progress bar
        tqdm_bar = tqdm(total=file_size, unit='B', unit_scale=True, desc='Uploading', position=0, leave=True)

        # Save the uploaded file in chunks
        chunk_size = 1024  # Adjust the chunk size as needed
        uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

        with open(uploaded_file_path, 'wb') as uploaded_file:
            for chunk in file.stream:
                uploaded_file.write(chunk)
                tqdm_bar.update(len(chunk))

        tqdm_bar.close()
        return jsonify({'message': 'File uploaded successfully', 'filename': file.filename})

    return jsonify({'error': 'Invalid file format'})

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(host='0.0.0.0', port=5000, debug=True)
