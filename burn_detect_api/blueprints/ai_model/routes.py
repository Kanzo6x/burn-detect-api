from flask import Blueprint, render_template
from flask_restful import Resource, Api, reqparse

ai_model = Blueprint('ai_model', __name__, template_folder='templates')
api = Api(ai_model)


@ai_model.route('/',methods=['GET'])
def sendphoto():
    return render_template('ai_model/BurnDetector.html'),200


class AiModelResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('image', type=str, required=True, help='Image is required')
    def post(self):
        try:
            pass
        except Exception as e:
            pass

api.add_resource(AiModelResource, '/predict', endpoint='predict')