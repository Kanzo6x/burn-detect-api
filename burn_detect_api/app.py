from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

db = SQLAlchemy()
admin = Admin()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospitals.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key-here'  # Required for CSRF
    
    admin.name = 'Burn Detection Admin'
    admin.template_mode = 'bootstrap4'
    admin.url = '/admin'
    
    db.init_app(app)
    admin.init_app(app)
    
    with app.app_context():
        from burn_detect_api.blueprints.hospitals.models import Hospital
        # Add Hospital model to admin
        admin.add_view(ModelView(Hospital, db.session))
        db.create_all()
        
    from burn_detect_api.blueprints.hospitals.routes import Location
    app.register_blueprint(Location)
    
    Migrate(app, db)
    return app
