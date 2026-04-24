import os
import numpy as np
from flask import Flask, request, render_template, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure upload folder and allowed files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load your trained AI brain!
print("Loading AI Model... This might take a few seconds.")
MODEL_PATH = os.path.join('model', 'deepfake_detector_model.h5')
model = load_model(MODEL_PATH)
print("Model Loaded Successfully!")

def process_and_predict(image_path):
    # 1. Prepare the image (exactly like Kaggle)
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    # 2. Ask the AI
    prediction = model.predict(img_array, verbose=0)
    score = float(prediction[0][0])

    # 3. Format the result
    if score >= 0.5:
        return {"verdict": "REAL", "confidence": f"{(score * 100):.2f}%"}
    else:
        return {"verdict": "FAKE", "confidence": f"{((1.0 - score) * 100):.2f}%"}

@app.route('/', methods=['GET'])
def index():
    # Serve the UI page
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # Run the prediction
            result = process_and_predict(filepath)
            
            # Clean up: delete the image so the server doesn't get full
            os.remove(filepath)
            
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)