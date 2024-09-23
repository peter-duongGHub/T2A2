from init import db, ma, bcrypt
from flask import request, Blueprint
from models.player import Players, player_schema, players_schema
from models.game import Games
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from auth import check_admin

from sqlalchemy.exc import SQLAlchemyError
# from controllers.comments_controller import comments_bp
from controllers.event_controller import event_bp

player_bp = Blueprint("player", __name__, url_prefix="/<int:game_id>/players")
@player_bp.register_blueprint(event_bp)

# POST (CREATE) - Create Player into databse from a HTTP Request
@player_bp.route("/", methods=["POST"])
def create_player(game_id):
    # Retrieve JSON data from the request
    request_data = request.get_json()
    body_name = request_data.get("name")

    # Validate required fields
    # if not name or date or role:
    #     return{"error": "Name, date & role are required"}, 400

    # Check if the name is already in use
    player_stmt = db.Select(Players).filter_by(name=body_name)
    existing_user = db.session.scalar(player_stmt)
    if existing_user:
        return{"error"}, 400

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

        token = create_access_token(identity=str(player.id), expires_delta=timedelta(days=1))

        # Add and commit the new player to the database
        # try:
    db.session.add(player)
    db.session.commit()
    # except SQLAlchemyError as e:
    #     return{"error": "Database commit failed", "details": str(e)}, 500

    # Return the newly created player's data
    return player_schema.dump(player), 201

# # Update player's name
# @player_bp.route("/<int:player_id>", methods=["PUT", "PATCH"])
# @jwt_required()
# def update_player(player_id, game_id):
#     request_data = request.get_json()
#     name = request_data.get("name")

#     # Query the database for the user
#     try:
#         stmt = db.Select(Players).filter_by(id=player_id)
#         player = db.session.scalar(stmt)

#     except SQLAlchemyError as e:
#         return{"error": "Database query failed", "details": str(e)}, 500

#     if player is None:
#         return{"error": "No such player exists"}, 404

#     # Update user attributes if provided
#     if player:
#         player.name = name or player.name
#     try:
#         db.session.commit()
#     except SQLAlchemyError as e:
#         return{"error": "Database commit failed", "details": str(e)}, 500

#     # Return the updated user information
#     return player_schema.dump(player), 200
    
# # delete player
# @player_bp.route("/<int:player_id>", methods=["DELETE"])
# @jwt_required()
# def delete_user(player_id):
#     try:
#         # Attempt to retrieve the user with the given id
#         stmt = db.Select(Players).filter_by(id=player_id)
#         player = db.session.scalar(stmt)

#         # If user is found, delete and commit
#         if player:
#             db.session.delete(player)
#             db.session.commit()
#             # Return a success message
#             return (f"Player with id {player_id} is deleted.")
        
#         # If user is not found, return a 404 error
#         else:
#             return (f"Player with id {player_id} not found."), 404
    
#     except Exception as e:
#         # Handle any unexpected errors
#         return (str(e)), 500
    

# # View all players
# @player_bp.route("/", methods=["GET"])
# def view_players(game_id):
#     stmt = db.select(Players)
#     player = db.session.scalars(stmt)

#     if player:
#         return players_schema.dump(player), 201
#     else:
#         return {"error" : "There are no players to show"}
    
# # View specific players
# @player_bp.route("/<int:player_id>", methods=["GET"])
# def specific_players(player_id, game_id):
#     stmt = db.select(Players).filter_by(id=player_id)
#     player = db.session.scalar(stmt)

#     if player:
#         return player_schema.dump(player), 201
#     else:
#         return {"error" : f"Player with id {player_id} can not be found."}
    
