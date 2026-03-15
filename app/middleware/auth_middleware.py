from flask import request, jsonify #imports request (to access incoming HTTP request data) and jsonify (to convert Python data into a JSON response) from the Flask framework
from flask_jwt_extended import get_jwt_identity #imports a function used for JWT authentication, get_jwt_identity() retrieves the identity stored in the JWT token 
from app.models import User #Imports the User model from your database, This represents the users table.


# ------------------------------------------------
# Get current logged-in user from JWT
# ------------------------------------------------
def get_current_user(): #This function retrieves the currently authenticated user based on the JWT token.
    try: #Starts a try block, becuase JWT extraction or database query might fail.
        user_id = int(get_jwt_identity()) #gets the current logged-in user’s ID from the JWT token using get_jwt_identity() and converts it into an integer
        user = User.query.get(user_id) #Queries the database for that user.

        if not user: #Checks if the user does not exist in the database.
            return None, (jsonify({"msg": "User not found"}), 404) #Returns two things: None & Error response

        return user, None #returns the user object as the result and None as the second value, usually indicating no error occurred

    except Exception: #If any error occurs, eg: Missing token, Invalid token, JWT decoding failure
        return None, (jsonify({"msg": "Invalid or missing token"}), 401) #Returns an authentication error, 401 → Unauthorized


# ------------------------------------------------
# Validate required JSON fields
# ------------------------------------------------
def require_fields(*fields): #defines a function require_fields that accepts any number of field names (*fields) as arguments, usually to check if those required fields are present in the input data
    data = request.get_json() or {} #Reads JSON request body.

    missing = [field for field in fields if not data.get(field)] #This is a list comprehension, It finds all missing fields.

    if missing: #Checks if any required fields are missing.
        #Returns error response.
        return None, (
            jsonify({"msg": f"Missing fields: {', '.join(missing)}"}),
            400,
        )

    return data, None #returns data as the result and None to indicate that no error occurred