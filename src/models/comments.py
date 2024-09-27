# Import SQLAlchemy & Marshmallow object from init file for creating Model and Schema
from init import db, ma

# Import fields module from Marshmallow for defining schemas and validation of user input
from marshmallow import fields

# Import validate module to use Regexp for validation of user inputs
from marshmallow.validate import Regexp

# Create Comments model using SQLAlchemy object
class Comments(db.Model):
    
    # Defined table name and the attributes, including data type and constraints
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String, nullable=False)

    # Foreign keys reference players and events primary keys id as joint table
    player_id = db.Column(db.Integer, db.ForeignKey("players.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)

    # Defined relationships between players and events model to share certain attributes with comments model
    player = db.Relationship("Players", back_populates="comments")
    event = db.Relationship("Events", back_populates="comments")

# Create Comment Schema to serialise and deserialise objects
class CommentSchema(ma.Schema):

    # Specific attributes provided from other model schemas to the comments schema for CRUD operations
    player = fields.Nested("PlayerSchema", only=["name", "role", "game"])
    event = fields.Nested("EventSchema", only=["description", "duration", "date"])

    # Validation of message attribute, restricting user input to certain conditions
    message = fields.String(required=True, validate=Regexp("^.{1,50}$", error="Message must only contain characters A-Z, between 1 to 50 characters."))

    # Meta class to serialise attributes associated to comment model
    class Meta:
        fields = ("id", "message", "player", "event")

# Used for handling multiple comment object
comments_schema = CommentSchema(many=True)

# Used for handling single comment object
comment_schema = CommentSchema()
