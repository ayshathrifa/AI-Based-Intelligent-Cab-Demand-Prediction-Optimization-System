import os
from flask import Blueprint, request, jsonify, current_app
from database.db import log_event

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Only CSV files allowed'}), 400
    save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
    file.save(save_path)
    with open(save_path, 'r') as f:
        rows = sum(1 for _ in f) - 1
    log_event('INFO', f'Dataset uploaded: {file.filename} ({rows} rows)')
    return jsonify({'message': 'Upload successful', 'filename': file.filename, 'rows': rows}), 200
