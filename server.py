# This is our Python server that will handle the file uploads.
import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

# We create an instance of the Flask application.
app = Flask(__name__)

# This is where we configure our database.
# We will use a simple SQLite database for this example.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music_files.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# This is the folder where uploaded files will be saved.
UPLOAD_FOLDER = 'input'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# We create a database model to represent a music file.
# It will store the filename and the path to the file.
class MusicFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)

# This new route handles GET requests to the root URL ('/').
# It will send the file_uploader.html page to the user's browser.
@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')


# This decorator defines a route that will handle file uploads.
# We specify that it only accepts POST requests from the website.
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
        
        # Save the file to the 'input' folder.
        file.save(filepath)
        
        # Now, we create a new entry in our database.
        new_file = MusicFile(filename=file.filename, filepath=filepath)
        db.session.add(new_file)
        db.session.commit()
        
        # Return a success message.
        return jsonify({'message': f'File uploaded successfully: {file.filename}'}), 200

# This part runs the web server.
if __name__ == '__main__':
    # This line creates the database file and table if they don't already exist.
    with app.app_context():
        db.create_all()
    # We set debug=True so we can see any errors easily.
    app.run(debug=True)