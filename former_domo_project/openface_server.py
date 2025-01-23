from flask import Flask, request, jsonify
import subprocess
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
RESULT_FOLDER = './results'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/process', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the uploaded file
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Run OpenFace
    output_csv = os.path.join(app.config['RESULT_FOLDER'], filename.replace('.jpeg', '.csv'))
    try:
        subprocess.run([
            'build/bin/FaceLandmarkImg',
            '-f', file_path,
            '-gaze',
            '-of', output_csv  # Output CSV file
        ], check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Error during OpenFace processing', 'details': str(e)}), 500

    # Return the CSV file path
    if os.path.exists(output_csv):
        return jsonify({'csv_path': output_csv}), 200
    else:
        return jsonify({'error': 'CSV file not generated'}), 500
    
@app.route('/test', methods=['POST'])
def test():
    #os.environ['TEST_VARIABLE'] = '42'
    try:
        result = subprocess.run([
            'pwd'
        ], capture_output=True, text=True, check=True)
        return jsonify({'pwd': result.stdout.strip()}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Error during environment variable test', 'details': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)