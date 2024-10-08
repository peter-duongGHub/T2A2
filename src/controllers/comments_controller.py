# Import flask modules request and blueprint. Request is to retrieve JSON body data and Blueprint to create comment blueprint decorator
from flask import request, Blueprint
# Import SQLAlchemy object instance from the init file for database operations
from init import db
# Import model objects to create object instances and schema to deserialise objects for view
from models.comments import Comments, comment_schema, comments_schema, CommentSchema
from models.events import Events, event_schema, events_schema
from models.player import Players

# Import flask modules for authentication
from flask_jwt_extended import jwt_required, get_jwt_identity

# Create comment blueprint for registering blueprint in other files
comments_bp = Blueprint("comments", __name__,
                        url_prefix="/<int:event_id>/comments")

# Create route to view all comment objects


@comments_bp.route("/", methods=["GET"])
def view_comments(game_id, player_id, user_id, event_id):
    try:
        # Retrieve all comment objects from the database
        stmt = db.Select(Comments)
        comment = db.session.scalars(stmt)
        # If there are comment objects in the database:
        if comment:
            # Return deserialised comment objects to the view with a success 200 code
            return comments_schema.dump(comment), 200
        else:
            # Return an error message if there are no comment objects
            return {"error": "There are no comments to view"}, 404
    # Error handling for exceptional errors that may occur
    except Exception as e:
        return {"error": f"{e}"}, 400

# Create route to view specific comment object


@comments_bp.route("/<int:comment_id>", methods=["GET"])
def specific_comment(game_id, player_id, user_id, event_id, comment_id):
    try:
        # Fetch comment with particular id based on dynamic route comment id - checks inside database for specific comment object
        stmt = db.Select(Comments).filter_by(id=comment_id)
        comment = db.session.scalar(stmt)
        # If the comment exists:
        if comment:
            # Return to the view a deserialised comment object with a success code 200
            return comment_schema.dump(comment), 200
        else:
            # Return to the view an error message, there is no comment id equal to comment_id
            return {"error": f"There is no comment with id {comment_id}."}, 404
    # Error handling for exceptional errors that may occur
    except Exception as e:
        return {"error": f"{e}"}, 400

# Create a route to create a comment for an event, requiring a JWT from when a player was created


@comments_bp.route("/", methods=["POST"])
@jwt_required()
def create_comment(game_id, player_id, user_id, event_id):
    try:
        # Fetch player object from database with the id related to the JWT identity
        stmt = db.Select(Players).filter_by(id=player_id)
        player = db.session.scalar(stmt)

        # Fetch the event object relating to the event id in the dynamic route
        event_stmt = db.Select(Events).filter_by(id=event_id)
        event = db.session.scalar(event_stmt)

        # Extract JSON body from front-end into a variable message
        request_body = CommentSchema().load(request.get_json())
        message = request_body.get("message")

        # If there is a player object with the specific id:
        if player:
            # Create a comment object with attributes
            comment = Comments(
                message=message,
                player_id=player.id,
                event_id=event.id
            )

            # Add the comment object to the database session and commit the change to the database session
            db.session.add(comment)
            db.session.commit()
            # Return to the view a deserialised comment object with a success code 201
            return comment_schema.dump(comment), 201
        # If there is no player with id relating to JWT return an error message
        else:
            return {f"There is no such event with event id {event_id}."}, 404
    # Error handling for exceptional errors that may occur
    except Exception as e:
        return {"error": f"{e}"}, 400

# Create a route to update a specific comment


@comments_bp.route("<int:comment_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_comment(event_id, game_id, player_id, comment_id, user_id):
    try:
        # Query specific comment object from the database based on dynamic route comment id
        stmt = db.Select(Comments).filter_by(id=comment_id)
        comment = db.session.scalar(stmt)

        # Retrive JSON body input from front-end and extract "message" in a variable and validation through comment schema
        request_body = CommentSchema().load(request.get_json())
        message = request_body.get("message")
        # If there is the specific comment object in the database:
        if comment:
            # Change comments attribute message to JSON input "message" from front-end
            comment.message = message or comment.message
            # Commit changes to the database session
            db.session.commit()
            # Return to the view a deserialised comment object with success code 200
            return comment_schema.dump(comment), 200
        # If specific comment doesnt exist in database:
        else:
            # Return error message that it does not exist
            return {"error": f"There is no comment with id {comment_id}."}, 404
    # Error handling for exceptional errors that may occur
    except Exception as e:
        return {"error": f"{e}"}, 400

# Create a route to delete a specific commment


@comments_bp.route("<int:comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment(event_id, game_id, player_id, comment_id, user_id):
    try:
        # Fetch a specific comment object from the database based on the dynamic route comment id
        stmt = db.Select(Comments).filter_by(id=comment_id)
        comment = db.session.scalar(stmt)

        # If comment object exists:
        if comment:
            # Delete the comment object from the database session and commit the change to the database session
            db.session.delete(comment)
            db.session.commit()
            # Return to the view a success message of the deleted comment object
            return {"success": f"Deleted comment with id {comment_id}."}, 200
        else:
            # If there is no specific comment object in the database return error message.
            return {"error": "Please enter a valid comment id."}, 404
    # Error handling for exceptional errors that may occur
    except Exception as e:
        return {"error": f"{e}"}, 400
