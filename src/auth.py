from flask_jwt_extended import get_jwt_identity
from functools import wraps
from init import db
from models.user import User

def check_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Retrieve the user's ID from JWT
        user_id = get_jwt_identity()
        
        # Query the database to get the user by their ID
        stmt = db.Select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
            
        # Check if the user is an admin
        if user and user.is_authorised:
            return func(*args, **kwargs)
        # Return an error response if the user is not an admin
        else:
            return {"error": "Only admins can perform delete."}, 403

    return wrapper