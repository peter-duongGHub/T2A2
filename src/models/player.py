from init import db, ma
from marshmallow import fields

class Players(db.Model):
    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    level = db.Column(db.Integer, default=0)
    date = db.Column(db.Date, nullable=False)
    role = db.Column(db.String, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False)

    game = db.Relationship("Games", back_populates="players")
    events = db.Relationship("Event", back_populates="player")

    # comments = db.Relationship("Comments", back_populates="player")
    # records = db.Relationship("Record", back_populates="player")

class PlayerSchema(ma.Schema):

    game = fields.Nested("GameSchema", only=["name", "description", "user"])
    events = fields.List(fields.Nested("EventSchema", only=["description", "date", "duration"]))
    # comments = fields.Nested("CommentSchema", only=["id", "message"])
    # records = fields.Nested("RecordSchema", only=["progress, date"])


    class Meta:
        fields = ("id", "name", "level", "date", "role", "game", "events")

players_schema = PlayerSchema(many=True)
player_schema = PlayerSchema()
