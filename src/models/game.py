# Import SQLAlchemy & Marshmallow object from init file for creating Model and Schema
from init import db, ma
# Import fields module from Marshmallow for defining schemas and validation of user input
from marshmallow import fields
# Import validate module to use Regexp
from marshmallow.validate import Regexp

# Create Games model using SQLAlchemy object
class Games(db.Model):
    # Defined table name and the attributes, including data type and constraints
    __tablename__ = "games"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    # Foreign key referenced to user model primary key id 
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # Defined relationships between users and players models to share certain attributes with game model
    user = db.Relationship("Users", back_populates="games")
    players = db.Relationship("Players", back_populates="game")

# Create Game Schema to serialise and deserialise objects
class GameSchema(ma.Schema):

    # Specific attributes provided from other model schemas to the games schema for CRUD operations
    user = fields.Nested('UserSchema', only=["name", "email", "id", "is_authorised"])
    players = fields.List(fields.Nested("PlayerSchema", exclude=["game"]))
    
    # Validation of attributes, restricting user input to certain conditions
    name = fields.String(required=True, validate=Regexp("/r'^[A-Za-z]{1,50}$'/"), 
    error="Accepting letters ONLY from 1-50 characters max")
    description = fields.String(required=True, validate=Regexp("/r'^[A-Za-z]{1,50}$'/"), 
    error="Accepting letters ONLY from 1-50 characters max")

    # Meta class to serialise attributes associated to game model
    class Meta:
        fields = ("id", "name", "description", "user", "players")

# Used for handling multiple game object
games_schema = GameSchema(many=True)

# Used for handling a single game object
game_schema = GameSchema()

