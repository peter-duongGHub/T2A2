# Import SQLAlchemy object from init file
from init import db
# Import Comment and Event model for creating of object instances and event schemas for deserialising of objects to present to the view
from models.comments import Comments, comments_schema, comment_schema
from models.events import Events, event_schema,events_schema, EventSchema
# Import flask request and Blueprint modules. Requst module for retrieving JSON body input and Blueprint to create decorator event blueprint
from flask import Blueprint, request
# Import flask module to authenticate player and assign created event to the authenticated player
from flask_jwt_extended import jwt_required, get_jwt_identity
# Import player model to create player object instances
from models.player import Players
# Import comment controller to extend event blueprint into the comment blueprint URL prefix
from controllers.comments_controller import comments_bp
from datetime import datetime

from marshmallow import ValidationError

# Create event blueprint for use in decorator for endpoints
event_bp = Blueprint("event", __name__, url_prefix="/<int:player_id>/events")
event_bp.register_blueprint(comments_bp)

# Create a route for getting a specific event depending on the event id in the dynamic route
@event_bp.route("/<int:event_id>", methods=["GET"])
def get_specific(event_id, user_id, player_id, game_id):
    try:
        # Retrieve Event objects depending on the event id dynamic route
        stmt = db.Select(Events).filter_by(id=event_id)
        event = db.session.scalar(stmt)

        # If there is an event associated to the route event id:
        if event:
            # Return to the view a deserialised event object with a success 200 code
            return event_schema.dump(event), 200
        else:
            # Return an error message stating no specific event
            return {"error" : f"Cannot find event with event id: {event_id}"}, 404
    except Exception as e:
        return {"error" : f"{e}"}


# Create a route for getting all events from the database
@event_bp.route("/", methods=["GET"])
def get_all(user_id, player_id, game_id):
    try:
        # Fetch all event objects from the database
        stmt = db.Select(Events)
        event = db.session.scalars(stmt)
        # If there are event objects:
        if event:
            # Return deserialised event objects to the view with a success code 200
            return events_schema.dump(event), 200
        else:
            # Return an error message if there are no event objects
            return {"error" : f"No events to view."}, 404
    except Exception as e:
        return {"error" : f"{e}"}

# Create a route for creating events if there is a player with the correct JSON web token 
@event_bp.route("/", methods=["POST"])
@jwt_required()
def create_event(user_id, player_id, game_id):
    # Retrieve JSON body data from front-end
    request_data = EventSchema().load(request.get_json())
    # Check the database for specific player with player id from the dynamic route
    stmt = db.Select(Players).filter_by(id=player_id)
    player = db.session.scalar(stmt)
    # If there is a player with specific player id:
    try:
        if player:
            # Create event object with associated player id
            event = Events(
                description = request_data.get("description"),
                duration = request_data.get("duration"),
                player_id = player.id
            )
            date = request_data.get("date")
            if date:
                date_object = datetime.strptime(date, "%m/%d/%Y")
                event.date = date_object
            # Return to the view a deserialised event object with success 201 code
            return event_schema.dump(event), 201
        else:
            # Return an error message because player doesnt exist
            return {"error" : f"You cannot create an event as player {player_id} does not exist."}, 404
    except ValidationError as e:
        return {"error" : {e}}, 400
    except Exception as e:
        return {"error" : {e}}, 400


# Create a route for updating events if there is a player with the correct JSON web token 
@event_bp.route("/<int:event_id>", methods=["PUT","PATCH"])
@jwt_required()
def update_event(event_id, user_id, player_id, game_id):
    try: 
        # Retrieve JSON body data from the front-end input
        request_body = EventSchema().load(request.get_json(), partial=True)
        # Check the database for player object with player id from the dynamic route
        stmt = db.Select(Events).filter_by(id=event_id)
        event = db.session.scalar(stmt)

        # If there is a event with specific event id:
        if event:
            # Change the event's description attribute to the input description
            event.description = request_body.get("description") or event.description
        else: 
            # Return error message if the player with specific player id doesnt exist
            return {"error" : "Event does not exist."}, 404
        
        # Commit the changes to the database session
        db.session.commit()
        # Return a deserialised event object to the view with a success 200 code
        return event_schema.dump(event), 200
    except ValidationError as e:
        return {"error" : f"{e}"}, 400
    except Exception as e:
        return {"error" : f"{e}"}, 400

# Create a route for deleting events if there is a player with the correct JSON web token 
@event_bp.route("/<int:event_id>", methods=["DELETE"])
@jwt_required()
def delete_event(event_id, user_id, player_id, game_id):
    try:
        # Check event table for specific event object with event id
        stmt = db.Select(Events).filter_by(id=event_id)
        event = db.session.scalar(stmt)
        # If there is an event object with the specific id:
        if event:
            # Delete the specific event object and commit the changes to the database session
            db.session.delete(event)
            db.session.commit()
            return {"Success" : f"User with {user_id} was successfully deleted."}
        else:
            # Return an error message that there is no event object with the specific id
            return{"error" : f"There is no event with id {event_id}."}, 404 
    except Exception as e:
        return {"error" : f"{e}"}
        
