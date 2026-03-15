from flask import Blueprint, jsonify #imports Blueprint (to create and organize routes) and jsonify (to return responses in JSON format) from Flask

main_bp = Blueprint('main', __name__) #creates a Blueprint object "main" Flask uses it internally to identify this route group, "__name__" tells Flask which Python module the blueprint belongs to
@main_bp.route('/') #This defines a URL route. '/' is the root URL of the website.
def home(): #This function runs whenever someone visits: '/' This is the controller logic for the home route.
    return jsonify({"message": "Flask routes working!"}) #This sends a JSON response back to the client.

