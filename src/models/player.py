from init import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp

class Players(db.Model):
    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    level = db.Column(db.Integer, default=0)
    date = db.Column(db.Date, nullable=True)
    role = db.Column(db.String, nullable=False)
    
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)

    game = db.Relationship("Games", back_populates="players")
    events = db.Relationship("Events", back_populates="player")

    comments = db.Relationship("Comments", back_populates="player")
    records = db.Relationship("Records", back_populates="player")


class PlayerSchema(ma.Schema):

    game = fields.Nested("GameSchema", only=["name", "description", "user", "id"])
    events = fields.List(fields.Nested("EventSchema", only=["description", "date", "duration"]))
    comments = fields.List(fields.Nested("CommentSchema", only=["id", "message"]))
    records = fields.List(fields.Nested("RecordSchema", only=["progress, date"]))

    # name = fields.String(required=True, validate=Regexp())


    class Meta:
        fields = ("id", "name", "level", "date", "role", "game", "events", "comments", "records")

players_schema = PlayerSchema(many=True)
player_schema = PlayerSchema()
