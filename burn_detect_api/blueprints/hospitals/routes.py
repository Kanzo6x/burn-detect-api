from flask import Blueprint,Response
from flask_restful import Api,Resource
from burn_detect_api.blueprints.hospitals.models import Hospital
from burn_detect_api.app import db
import json

Location = Blueprint('Location',__name__)
api = Api(Location)


#this resource have a get method only that retrives all distincit governorate names
#from the db model that named Hospital of course it returns as tuble so we need to 
#as a list thent return it as json response object 

class LocationResource(Resource):  #this resource will be named '/all_hospitals' 
    def get(self):
        try:
            governorates = db.session.query(Hospital.governorate).distinct().all()
            governorates_list = [gov[0] for gov in governorates]
            
            return {
                'success': True,
                'data': governorates_list,
                'message': 'Governorates retrieved successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }, 500
        
api.add_resource(LocationResource,'/all_hospitals',endpoint='getHospitals')



#this resource have a get method only that retrives all hospitals data
#from the db model that named Hospital of course it returns 

class GovernorateResource(Resource):
    def get(self, governorate):
        try:
            hospitals = Hospital.query.filter_by(governorate=governorate).all()
            hospitals_list = [hospital.serialize() for hospital in hospitals]
            
            response_data = {
                'success': True,
                'data': hospitals_list,
                'message': 'Hospitals retrieved successfully'
            }
            
            return Response(
                json.dumps(response_data, ensure_ascii=False,indent=4), 
                mimetype='application/json'
            )

        except Exception as e:
            error_response = {
                'success': False,
                'message': str(e)
            }
            return Response(
                json.dumps(error_response, ensure_ascii=False), 
                mimetype='application/json', 
                status=500
            )

api.add_resource(GovernorateResource, '/Governorate/<string:governorate>', endpoint='SpecificGovernorate')