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

    games = db.Relationship("Games", back_populates="user")

class UserSchema(ma.Schema):
    
    games = fields.List(fields.Nested("GameSchema", exclude=["user"]))

    name = fields.String(required=True, validate=Regexp("/r'^[A-Za-z]{1,50}$'/", error="Name must only contain characters A-Z, between 1 to 50 characters."))

    password = fields.String(required=True, validate=Regexp("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,16}$", 
    error="Password must contain at least one letter, one digit, and is between eight and sixteen characters in length."))

    email = fields.String(required=True, validate=Regexp("^\S+@\S+$", 
    error="Email must contain @ symbol followed and preceding non white space characters."))

    class Meta:
        fields = ("id", "name", "password", "email", "is_authorised", "games")


user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True, exclude=["password"])