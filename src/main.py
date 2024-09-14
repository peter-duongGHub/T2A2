from init import db, ma, bcrypt, jwt
from flask import Flask
import os
# from controllers.event_controller import event_bp
from controllers.cli_controllers import db_commands

def create_app():

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["JWT_SECRET_KEY"] = os.environ.get("SECRET_KEY")

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # app.register_blueprint(event_bp)
    app.register_blueprint(db_commands)

    return app
