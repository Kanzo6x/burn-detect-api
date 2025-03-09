from flask import Blueprint, render_template, request
from flask_restful import Resource, Api
import os
from PIL import Image
import numpy as np
from tensorflow import keras

ai_model = Blueprint('ai_model', __name__, template_folder='templates')
api = Api(ai_model)

# Load the ML model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'efficientnet_model.h5')  # Change extension to .h5
try:
    model = keras.models.load_model(MODEL_PATH)
except Exception as e:
    print(f"Error loading model: {str(e)}")
    model = None

@ai_model.route('/',methods=['GET'])
def sendphoto():
    return render_template('ai_model/BurnDetector.html'),200

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
            
            # Resize image to match your model's input size
            image = image.resize((224, 224))  # Adjust size as per your model
            
            # Convert to numpy array and preprocess
            image_array = np.array(image)
            # Normalize if needed
            image_array = image_array / 255.0
            
            # Add batch dimension
            image_array = np.expand_dims(image_array, axis=0)
            
            # Make prediction
            prediction = model.predict(image_array)
            
            # Get the class with highest probability
            predicted_class = int(np.argmax(prediction[0]))
            confidence = float(np.max(prediction[0]))
            
            result = {
                'success': True, 
                'data': {
                    'class': predicted_class,
                    'confidence': confidence,
                    'raw_predictions': prediction.tolist()
                },
                'message': 'Image prediction successful'
            }
            
            return result, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Prediction error: {str(e)}'
            }, 500

api.add_resource(AiModelResource, '/predict', endpoint='predict')