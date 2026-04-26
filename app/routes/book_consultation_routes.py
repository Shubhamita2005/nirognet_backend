from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.book_consultation_controller import (
    get_specialties,
    get_doctors,
    create_consultation,
    get_my_consultations,
)

book_bp = Blueprint("book_consultation", __name__)

# Public
book_bp.route("/api/specialties", methods=["GET"])(get_specialties)

# Auth required
book_bp.route(
    "/api/specialties/<int:specialty_id>/doctors",
    methods=["GET"]
)((get_doctors))
book_bp.route("/api/consultations", methods=["POST"])(jwt_required()(create_consultation))
book_bp.route("/api/consultations", methods=["GET"])(jwt_required()(get_my_consultations))