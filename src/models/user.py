# Import SQLAlchemy & Marshmallow object from init file for creating Model and Schema
from init import db,ma
# Import fields module from Marshmallow for defining schemas and validation of user input
from marshmallow import fields
# Import validate module to use Regexp
from marshmallow.validate import Regexp

# Create Users model using SQLAlchemy object
class Users(db.Model):
    # Defined table name and the attributes, including data type and constraints
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    is_authorised = db.Column(db.Boolean, default=False)

    # Defined relationships between games model to share certain attributes with users model
    games = db.Relationship("Games", back_populates="user", cascade="all, delete")

# Create User Schema to serialise and deserialise objects
class UserSchema(ma.Schema):
    
    # Specific attributes provided from other model schemas to the user schema for CRUD operations
    games = fields.List(fields.Nested("GameSchema", exclude=["user"]))

    # Validation of attributes, restricting user input to certain conditions
    name = fields.String(required=True, validate=Regexp("^[a-zA-Z]{1,50}$", error="Name must only contain characters A-Z, between 1 to 50 characters."))

    password = fields.String(required=True, validate=Regexp("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,16}$", 
    error="Password must contain at least one letter, one digit, and is between eight and sixteen characters in length."))

    email = fields.String(required=True, validate=Regexp("^\S+@\S+$", 
    error="Email must contain @ symbol followed and preceding non white space characters."))
    
    # Meta class to serialise attributes associated to user model
    class Meta:
        fields = ("id", "name", "password", "email", "is_authorised", "games")

# Used for handling a single user object and exclude password from user schema
user_schema = UserSchema(exclude=["password"])

# Used for handling multiple player objects and exclude password from user schema
users_schema = UserSchema(many=True, exclude=["password"])