# Import flask modules request and blueprint. Request is to retrieve JSON body data and Blueprint to create comment blueprint decorator
from flask import request, Blueprint
# Import SQLAlchemy object instance from the init file for database operations
from init import db
# Import model objects to create object instances and schema to deserialise objects for view
from models.comments import Comments, comment_schema, comments_schema
from models.events import Events, event_schema, events_schema
from models.player import Players

# Import flask modules for authentication
from flask_jwt_extended import jwt_required, get_jwt_identity

# Create comment blueprint for registering blueprint in other files
comments_bp = Blueprint("comments", __name__, url_prefix="/<int:event_id>/comments")

# Create route to view all comment objects
@comments_bp.route("/", methods=["GET"])
def view_comments(game_id, player_id):
    # Retrieve all comment objects from the database
    stmt = db.Select(Comments)
    comment = db.session.scalars(stmt)
    # If there are comment objects in the database:
    if comment:
        # Return deserialised comment objects to the view with a success 200 code
        return comments_schema.dump(comment), 200
    else:
        # Return an error message if there are no comment objects
        return {"error" : "There are no comments to view"}

# Create route to view specific comment object
@comments_bp.route("/<int:comment_id>", methods=["GET"])
def specific_comment(comment_id, game_id, player_id):
    # Fetch comment with particular id based on dynamic route comment id - checks inside database for specific comment object
    stmt = db.Select(Comments).filter_by(id=comment_id)
    comment = db.session.scalar(stmt)
    # If the comment exists:
    if comment:
        # Return to the view a deserialised comment object with a success code 200
        return comment_schema.dump(comment), 200
    else:
        # Return to the view an error message, there is no comment id equal to comment_id
        return {"error" : f"There is no comment with id {comment_id}."}

# Create a route to create a comment for an event, requiring a JWT from when a player was created
@comments_bp.route("/", methods=["POST"])
@jwt_required()
def create_comment(event_id, player_id, game_id):
    # Fetch player object from database with the id related to the JWT identity
    stmt = db.Select(Players).filter_by(id=get_jwt_identity())
    player = db.session.scalar(stmt)\

    # Fetch the event object relating to the event id in the dynamic route
    event_stmt = db.Select(Events).filter_by(id=event_id)
    event = db.session.scalar(event_stmt)

    # Extract JSON body from front-end into a variable message
    request_body = request.get_json()
    message = request_body.get("message")

    # If there is a player object with the specific id:
    if player:
        # Create a comment object with attributes
        comment = Comments(
            message = message,
            player_id = player.id
        )
        # If there is the specific event object create comment attribute event_id associated to the id of the specific event id in the database
        if event:
            comment.event_id = event.id
        # If there is no specific event object in the database leave comment attribute as event
        else: 
            comment.event_id = event

        # Add the comment object to the database session and commit the change to the database session
        db.session.add(comment)
        db.session.commit()
    # If there is no player with id relating to JWT return an error message
    else:
        return {f"There is no such event with event id {event_id}."}
    
    # Return to the view a deserialised comment object with a success code 201
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

    