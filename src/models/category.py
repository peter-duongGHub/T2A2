# Import SQLAlchemy & Marshmallow object from init file for creating Model and Schema
from init import db, ma

# Import fields module from Marshmallow for defining schemas and validation of user input
from marshmallow import fields

# Import validate module to use Regexp and OneOf
from marshmallow.validate import Regexp, OneOf

CATEGORIES = ("CHARACTER", "ACTION", "SOCIAL")

# Create Category model using SQLAlchemy object
class Category(db.Model):

    # Defined table name and the attributes, including data type and constraints
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # Foreign key referenced to events model primary key id 
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)

    # Defined relationships between events model to share certain attributes with category model
    event = db.Relationship("Events", back_populates="categories")

# Create Category Schema to serialise and deserialise objects
class CategorySchema(ma.Schema):

    # Specific attributes provided from other events schemas to the category schema for CRUD operations
    event = fields.Nested("EventSchema", exclude=["categories"])

    # Validation of attributes, restricting user input to certain conditions
    name = fields.String(required=True, validate=OneOf(CATEGORIES))

    # Meta class to serialise attributes associated to category model
    class Meta:
        fields = ("id", "name", "event")

# Used for handling multiple category objects
categories_schema = CategorySchema(many=True)

# Used for handling a single category object
category_schema = CategorySchema()


