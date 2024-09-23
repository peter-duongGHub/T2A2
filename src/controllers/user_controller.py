# Import SQLAlchemy and Bcrypt objects for database operations and hashing respectively
from init import db, bcrypt
# Import flask modules Blueprint and request to use decorator routes and retrieve body data from front-end respectively
from flask import Blueprint, request
# Import sqlalchemy.exc modules IntegrityError and SQLAlchemyError for Error Handling
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
# Import Marshmallow module ValidationError for Error Handling
from marshmallow import ValidationError
# Import Psycopg2 driver for module errorcodes for error handling
from psycopg2 import errorcodes
# Import flask_jwt_extended module to create tokens, retrieve token id's and authentication
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
# Import datetime to add expiry to tokens
from datetime import timedelta
# Import auth file to provide administration checks for certain functions
from auth import check_admin
# Import user model for creating user object(s) and schema for serialising and deserialising for display to the view
from models.user import Users, user_schema, UserSchema
from controllers.game_controller import game_bp
# Create blueprint for use as decorator by registering blueprint with main file function
user_bp = Blueprint("use", __name__, url_prefix="/user")
user_bp.register_blueprint(game_bp)

# Create a route to register users
@user_bp.route("/register", methods=["POST"])
def create_user():
    try: 
        # Retrieve body data from the front-end (from JSON body)
        request_data = UserSchema().load(request.get_json())
        # Create user object from user input from JSON body (front-end)
        user = Users(
            name = request_data.get("name"),
            email = request_data.get("email")
        )
        # Retrieve password from front-end JSON body if it exists 
        password = request_data.get("password")
        if password:
            # Hash the password (encrypt) with bcrypt module and assign the password to the created user objects password attribute
            hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
            user.password = hashed_password or user.password
        # If is_authorised is input by the user assign is_authorised to the created user objects is_authorised attribute
        is_authorised = request_data.get("is_authorised")
        if is_authorised:
            user.is_authorised = is_authorised or user.is_authorised

        # Add the user object to the database session
        db.session.add(user)
        # Commit the addition of the user object to the database session
        db.session.commit()
        # Return a view of the user object with a success code 201
        return user_schema.dump(user), 201
    # Error Handling if there are missing values that are required
    except IntegrityError as e:
        if e.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The {e.orig.diag.column_name} is required"}, 400
        # Error Handling if there is already the same email in the database
        if 'unique constraint' in str(e.orig):
            return {"error": "Email already in database, please enter a unique email address"}, 400
    # Error handling for the user input, if the input does not match validating inputs error appears
    except ValidationError as e:
            return{"error" : f"{e}"}, 400

# Create a route to delete a specific user based on user_id on the route
@user_bp.route("/<int:user_id>", methods=["DELETE"])
# JSON web token is required as a bearer token and check for is_authorised to use the endpoint
@jwt_required()
@check_admin
def delete_user(user_id):
    try:
        # Fetch the specific user from the database with user_id
        stmt = db.Select(Users).filter_by(id=user_id)
        user = db.session.scalar(stmt)

        # If there is such a user with the specific user_id:
        if user:
            # Delete the user if found and commit to the database session
            db.session.delete(user)
            db.session.commit()
            
            # Return a success message of the user_id deleted and a success code 200
            return{"message": f"User with id {user_id} has been deleted."}, 200
        
        else:
            # Return a message showing the user is not in the database
            return{"error": f"User with id {user_id} not found."}, 404
    
    # Error handling to handle any unexpected errors that may occur
    except Exception as e:
        return{"error": "An unexpected error occurred", "details": str(e)}, 500


# Create a route to update a specific user based on user_id on the route
@user_bp.route("/<int:user_id>", methods=["PUT", "PATCH"])
# JSON Web token required so that only users with the associated JWT can make changes to the user
@jwt_required()
def update_user(user_id):
    try:    
        # Load and validate fields from the request body
        body_data = UserSchema().load(request.get_json(), partial=True)
        
        # Extract the password and name from the body data 
        request_password = body_data.get("password")
        request_name = body_data.get("name")
        # Fetch the user from the user_id from the dynamic route - looking through the database for the user that matches the id
        stmt = db.Select(Users).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        
        # If the user_id matches the id of the token identity:
        if user_id == get_jwt_identity():
            # Update user and password fields if present in the request
            user.name = request_name or user.name
            if request_password:
                user.password = bcrypt.generate_password_hash(request_password).decode("utf-8") or user.password
            
            # Commit changes to the database session
            db.session.commit()
            
            # Return the updated user data with a success 200 code
            return user_schema.dump(user), 200
        
        # If no such user with the user_id return message
        elif not user:
            return{"error" : f"No such user with {user_id}"}
        
        # Else return message for if the token is not the correctly associated token to the user_id
        else:
            return{"error": f"Only user with the correct token can change user with id {user_id}"}, 404
        
    # Error handling for validating user input - if the user input is not valid error with specific input required appears
    except ValidationError as e:
            return{"error" : f"{e}"}, 400

    # General Error handling for any errors that may appear
    except Exception as e:
        # Handle unexpected errors
        return{"error": "An unexpected error occurred", "details": str(e)}, 500

# Create a route to login the user
@user_bp.route("/login", methods=["POST"])
def login_user():
    try:
        # Retrieve JSON data from the request body
        body_data = request.get_json()
        
        # Store the request body email and password into variables if present
        request_email = body_data.get("email")
        request_password = body_data.get("password")
        
        # If either email or password not in request body return message
        if not request_email or not request_password:
            return{"error": "Email and password are required"}, 400
        
        # Query the database for the user by email
        stmt = db.Select(Users).filter_by(email=request_email)
        user = db.session.scalar(stmt)
        
        # If there is a user and the password in the database matches with the request body password:
        if user and bcrypt.check_password_hash(user.password, request_password):
            # Create JWT token for authenticated user
            token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
            
            # Return user details (email, admin rights) and token
            return{
                "Your email": user.email,
                "Admin": user.is_authorised,
                "Your Token": token
            }, 200
        
        else:
            # If user not found or password incorrect
            return{"error": "Invalid email or password"}, 401
    

    # Error handling for any other exceptions that may occur
    except Exception as e:
        # Handle other unexpected errors
        return{"error": "An unexpected error occurred", "details": str(e)}, 500
