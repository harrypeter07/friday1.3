from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
METADATA_FILE = os.path.join(UPLOAD_FOLDER, 'metadata.json')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load or initialize metadata
if os.path.exists(METADATA_FILE):
    with open(METADATA_FILE, 'r') as f:
        file_metadata = json.load(f)
else:
    file_metadata = {}

# Save metadata helper
def save_metadata():
    with open(METADATA_FILE, 'w') as f:
        json.dump(file_metadata, f)

@app.route('/upload', methods=['POST'])
def upload():
    print('--- Upload endpoint called: client connected ---')
    if 'file' not in request.files:
        print('No file part in request')
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        print('No selected file')
        return 'No selected file', 400
    save_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(save_path)
    # Store upload time
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    file_metadata[file.filename] = now
    save_metadata()
    print(f'File uploaded: {file.filename} at {now}')
    return 'OK', 200

@app.route('/api/files', methods=['GET'])
def api_list_files():
    files = [f for f in os.listdir(UPLOAD_FOLDER) if f != 'metadata.json']
    return jsonify([
        {'filename': f, 'uploaded_at': file_metadata.get(f, '')}
        for f in files
    ])

@app.route('/files', methods=['GET'])
def html_list_files():
    files = [f for f in os.listdir(UPLOAD_FOLDER) if f != 'metadata.json']
    success = request.args.get('success')
    html = '<h2>Uploaded Files</h2>'
    if success:
        html += '<div style="color: green; font-weight: bold;">File uploaded successfully!</div>'
    html += '<ul>'
    for f in files:
        date = file_metadata.get(f, '')
        html += f'<li><a href="/files/{f}" download>{f}</a> <span style="color: #888; font-size: 0.9em;">({date})</span></li>'
    html += '</ul>'
    return html

@app.route('/files/<filename>', methods=['GET'])
def get_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000) 