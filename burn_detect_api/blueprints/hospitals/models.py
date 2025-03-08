from burn_detect_api.app import db

class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    hospital_name = db.Column(db.String(255), nullable=False)  
    address = db.Column(db.String(255), nullable=False)  
    governorate = db.Column(db.String(100), nullable=False)  
    coordinates = db.Column(db.String(100), nullable=False)  

    def __repr__(self):
        return f"<Location {self.hospital_name}>"

    def serialize(self):
        return {
            'id': self.id,
            'hospital_name': self.hospital_name,
            'address': self.address,
            'governorate': self.governorate,
            'coordinates': self.coordinates
        }

    def __str__(self):
        return self.hospital_name
