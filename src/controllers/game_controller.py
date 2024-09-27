# Import SQLAlchemy and Bcrypt objects for database operations and hashing respectively
from init import db, ma
# Import flask modules Blueprint and request to use decorator routes and retrieve body data from front-end respectively
from flask import Blueprint, request
# Import game and user model with Game and User object instance and game schemas for CRUD operations and view respectively
from models.game import Games, game_schema, games_schema, GameSchema
from models.user import Users

from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

# Import check admin function from auth file to authenticate user to endpoint
from check import check_admin
# Import flask_jwt_extended module to retrieve token id's and authentication
from flask_jwt_extended import jwt_required, get_jwt_identity

# Import player blueprint to register blueprint in game controller for url prefix routing
from controllers.player_controller import player_bp
game_bp = Blueprint("game", __name__, url_prefix="/<int:user_id>/game")
game_bp.register_blueprint(player_bp)

# Creating a game depending on authentication and required JWT from user


@game_bp.route("/", methods=["POST"])
@jwt_required()
@check_admin
def create_game(user_id):
    try:
        # Get the body data from JSON body (name, description)
        request_data = GameSchema().load(request.get_json(), partial=True)
        name = request_data.get("name")
        description = request_data.get("description")
        # Query into Users table for user object id relating to the JWT identity
        stmt = db.Select(Users).filter_by(id=get_jwt_identity())
        user = db.session.scalar(stmt)

        # Create game object from JSON body and user id relating to JWT
        game = Games(
            name=name,
            description=description,
            user_id=user.id
        )

        # Add game object to database session
        db.session.add(game)
        # Commit the game object to the database session
        db.session.commit()
        # Return a view to the front-end of the game object - deserialised with schema and success code 201
        return game_schema.dump(game), 201
    except IntegrityError as e:
        if e.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The {e.orig.diag.column_name} is required"}, 400
    except ValidationError as e:
        return {"error": str(e)}, 400
    except Exception as e:
        return {"error": f"{e}"}

# Fetch specific game to view - READ


@game_bp.route("/<int:game_id>", methods=["GET"])
def view_games(game_id, user_id):
    try:
        # Fetch specific game based on dynamic route (game_id)
        stmt = db.Select(Games).filter_by(id=game_id)
        game = db.session.scalar(stmt)

        # If game with game_id exists return to the view a deserialised game object with code 200 success
        if game:
            return game_schema.dump(game), 200
        # Else return an error message
        else:
            return {"error": f"There is no game with id: {game_id}"}, 404
    except Exception as e:
        return {"error": f"{e}"}

# Create a route to fetch all games


@game_bp.route("/", methods=["GET"])
def get_games(user_id):
    try:
        # Fetch all games from the database and order by description descending
        stmt = db.Select(Games).order_by(Games.description.desc())
        game = db.session.scalars(stmt)

        # If there are games in the database:
        if game:
            # Deserialise the object and send to the view with a success code 200
            return games_schema.dump(game), 200
        # If there are no games in the database return a message there are no games
        else:
            return {"error": "There are currently no games to view."}, 404
    except Exception as e:
        return {"error": f"{e}"}


# Create a route to update game attributes, must be authenticated and contain a JWT as bearer token
@game_bp.route("/<int:game_id>", methods=["PUT", "PATCH"])
@jwt_required()
@check_admin
def update_game(game_id, user_id):
    try:
        # Grab the body data from the JSON body and extract the name and description
        request_data = GameSchema().load(request.get_json())
        name = request_data.get("name")
        description = request_data.get("description")
        # Check to see if there is a game with same id as game_id
        stmt = db.Select(Games).filter_by(id=game_id)
        game = db.session.scalar(stmt)

        # If there is a game with id = game_id in the database change the name and description attribute using the body data from request
        if game:
            game.name = name or game.name
            game.description = description or game.description
        # If no game with id = game_id return to view that the game does not exist
        else:
            return {"error": "No such game exists"}, 404
        # Commit the changes to the database session
        db.session.commit()
        # Return to the view a deserialised game object and success 200 code
        return game_schema.dump(game), 200
    except Exception as e:
        return {"error": f"{e}"}

# Create a route to delete a game from the database, must be authenticated and have a JWT


@game_bp.route("/<int:game_id>", methods=["DELETE"])
@jwt_required()
@check_admin
def delete_game(game_id, user_id):
    try:
        # Check if game with game_id exists in the database
        stmt = db.Select(Games).filter_by(id=game_id)
        game = db.session.scalar(stmt)
        # If game is found, delete the game object and commit the change to the database session
        if game:
            db.session.delete(game)
            db.session.commit()
            # Return a success message that the game has been deleted with success 200 code
            return {"message": f"Game with id {game_id} is deleted."}, 200

        # If user is not found, return message and error code 400
        else:
            return {"message": f"Game with id {game_id} not found."}, 404

    # Error handle for any other outlier errors
    except Exception as e:
        return {"message": f"{str(e)}"}, 500
