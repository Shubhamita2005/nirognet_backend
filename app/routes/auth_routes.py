from flask import Blueprint #A Blueprint is a way to organize Flask applications into modules eg: auth_routes, emergency_chat_routes etc.
from flask_jwt_extended import jwt_required # imports the jwt_required decorator from Flask-JWT-Extended to protect routes so that only authenticated users with a valid JWT token can access them
#This imports functions from the controller layer, the controller layer contain the business logic.
from app.controllers.auth_controller import (
    register,
    login,
    get_profile,
    update_profile,
    update_health,
    change_password
)

auth_bp = Blueprint("auth", __name__) #Creates a Blueprint object named "auth", used internally by flask. auth: the name of the blueprint, __name__ : the current python module name. Flask uses this to locate files and template. all routes defined using auth_bp belong to the authentication module

# defines API routes for register, login, profile access, health update, and password change, with some routes protected using jwt_required so only authenticated users can access them in Flask
auth_bp.route("/api/register", methods=["POST"])(register)
auth_bp.route("/api/login", methods=["POST"])(login)

auth_bp.route("/api/profile", methods=["GET"])(jwt_required()(get_profile))
auth_bp.route("/api/profile", methods=["PUT"])(jwt_required()(update_profile))
auth_bp.route("/api/profile/health", methods=["PUT"])(jwt_required()(update_health))
auth_bp.route("/api/change-password", methods=["PUT"])(jwt_required()(change_password))