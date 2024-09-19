from init import db, bcrypt
from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from marshmallow import ValidationError
from psycopg2 import errorcodes
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from auth import check_admin

user_bp = Blueprint("use", __name__, url_prefix="/user")

from models.user import User, user_schema, UserSchema

# Create a user - DONE WITH ERROR HANDLING CREATING USER
@user_bp.route("/register", methods=["POST"])
def create_user():
    try: 
        request_data = UserSchema().load(request.get_json())
        user = User(
            name = request_data.get("name"),
            email = request_data.get("email")
            # is_authorised = request_data.get("is_authorised")
        )
        password = request_data.get("password")
        if password:
            hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
            user.password = hashed_password or user.password

        is_authorised = request_data.get("is_authorised")
        if is_authorised:
            user.is_authorised = is_authorised or user.is_authorised

        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201
    except IntegrityError as e:
        if e.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The {e.orig.diag.column_name} is required"}, 400
        if 'unique constraint' in str(e.orig):
            return {"error": "Email already in database, please enter a unique email address"}, 400
    except ValidationError:
        return{"message": "Please enter a name starting with an alphanumeric character."}

# Delete a user
@user_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
@check_admin
def delete_user(user_id):
    try:
        # Fetch the user from the database
        stmt = db.Select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)

        if user:
            # Delete the user if found
            db.session.delete(user)
            db.session.commit()
            
            # Return a success message
            return{"message": f"User with id {user_id} has been deleted."}, 200
        
        else:
            # Return a not found error message
            return{"error": f"User with id {user_id} not found."}, 404
    
    except SQLAlchemyError as e:
        # Handle SQLAlchemy errors
        db.session.rollback()  # Rollback any changes to maintain database integrity
        return{"error": "Database error", "details": str(e)}, 500
    
    except Exception as e:
        # Handle other unexpected errors
        return{"error": "An unexpected error occurred", "details": str(e)}, 500


# Update
@user_bp.route("/", methods=["PUT", "PATCH"])
@jwt_required()
def update_user():
    try:    
        # Load and validate fields from the request body
        body_data = UserSchema().load(request.get_json(), partial=True)
        
        # Extract the password if provided
        request_password = body_data.get("password")
        request_name = body_data.get("name")
        # Fetch the current user from the database
        user_id = get_jwt_identity()
        stmt = db.Select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        
        if user:
            # Update user fields if present in the request
            user.name = request_name or user.name
            if request_password:
                user.password = bcrypt.generate_password_hash(request_password).decode("utf-8") or user.password
            
            # Commit changes to the database
            db.session.commit()
            
            # Return the updated user data
            return user_schema.dump(user), 200
        
        else:
            # Return an error response if the user is not found
            return{"error": "User does not exist."}, 404
        
    except SQLAlchemyError as e:
        # Handle SQLAlchemy errors
        db.session.rollback()  # Rollback any changes to maintain database integrity
        return{"error": "Database error", "details": str(e)}, 500

    except Exception as e:
        # Handle unexpected errors
        return{"error": "An unexpected error occurred", "details": str(e)}, 500

# Login User
@user_bp.route("/login", methods=["POST"])
def login_user():
    try:
        # Retrieve JSON data from the request
        body_data = request.get_json()
        
        # Validate that the required fields are present
        request_email = body_data.get("email")
        request_password = body_data.get("password")
        
        if not request_email or not request_password:
            return{"error": "Email and password are required"}, 400
        
        # Query the database for the user by email
        stmt = db.Select(User).filter_by(email=request_email)
        user = db.session.scalar(stmt)
        
        if user and bcrypt.check_password_hash(user.password, request_password):
            # Create JWT token for authenticated user
            token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
            
            # Return user details and token
            return{
                "Your email": user.email,
                "Admin": user.is_authorised,
                "Your Token": token
            }, 200
        
        # If user not found or password incorrect
        return{"error": "Invalid email or password"}, 401
    
    except SQLAlchemyError as e:
        # Handle SQLAlchemy errors
        return {"error": "Database error", "details": str(e)}, 500

    except Exception as e:
        # Handle other unexpected errors
        return{"error": "An unexpected error occurred", "details": str(e)}, 500
