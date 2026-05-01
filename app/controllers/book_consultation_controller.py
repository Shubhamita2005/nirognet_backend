from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.services.book_consultation_services import (
    list_specialties,
    list_doctors_flat,
    create_consultation,
    list_user_consultations,
    get_available_slots,
    update_consultation_type_service
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
def create_consultation_controller():
    data = request.get_json() or {}

    # 🔥 TEMP JWT BYPASS (for testing)
    try:
        user_id = int(get_jwt_identity())
    except:
        user_id = 2

    doctor_id = data.get("doctor_id")
    date_time_str = data.get("date_time")

    if not doctor_id  or not date_time_str:
        return jsonify({"msg": "doctor_id,  date_time required"}), 400

    try:
        date_time = datetime.fromisoformat(date_time_str)
    except ValueError:
        return jsonify({"msg": "Invalid date_time format"}), 400

    # 👇 CALL SERVICE LAYER
    consultation, error = create_consultation(
        user_id,
        doctor_id,
        date_time
    )

    if error:
        return jsonify({"msg": error}), 400

    return jsonify({
        "msg": "Consultation booked successfully",
        "consultation": consultation
    }), 201



# -----------------------
# Get user consultations
# -----------------------
def get_my_consultations():
    user_id = int(get_jwt_identity())
    consultations = list_user_consultations(user_id)
    return jsonify({"consultations": consultations}), 200
#------
#get doctor slots
#------
def get_doctor_slots(doctor_id: int):
    # 1. Get date from query params
    date_str = request.args.get("date")

    if not date_str:
        return jsonify({"msg": "date query param is required (YYYY-MM-DD)"}), 400

    # 2. Convert to date
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"msg": "Invalid date format. Use YYYY-MM-DD"}), 400

    # 3. Call service layer
    slots = get_available_slots(doctor_id, date)

    # 4. Return response
    return jsonify({"slots": slots}), 200

def update_consultation_type(consultation_id: int):
    data = request.get_json() or {}

    # 🔥 TEMP JWT BYPASS (same as before)
    try:
        user_id = int(get_jwt_identity())
    except:
        user_id = 1

    appointment_type_id = data.get("appointment_type_id")

    # ❗ validation
    if not appointment_type_id:
        return jsonify({"msg": "appointment_type_id is required"}), 400

    # 👇 call service layer
    consultation, error = update_consultation_type_service(
        consultation_id,
        user_id,
        appointment_type_id
    )

    if error:
        return jsonify({"msg": error}), 400

    return jsonify({
        "msg": "Appointment type updated successfully",
        "consultation": consultation
    }), 200