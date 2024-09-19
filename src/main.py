from init import db, ma, bcrypt, jwt
from flask import Flask
import os
# from controllers.event_controller import event_bp
from controllers.cli_controllers import db_commands
from controllers.player_controller import player_db
from controllers.game_controller import game_bp
from controllers.user_controller import user_bp
from controllers.comments_controller import comments_bp
from controllers.event_controller import event_bp

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
    app.register_blueprint(player_db)
    app.register_blueprint(game_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(event_bp)
    return app

