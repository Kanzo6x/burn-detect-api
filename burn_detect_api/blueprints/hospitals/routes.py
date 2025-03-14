from flask import Blueprint
from flask_restful import Api,Resource
from burn_detect_api.blueprints.hospitals.models import Hospital
from burn_detect_api.app import db

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

class GovernorateResource(Resource): #this resource will be named '/Governorate/<string:governorate>'
    def get(self, governorate):
        try:
            hospitals = Hospital.query.filter_by(governorate=governorate).all()
            hospitals_list = [hospital.serialize() for hospital in hospitals]
            
            return {
                'success': True,
                'data': hospitals_list,
                'message': 'Hospitals retrieved successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }, 500

api.add_resource(GovernorateResource,'/Governorate/<string:governorate>',endpoint='SpecificGovernorate') #/Governorate/Cairo