from init import db, jwt
# from jwt_extended import jwt_required

# from models.comments import Comments, comments_schema, comment_schema
from models.events import Events, event_schema,events_schema
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.player import Players

event_bp = Blueprint("event", __name__, url_prefix="/events")

# GET SPECIFIC EVENT
@event_bp.route("/<int:event_id>", methods=["GET"])
def get_specific(event_id):
    stmt = db.Select(Events).filter_by(id=event_id)
    event = db.session.scalar(stmt)

    if event:
        return event_schema.dump(event), 201
    else:
        return {f"Cannot find event with event id: '{event_id}'"}


# GET ALL EVENTS
@event_bp.route("/", methods=["GET"])
def get_all():
    stmt = db.Select(Events)
    event = db.session.scalars(stmt)
    if event:
        return events_schema.dump(event), 201
    else:
        return {"error" : f"No events to view."}

# Player Create Event
@event_bp.route("/player/<int:player_id>", methods=["POST"])
@jwt_required()
def create_event(player_id):
    request_data = request.get_json()
    stmt = db.Select(Player).filter_by(id=player_id)
    player = db.session.scalar(stmt)

    if player:
        event = Events(
            description = request_data.get("description"),
            date = request_data.get("date"),
            duration = request_data.get("duration"),
            player_id = player.id
        )
        return event_schema.dump(event), 201
    else:
        return {"error" : "You cannot create an event as player {player_id} does not exist."}


# Update Event
@event_bp.route("/player/<int:player_id>", methods=["PUT","PATCH"])
@jwt_required()
def update_event(player_id):
    request_body = request.get_json()
    stmt = db.Select(Player).filter_by(id=player_id)
    player = db.session.scalar(stmt)

    if player:
        player.description = request_body.get("description") or player.description
    else: 
        return {"error" : "Player does not exist."}
    
    db.session.commit()
    return event_schema.dump(player), 200

# Delete Event
@event_bp.route("/<int:event_id>", methods=["DELETE"])
@jwt_required()
def delete_event(event_id):
    stmt = db.Select(Events).filter_by(id=event_id)
    event = db.session.scalar(stmt)

    if event:
        db.session.delete()
        db.session.commit()
    else:
        return{"error" : "There is no event with id {event_id}."}
    
