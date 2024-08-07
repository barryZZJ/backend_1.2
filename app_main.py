import os

from flask import request, jsonify, send_from_directory, send_file
from werkzeug.utils import secure_filename

from const import UPLOAD_FOLDER
from measure.routes import measure_bp
from desensitize.routes import desensitize_bp
from assess.routes import assess_bp

from app import app



app.register_blueprint(measure_bp)
app.register_blueprint(desensitize_bp)
app.register_blueprint(assess_bp)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # 1GB

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                   filename))
            return "success"
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/download', methods=['GET'])
def download():
    data = request.args
    if not data or 'filename' not in data:
        return jsonify({'error': 'argument "filename" is required'}), 400

    filename = secure_filename(data['filename'])
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404

    range_header = request.headers.get('Range', None)
    if range_header:
        return send_file(file_path, conditional=True)
    else:
        return send_file(file_path)


@app.route('/', methods=['GET'])
def status():
    return jsonify({'message': 'Connection successful'})

if __name__ == '__main__':
    app.run(debug=True, host='172.16.3.75')
