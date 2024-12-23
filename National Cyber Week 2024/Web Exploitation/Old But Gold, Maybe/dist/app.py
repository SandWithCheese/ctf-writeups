from flask import Flask, request, jsonify, render_template
from lxml import etree
from random import randint
import os
import uuid

app = Flask(__name__)

SONG_DB_PATH = os.path.join(os.path.dirname(__file__), 'database/song_data.xml')
song_db = None

try:
    app.logger.info("Loading song database")
    if os.path.exists(SONG_DB_PATH):
        with open(SONG_DB_PATH, 'r', encoding='utf-8', errors='ignore') as f:
            song_db = etree.parse(f)
        app.logger.info("Song database loaded successfully")
    else:
        app.logger.error(f"Song database file not found at: {SONG_DB_PATH}")
except Exception as e:
    app.logger.error(f"Error loading the song database: {e}")
    song_db = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/xml', methods=['POST'])
def xml_endpoint():
    try:
        xml_data = request.form['xml_data']
        parser = etree.XMLParser(resolve_entities=True, no_network=False, load_dtd=True)
        root = etree.fromstring(xml_data.encode(), parser=parser)
        input_song_id = root.find('.//songId').text
        
        if input_song_id is None or not input_song_id.isdigit() or int(input_song_id) < 0:
            return jsonify({'message': 'Invalid Song ID'}), 400
        
        if song_db is not None:
            song_exists = song_db.xpath(f"//song[songId='{input_song_id}']")
            if song_exists:
                song = song_exists[0]
                response = {
                    'message': 'Song found',
                    'songId': song.find('songId').text,
                    'songName': song.find('songName').text,
                    'songArtist': song.find('songArtist').text
                }
            else:
                response = {'message': 'Song not found'}
        else:
            response = {'message': 'Song database is not available'}

        return jsonify(response)
    
    except etree.XMLSyntaxError as e:
        random_id = str(uuid.uuid4())
        app.logger.error(f"XMLSyntaxError {random_id}: {e}")
        return jsonify({
            'error': f'Invalid XML, error ID: {random_id}'
        }), 400

    except Exception as e:
        random_id = str(uuid.uuid4())
        app.logger.error(f"Exception {random_id}: {e}")
        return jsonify({
            'error': f'Unknown error, error ID: {random_id}'
        }), 500

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)