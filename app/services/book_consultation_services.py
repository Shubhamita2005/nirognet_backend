from app.models import Specialty, Doctor, DoctorSchedule, Hospital
from app.extensions import db
from datetime import datetime

# -----------------------
# List all specialties
# -----------------------
def list_specialties():
    return [s.to_dict() for s in Specialty.query.all()]

# -----------------------
# List doctors by specialty
# -----------------------
def list_doctors_by_specialty(specialty_id: int):
    doctors = Doctor.query.filter_by(specialty_id=specialty_id, available=True).all()
    return [d.to_dict() for d in doctors]

# -----------------------
# Book a consultation
# -----------------------
def book_consultation(user_id: int, doctor_id: int, date_time: datetime):
    doctor = Doctor.query.get(doctor_id)
    if not doctor or not doctor.available:
        return None, "Doctor unavailable"

    consultation = Consultation(
        doctor_id=doctor_id,
        user_id=user_id,
        date_time=date_time,
        status="pending"
    )
    db.session.add(consultation)
    db.session.commit()
    return consultation.to_dict(), None

# -----------------------
# List user consultations
# -----------------------
def list_user_consultations(user_id: int):
    consultations = Consultation.query.filter_by(user_id=user_id).all()
    return [c.to_dict() for c in consultations]


def list_doctors_flat(specialty_id: int):
    results = (
        db.session.query(Doctor, DoctorSchedule, Hospital)
        .join(DoctorSchedule, Doctor.id == DoctorSchedule.doctor_id)
        .join(Hospital, DoctorSchedule.hospital_id == Hospital.id)
        .filter(Doctor.specialty_id == specialty_id, Doctor.available == True)
        .all()
    )

    output = []

    for doctor, schedule, hospital in results:
        output.append({
            "doctor_id": doctor.id,
            "doctor_name": doctor.name,
            "day": schedule.day_of_week,
            "start_time": str(schedule.start_time),
            "end_time": str(schedule.end_time),
            "hospital": hospital.name
        })

    return output