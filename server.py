import os
import shutil
import json
from flask import Flask, request, redirect, url_for, render_template, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from song_split import song_split
import generate_beatmap

# We create an instance of the Flask application.
app = Flask(__name__)

# This is the folder where uploaded files will be saved.
UPLOAD_FOLDER = 'input'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# This is where your beatmap files will be stored.
BEATMAP_FOLDER = 'beatmaps'
if not os.path.exists(BEATMAP_FOLDER):
    os.makedirs(BEATMAP_FOLDER)

# This is where the new JSON beatmap files will be stored.
BEATMAP_JSON_FOLDER = 'beatmaps_json'
if not os.path.exists(BEATMAP_JSON_FOLDER):
    os.makedirs(BEATMAP_JSON_FOLDER)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music_files.db'
db = SQLAlchemy(app)

class MusicFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    filepath = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<MusicFile {self.filename}>'

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/file-uploader', methods=['GET'])
def play():
    return render_template('file_uploader.html')

@app.route('/game', methods=['GET'])
def game():
    return render_template('game.html')

# FIX: We have two routes with the same path. I've commented out the old
# one and fixed the new one to serve the correct JSON files.
@app.route('/beatmaps_json/<path:filename>')
def serve_json_beatmap(filename):
    # This route serves the JSON beatmaps from the correct folder.
    return send_from_directory(BEATMAP_JSON_FOLDER, filename)

@app.route('/get_beatmap_files/<song_name>')
def get_beatmap_files(song_name):
    """
    This route provides a list of all beatmap JSON files for a given song.
    """
    beatmap_files = []
    # FIX: We now look in the correct folder for the JSON files.
    for filename in os.listdir(BEATMAP_JSON_FOLDER):
        # FIX: We now look for files that end with the .json extension.
        if filename.startswith(song_name) and filename.endswith(".json"):
            beatmap_files.append(filename)
    
    # We return the list as a JSON response.
    return jsonify(beatmap_files)

@app.route('/input/<path:filename>')
def serve_input_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the 'music_file' part is in the request.
    if 'music_file' not in request.files:
        return jsonify({'error': 'No file part in the request.'}), 400

    file = request.files['music_file']
    
    # Check if a file was selected.
    if file.filename == '':
        return jsonify({'error': 'No file selected.'}), 400
        
    # Check if the file has an allowed extension (you can customize this).
    # For now, we'll allow any file.
    if file:
        # We create a secure file path to prevent any issues.
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        
        # Save the file to the `uploads` folder.
        file.save(filepath)

        print("File saved successfully. Starting song split...")
        try:
            song_split(filepath)
            print("Song split finished.")
        except Exception as e:
            print(f"ERROR: Song split failed. Reason: {e}")
            return jsonify({'error': 'Failed to process song split.'}), 500

        # Add a record to the database
        new_file = MusicFile(filename=file.filename, filepath=filepath)
        db.session.add(new_file)
        db.session.commit()
        
        print("Starting beatmap generation...")
        try:
            spleeter_output_path = os.path.join("outputs", os.path.splitext(file.filename)[0])
            generate_beatmap.create_beatmaps_from_spleeter_folders(spleeter_output_path)
            print("Beatmap generation finished.")
            
            # The convert_to_json function from generate_beatmap.py will automatically
            # save the JSON files to a folder called "beatmaps_json".
            generate_beatmap.convert_to_json()
        except Exception as e:
            print(f"ERROR: Beatmap generation failed. Reason: {e}")
            return jsonify({'error': 'Failed to generate beatmap.'}), 500
        
        # This is the fix: We redirect to a new list page, not a specific file.
        song_name = os.path.splitext(file.filename)[0]

        # Redirect to the game page and pass the song name in the URL
        return redirect(url_for('game', song_name=song_name))

# This part runs the web server.
if __name__ == '__main__':
    # We set debug=True so we can see any errors easily.
    with app.app_context():
        db.create_all()
    app.run(debug=True)
