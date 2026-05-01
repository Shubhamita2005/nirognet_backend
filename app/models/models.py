from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# =========================
# User
# =========================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    name = db.Column(db.String(150), default="Guest")
    age = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    contact = db.Column(db.String(50))
    address = db.Column(db.String(300))

    blood_group = db.Column(db.String(10))
    blood_pressure = db.Column(db.String(50))

    language = db.Column(db.String(50), default="English")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name
        }


# =========================
# Hospital
# =========================
class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    distance = db.Column(db.String(50))
    doctors = db.Column(db.Integer)
    beds = db.Column(db.String(100))
    ventilators = db.Column(db.String(100))
    blood = db.Column(db.String(100))

    def to_dict(self):
        return {"id": self.id, "name": self.name}


# =========================
# Specialty
# =========================
class Specialty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name}


# =========================
# Doctor
# =========================
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)

    specialty_id = db.Column(db.Integer, db.ForeignKey("specialty.id"))
    specialty = db.relationship("Specialty", backref="doctors")

    available = db.Column(db.Boolean, default=True)
    contact = db.Column(db.String(50))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "specialty": self.specialty.name if self.specialty else None
        }


# =========================
# Doctor Schedule
# =========================
class DoctorSchedule(db.Model):
    __tablename__ = "doctor_schedule"

    id = db.Column(db.Integer, primary_key=True)

    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey("hospital.id"), nullable=False)

    day_of_week = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    doctor = db.relationship("Doctor", backref="schedules")
    hospital = db.relationship("Hospital", backref="schedules")


# =========================
# Appointment Type
# =========================
class AppointmentType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    icon = db.Column(db.String(50))


# =========================
# Consultation (IMPORTANT)
# =========================
class Consultation(db.Model):
    __table_args__ = (
        db.UniqueConstraint('doctor_id', 'date_time', name='unique_slot'),
    )

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"), nullable=False)
    appointment_type_id = db.Column(db.Integer, db.ForeignKey("appointment_type.id"), nullable=True)

    date_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default="pending")

    doctor = db.relationship("Doctor", backref="consultations")
    user = db.relationship("User")


# =========================
# Medicine
# =========================
class Medicine(db.Model):
    __tablename__ = "medicines"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)