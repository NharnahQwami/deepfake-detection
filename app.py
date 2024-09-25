import os
import requests
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()  # Load .env file
# Load environment variables

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'}

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Load Gemini API key
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to interact with the Gemini API
def send_to_gemini(filepath=None, link=None):
    url = "https://test-xcrz.onrender.com/detect_deepfake?file_url="
    headers = {
        'Authorization': f'Bearer {GEMINI_API_KEY}',
        'Content-Type': 'application/json',
    }

    # If a file is being sent
    if filepath:
        with open(filepath, 'rb') as image_file:
            files = {'file': image_file}
            response = requests.post(url, headers=headers, files=files)
    
    # If a link is being sent
    elif link:
        data = {'image_url': link}
        response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return {'error': 'Error processing image with Gemini API'}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Send the file to Gemini API for detection
        result = send_to_gemini(filepath=filepath)
        return result if 'error' in result else f"AI Detection Result: {result}"

    return 'Invalid file format'

@app.route('/submit', methods=['POST'])
def submit_link():
    link = request.form['link']
    result = send_to_gemini(link=link)
    return result if 'error' in result else f"AI Detection Result: {result}"

if __name__ == '__main__':
    app.run(debug=True)
