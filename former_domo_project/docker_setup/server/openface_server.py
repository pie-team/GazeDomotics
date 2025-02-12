from flask import Flask, jsonify, request
import subprocess
import os
from werkzeug.utils import secure_filename
import docker #import from_env, containers

app = Flask(__name__)
UPLOAD_FOLDER = '/home/openface-build'  # Mounted in Docker Compose
RESULT_FOLDER = '/home/openface-build/output'  # Mounted in Docker Compose
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Initialize Docker client
client = docker.from_env()

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

    # Run OpenFace in the OpenFace container
    output_csv = os.path.join(app.config['RESULT_FOLDER'], 'test.csv')#filename.replace('.jpeg', '.csv'))
    try:
        exec_result = client.containers.get('openface_container').exec_run([
            'build/bin/FaceLandmarkImg',
            '-gaze',
            '-f', file_path,    
            '-of', output_csv  # Output CSV file
        ])
        if exec_result.exit_code != 0:
            raise Exception(exec_result.output.decode('utf-8'))
    except Exception as e:
        return jsonify({'error': 'Error during OpenFace processing', 'details': str(e)}), 500

    # Copy the output CSV file to the host's output directory
    host_output_csv = os.path.join('/Users/Louis/git/GazeDomotics/former_domo_project/docker_setup/server/output', filename.replace('.jpeg', '.csv'))
    try:
        subprocess.run(['cp', output_csv, host_output_csv], check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Error copying CSV file to host directory', 'details': str(e)}), 500

    return jsonify({'csv_path': host_output_csv}), 200
 

    output_csv = '/home/openface-build/output/test.csv'
    # Return the CSV file path
    if os.path.exists(output_csv):
        return jsonify({'csv_path': output_csv}), 200
    else:
        return jsonify({'error': 'CSV file not generated'}), 500

    # Copy the output CSV file to the host's output directory
    host_output_csv = os.path.join('/Users/Louis/git/GazeDomotics/former_domo_project/docker_setup/server/output', filename.replace('.jpeg', '.csv'))
    try:
        subprocess.run(['cp', output_csv, host_output_csv], check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Error copying CSV file to host directory', 'details': str(e)}), 500

    return jsonify({'csv_path': host_output_csv}), 200
 
@app.route('/test', methods=['GET', 'POST'])
def test():
    try:
        exec_result = client.containers.get('openface_container').exec_run(['ls', '/'])
        return ('Result:\n' + exec_result.output.decode('utf-8').strip() + '\n'), 200
    except Exception as e:
        return jsonify({'error': 'Error during environment variable test', 'details': str(e)}), 500

@app.route('/')
def hello():
	return "Hello World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug = True)