from init import db, ma
from flask import Blueprint, request
from models.game import Games, game_schema, games_schema
from auth import check_admin
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import Users

from controllers.player_controller import player_bp
game_bp = Blueprint("game", __name__, url_prefix="/game")
game_bp.register_blueprint(player_bp)

# Creating a game into database from HTTP request - CREATE
@game_bp.route("/", methods=["POST"])
@jwt_required()
@check_admin
def create_game():
    request_data = request.get_json()
    name = request_data.get("name")
    description = request_data.get("description")
    stmt = db.Select(Users).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt)

    game = Games(
        name = name,
        description = description,
        user_id = user.id
        )

    db.session.add(game)
    db.session.commit()
    return game_schema.dump(game), 201

# Fetch specific game to view - READ
@game_bp.route("/<int:game_id>", methods=["GET"])
def view_games(game_id):
    stmt = db.Select(Games).filter_by(id=game_id)
    game = db.session.scalar(stmt)

    if game:
        return game_schema.dump(game), 200
    else:
        return{"error": f"There is no game with id: {game_id}"}
    
# Fetch all games to view 
@game_bp.route("/", methods=["GET"])
def get_games():
    stmt = db.Select(Games).order_by(Games.description.desc())
    game = db.session.scalars(stmt)

    if game:
        return games_schema.dump(game), 200
    else:
        return {"error" : "There are currently no games to view."}    


# Update specific game - Update
@game_bp.route("/<int:game_id>", methods=["PUT", "PATCH"])
@jwt_required()
@check_admin
def update_game(game_id):
    request_data = request.get_json()
    name = request_data.get("name")
    description = request_data.get("description")
    stmt = db.Select(Games).filter_by(id=game_id)
    game = db.session.scalar(stmt)

    if game:
        game.name = name or game.name
        game.description = description or game.description
        
    else:
        return{"error": "No such game exists"}, 404
    
    db.session.commit()
    return game_schema.dump(game), 201

# Delete specific game - Delete
@game_bp.route("/<int:game_id>", methods=["DELETE"])
@jwt_required()
@check_admin
def delete_game(game_id):
    try:
        # Attempt to retrieve the user with the given id
        stmt = db.Select(Games).filter_by(id=game_id)
        game = db.session.scalar(stmt)
        # If user is found, delete and commit
        if game:
            db.session.delete(game)
            db.session.commit()
            # Return a success message
            return {"message" : f"Game with id {game_id} is deleted."}
            
        # If user is not found, return a 404 error
        else:
            return {"message" : f"Game with id {game_id} not found."}, 404
        
    except Exception as e:
        # Handle any unexpected errors
        return {"message" : f"{str(e)}"}, 500
    


