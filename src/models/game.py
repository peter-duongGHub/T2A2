from init import db, ma
from marshmallow import fields


class Game(db.Model):
    __tablename__ = "game"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), primary_key=True)

class GameSchema(ma.Schema):
    class Meta:
        fields = ("id", "description")

games_schema = GameSchema(many=True)
game_schema = GameSchema()

