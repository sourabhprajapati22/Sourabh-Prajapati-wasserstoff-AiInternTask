from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from services.processor import process_query
from config import Config
import requests

api_bp = Blueprint('api', __name__)


def get_uploaded_files():
    folder = current_app.config['UPLOAD_FOLDER']
    return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]



@api_bp.route('/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist('files[]')
    filenames = []
    for file in files:
        filename = secure_filename(file.filename)
        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)
        filenames.append(filename)
    return jsonify({'files':get_uploaded_files()})


@api_bp.route('/query', methods=['POST'])
def handle_query():
    query = request.form.get('query')
    answer=process_query(query)
    return jsonify({'answer': answer})


@api_bp.route('/data')
def list_files():
    upload_folder = current_app.config['UPLOAD_FOLDER']
    try:
        files = [f for f in os.listdir(upload_folder) if os.path.isfile(os.path.join(upload_folder, f))]
        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/upload_from_url', methods=['POST'])
def upload_from_url():
    url = request.form.get('pdf_url')
    if not url or not url.lower().endswith('.pdf'):
        return jsonify({'error': 'Invalid PDF URL'}), 400

    try:
        response = requests.get(url)
        if response.status_code == 200:
            filename = os.path.basename(url)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return jsonify({'files': os.listdir(current_app.config['UPLOAD_FOLDER'])})
        else:
            return jsonify({'error': 'Failed to download file'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
