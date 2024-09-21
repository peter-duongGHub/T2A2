from flask import Blueprint, request
from models.record import Records, record_schema, records_schema
from models.player import Players
from init import db
from flask_jwt_extended import jwt_required

record_bp = Blueprint("records", __name__, url_prefix="/records")

# Create record for progress
@record_bp.route("/<int:player_id>", methods=["POST"])
def create_record(player_id):
    request_body = request.get_json()
    
    stmt = db.Select(Players).filter_by(id=player_id)
    player = db.session.scalar(stmt)

    if player:
        record = Records(
            progress = request_body.get("progress"),
            date = request_body.get("date"), 
            player_id = player.id
        )
        db.session.add(record)
        db.session.commit()
        return record_schema.dump(record), 201
    
    else:
        return {"error" : "There is no player with id {player_id}, therefor a record cannot be created"}
    
# View ALL records for progress
@record_bp.route("/", methods=["GET"])
def view_records():
    stmt = db.Select(Records)
    records = db.session.scalars(stmt)

    if records:
        return records_schema.dump(records), 200
    
    else:
        return {"There are no records to return"}
    
# View SPECIFIC records for progress
@record_bp.route("/<int:record_id>", methods=["GET"])
def specific_records(record_id):
    stmt = db.Select(Records).filter_by(id=record_id)
    record = db.session.scalar(stmt)

    if record:
        return record_schema(record), 200
    else:
        return {f"There is no record with id {record_id}."}
    
# Update record for progress
@record_bp.route("/<int:record_id>", methods=["PUT", "PATCH"])
def update_record(record_id):
    stmt = db.Select(Records).filter_by(id=record_id)
    record = db.session.scalar(stmt)

    request_body = request.get_json()

    if record:
        record.progress = request_body.get("progress")

        db.session.commit()
        return record_schema.dump(record)
    else: 
        return {f"There is no record with record id {record_id}"}

# Delete record for progress
@record_bp.route("/<int:record_id>", methods=["DELETE"])
@jwt_required()
def delete_record(record_id):
    stmt = db.Select(Records).filter_by(id=record_id)
    record = db.session.scalar(stmt)

    if record:
        db.session.delete(record)
        db.session.commit()
        return {f"The record with id {record_id} has been deleted successfully."}
    else:
        return {f"There is no such record with id {record_id}."}
    

