from init import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp

class Games(db.Model):
    __tablename__ = "games"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.Relationship("Users", back_populates="games")
    players = db.Relationship("Players", back_populates="game")

class GameSchema(ma.Schema):

    user = fields.Nested('UserSchema', only=["name", "email", "id", "is_authorised"])
    players = fields.List(fields.Nested("PlayerSchema", exclude=["game"]))
    name = fields.String(required=True, validate=Regexp("/^[A-Za-z]+$/"))
    description = fields.String(required=True, validate=Regexp("/r'^[A-Za-z]{1,40}$'/"))

    class Meta:
        fields = ("id", "name", "description", "user", "players")

games_schema = GameSchema(many=True)
game_schema = GameSchema()

