from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.services.book_consultation_services import (
    list_specialties,
    list_doctors_flat,
    book_consultation,
    list_user_consultations,
)
from datetime import datetime

# -----------------------
# Get all specialties
# -----------------------
def get_specialties():
    specialties = list_specialties()
    return jsonify({"specialties": specialties}), 200

# -----------------------
# Get doctors by specialty
# -----------------------
def get_doctors(specialty_id: int):
    doctors = list_doctors_flat(specialty_id)
    return jsonify({"doctors": doctors}), 200

# -----------------------
# Book a consultation
# -----------------------
def create_consultation():
    data = request.get_json() or {}
    user_id = int(get_jwt_identity())
    doctor_id = data.get("doctor_id")
    date_time_str = data.get("date_time")

    if not doctor_id or not date_time_str:
        return jsonify({"msg": "doctor_id and date_time required"}), 400

    try:
        date_time = datetime.fromisoformat(date_time_str)
    except ValueError:
        return jsonify({"msg": "Invalid date_time format"}), 400

    consultation, error = book_consultation(user_id, doctor_id, date_time)
    if error:
        return jsonify({"msg": error}), 400

    return jsonify(consultation), 201

# -----------------------
# Get user consultations
# -----------------------
def get_my_consultations():
    user_id = int(get_jwt_identity())
    consultations = list_user_consultations(user_id)
    return jsonify({"consultations": consultations}), 200