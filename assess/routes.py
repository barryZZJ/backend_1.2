import os

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from const import UPLOAD_FOLDER

from .audio_assess import audio_assess
from .csv_assess import csv_assess
from .image_assess import image_assess
from .location_assess import location_assess
from .ofd_assess import ofd_assess
from .table_assess import table_assess
from .pdf_assess import pdf_assess
from .text_assess import text_assess
from .trace_assess import trace_assess
from .video_assess import video_assess

assess_bp = Blueprint('assess', __name__)

@assess_bp.route('/assess/audio_stream', methods=['POST'])
def assess_real_time_audio():
    data = request.json
    filepath1 = os.path.join(UPLOAD_FOLDER, secure_filename(data['filename1']))
    filepath2 = os.path.join(UPLOAD_FOLDER, secure_filename(data['filename2']))
    result = audio_assess(filepath1, filepath2, 'cos')
    return jsonify({'result': result})

@assess_bp.route('/assess/audio', methods=['POST'])
def assess_audio():
    data = request.json
    filepath1 = os.path.join(UPLOAD_FOLDER, secure_filename(data['filename1']))
    filepath2 = os.path.join(UPLOAD_FOLDER, secure_filename(data['filename2']))
    result = audio_assess(filepath1, filepath2, 'cos')
    return jsonify({'result': result})

@assess_bp.route('/assess/csv', methods=['POST'])
def assess_csv():
    data = request.json
    filepath1 = os.path.join(UPLOAD_FOLDER, secure_filename(data['filename1']))
    filepath2 = os.path.join(UPLOAD_FOLDER, secure_filename(data['filename2']))
    result = csv_assess(filepath1, filepath2)
    return jsonify({'result': result})

@assess_bp.route('/assess/image', methods=['POST'])
def assess_image():
    data = request.json
    filepath1 = os.path.join(UPLOAD_FOLDER, secure_filename(data['filename1']))
    filepath2 = os.path.join(UPLOAD_FOLDER, secure_filename(data['filename2']))
    result = image_assess(filepath1, filepath2, 'ssim')
    return jsonify({'result': result})

@assess_bp.route('/assess/location', methods=['POST'])
def assess_location():
    data = request.json
    result = location_assess(data['loc1'], data['loc2'])
    return jsonify({'result': result})


@assess_bp.route('/assess/table', methods=['POST'])
def assess_table():
    data = request.json
    filepath1 = os.path.join(UPLOAD_FOLDER, secure_filename(data['filename1']))
    filepath2 = os.path.join(UPLOAD_FOLDER, secure_filename(data['filename2']))
    result = table_assess(filepath1, filepath2)
    return jsonify({'result': result})

@assess_bp.route('/assess/ofd', methods=['POST'])
def assess_ofd():
    data = request.json
    filepath1 = os.path.join(UPLOAD_FOLDER, secure_filename(data['filename1']))
    filepath2 = os.path.join(UPLOAD_FOLDER, secure_filename(data['filename2']))
    result = ofd_assess(filepath1, filepath2)
    return jsonify({'result': result})

@assess_bp.route('/assess/pdf', methods=['POST'])
def assess_pdf():
    data = request.json
    filepath1 = os.path.join(UPLOAD_FOLDER, secure_filename(data['filename1']))
    filepath2 = os.path.join(UPLOAD_FOLDER, secure_filename(data['filename2']))
    result = pdf_assess(filepath1, filepath2)
    return jsonify({'result': result})

@assess_bp.route('/assess/text', methods=['POST'])
def assess_text():
    data = request.json
    result = text_assess(data['text1'], data['text2'])
    return jsonify({'result': result})

@assess_bp.route('/assess/trace', methods=['POST'])
def assess_trace():
    data = request.json
    result = trace_assess(data['trace1'], data['trace2'])
    return jsonify({'result': result})

@assess_bp.route('/assess/video', methods=['POST'])
def assess_video():
    data = request.json
    filepath1 = os.path.join(UPLOAD_FOLDER, secure_filename(data['filename1']))
    filepath2 = os.path.join(UPLOAD_FOLDER, secure_filename(data['filename2']))
    result = video_assess(filepath1, filepath2, 'ssim')
    return jsonify({'result': result})
