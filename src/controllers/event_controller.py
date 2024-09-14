from init import db, jwt
from models.comments import Comments, comments_schema, comment_schema
from models.events import Event, event_schema,events_schema
from flask import Blueprint, request


event_bp = Blueprint("event", __name__, url_prefix="/events")

# GET SPECIFIC EVENT
@event_bp.route("/<id:event_id>", method=["GET"])
def get_specific(event_id):
    stmt = db.Select(Event).filter_by(id=event_id)
    event = db.session.scalar(stmt)

    if event:
        return event_schema.dump(event), 201
    else:
        return {f"Cannot find card with card id: '{event_id}'"}


# GET ALL EVENTS
@event_bp.route("/", method=["GET"])
def get_all():
    stmt = db.Select(Event)
    event = db.session.scalar(stmt)
    return events_schema.dump(event), 201

# User Create Event
@event_bp.route("/", method=["POST"])
@jwt_required
def create_event():
    request_data = request.get_json()


