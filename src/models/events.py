# Import SQLAlchemy & Marshmallow object from init file for creating Model and Schema
from init import db, ma
# Import fields module from Marshmallow for defining schemas and validation of user input through the use of validates and ValidationError for error handling
from marshmallow import fields, validates, ValidationError
# Import validate module to use Regexp and OneOf for validation of inputs
from marshmallow.validate import Regexp, OneOf

# Defined constant to limit user inputs to ACTION, QUEST or SOCIAL for description attribute
DESCRIPTION = ("ACTION", "QUEST", "SOCIAL")

# Create Events model using SQLAlchemy object
class Events(db.Model):
    # Defined table name and the attributes, including data type and constraints
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    date = db.Column(db.Date)
    duration = db.Column(db.Float, nullable=False)

    # Foreign key referenced to players model primary key id 
    player_id = db.Column(db.Integer, db.ForeignKey("players.id"), nullable=False)
    
    # Defined relationships between comments,player models to share certain attributes with events model
    comments = db.Relationship("Comments", back_populates="event", cascade="all, delete")
    player = db.Relationship("Players", back_populates="events")

# Create Event Schema to serialise and deserialise objects
class EventSchema(ma.Schema):
    
    # Specific attributes provided from other model schemas to the event schema for CRUD operations
    comments = fields.List(fields.Nested("CommentSchema", exclude=["event"]))
    player = fields.Nested("PlayerSchema")

    # Validation of attributes, restricting user input to certain conditions
    description = fields.String(required=True, validate=OneOf(DESCRIPTION))
    date = fields.Date(required=True, validate=Regexp("/^\d{2}\/\d{2}\/\d{4}$/" , error="Date must be in the format mm-dd-yyyy"))
    duration = fields.Float(required=True)

    # Validate user import duration using marshmallow validates module
    @validates('duration')
    def validate_duration(self, value):
        if value < 0:
            raise ValidationError('Duration must be a non-negative number.')
        # Validation for a maximum duration - 24 hours
        if value > 24:  # Maximum duration (in hours)
            raise ValidationError('Duration must not exceed 24 hours.')

    # Meta class to serialise attributes associated to event model
    class Meta:
        fields = ("id", "description", "date", "duration", "comments", "player")

# Used for handling multiple event objects
events_schema = EventSchema(many=True)
# Used for handling a single event object
event_schema = EventSchema()