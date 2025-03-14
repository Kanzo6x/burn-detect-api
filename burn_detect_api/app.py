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

    admin.name = 'Burn Detection Admin'
    admin.template_mode = 'bootstrap4'
    admin.url = '/admin'

    db.init_app(app)
    admin.init_app(app)
    Migrate(app, db)


    from burn_detect_api.blueprints.hospitals.routes import Location
    app.register_blueprint(Location)

    from burn_detect_api.blueprints.ai_model.routes import ai_model
    app.register_blueprint(ai_model)

    from burn_detect_api.blueprints.hospitals.models import Hospital
    admin.add_view(ModelView(Hospital, db.session))


    return app
