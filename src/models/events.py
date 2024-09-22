# Import SQLAlchemy & Marshmallow object from init file for creating Model and Schema
from init import db, ma
# Import fields module from Marshmallow for defining schemas and validation of user input
from marshmallow import fields, validates, ValidationError
# Import validate module to use Regexp
from marshmallow.validate import Regexp

# Create Events model using SQLAlchemy object
class Events(db.Model):
    # Defined table name and the attributes, including data type and constraints
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(40), nullable=False)
    date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Float, nullable=False)

    # Foreign key referenced to players model primary key id 
    player_id = db.Column(db.Integer, db.ForeignKey("players.id"), nullable=False)
    
    # Defined relationships between comments,player and categories models to share certain attributes with events model
    comments = db.Relationship("Comments", back_populates="event")
    player = db.Relationship("Players", back_populates="events")
    categories = db.Relationship("Category", back_populates="event")

# Create Event Schema to serialise and deserialise objects
class EventSchema(ma.Schema):
    
    # Specific attributes provided from other model schemas to the event schema for CRUD operations
    categories = fields.List(fields.Nested("CategorySchema", only=[""]))
    comments = fields.List(fields.Nested("CommentSchema", exclude=["event"]))
    player = fields.Nested("PlayerSchema", exclude=["date"])

    # Validation of attributes, restricting user input to certain conditions
    description = fields.String(required=True, validate=Regexp("/r'^[A-Za-z]{1,50}$'/", error="Description must only contain characters A-Z, between 1 to 50 characters."))
    date = fields.Date(required=True, validate=Regexp("^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$", error="Date must be in the format dd/mm/yyyy, dd-mm-yyyy or dd.mm.yyyy."))
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
        fields = ("id", "description", "date", "duration", "comments", "player", "categories")

# Used for handling multiple event objects
events_schema = EventSchema(many=True)
# Used for handling a single event object
event_schema = EventSchema()