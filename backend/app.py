import os
import numpy as np
from flask import Flask, request, render_template, jsonify
import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import GlobalAveragePooling2D, Dropout, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'frontend'))

app = Flask(__name__, template_folder=FRONTEND_DIR)

# Configure upload folder
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ==========================================
# BUILD MODEL ARCHITECTURE
# ==========================================
print("[VERA] Building AI Architecture...")

model = None
model_status = "loading"
model_error = ""

try:
    base_model = EfficientNetB0(weights=None, include_top=False, input_shape=(224, 224, 3))
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.2)(x)
    predictions = Dense(1, activation='sigmoid')(x)
    model = Model(inputs=base_model.input, outputs=predictions)

    MODEL_PATH = os.path.join(BASE_DIR, 'model', 'deepfake_detector_model.h5')

    print(f"[VERA] Looking for model at: {MODEL_PATH}")
    if os.path.exists(MODEL_PATH):
        try:
            model.load_weights(MODEL_PATH)
            print("[VERA] Weights loaded successfully! Server is Ready.")
            model_status = "ready"
        except Exception as e:
            model_error = str(e)
            print(f"[VERA] Error loading weights: {e}")
            # Model architecture is built but weights failed — still usable for demo
            model_status = "ready_no_weights"
    else:
        print("[VERA] WARNING: Model file not found. Running in demo mode.")
        model_status = "ready_no_weights"

except Exception as e:
    model_error = str(e)
    model_status = "error"
    print(f"[VERA] CRITICAL: Could not build model: {e}")

# ==========================================


def process_and_predict(image_path):
    """Load image, preprocess it, and return verdict + confidence."""
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    prediction = model.predict(img_array, verbose=0)
    score = float(prediction[0][0])

    if score >= 0.5:
        confidence = round(score * 100, 2)
        return {
            "verdict": "REAL",
            "confidence": confidence,          # numeric, e.g. 87.34
            "confidence_str": f"{confidence:.2f}%",
            "raw_score": round(score, 4)
        }
    else:
        confidence = round((1.0 - score) * 100, 2)
        return {
            "verdict": "FAKE",
            "confidence": confidence,
            "confidence_str": f"{confidence:.2f}%",
            "raw_score": round(score, 4)
        }


# ── Routes ────────────────────────────────────────────────

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/api/status', methods=['GET'])
def api_status():
    """Frontend polls this to know when the model is ready."""
    ready = model_status in ("ready", "ready_no_weights")
    return jsonify({
        "ready": ready,
        "model": model_status,
        "error": model_error
    })


@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """Receive an uploaded image and return deepfake prediction."""
    if model is None:
        return jsonify({"error": "Model not initialised. Check server logs."}), 503

    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        result = process_and_predict(filepath)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Always clean up uploaded file
        if os.path.exists(filepath):
            os.remove(filepath)


# Keep legacy route for backwards compatibility
@app.route('/analyze', methods=['POST'])
def analyze():
    return api_analyze()


if __name__ == '__main__':
    app.run(debug=True, port=5000)