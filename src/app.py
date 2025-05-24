from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    print(f'File uploaded: {file.filename}')
    return 'OK', 200

@app.route('/api/files', methods=['GET'])
def api_list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify(files)

@app.route('/files', methods=['GET'])
def html_list_files():
    files = os.listdir(UPLOAD_FOLDER)
    success = request.args.get('success')
    html = '<h2>Uploaded Files</h2>'
    if success:
        html += '<div style="color: green; font-weight: bold;">File uploaded successfully!</div>'
    html += '<ul>'
    for f in files:
        html += f'<li><a href="/files/{f}" download>{f}</a></li>'
    html += '</ul>'
    return html

@app.route('/files/<filename>', methods=['GET'])
def get_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000) 