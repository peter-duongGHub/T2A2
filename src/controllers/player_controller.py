# Import SQLAlchemy object instance for use in database operations and queries
from init import db
# Import flask modules request and Blueprint to grab JSON body text from front-end and Blueprint to create decorator endpoints by registering blueprint
from flask import request, Blueprint
# Import Player model and schema for creating of player objects and player schema to return a deserialised player object to the view
from models.player import Players, player_schema, players_schema
# Import Game model for creating of game objects
from models.game import Games
# Import flask module to create tokens for player creation and jwt required for authentication
from flask_jwt_extended import create_access_token, jwt_required
# Import datetime for expiry of tokens
from datetime import timedelta
# Import module for error handling of incorrect date format
from sqlalchemy.exc import DataError
# Import event controller to pass on url prefix to event controller blueprint
from controllers.event_controller import event_bp


player_bp = Blueprint("player", __name__, url_prefix="/<int:game_id>/players")
@player_bp.register_blueprint(event_bp)

# POST (CREATE) - Create Player into databse from a HTTP Request
@player_bp.route("/", methods=["POST"])
def create_player(game_id, user_id):
    try:
        # Retrieve JSON data from the request
        request_data = request.get_json()
        body_name = request_data.get("name")
        role = request_data.get("role")

        # Validate required fields
        if not body_name or role:
            return{"error": "Name & role are required"}, 400

        # Check if the name is already in use
        player_stmt = db.Select(Players).filter_by(name=body_name)
        existing_user = db.session.scalar(player_stmt)
        if existing_user:
            return{"error" : f"Player with name {body_name} already exists"}, 400

        else:
        # Create a new Player instance
            stmt = db.Select(Games).filter_by(id=game_id)
            game = db.session.scalar(stmt)
            player = Players(
                    name= body_name,
                    date= request_data.get("date"),
                    role= request_data.get("role"),
                    game_id = game.id
                )
            # Create token for created player object
            token = create_access_token(identity=str(player.id), expires_delta=timedelta(days=1))

        # Add and commit the new player to the database
        db.session.add(player)
        db.session.commit()

        # Return the newly created player's data to the view after deserialising player object
        return player_schema.dump(player), 201
    # Error handling if user input is not in correct date format 
    except DataError:
        return{"error" : "Please enter date in the correct format yyyy-mm-dd or yyyy-mm-dd."}
        

# Update player's name
@player_bp.route("/<int:player_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_player(player_id, game_id, user_id): 
    # Retrive data from the front-end JSON body and extract the name input
    request_data = request.get_json()
    name = request_data.get("name")

    # If there is a name input:
    if name:
        # Query the database for a player with an id equal to the player_id in the route
        stmt = db.Select(Players).filter_by(id=player_id)
        player = db.session.scalar(stmt)
        # If there is no such player return error message
        if player is None:
            return{"error": "No such player exists"}, 404
        
        # Update user attributes if provided
        if player:
            player.name = name or player.name

            db.session.commit()

        # Return the updated user information
        return player_schema.dump(player), 200
    else:
        return {"error" : "Please enter a new player name to update existing player name"}
    
# delete player
@player_bp.route("/<int:player_id>", methods=["DELETE"])
@jwt_required()
def delete_user(player_id, user_id, game_id):
    try:
        # Attempt to retrieve the user with the given id
        stmt = db.Select(Players).filter_by(id=player_id)
        player = db.session.scalar(stmt)

        # If user is found, delete and commit
        if player:
            db.session.delete(player)
            db.session.commit()
            # Return a success message
            return (f"Player with id {player_id} is deleted.")
        
        # If user is not found, return a 404 error
        else:
            return (f"Player with id {player_id} not found."), 404
    
    except Exception as e:
        # Handle any unexpected errors
        return (str(e)), 500
    

# View all players
@player_bp.route("/", methods=["GET"])
def view_players(game_id, user_id):
    stmt = db.select(Players)
    player = db.session.scalars(stmt)

    if player:
        return players_schema.dump(player), 201
    else:
        return {"error" : "There are no players to show"}
    
# View specific players
@player_bp.route("/<int:player_id>", methods=["GET"])
def specific_players(player_id, game_id, user_id):
    stmt = db.select(Players).filter_by(id=player_id)
    player = db.session.scalar(stmt)

    if player:
        return player_schema.dump(player), 201
    else:
        return {"error" : f"Player with id {player_id} can not be found."}
    
