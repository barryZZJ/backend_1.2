# measure/__init__.py
import os

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from const import UPLOAD_FOLDER
from .audio_measure import audio_measure
from .audio_stream_measure import audio_stream_measure
from .csv_measure import csv_measure
from .image_measure import image_measure
from .location_measure import location_measure
from .number_measure import number_measure
from .ofd_pdf_measure import pdf_measure
from .text_measure import text_measure
from .trace_measure import trace_measure
from .video_measure import video_measure

measure_bp = Blueprint('measure', __name__)

@measure_bp.route('/measure/audio_stream', methods=['POST'])
def measure_real_time_audio():
    data = request.json
    filename = secure_filename(data['filename'])
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    data.setdefault('keyword', '')
    result = audio_stream_measure(filepath, data['keyword'])
    return jsonify({'result': result})

@measure_bp.route('/measure/audio', methods=['POST'])
def measure_audio():
    data = request.json
    filename = secure_filename(data['filename'])
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    data.setdefault('keyword', '')
    result = audio_measure(filepath, data['keyword'])
    return jsonify({'result': result})

@measure_bp.route('/measure/csv', methods=['POST'])
def measure_csv():
    data = request.json
    filename = secure_filename(data['filename'])
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    result = csv_measure(filepath)
    return jsonify({'result': result})

@measure_bp.route('/measure/image', methods=['POST'])
def measure_image():
    data = request.json
    print(data)
    filename = secure_filename(data['filename'])
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    result = image_measure(filepath)
    print(result)
    return jsonify({'result': result})

@measure_bp.route('/measure/location', methods=['POST'])
def measure_location():
    data = request.json
    location = data['location']
    zone_coords = data['zone_coords']
    dist_thresh = data.get('dist_thresh', 1000)
    print(data)
    result = location_measure(location, zone_coords, dist_thresh)
    return jsonify({'result': result})


@measure_bp.route('/measure/number', methods=['POST'])
def measure_number():
    data = request.json
    print(data)
    result = number_measure(data['num_to_measure'], data['num_private'])
    return jsonify({'result': result})

@measure_bp.route('/measure/pdf', methods=['POST'])
def measure_pdf():
    data = request.json
    filename = secure_filename(data['filename'])
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    result = pdf_measure(filepath)
    return jsonify({'result': result})

@measure_bp.route('/measure/text', methods=['POST'])
def measure_text():
    data = request.json
    text = data['text']
    data.setdefault('keyword', '')
    result = text_measure(text, data['keyword'])
    return jsonify({'result': result})

@measure_bp.route('/measure/trace', methods=['POST'])
def measure_trace():
    data = request.json
    trace = data['trace']
    zone_coords = data['zone_coords']
    dist_thresh = data.get('dist_thresh', 1000)
    result = trace_measure(trace, zone_coords, dist_thresh)
    return jsonify({'result': result})

@measure_bp.route('/measure/video', methods=['POST'])
def measure_video():
    data = request.json
    filename = secure_filename(data['filename'])
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    result = video_measure(filepath)
    return jsonify({'result': result})
