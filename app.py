import os
import io
import uuid
import numpy as np
from flask import Flask, request, render_template, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

# ─────────────────────────────────────────────
#  App Configuration
# ─────────────────────────────────────────────
app = Flask(__name__)

BASE_DIR       = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER  = os.path.join(BASE_DIR, 'uploads')
MODEL_PATH     = os.path.join(BASE_DIR, 'model', 'deepfake_detector_model.h5')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER']    = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# ─────────────────────────────────────────────
#  Model Loading
# ─────────────────────────────────────────────
model        = None
model_status = "not_loaded"

print(f"[VERA] Looking for model at: {MODEL_PATH}")

if not os.path.exists(MODEL_PATH):
    model_status = "missing"
    print("[VERA] CRITICAL: Model file not found. Place 'deepfake_detector_model.h5' inside the 'model/' folder.")
else:
    try:
        model        = load_model(MODEL_PATH)
        model_status = "ready"
        print("[VERA] Model loaded successfully.")
    except Exception as e:
        model_status = "error"
        print(f"[VERA] Failed to load model: {e}")

# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────
def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def preprocess_and_predict(image_path: str) -> dict:
    """Load, preprocess, and run inference on the given image path."""
    img       = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    prediction = model.predict(img_array, verbose=0)
    score      = float(prediction[0][0])

    if score >= 0.5:
        return {
            "verdict":    "REAL",
            "confidence": round(score * 100, 2),
            "raw_score":  round(score, 4),
        }
    else:
        return {
            "verdict":    "FAKE",
            "confidence": round((1.0 - score) * 100, 2),
            "raw_score":  round(score, 4),
        }

# ─────────────────────────────────────────────
#  Routes
# ─────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/status')
def status():
    """Health-check endpoint the front-end can poll."""
    return jsonify({
        "app":    "Vera Deepfake Detector",
        "model":  model_status,
        "ready":  model_status == "ready",
    })


@app.route('/api/analyze', methods=['POST'])
def analyze():
    # 1. Guard: model must be ready
    if model_status != "ready":
        return jsonify({"error": f"Model is not ready (status: {model_status})."}), 503

    # 2. Guard: file must be present
    if 'file' not in request.files:
        return jsonify({"error": "No file included in the request."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected."}), 400

    # 3. Guard: extension whitelist
    if not allowed_file(file.filename):
        return jsonify({"error": f"Unsupported file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"}), 415

    # 4. Save with a unique name to avoid collisions
    ext      = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        result = preprocess_and_predict(filepath)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Always clean up the uploaded file
        if os.path.exists(filepath):
            os.remove(filepath)


# ─────────────────────────────────────────────
#  Entry Point
# ─────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, port=5000)