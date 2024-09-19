# from init import db, ma, bcrypt
# from flask import request, Blueprint, jsonify
# from models.player import Player, player_schema, players_schema
# from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
# from datetime import timedelta

# from sqlalchemy.exc import SQLAlchemyError

# player_db = Blueprint("player", __name__, url_prefix="/auth")


# # POST (CREATE) - Register Player into databse from a HTTP Request from the user
# @player_db.route("/register", methods=["POST"])
# def register_player():
#     # Retrieve JSON data from the request
#     request_data = request.get_json()
    
#     # Extract player data from the request
#     name = request_data.get("name")
#     level = request_data.get("level")
#     date = request_data.get("date")
#     email = request_data.get("email")
#     password = request_data.get("password")

#     # Validate required fields
#     if not name or not email or not password:
#         return jsonify({"error": "Name, email, and password are required"}), 400

#     # Check if the email is already in use
#     existing_user = db.Select(Player).filter_by(email=email)
#     if existing_user:
#         return jsonify({"error": "Email already in use"}), 400

#     # Create a new Player instance
#     player = Player(
#         name=name,
#         level=level,
#         date=date,
#         email=email
#     )
    
#     # Hash the password and set it
#     hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
#     player.password = hashed_password

#     # Add and commit the new player to the database
#     try:
#         db.session.add(player)
#         db.session.commit()
#     except SQLAlchemyError as e:
#         return jsonify({"error": "Database commit failed", "details": str(e)}), 500

#     # Return the newly created player's data
#     return jsonify(player_schema.dump(player)), 201

# # Login a Player depending on the email they enter, provide a token with an expiry if their email matches email stored within database.
# @player_db.route("/login", methods=["POST"])
# def login_player():
#     # Retrieve the JSON data from the request
#     request_data = request.get_json()
#     email = request_data.get("email")
#     password = request_data.get("password")

#     if not email or not password:
#         return jsonify({"error": "Email and password are required as input"}), 400

#     try:
#         # Query the database for the user by email
#         user = db.Select(Player).filter_by(email=email)
#     except SQLAlchemyError as e:
#         return jsonify({"error": "Database query failed", "details": str(e)}), 500

#     if user and bcrypt.check_password_hash(user.password, password):
#         # Generate an access token for the user
#         token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
#         response_data = {
#             "email": user.email,
#             "is_authorised": user.is_authorised,
#             "token": token
#         }
#         return jsonify(response_data), 200
#     else:
#         # Respond with an error if credentials are invalid
#         return jsonify({"error": "Invalid email or password"}), 400
    
# # Change Player name, password and email
# @player_db.route("/player", methods=["PUT", "PATCH"])
# @jwt_required()
# def update_player():
#     request_data = request.get_json()
#     email = request_data.get("email")
#     name = request_data.get("name")
#     password = request_data.get("password")

#     # Retrieve the current user's identity from JWT
#     user_id = get_jwt_identity()

#     # Query the database for the user
#     try:
#         user = db.Select(Player).filter_by(id=user_id)
#     except SQLAlchemyError as e:
#         return jsonify({"error": "Database query failed", "details": str(e)}), 500

#     if user is None:
#         return jsonify({"error": "No such user exists"}), 404

#     # Update user attributes if provided
#     if email:
#         user.email = email
#     if name:
#         user.name = name
#     if password:
#         hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
#         user.password = hashed_password

#     try:
#         db.session.commit()
#     except SQLAlchemyError as e:
#         return jsonify({"error": "Database commit failed", "details": str(e)}), 500

#     # Return the updated user information
#     return jsonify(players_schema.dump(user)), 200
    
# @player_db.route("/users/<int:player_id>", methods=["DELETE"])
# @jwt_required()
# # @auth_as_admin_decorator
# def delete_user(player_id):
#     try:
#         # Attempt to retrieve the user with the given id
#         stmt = db.Select(Player).filter_by(id=player_id)
#         player = db.session.scalar(stmt)

#         # If user is found, delete and commit
#         if player:
#             db.session.delete(player)
#             db.session.commit()
#             # Return a success message
#             return jsonify(message=f"Player with id {player_id} is deleted.")
        
#         # If user is not found, return a 404 error
#         else:
#             return jsonify(message=f"Player with id {player_id} not found."), 404
    
#     except Exception as e:
#         # Handle any unexpected errors
#         return jsonify(message=str(e)), 500