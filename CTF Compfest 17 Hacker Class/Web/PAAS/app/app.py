import pickle
import base64
from flask import Flask, request, jsonify, render_template
import pickletools
import io
from contextlib import redirect_stdout

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')  # Optional: static landing page

@app.route('/serialize', methods=['POST'])
def serialize():
    json_data = request.get_json()
    input_data = json_data['data']
    pickled_data, dis_output_str = pickle_json(input_data)
    return jsonify({'serialized_data': pickled_data, 'disassembly': dis_output_str})

@app.route('/deserialize', methods=['POST'])
def deserialize():
    json_data = request.get_json()
    input_data = json_data['data']
    try:
        pickled_data_bytes = base64.urlsafe_b64decode(input_data)
        deserialized_data = pickle.loads(pickled_data_bytes)
        return jsonify({
            'deserialized_data': str(deserialized_data),  # convert to string so file contents can be shown
            'disassembly': disassembly_str(pickled_data_bytes)
        })
    except Exception as e:
        return jsonify({'error': str(e)})

def pickle_json(json_data):
    pickled_data = base64.urlsafe_b64encode(
        pickle.dumps(json_data)).decode('utf-8')

    pickled_data_bytes = base64.urlsafe_b64decode(pickled_data)

    return pickled_data, disassembly_str(pickled_data_bytes)

def disassembly_str(pickled_data_bytes):
    dis_output = io.StringIO()
    with redirect_stdout(dis_output):
        pickletools.dis(pickled_data_bytes)
    return dis_output.getvalue()

if __name__ == '__main__':  
    app.run('0.0.0.0', 8888, debug=True)
