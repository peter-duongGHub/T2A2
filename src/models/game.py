from init import db, ma
from marshmallow import fields


class Games(db.Model):
    __tablename__ = "games"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    user = db.Relationship("Users", back_populates="games")
    players = db.Relationship("Players", back_populates="game")

class GameSchema(ma.Schema):

    user = fields.Nested('UserSchema', only=["name", "email", "id"])
    players = fields.List(fields.Nested('PlayerSchema', exclude=["game"]))

    class Meta:
        fields = ("id", "name", "description", "user")

games_schema = GameSchema(many=True)
game_schema = GameSchema()

