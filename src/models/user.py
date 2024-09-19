from init import db,ma
from marshmallow import fields
from marshmallow.validate import Regexp

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    is_authorised = db.Column(db.Boolean, default=False)

    games = db.Relationship("Game", back_populates="user")

class UserSchema(ma.Schema):
    
    games = fields.List(fields.Nested("GameSchema", exclude=["user"]))
    name = fields.String(required=True, validate=Regexp("[a-zA-Z0-9]+"))

    class Meta:
        fields = ("id", "name", "password", "email", "is_authorised", "games")

user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True, exclude=["password"])