from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.book_consultation_controller import (
    get_specialties,
    get_doctors,
    get_doctor_slots,
    create_consultation_controller,
    get_my_consultations,
    update_consultation_type
)

book_bp = Blueprint("book_consultation", __name__)

# Public
book_bp.route("/api/specialties", methods=["GET"])(get_specialties)
book_bp.route("/api/specialties/<int:specialty_id>/doctors",methods=["GET"])((get_doctors))#get doctors of a specific specialty

book_bp.route("/api/doctors/<int:doctor_id>/slots", methods=["GET"])(get_doctor_slots)#slot for a specific doctor.
# Auth required
book_bp.route("/api/consultations", methods=["POST"])((create_consultation_controller))
book_bp.route("/api/consultations/<consultation_id>/type", methods=["PUT"])((update_consultation_type))

book_bp.route("/api/consultations", methods=["GET"])(jwt_required()(get_my_consultations))