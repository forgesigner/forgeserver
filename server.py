import subprocess
from dataclasses import dataclass
from typing import Union

from flask import Flask, request, jsonify, send_from_directory, abort
from werkzeug.datastructures import FileStorage

from config import API_KEY
import os

app = Flask(__name__)

app.config['IMAGES'] = '/root/forger/signheredetectordataset/CUAD_v1_rasterized'
app.config['ANNOTATIONS'] = '/root/forger/signheredetectordataset/CUAD_v1_annotations'
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'json'}

file_counter = 0


@dataclass
class DataItem:
    annot: Union[FileStorage, None]
    image: Union[FileStorage, None]


def is_authorized(api_key):
    return api_key == API_KEY


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def num_of_folders():
    return len(os.listdir(app.config['IMAGES']))


def run_script():
    subprocess.run(["/bin/bash", "/root/forger/signheredetector/train.sh"])


def save_files(annot: FileStorage, image: FileStorage):
    n = num_of_folders()
    os.mkdir(os.path.join(app.config['IMAGES'], "0" * (5 - len(str(n))) + str(n)))
    os.mkdir(os.path.join(app.config['ANNOTATIONS'], "0" * (5 - len(str(n))) + str(n)))
    annot.save(os.path.join(app.config['ANNOTATIONS'], "0" * (5 - len(str(n))) + str(n), annot.filename))
    image.save(os.path.join(app.config['IMAGES'], "0" * (5 - len(str(n))) + str(n), image.filename))
    global file_counter
    file_counter += 1
    if file_counter >= 1:
        run_script()
        file_counter = 0


def process_files(files):
    processed_files = {}
    for key in files.keys():
        t, idx = key.split('_')[0], key.split('_')[1]
        if idx not in processed_files.keys():
            if t == 'annot':
                processed_files[idx] = DataItem(files[key], None)
            elif t == 'image':
                processed_files[idx] = DataItem(None, files[key])
        else:
            if t == 'annot':
                processed_files[idx].annot = files[key]
            elif t == 'image':
                processed_files[idx].image = files[key]
    return processed_files


@app.route('/upload', methods=['POST'])
def upload_file():
    api_key = request.headers.get('Authorization')
    if not is_authorized(api_key):
        return jsonify({"error": "Unauthorized"}), 401

    files = request.files.to_dict()
    if len(files.keys()) % 2 == 1:
        return jsonify({"error": "Even amount of files are required"}), 400
    processed_files = process_files(files)

    for idx in processed_files.keys():
        if processed_files[idx].annot is None or processed_files[idx].image is None:
            return jsonify({"error": "Invalid request"}), 400

        if not allowed_file(processed_files[idx].annot.filename) or not allowed_file(
                processed_files[idx].image.filename):
            return jsonify({"error": "Invalid file type"}), 400

        save_files(processed_files[idx].annot, processed_files[idx].image)

    return jsonify({"message": "Files successfully uploaded"}), 200


@app.route('/download_checkpoint')
def download_file():
    directory = "/root/forger/checkpoints"
    try:
        return send_from_directory(directory, 'best_checkpoint.pth', as_attachment=True)
    except FileNotFoundError:
        abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
