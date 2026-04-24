from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.consultation_controller import get_appointment_types, book_consultation

consultation_bp = Blueprint("consultation", __name__)

# Get list of appointment types
consultation_bp.route("/api/appointment-types", methods=["GET"])(jwt_required()(get_appointment_types))

# Book a consultation
consultation_bp.route("/api/consultations", methods=["POST"])(jwt_required()(book_consultation))