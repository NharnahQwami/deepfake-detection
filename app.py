from flask import Flask, render_template, request, jsonify
import torch
from PIL import Image
from transformers import ViTForImageClassification, ViTImageProcessor
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load model and processor globally
model = ViTForImageClassification.from_pretrained("Wvolf/ViT_Deepfake_Detection", num_labels=2)
processor = ViTImageProcessor.from_pretrained("Wvolf/ViT_Deepfake_Detection")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyze_image(image_path):
    try:
        # Load and process image
        image = Image.open(image_path)
        inputs = processor(images=image, return_tensors="pt")
        
        # Get model prediction
        outputs = model(**inputs)
        logits = outputs.logits
        
        # Get prediction probabilities
        probs = torch.nn.functional.softmax(logits, dim=-1)
        
        # Convert to Python list
        probs = probs[0].detach().numpy().tolist()
        
        # Get predicted class
        predicted_class = "real" if probs[0] > probs[1] else "fake"
        confidence = probs[0] if predicted_class == "real" else probs[1]
        
        return {
            'prediction': predicted_class,
            'confidence': float(confidence),
            'probabilities': {
                'real': float(probs[0]),
                'fake': float(probs[1])
            }
        }
            
    except Exception as e:
        return {'error': f"Processing Error: {str(e)}"}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect_deepfake():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            file.save(filepath)
            result = analyze_image(filepath)
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
    
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True)