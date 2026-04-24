from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.models import AppointmentType, Consultation
from app.extensions import db
from datetime import datetime

# -----------------------
# Get Appointment Types
# -----------------------
def get_appointment_types():
    types = AppointmentType.query.all()
    return jsonify({"appointment_types": [t.to_dict() for t in types]}), 200

# -----------------------
# Book Consultation
# -----------------------
def book_consultation():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    doctor_id = data.get("doctor_id")
    appointment_type_id = data.get("appointment_type_id")
    date_time_str = data.get("date_time")

    if not doctor_id or not appointment_type_id or not date_time_str:
        return jsonify({"msg": "doctor_id, appointment_type_id, date_time required"}), 400

    try:
        date_time = datetime.fromisoformat(date_time_str)
    except ValueError:
        return jsonify({"msg": "Invalid date_time format"}), 400

    consultation = Consultation(
        user_id=user_id,
        doctor_id=doctor_id,
        appointment_type_id=appointment_type_id,
        date_time=date_time,
        status="pending"
    )

    db.session.add(consultation)
    db.session.commit()

    return jsonify({"msg": "Consultation booked", "consultation": consultation.to_dict()}), 201