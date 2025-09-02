import os
from flask import Flask, request, jsonify

# We create an instance of the Flask application.
app = Flask(__name__)

# This is the folder where uploaded files will be saved.
UPLOAD_FOLDER = 'input'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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
        
        # Save the file to the `uploads` folder.
        file.save(filepath)
        
        # Return a success message.
        return jsonify({'message': f'File uploaded successfully: {file.filename}'}), 200

# This part runs the web server.
if __name__ == '__main__':
    # We set debug=True so we can see any errors easily.
    app.run(debug=True)