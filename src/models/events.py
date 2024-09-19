from init import db, ma
from marshmallow import fields
from marshmallow.validate import And, Regexp, OneOf

class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(40), nullable=False)
    date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=False)

    comments = db.Relationship("Comment", back_populates="event")
    player = db.Relationship("Player", back_populates="events")

class EventSchema(ma.Schema):

    comments = fields.List(fields.Nested("CommentSchema", exclude=["event"]))
    player = fields.Nested("PlayerSchema", exclude=["date"])

    class Meta:
        fields = ("id", "description", "date", "duration", "comments")

    # name = fields.String(required=True, validate=Regexp(""))
    # description = fields.String(required=True, validate=Regexp(""))
    # duration = fields.String(required=True, validate=Regexp(""))

events_schema = EventSchema(many=True)
event_schema = EventSchema()