# Import SQLAlchemy & Marshmallow object from init file for creating Model and Schema
from init import db, ma
# Import fields module from Marshmallow for defining schemas and validation of user input
from marshmallow import fields
# Import validate module to use Regexp
from marshmallow.validate import Regexp, OneOf

ROLES = ("Tank", "Healer", "DPS")

# Create Players model using SQLAlchemy object
class Players(db.Model):
    # Defined table name and the attributes, including data type and constraints
    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    date = db.Column(db.Date)
    role = db.Column(db.String, nullable=False)

    # Foreign key referenced to games model primary key id 
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)

    # Defined relationships between games, events and comments models to share certain attributes with players model
    game = db.Relationship("Games", back_populates="players")
    events = db.Relationship("Events", back_populates="player", cascade="all, delete")
    comments = db.Relationship("Comments", back_populates="player", cascade="all, delete")

# Create Player Schema to serialise and deserialise objects
class PlayerSchema(ma.Schema):

    # Specific attributes provided from other model schemas to the player schema for CRUD operations
    game = fields.Nested("GameSchema", exclude=["players"])
    events = fields.List(fields.Nested("EventSchema", only=["description", "date", "duration"]))
    comments = fields.List(fields.Nested("CommentSchema", only=["id", "message"]))
    
    # Validation of attributes, restricting user input to certain conditions
    name = fields.String(required=True, validate=Regexp("/r'^[A-Za-z]{1,50}$'/", error="Name must only contain letters and must be between 1-50 characters long."))
    date = fields.Date(required=True, validate=Regexp("^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$" , error="Date must be in the format yyyy-mm-dd or yyyy-m-d"))
    role = fields.String(required=True, validate=OneOf(ROLES), error="Role selected must be Tank, Healer or DPS")

    # Meta class to serialise attributes associated to player model
    class Meta:
        fields = ("id", "name", "date", "role", "game", "comments")

# Used for handling a single player object
players_schema = PlayerSchema(many=True)

# Used for handling multiple player objects
player_schema = PlayerSchema()

