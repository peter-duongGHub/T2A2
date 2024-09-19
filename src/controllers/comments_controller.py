from flask import request, Blueprint
from models.comments import Comments, comment_schema, comments_schema
from init import db, ma
from models.events import Events, event_schema, events_schema

comments_bp = Blueprint("comments", __name__, url_prefix="/events/<int:event_id>/comments")

# View all comments
@comments_bp.route("/", methods=["GET"])
def view_comments():
    stmt = db.Select(Comments)
    comment = db.session.scalars(stmt)
    if comment:
        return comments_schema.dump(comment), 200
    else:
        return {"error" : "There are no comments to view"}

# View specific comment
@comments_bp.route("/<int:comment_id>", methods=["GET"])
def specific_comment(comment_id):
    stmt = db.Select(Comments).filter_by(id=comment_id)
    comment = db.session.scalar(stmt)
    if comment:
        return comment_schema.dump(comment), 200
    else:
        return {"error" : f"There is no comment with id {comment_id}."}

# Create a comment
@comments_bp.route("<int:event_id>", methods=["POST"])
def create_comment(event_id):
    stmt = db.Select(Events).filter_by(id=event_id)
    event = db.session.scalar(stmt)

    request_body = request.get_json()
    message = request_body.get("message")


    if event:
        comment = Comments(
            message = "This is a random message",
            event_id = event.id
        )
        db.session.add(comment)
        db.session.commit()

    else:
        return {f"There is no such event with event id {event_id}."}
    
    return comment_schema.dump(comment), 201

# Update comment
@comments_bp.route("<int:comment_id>", methods=["PUT", "PATCH"])
def update_comment(comment_id):
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
def delete_comment(comment_id):
    stmt = db.Select(Comments).filter_by(id=comment_id)
    comment = db.session.scalar(stmt)

    if comment:
        db.session.delete(comment)
        db.session.commit()
        return {"success" : f"Deleted comment with id {comment_id}."}
    else:
        return {"error" : "Please enter a valid comment id."}

    