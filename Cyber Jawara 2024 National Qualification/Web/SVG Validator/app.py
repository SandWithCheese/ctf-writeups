import hashlib
import os
import random
import requests
import secrets
import string
from flask import Flask, render_template, request, jsonify
from lxml import etree

RECAPTCHA_SECRET_KEY = os.getenv('RECAPTCHA_SECRET_KEY')

app = Flask(__name__)

UPLOAD_FOLDER = '/tmp/'
MAX_FILE_SIZE = 5 * 1024
ALLOWED_EXTENSIONS = {'svg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def random_filename(extension):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12)) + '.' + extension

@app.route('/')
def index():
    site_key = os.getenv('RECAPTCHA_SITE_KEY')
    return render_template('index.html', site_key=site_key)

def is_valid_svg(file_path):
    tree = etree.parse(file_path)
    root = tree.getroot()
    return root.tag.endswith('svg')

@app.route('/upload', methods=['POST'])
def upload_file():
    recaptcha_response = request.form.get('g-recaptcha-response')
    if not recaptcha_response:
        return jsonify({'error': 'Missing reCAPTCHA'}), 400

    # Verify reCAPTCHA
    recaptcha_verify_url = 'https://www.google.com/recaptcha/api/siteverify'
    recaptcha_data = {
        'secret': RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    recaptcha_response = requests.post(recaptcha_verify_url, data=recaptcha_data)
    recaptcha_result = recaptcha_response.json()

    if not recaptcha_result.get('success'):
        return jsonify({'error': 'Invalid reCAPTCHA'}), 400

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file extension'}), 400

    file_path = ''

    try:
        extension = file.filename.rsplit('.', 1)[1].lower()

        filename = hashlib.sha256(
            (file.filename + str(secrets.token_hex)[:16]).encode('utf-8')
        ).hexdigest() + '.' + extension
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        valid = is_valid_svg(file_path)
        os.remove(file_path)

        return jsonify({'valid': valid})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5557)