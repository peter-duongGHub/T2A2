from init import db, ma
from marshmallow import fields
from marshmallow.validate import And, Regexp, OneOf

class Comments(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String, nullable=False)

    player_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)

    player = db.Relationship("Player", back_populates="comments")
    event = db.Relationship("Event", back_populates="comments")


class CommentSchema(ma.Schema):

    player = fields.Nested("PlayerSchema", only=["name", "role", "level"])
    event = fields.Nested("EventSchema", only=["description", "duration", "date"])

    class Meta:
        fields = ("id", "message", "player", "event")

    # message = fields.String(required=True, validate=Regexp(""), error="Invalid message format.")

comments_schema = CommentSchema(many=True)
comment_schema = CommentSchema()
