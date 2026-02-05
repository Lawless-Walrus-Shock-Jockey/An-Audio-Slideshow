from flask import Flask, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os
from pydub import AudioSegment

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'mp3', 'wav'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_audio(input_path, output_path):
    # Example: Just convert to WAV format
    sound = AudioSegment.from_file(input_path)
    sound.export(output_path, format="wav")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        file.save(input_path)
        process_audio(input_path, output_path)
        return jsonify({'message': 'File uploaded and processed successfully', 'filename': filename})
    return jsonify({'error': 'Invalid file format'})

@app.route('/download/&lt;filename&gt;', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)