from flask import Blueprint, render_template, request
from flask_restful import Resource, Api
from PIL import Image
import numpy as np
import tensorflow as tf
import os

ai_model = Blueprint('ai_model', __name__, template_folder='templates')
api = Api(ai_model)

# 🔹 Class labels
class_labels = ["First-degree Burn", "Second-degree Burn", "Third-degree Burn"]

# 🔹 Model path
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'efficientnet_model.h5')

# 🔹 Global model cache
_model_instance = None

def load_model():
    global _model_instance
    if _model_instance is None:
        try:
            _model_instance = tf.keras.models.load_model(MODEL_PATH)
            print("✅ Model loaded successfully.")
        except Exception as e:
            print(f"❌ Failed to load model: {str(e)}")
            _model_instance = None
    return _model_instance

def predict_burn(image_file):
    model = load_model()
    if model is None:
        raise Exception("Model is not loaded.")

    # Load and preprocess the image
    image = Image.open(image_file)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image = image.resize((224, 224))
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    # Predict
    prediction = model.predict(image_array)[0]
    top_2_indices = np.argsort(prediction)[-2:][::-1]
    top_2_results = [
        {"class": class_labels[i], "confidence": float(prediction[i])}
        for i in top_2_indices
    ]
    return top_2_results, prediction

@ai_model.route('/', methods=['GET'])
def sendphoto():
    return render_template('ai_model/BurnDetector.html'), 200

# 🔹 Route: /predict
class AiModelResource(Resource):
    def post(self):
        try:
            if 'image' not in request.files:
                return {
                    'success': False,
                    'message': 'No image file provided'
                }, 400

            image_file = request.files['image']
            top_predictions, _ = predict_burn(image_file)
            top_class = top_predictions[0]["class"]
            confidence = top_predictions[0]["confidence"]
            confidence_threshold = 0.7

            if confidence < confidence_threshold:
                return {
                    "success": True,
                    "message": "⚠ Low confidence prediction. Please verify manually.",
                    "data": {"class": top_class}
                }, 200

            return {
                "success": True,
                "data": {"class": top_class},
                "message": "Burn degree prediction successful"
            }, 200

        except Exception as e:
            return {
                'success': False,
                'message': f'Prediction error: {str(e)}'
            }, 500

api.add_resource(AiModelResource, '/predict', endpoint='predict')

# 🔹 Route: /model-status
@ai_model.route('/model-status', methods=['GET'])
def model_status():
    model = load_model()
    if model is not None:
        return {
            "success": True,
            "message": "✅ Model is loaded and ready."
        }, 200
    else:
        return {
            "success": False,
            "message": "❌ Model is not loaded."
        }, 500
