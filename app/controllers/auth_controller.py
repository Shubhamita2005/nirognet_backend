from flask import request, jsonify #Used to get data sent by the client (Postman / frontend / mobile app). Converts Python dictionary → JSON response, JSON is the standard format for APIs.
from flask_jwt_extended import create_access_token, get_jwt_identity #mports create_access_token (used to generate a JWT login token) and get_jwt_identity (used to get the identity of the logged-in user from the token) from the flask_jwt_extended library
from app.extensions import db #Imports database object (SQLAlchemy), used to interact with the database.
from app.models import User #Imports the User database model, represents users table in database.


# -----------------------
# Register
# -----------------------
def register(): #Defines a function that handles user registration.
    data = request.get_json() or {} #Gets JSON data sent in request body, If request body is empty → use empty dictionary {}.
    #Extract values from JSON.
    email = data.get("email")
    password = data.get("password")

    if not email or not password: #Checks if email or password missing.
        return jsonify({"msg": "Email and password required"}), 400 #Returns error response, 400 = Bad Request

    if User.query.filter_by(email=email).first(): #checks the database to see if a user with the given email already exists and returns the first matching record.
        return jsonify({"msg": "User already exists"}), 400 #Stops duplicate registration.

    user = User(email=email) #Creates a new User object.
    user.set_password(password) #This function hashes the password.
    user.name = data.get("name", user.name) #If name exists in JSON → update it, Otherwise keep existing value.
    user.contact = data.get("contact", user.contact) #This line updates user.contact with the value from data["contact"] if it exists; otherwise it keeps the existing user.contact value.

    db.session.add(user) #Adds new user to database session.
    db.session.commit() #Actually saves the user in the database.

    return jsonify({"msg": "User registered"}), 201 #201 = Created


# -----------------------
# Login
# -----------------------
def login(): #Handles user login.
    #gets the JSON data from the request (or an empty dictionary if none is provided) and extracts the email and password values from it.
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    
    #If missing credentials → return error
    if not email or not password:
        return jsonify({"msg": "Email and password required"}), 400

    user = User.query.filter_by(email=email).first() #Search database for that email.
    if not user or not user.check_password(password): #Two checks: User exists, Password correct. check_password() compares hashed password. 
        return jsonify({"msg": "Invalid credentials"}), 401 #401 = Unauthorized

    access_token = create_access_token(identity=str(user.id)) #Creates a JWT token containing user ID.
    return jsonify({"access_token": access_token}), 200 #Client must store token and send it in future requests.


# -----------------------
# Get profile
# -----------------------
def get_profile(): #Returns user profile.
    user_id = int(get_jwt_identity()) #Extract user ID from token.
    user = User.query.get(user_id) #Find user with that ID.

    if not user:
        return jsonify({"msg": "User not found"}), 404 #404 = Not found.

    return jsonify(user.to_dict()), 200 #to_dict() converts user object → dictionary.


# -----------------------
# Update profile
# -----------------------
def update_profile(): #Allows user to update personal details.
    
    #Get user from token
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    #Check if user exists
    if not user:
        return jsonify({"msg": "User not found"}), 404

    data = request.get_json() or {} #Get new data

    #updates the user's name, gender, contact, address, and language with values from data if provided; otherwise it keeps the existing values
    user.name = data.get("name", user.name)
    user.gender = data.get("gender", user.gender)
    user.contact = data.get("contact", user.contact)
    user.address = data.get("address", user.address)
    user.language = data.get("language", user.language)

    if "age" in data: #Check if age was sent.
        #Convert age → integer, If empty → store None.
        try:
            user.age = int(data["age"]) if data["age"] else None
        #Handle invalid age
        except ValueError:
            return jsonify({"msg": "Invalid age"}), 400

    db.session.commit() #Save changes
    return jsonify(user.to_dict()), 200 #Return updated profile



# -----------------------
# Update health
# -----------------------
def update_health(): #Updates health data.

    #Get user
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    data = request.get_json() or {}

    #Update fields
    user.blood_group = data.get("blood_group", user.blood_group)
    user.blood_pressure = data.get("blood_pressure", user.blood_pressure)

    db.session.commit() #Save changes
    return jsonify(user.to_dict()), 200 #Return updated data


# -----------------------
# Change password
# -----------------------
def change_password(): #Allows user to change password securely.
    #Get user
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    #Check user exists
    if not user:
        return jsonify({"msg": "User not found"}), 404

    #Get password data
    data = request.get_json() or {}
    old = data.get("old_password")
    new = data.get("new_password")

    #Validate fields
    if not old or not new: #If missing password fields.
        return jsonify({"msg": "old_password and new_password required"}), 400

    #Verify old password
    if not user.check_password(old): #Checks if user entered correct current password.
        return jsonify({"msg": "Old password incorrect"}), 401

    #Set new password
    user.set_password(new) #Hashes and updates password.
    db.session.commit() #Save changes

    #Success response
    return jsonify({"msg": "Password changed"}), 200