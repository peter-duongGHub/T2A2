# Import SQLAlchemy object instance for use in database operations and queries
from init import db
# Import flask modules request and Blueprint to grab JSON body text from front-end and Blueprint to create decorator endpoints by registering blueprint
from flask import request, Blueprint
# Import Player model and schema for creating of player objects and player schema to return a deserialised player object to the view
from models.player import Players, player_schema, players_schema, PlayerSchema
# Import Game model for creating of game objects
from models.game import Games
# Import Game model for creating of user objects
from models.user import Users
# Import flask module to create tokens for player creation and jwt required for authentication
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
# Import datetime for expiry of tokens
from datetime import timedelta
# Import module for error handling of incorrect date format
from sqlalchemy.exc import DataError
# Import event controller to pass on url prefix to event controller blueprint
from controllers.event_controller import event_bp
# Import datetime module for conversion of string to data object for database operation
from datetime import datetime

# Error handling modules imported 
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
# Authentication to check JWT included and admin rights
from check import check_admin

# Create player blue print for use as decorator
player_bp = Blueprint("player", __name__, url_prefix="/<int:game_id>/players")
player_bp.register_blueprint(event_bp)

# Create a route to create a player object into the database


@player_bp.route("/", methods=["POST"])
# JWT required, requires a user JWT created after logging in user to be input as bearer token
@jwt_required()
def create_player(game_id, user_id):
    try:
        # Retrieve JSON data from the request
        request_data = PlayerSchema().load(request.get_json())
        body_name = request_data.get("name")
        role = request_data.get("role")

        # Query to select user objects from the database
        user_stmt = db.Select(Users).filter_by(id=user_id)
        user = db.session.scalar(user_stmt)

        # Check if the name for the created player is already in the database
        player_stmt = db.Select(Players).filter_by(name=body_name)
        existing_player = db.session.scalar(player_stmt)
        # If name exists in database:
        if existing_player:
            # return error message
            return {"error": f"Player with name {body_name} already exists"}, 400

        else:
            # Create a new Player instance with attribute of specific game and date attached to player

            player = Players(
                name=body_name,
                role=role,
            )
            # If user exists:
            if user:
                # Referenced foreign key column will be id of user
                player.user_id = user.id
            else:
                # Else an error message will be returned to the view
                return {"error": "Please enter a correct user id in the route"}

            # Query to select game objects from the database
            game_stmt = db.Select(Games).filter_by(id=game_id)
            game = db.session.scalar(game_stmt)

            # If the game object exists with game_id:
            if game:
                # Referenced foreign key column will be id of game
                player.game_id = game.id

            else:
                # else return an error message
                return {"error": "Incorrect route game does not exist"}

            # Get the data input from the body of request
            date = request_data.get("date")
            # If it exists:
            if date:
                # Change the format of the string into a date for storing inside database
                date_object = datetime.strptime(date, "%m/%d/%Y")
                dt = date_object.replace(tzinfo=None)
                player.date = date

            # Add and commit the new player to the database
            db.session.add(player)
            db.session.commit()

            # Create token for newly created player object
            token = create_access_token(identity=str(
                player.id), expires_delta=timedelta(days=1))
            player_stmt = db.Select(Players).filter_by(id=player.id)
            player_obj = db.session.scalar(player_stmt)

        # Return the newly created player's data to the view after deserialising player object
        return {"player_name": player_obj.name,
                "creation_date": player_obj.date,
                "role": player_obj.role,
                "id": player_obj.id,
                "token": token,
                "user": player_obj.user.id,
                "game": player_obj.game.id
                }, 201
    # Error handling if user input is not in correct date format
    except DataError:
        return {"error": "Please enter date in the correct format MM-DD-YYYY or MM-DD-YYYY."}, 400

    except ValueError:
        return {"error": "Date must be in format MM-DD-YYYY"}, 400
    # Error handling if missing specific attributes for input
    except IntegrityError as e:
        if e.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The {e.orig.diag.column_name} is required"}, 400
    # Error handling any exceptions that may occur not accounted for
    except Exception as e:
        return {"error": f"{e}"}, 400

# Create a route to update a player objects inside the database name


@player_bp.route("/<int:player_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_player(player_id, game_id, user_id):
    try:
            # Query to select specific player with the correct token id
            player_stmt = db.Select(Players).filter_by(id=get_jwt_identity())
            player = db.session.scalar(player_stmt)
            # If player exists:
            if player:

                # Retrive data from the front-end JSON body and extract the name input
                request_data = PlayerSchema().load(request.get_json())
                name = request_data.get("name")

                # If there is a name input:
                if name:
                    # Query the database for a player with an id equal to the player_id in the route
                    name_stmt = db.Select(Players).filter_by(name=name)
                    player_name = db.session.scalar(name_stmt)
                    if player_name:
                        return {"error": "Name already exists in database"}, 400

                    else:
                        # Change the player name with id equal to player id to the front-end input name and commit to the database session
                        player.name = name or player.name
                        db.session.commit()

                        # Return the updated player information to the view owith a success code 200
                        return player_schema.dump(player), 200
                else:
                    # If there is no name input return an error message
                    return {"error": "Please input a name to change the player name"}, 400
            # If the player does not exist with the correct JWT id:
            else:
                return {"error" : "Only players with correct JWT can update player details."}, 400
    # Error Handle exceptions that may occur
    except Exception as e:
        return {"error": f"{e}"}, 400

# Create a route to delete a specific player depending on the id of the player in the dynamic route


@player_bp.route("/<int:player_id>", methods=["DELETE"])
@jwt_required()
def delete_player(player_id, user_id, game_id):
    try:
        # Query to filter player based on the id of the player JWT
        player_stmt = db.Select(Players).filter_by(id=get_jwt_identity())
        player = db.session.scalar(player_stmt)
        if player:
                # Query to delete player object and commit to the database session
                db.session.delete(player)
                db.session.commit()
                # Return a success message of the deleted player id
                return (f"Player with id {player_id} is deleted."), 200
        else: 
            # return error message if no player with correct JWT
            return{"error" : "Please check correct player JWT is input and correct player id is input"}, 400
    # General Error handling for any unexpected errors
    except Exception as e:
        return (str(e)), 400


# Create an route to view all players
@player_bp.route("/", methods=["GET"])
def view_players(game_id, user_id):
    try:
        # Fetch all player objects from the database
        stmt = db.select(Players)
        player = db.session.scalars(stmt)

        # If there are player objects:
        if player:
            # Provide the view with deserialised player objects
            return players_schema.dump(player), 200
        # If there isnt return an error message
        else:
            return {"error": "There are no players to show"}, 404
    # Error handling in case error occurs
    except Exception as e:
        return {"error": f"{e}"}, 400

# Create an endpoint to view specific player


@player_bp.route("/<int:player_id>", methods=["GET"])
def specific_players(player_id, game_id, user_id):
    try:
        # Fetch specific player from the database depending on the id in the dynamic route
        stmt = db.select(Players).filter_by(id=player_id)
        player = db.session.scalar(stmt)

        # If there is a player with the player id in the dynamic route:
        if player:
            # Return to the view the specific player object deserialised with a success code
            return player_schema.dump(player), 200
        else:
            # Return an error message if there is no player with the specific id
            return {"error": f"Player with id {player_id} can not be found."}, 404
    # Error handling in case there are exceptions in error
    except Exception as e:
        return {"error": f"{e}"}, 400
