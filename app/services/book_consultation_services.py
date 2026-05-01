from app.models import Specialty, Doctor, DoctorSchedule, Hospital, Consultation
from app.extensions import db
from datetime import datetime, timedelta, date as dt_date

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
def get_available_slots(doctor_id: int, date: dt_date):
    # 1. Get day name (Monday, Tuesday...)
    day_name = date.strftime("%A")

    # 2. Get doctor's schedule for that day
    schedules = DoctorSchedule.query.filter_by(
        doctor_id=doctor_id,
        day_of_week=day_name
    ).all()

    if not schedules:
        return []  # Doctor not available that day

    all_slots = []

    # 3. Generate 15-min slots for each schedule
    for schedule in schedules:
        start = schedule.start_time
        end = schedule.end_time

        current = datetime.combine(date, start)
        end_dt = datetime.combine(date, end)

        while current < end_dt:
            next_time = current + timedelta(minutes=15)

            all_slots.append({
                "time": current.strftime("%H:%M"),
                "available": True  # default
            })

            current = next_time

    # 4. Get already booked slots
    booked = Consultation.query.filter(
        Consultation.doctor_id == doctor_id,
        db.func.date(Consultation.date_time) == date
    ).all()

    booked_times = {
        c.date_time.strftime("%H:%M") for c in booked
    }

    # 5. Mark unavailable slots
    for slot in all_slots:
        if slot["time"] in booked_times:
            slot["available"] = False

    return all_slots

def create_consultation(user_id, doctor_id, date_time):
    """
    Creates a consultation (booking a slot)

    Returns:
        (consultation_dict, None) on success
        (None, error_message) on failure
    """

    # 🔥 STEP 1: Check if slot already booked
    existing = Consultation.query.filter_by(
        doctor_id=doctor_id,
        date_time=date_time
    ).first()

    if existing:
        return None, "Slot already booked"

    # 🔥 STEP 2: Create new consultation
    consultation = Consultation(
        user_id=user_id,
        doctor_id=doctor_id,
        date_time=date_time,
        status="pending"
    )

    # 🔥 STEP 3: Save to DB
    db.session.add(consultation)
    db.session.commit()

    # 🔥 STEP 4: Return response
    return {
        "id": consultation.id,
        "doctor_id": consultation.doctor_id,
        "user_id": consultation.user_id,
        "appointment_type_id": consultation.appointment_type_id,
        "date_time": consultation.date_time.isoformat(),
        "status": consultation.status
    }, None
def update_consultation_type_service(consultation_id, user_id, appointment_type_id):

    # 1. Check consultation exists
    consultation = Consultation.query.get(consultation_id)
    if not consultation:
        return None, "Consultation not found"

    # 2. (IMPORTANT) Check ownership
    if consultation.user_id != user_id:
        return None, "Unauthorized"

    # 3. Validate appointment type (since only 2 allowed)
    if appointment_type_id not in [1, 2]:
        return None, "Invalid appointment type"

    # 4. Update
    consultation.appointment_type_id = appointment_type_id

    # 5. Save
    db.session.commit()

    # 6. Return updated data
    return {
        "id": consultation.id,
        "doctor_id": consultation.doctor_id,
        "user_id": consultation.user_id,
        "appointment_type_id": consultation.appointment_type_id,
        "date_time": consultation.date_time.isoformat(),
        "status": consultation.status
    }, None