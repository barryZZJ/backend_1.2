import os

from PIL import Image
from flask import Blueprint, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename

from const import UPLOAD_FOLDER

from .audio_desensitize import add_beep
from .audio_stream_desensitize import add_beep_to_stream
from .csv.csv_desensitize import csv_desensitize
from .image_desensitize import gaussian_blur_region
from .location_desensitize import lap_coord_desensitize
from .number_desensitize import number_desensitize
from .ofd_desensitize import ofd_desensitize
from .pdf_desensitize import pdf_desensitize
from .table_desensitize import table_desensitize
from .text_desensitize import randomize_string
from .trace_desensitize import trace_desensitize
from .video_desensitize import pixelate_video_region

desensitize_bp = Blueprint('desensitize', __name__)

@desensitize_bp.route('/desensitize/audio_stream', methods=['POST'])
def desensitize_real_time_audio():
    data = request.json

    ifilename = secure_filename(data['ifilename'])
    ofilename = secure_filename(data['ofilename'])
    iformat = data['iformat']
    oformat = data['oformat']
    start = data['start']
    duration = data['duration']

    input_path = os.path.join(UPLOAD_FOLDER, ifilename)
    output_path = os.path.join(UPLOAD_FOLDER, ofilename)

    if not os.path.exists(input_path):
        return jsonify({'error': 'Input file not found'}), 404

    add_beep_to_stream(input_path, iformat, output_path, oformat, start, duration)

    return jsonify({'result': url_for('download', filename=ofilename)})

@desensitize_bp.route('/desensitize/audio', methods=['POST'])
def desensitize_audio():
    data = request.json

    ifilename = secure_filename(data['ifilename'])
    ofilename = secure_filename(data['ofilename'])
    iformat = data['iformat']
    oformat = data['oformat']
    start = data['start']
    duration = data['duration']

    input_path = os.path.join(UPLOAD_FOLDER, ifilename)
    output_path = os.path.join(UPLOAD_FOLDER, ofilename)

    if not os.path.exists(input_path):
        return jsonify({'error': 'Input file not found'}), 404

    add_beep(input_path, iformat, output_path, oformat, start, duration)

    return jsonify({'result': url_for('download', filename=ofilename)})

@desensitize_bp.route('/desensitize/csv', methods=['POST'])
def desensitize_csv():
    data = request.json

    ifilename = secure_filename(data['ifilename'])
    ofilename = secure_filename(data['ofilename'])

    input_path = os.path.join(UPLOAD_FOLDER, ifilename)
    output_path = os.path.join(UPLOAD_FOLDER, ofilename)

    k = data['k']
    QI_INDEX = data['QI_INDEX']
    SA_INDEX = data['SA_INDEX']

    if not os.path.exists(input_path):
        return jsonify({'error': 'Input file not found'}), 404

    csv_desensitize(input_path, k, QI_INDEX, SA_INDEX, output_path)

    return jsonify({'result': url_for('download', filename=ofilename)})

@desensitize_bp.route('/desensitize/image', methods=['POST'])
def desensitize_image():
    data = request.json

    ifilename = secure_filename(data['ifilename'])
    ofilename = secure_filename(data['ofilename'])
    region = data['region']

    radius = data.get('radius', 5)

    input_path = os.path.join(UPLOAD_FOLDER, ifilename)
    output_path = os.path.join(UPLOAD_FOLDER, ofilename)

    if not os.path.exists(input_path):
        return jsonify({'error': 'Input file not found'}), 404

    original_image = Image.open(input_path)
    region_gaussian_blurred_image = gaussian_blur_region(original_image, *region, radius)
    region_gaussian_blurred_image.save(output_path)

    return jsonify({'result': url_for('download', filename=ofilename)})

@desensitize_bp.route('/desensitize/location', methods=['POST'])
def desensitize_location():
    data = request.json
    eps = data.get('eps', 0.9)
    result = lap_coord_desensitize(*data['loc'], eps=eps)
    return jsonify({'result': result})

@desensitize_bp.route('/desensitize/number', methods=['POST'])
def desensitize_number():
    data = request.json
    print(data)
    result = number_desensitize(data['num'])
    return jsonify({'result': result})

@desensitize_bp.route('/desensitize/ofd', methods=['POST'])
def desensitize_ofd():
    data = request.json
    print(data)

    ifilename = secure_filename(data['ifilename'])
    ofilename = secure_filename(data['ofilename'])
    pages = data['pages']

    input_path = os.path.join(UPLOAD_FOLDER, ifilename)
    output_path = os.path.join(UPLOAD_FOLDER, ofilename)

    if not os.path.exists(input_path):
        return jsonify({'error': 'Input file not found'}), 404

    ofd_desensitize(input_path, pages, output_path)

    return jsonify({'result': url_for('download', filename=ofilename)})

@desensitize_bp.route('/desensitize/pdf', methods=['POST'])
def desensitize_pdf():
    data = request.json
    print(data)

    ifilename = secure_filename(data['ifilename'])
    ofilename = secure_filename(data['ofilename'])
    pages = data['pages']

    input_path = os.path.join(UPLOAD_FOLDER, ifilename)
    output_path = os.path.join(UPLOAD_FOLDER, ofilename)

    if not os.path.exists(input_path):
        return jsonify({'error': 'Input file not found'}), 404

    pdf_desensitize(input_path, pages, output_path)

    return jsonify({'result': url_for('download', filename=ofilename)})

@desensitize_bp.route('/desensitize/table', methods=['POST'])
def desensitize_table():
    data = request.json

    ifilename = secure_filename(data['ifilename'])
    ofilename = secure_filename(data['ofilename'])

    input_path = os.path.join(UPLOAD_FOLDER, ifilename)
    output_path = os.path.join(UPLOAD_FOLDER, ofilename)

    if not os.path.exists(input_path):
        return jsonify({'error': 'Input file not found'}), 404

    table_desensitize(input_path, output_path)

    return jsonify({'result': url_for('download', filename=ofilename)})

@desensitize_bp.route('/desensitize/text', methods=['POST'])
def desensitize_text():
    data = request.json
    result = randomize_string(data['text'], data['keyword'])
    return jsonify({'result': result})

@desensitize_bp.route('/desensitize/trace', methods=['POST'])
def desensitize_trace():
    data = request.json
    trace = data['trace']
    zone_coords = data['zone_coords']
    eps = data.get('eps', 0.9)
    dist_thresh = data.get('dist_thresh', 1000)

    result = trace_desensitize(trace, zone_coords, eps, dist_thresh)
    return jsonify({'result': result})

@desensitize_bp.route('/desensitize/video', methods=['POST'])
def desensitize_video():
    data = request.json

    ifilename = secure_filename(data['ifilename'])
    ofilename = secure_filename(data['ofilename'])
    region = data['region']
    block_size = data.get('block_size', 5)

    input_path = os.path.join(UPLOAD_FOLDER, ifilename)
    output_path = os.path.join(UPLOAD_FOLDER, ofilename)

    if not os.path.exists(input_path):
        return jsonify({'error': 'Input file not found'}), 404

    pixelate_video_region(input_path, output_path, *region, block_size)

    return jsonify({'result': url_for('download', filename=ofilename)})