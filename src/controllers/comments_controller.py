from flask import request, Blueprint
from models.comments import Comments, comment_schema, comments_schema
from init import db, ma
from models.events import Events, event_schema, events_schema
from models.player import Players
from flask_jwt_extended import jwt_required, get_jwt_identity
comments_bp = Blueprint("comments", __name__, url_prefix="/<int:event_id>/comments")

# View all comments
@comments_bp.route("/", methods=["GET"])
def view_comments(game_id, player_id):
    stmt = db.Select(Comments)
    comment = db.session.scalars(stmt)
    if comment:
        return comments_schema.dump(comment), 200
    else:
        return {"error" : "There are no comments to view"}

# View specific comment
@comments_bp.route("/<int:comment_id>", methods=["GET"])
def specific_comment(comment_id, game_id, player_id):
    stmt = db.Select(Comments).filter_by(id=comment_id)
    comment = db.session.scalar(stmt)
    if comment:
        return comment_schema.dump(comment), 200
    else:
        return {"error" : f"There is no comment with id {comment_id}."}

# Create a comment
@comments_bp.route("/", methods=["POST"])
@jwt_required()
def create_comment(event_id, player_id, game_id):
    stmt = db.Select(Players).filter_by(id=player_id)
    player = db.session.scalar(stmt)

    event_stmt = db.Select(Events).filter_by(id=event_id)
    event = db.session.scalar(event_stmt)

    request_body = request.get_json()
    message = request_body.get("message")

    if player:
        comment = Comments(
            message = message,
            player_id = player.id
        )
    
        if event:
            comment.event_id = event.id
        else: 
            comment.event_id = event


        db.session.add(comment)
        db.session.commit()

    else:
        return {f"There is no such event with event id {event_id}."}
    
    return comment_schema.dump(comment), 201

# Update comment
@comments_bp.route("<int:comment_id>", methods=["PUT", "PATCH"])
def update_comment(event_id, game_id, player_id, comment_id):
    stmt = db.Select(Comments).filter_by(id=comment_id)
    comment = db.session.scalar(stmt)
    request_body = request.get_json()
    message = request_body.get("message")
    if comment:
        comment.message = message or comment.message
    
    else:
        return {"error" : f"There is no comment with id {comment_id}."}
    
    db.session.commit()
    return comment_schema.dump(comment), 200

# Delete comment
@comments_bp.route("<int:comment_id>", methods=["DELETE"])
def delete_comment(event_id, game_id, player_id, comment_id):
    stmt = db.Select(Comments).filter_by(id=comment_id)
    comment = db.session.scalar(stmt)

    if comment:
        db.session.delete(comment)
        db.session.commit()
        return {"success" : f"Deleted comment with id {comment_id}."}
    else:
        return {"error" : "Please enter a valid comment id."}

    