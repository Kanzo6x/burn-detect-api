from flask import Blueprint, render_template, request
from flask_restful import Resource, Api
from PIL import Image
import numpy as np
import tensorflow as tf
import os


ai_model = Blueprint('ai_model', __name__, template_folder='templates')
api = Api(ai_model)

# 🔹 Ensure class labels match model's expected order
class_labels = ["First-degree Burn", "Second-degree Burn", "Third-degree Burn"]

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'efficientnet_model.h5')  
try:
    model = tf.keras.models.load_model(MODEL_PATH)
except Exception as e:
    print(f"Error loading model: {str(e)}")
    model = None

@ai_model.route('/',methods=['GET'])
def sendphoto():
    return render_template('ai_model/BurnDetector.html'), 200

class AiModelResource(Resource):
    def post(self):
        try:
            if model is None:
                return {
                    'success': False,
                    'message': 'Model not properly loaded'
                }, 500

            # Check if image file is present in request
            if 'image' not in request.files:
                return {
                'success': False,
                'message': 'No image file provided'},400
            
            image_file = request.files['image']
            
            # Open and preprocess the image
            image = Image.open(image_file)

            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # Resize image to match model input
            image = image.resize((224, 224))

            # Convert to numpy array and normalize
            image_array = np.array(image) / 255.0  # Normalize to [0,1]

            # Ensure correct input shape (batch size of 1)
            image_array = np.expand_dims(image_array, axis=0)


            # 🔹 Make prediction
            prediction = model.predict(image_array)[0]  # Extract first sample output

            # 🔹 Get Top-2 Predictions
            top_2_indices = np.argsort(prediction)[-2:][::-1]
            top_2_results = [
                {"class": class_labels[i], "confidence": float(prediction[i])}
                for i in top_2_indices
            ]

            # 🔹 Get highest confidence class
            predicted_index = top_2_results[0]["class"]
            confidence = top_2_results[0]["confidence"]

            # 🔹 Confidence threshold check
            confidence_threshold = 0.7  # Adjust based on real test images
            if confidence < confidence_threshold:
                return {
                    "success": True,
                    "message": "⚠ Low confidence prediction. Please verify manually.",
                    "data": {"top_predictions": top_2_results}
             }, 200

            # 🔹 Return final result
            return {
                "success": True,
                "data": {
                    "class": predicted_index,
                    "confidence": confidence,
                    "raw_predictions": prediction.tolist()
                },
                "message": "Burn degree prediction successful"
            }, 200

            
        except Exception as e:
            return {
                'success': False,
                'message': f'Prediction error: {str(e)}'
            }, 500

api.add_resource(AiModelResource, '/predict', endpoint='predict')