# Import SQLAlchemy object instance for use in database operations and queries
from init import db
# Import flask modules request and Blueprint to grab JSON body text from front-end and Blueprint to create decorator endpoints by registering blueprint
from flask import request, Blueprint
# Import Player model and schema for creating of player objects and player schema to return a deserialised player object to the view
from models.player import Players, player_schema, players_schema, PlayerSchema
# Import Game model for creating of game objects
from models.game import Games
# Import flask module to create tokens for player creation and jwt required for authentication
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
# Import datetime for expiry of tokens
from datetime import timedelta
# Import module for error handling of incorrect date format
from sqlalchemy.exc import DataError
# Import event controller to pass on url prefix to event controller blueprint
from controllers.event_controller import event_bp
from datetime import datetime

from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from check import check_admin

player_bp = Blueprint("player", __name__, url_prefix="/<int:game_id>/players")
player_bp.register_blueprint(event_bp)

# Create a route to create a player object into the database
@player_bp.route("/", methods=["POST"])
@jwt_required
@check_admin
def create_player(game_id, user_id):
    try:
        # Retrieve JSON data from the request
        request_data = request.get_json()
        body_name = request_data.get("name")
        role = request_data.get("role")

        # Check if the name is already in use
        player_stmt = db.Select(Players).filter_by(name=body_name)
        existing_user = db.session.scalar(player_stmt)
        if existing_user:
            return{"error" : f"Player with name {body_name} already exists"}, 400

        else:
        # Create a new Player instance
            game_stmt = db.Select(Games).filter_by(id=game_id)
            game = db.session.scalar(game_stmt)

            player = Players(
                    name= body_name,
                    role= role,
                    game_id = game.id
                )
            date = request_data.get("date")
            if date:
                date_object = datetime.strptime(date, "%Y/%m/%d")
                dt = date_object.replace(tzinfo=None)
                player.date = dt

            
            # Add and commit the new player to the database
            db.session.add(player)
            db.session.commit()


            # Create token for newly created player object
            token = create_access_token(identity=str(player.id), expires_delta=timedelta(days=1))
            player_stmt = db.Select(Players).filter_by(id=player.id)
            player_obj = db.session.scalar(player_stmt)


        # Return the newly created player's data to the view after deserialising player object
        return {"name" : player_obj.name,
                "date" : player_obj.date,
                "role" : player_obj.role,
                "id" : player_obj.id,
                "token" : token
                }, 201
    # Error handling if user input is not in correct date format 
    except DataError:
        return{"error" : "Please enter date in the correct format yyyy-mm-dd or yyyy-mm-dd."}, 400
    
    except ValueError:
        return{"error" : "Date must be in format YYYY-MM-DD"}, 400
    
    except IntegrityError as e:
        if e.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The {e.orig.diag.column_name} is required"}, 400
        
    except Exception as e:
        return {"error" : f"{e}"}, 400


# Create a route to update a player objects inside the database name
@player_bp.route("/<int:player_id>", methods=["PUT", "PATCH"])
@jwt_required()
@check_admin
def update_player(player_id, game_id, user_id): 
    # Retrive data from the front-end JSON body and extract the name input
    request_data = request.get_json()
    name = request_data.get("name")

    # If there is a name input:
    if name:
        # Query the database for a player with an id equal to the player_id in the route
        name_stmt = db.Select(Players).filter_by(name=name)
        player_name = db.session.scalar(name_stmt)
        if player_name:
            return {"error" : "Name already exists in database"}, 400
        
        stmt = db.Select(Players).filter_by(id=player_id)
        player = db.session.scalar(stmt)

        # If there is no such player return error message
        if player is None:
            return{"error": "No such player exists"}, 404
        
        # If there is a player with id equal to the player id:
        elif player:
            # Change the player name with id equal to player id to the front-end input name and commit to the database session
            player.name = name or player.name
            db.session.commit()

        # Return the updated player information to the view owith a success code 200
            return player_schema.dump(player), 200
    
        else:
            return{"error" : "Only associated created players can update their own names."}
     # If there is no name input return an error message
    else:
        return {"error" : "Please input a name to change the player name"}
    
# Create a route to delete a specific player depending on the id of the player in the dynamic route
@player_bp.route("/<int:player_id>", methods=["DELETE"])
@jwt_required()
@check_admin
def delete_player(player_id, user_id, game_id):
    try:
        # Retrieve the Player object with the specified player id in the dynamic route
        stmt = db.Select(Players).filter_by(id=player_id)
        player = db.session.scalar(stmt)

        # If there is a player object with the specific player id delete the player and commit the change to the database session
        if player:
            db.session.delete(player)
            db.session.commit()
            # Return a success message of the deleted player id 
            return (f"Player with id {player_id} is deleted.")
        
        # If there is no such player with the player id return error message
        else:
            return (f"Player with id {player_id} not found."), 404
    # General Error handling for any unexpected errors
    except Exception as e:
        return (str(e)), 500
    

# Create an endpoint to view all players
@player_bp.route("/", methods=["GET"])
def view_players(game_id, user_id):
    # Fetch all player objects from the database
    stmt = db.select(Players)
    player = db.session.scalars(stmt)

    # If there are player objects:
    if player:
        # Provide the view with deserialised player objects
        return players_schema.dump(player), 200
    # If there isnt return an error message
    else:
        return {"error" : "There are no players to show"}, 404
    
# Create an endpoint to view specific player
@player_bp.route("/<int:player_id>", methods=["GET"])
def specific_players(player_id, game_id, user_id):
    # Fetch specific player from the database depending on the id in the dynamic route
    stmt = db.select(Players).filter_by(id=player_id)
    player = db.session.scalar(stmt)

    # If there is a player with the player id in the dynamic route:
    if player:
        # Return to the view the specific player object deserialised with a success code
        return player_schema.dump(player), 200
    else:
        # Return an error message if there is no player with the specific id
        return {"error" : f"Player with id {player_id} can not be found."}, 404
    
