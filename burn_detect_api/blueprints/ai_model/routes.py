from flask import Blueprint, render_template, request
from flask_restful import Resource, Api
from PIL import Image
import numpy as np
import torch
import torchvision.transforms as transforms
import torchvision.models as models
import os

ai_model = Blueprint('ai_model', __name__, template_folder='templates')
api = Api(ai_model)

# 🔹 Updated class labels
class_labels = ['first degree', 'second degree', 'third degree', 'normal skin']

# 🔹 Model path
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'efficientnet_model.pth')

# 🔹 Global model cache
_model_instance = None

def load_model():
    global _model_instance
    if _model_instance is None:
        try:
            # Initialize the EfficientNet model architecture
            _model_instance = models.efficientnet_b0(pretrained=False)
            # Modify the last fully connected layer to match your number of classes
            _model_instance.classifier[1] = torch.nn.Linear(1280, len(class_labels))
            
            # Load the state dictionary and fix the keys
            state_dict = torch.load(MODEL_PATH, map_location=torch.device('cpu'))
            # Remove the 'efficientnet.' prefix from keys
            new_state_dict = {}
            for key, value in state_dict.items():
                if key.startswith('efficientnet.'):
                    new_key = key.replace('efficientnet.', '')
                    new_state_dict[new_key] = value
                else:
                    new_state_dict[key] = value
            
            _model_instance.load_state_dict(new_state_dict)
            _model_instance.eval()
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Failed to load model: {str(e)}")
            _model_instance = None
    return _model_instance

def predict_burn(image_file):
    model = load_model()
    if model is None:
        raise Exception("Model is not loaded.")

    # Validate file
    if not image_file or not image_file.filename:
        raise Exception("Invalid image file")

    # Check file extension
    allowed_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}
    file_ext = os.path.splitext(image_file.filename.lower())[1]
    if file_ext not in allowed_extensions:
        raise Exception(f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}")

    try:
        # Preprocess image
        image = Image.open(image_file.stream)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Define image transformations
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        image_tensor = transform(image).unsqueeze(0)

        # Get prediction
        with torch.no_grad():
            prediction = model(image_tensor)
            probabilities = torch.nn.functional.softmax(prediction[0], dim=0)
            
        # Convert to numpy for processing
        prediction_np = probabilities.numpy()
        top_index = np.argmax(prediction_np)
        confidence = prediction_np[top_index]

        # Add a check to prevent misclassification
        if confidence < 0.5:
            top_class = "Unknown"
        else:
            top_class = class_labels[top_index]

        return {
            "data": {
                "class": top_class,
                "confidence": float(confidence)
            }
        }
    except Exception as e:
        raise Exception(f"Error processing image: {str(e)}")

# 🔹 UI Route
@ai_model.route('/', methods=['GET'])
def sendphoto():
    return render_template('ai_model/BurnDetector.html'), 200

# 🔹 Predict API
class AiModelResource(Resource):
    def post(self):
        try:
            if 'image' not in request.files:
                return {
                    'success': False,
                    'message': 'No image file provided'
                }, 400

            image_file = request.files['image']
            prediction_result = predict_burn(image_file)
            top_class = prediction_result["data"]["class"]
            confidence = prediction_result["data"]["confidence"]

            return {
                "success": True,
                "message": "Burn degree prediction successful.",
                "data": {
                    "class": top_class,
                    "confidence": round(confidence, 3)
                }
            }, 200

        except Exception as e:
            return {
                'success': False,
                'message': f'Prediction error: {str(e)}'
            }, 500


api.add_resource(AiModelResource, '/predict', endpoint='predict')