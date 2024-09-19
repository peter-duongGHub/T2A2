from init import db, ma, bcrypt
from flask import request, Blueprint
from models.player import Player, player_schema, players_schema
from models.game import Game, game_schema, games_schema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from auth import check_admin

from sqlalchemy.exc import SQLAlchemyError

player_db = Blueprint("player", __name__, url_prefix="/game")


# POST (CREATE) - Create Player into databse from a HTTP Request
@player_db.route("/<int:game_id>/player", methods=["POST"])
def create_player(game_id):
    # Retrieve JSON data from the request
    request_data = request.get_json()
    
    # Extract player data from the request
    name = request_data.get("name")
    date = request_data.get("date")
    role = request_data.get("role")
    stmt = db.Select(Game).filter_by(id=game_id)
    game = db.session.scalar(stmt)

    # Validate required fields
    if not name or date or role:
        return{"error": "Name, date & role are required"}, 400

    # Check if the name is already in use
    existing_user = db.Select(Player).filter_by(name=name)
    if existing_user:
        return{"error": "Name already in use"}, 400

    # Create a new Player instance
    player = Player(
        name=name,
        date=date,
        role=role,
        game_id = game.id
    )

    if player:
        token = create_access_token(identity=str(player.id), expires_delta=timedelta(days=1))

    # Add and commit the new player to the database
    try:
        db.session.add(player)
        db.session.commit()
    except SQLAlchemyError as e:
        return{"error": "Database commit failed", "details": str(e)}, 500

    # Return the newly created player's data
    return {"name" : player.name, "date" : player.date, "role" : player.role, "game_id" : game.id, "token" : token}

# Update player's name
@player_db.route("/<int:game_id>/players/<int:player_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_player(player_id):
    request_data = request.get_json()
    name = request_data.get("name")

    # Query the database for the user
    try:
        stmt = db.Select(Player).filter_by(id=player_id)
        player = db.session.scalar(stmt)

    except SQLAlchemyError as e:
        return{"error": "Database query failed", "details": str(e)}, 500

    if player is None:
        return{"error": "No such player exists"}, 404

    # Update user attributes if provided
    if player:
        player.name = name or player.name

    try:
        db.session.commit()
    except SQLAlchemyError as e:
        return{"error": "Database commit failed", "details": str(e)}, 500

    # Return the updated user information
    return players_schema.dump(player), 200
    
# delete player
@player_db.route("/users/<int:player_id>", methods=["DELETE"])
@jwt_required()
def delete_user(player_id):
    try:
        # Attempt to retrieve the user with the given id
        stmt = db.Select(Player).filter_by(id=player_id)
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
@player_db.route("/<int:game_id>/players", methods=["GET"])
def view_players():
    stmt = db.select(Player)
    player = db.session.scalars(stmt)

    if player:
        return players_schema.dump(player), 201
    else:
        return {"error" : "There are no players to show"}
    
# View specific players
@player_db.route("/<int:game_id>/players/<int:player_id>", methods=["GET"])
def specific_players(player_id):
    stmt = db.select(Player).filter_by(id=player_id)
    player = db.session.scalar(stmt)

    if player:
        return player_schema.dump(player), 201
    else:
        return {"error" : f"Player with id {player_id} can not be found."}
    
