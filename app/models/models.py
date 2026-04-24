from app.extensions import db  #Imports the SQLAlchemy database instance (db), allows to create database tables, define models, run queries, save data.
from werkzeug.security import generate_password_hash, check_password_hash # imports generate_password_hash (to securely hash passwords before storing them) and check_password_hash (to verify a password against the stored hash) from Werkzeug
from datetime import datetime

# =========================
# User Model (UNCHANGED LOGIC)
# =========================
class User(db.Model): #This creates a database model, SQLAlchemy will create a table named user.
    
    #These lines define database fields for a user model—id as the primary key, email as a unique required field, and password_hash to securely store the user's password hash
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    # Profile fields
    #These lines define optional user profile fields in the database such as name (default “Guest”), age, gender, contact, and address.
    name = db.Column(db.String(150), default="Guest")
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(50), nullable=True)
    contact = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(300), nullable=True)

    # Health Info
    #These lines define optional database fields to store the user's blood group and blood pressure information.
    blood_group = db.Column(db.String(10), nullable=True)
    blood_pressure = db.Column(db.String(50), nullable=True)

    # Preferences
    #This line creates a database column to store the user's language preference, with "English" set as the default value.
    language = db.Column(db.String(50), default="English")

    # ---------------------
    # Auth helpers
    # ---------------------
    def set_password(self, password: str): #Method to set a user password securely, self refers to the current user object.
        self.password_hash = generate_password_hash(password) #hashes the user's password using generate_password_hash and stores it in self.password_hash for secure storage

    def check_password(self, password: str) -> bool: #Used during login
        return check_password_hash(self.password_hash, password) # checks whether the given password matches the stored hashed password and returns True or False

    def to_dict(self): #converts a User object → dictionary, useful when sending API response
        return { #returns a dictionary containing the user's details 
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "contact": self.contact,
            "address": self.address,
            "blood_group": self.blood_group,
            "blood_pressure": self.blood_pressure,
            "language": self.language,
        }


# =========================
# Hospital Model (NEW)
# =========================
class Hospital(db.Model): #Creates a hospital table.
    id = db.Column(db.Integer, primary_key=True) #Unique hospital identifier.
    name = db.Column(db.String(200), nullable=False) #Hospital name.
    distance = db.Column(db.String(50), nullable=True) #Distance of the hospital from the user.
    doctors = db.Column(db.Integer, nullable=True) #Number of doctors present in the hospital.
    beds = db.Column(db.String(100), nullable=True) #Beds available in the hospital.
    ventilators = db.Column(db.String(100), nullable=True) #Ventilators available.
    blood = db.Column(db.String(100), nullable=True) #Blood Stock.

    def to_dict(self): #Converts hospital object → JSON friendly dictionary.
        #Returned dictionary.
        return {
            "name": self.name,
            "distance": self.distance,
            "doctors": self.doctors,
            "beds": self.beds,
            "ventilators": self.ventilators,
            "blood": self.blood,
        }


# =========================
# Seed Data (OPTIONAL, SAFE)
# =========================
def seed_hospitals(): #This function inserts default hospital data into the database, used when the database is empty.
    #It only inserts hospitals if none exist, so it won't duplicate data.
    """
    Seed hospital data only if table is empty.
    Safe to call multiple times.
    """
    #Check if any hospital already exists.
    if Hospital.query.first():
        return

    #creates a list of Hospital objects with details like name, distance, number of doctors, beds, ventilators, and blood stock
    hospitals = [
        Hospital(
            name="City General Hospital",
            distance="0.8 km",
            doctors=45,
            beds="120 (ICU: 25, Emergency: 30)",
            ventilators="15 (Available)",
            blood="Full Stock",
        ),
        Hospital(
            name="Metro Medical Center",
            distance="1.2 km",
            doctors=62,
            beds="180 (ICU: 35, Emergency: 45)",
            ventilators="22 (Available)",
            blood="Limited Stock",
        ),
        Hospital(
            name="Regional Health Institute",
            distance="2.1 km",
            doctors=38,
            beds="95 (ICU: 18, Emergency: 20)",
            ventilators="12 (Available)",
            blood="Full Stock",
        ),
    ]

    db.session.add_all(hospitals) #Adds all hospital objects to the database session.
    db.session.commit() #Actually writes the data into the database.



# =========================
# Specialty Model
# =========================
class Specialty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name}


# =========================
# Doctor Model
# =========================
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    specialty_id = db.Column(db.Integer, db.ForeignKey("specialty.id"))
    specialty = db.relationship("Specialty", backref="doctors")
    available = db.Column(db.Boolean, default=True)
    contact = db.Column(db.String(50), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "specialty": self.specialty.name if self.specialty else None,
            "available": self.available,
            "contact": self.contact,
        }


# =========================
# Consultation Model
# =========================
class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)  # Can link to User table if exists
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="pending")  # pending, confirmed, completed

    doctor = db.relationship("Doctor", backref="consultations")

    def to_dict(self):
        return {
            "id": self.id,
            "doctor": self.doctor.to_dict(),
            "user_id": self.user_id,
            "date_time": self.date_time.isoformat(),
            "status": self.status,
        }

       

# ----------------------
# Appointment Type
# ----------------------
class AppointmentType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # Online / Offline
    description = db.Column(db.String(200), nullable=True)
    icon = db.Column(db.String(50), nullable=True)   # Store icon name or identifier

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "icon": self.icon
        }

# ----------------------
# Consultation Booking
# ----------------------
class Consultation(db.Model):
    __table_args__ = {'extend_existing': True}  # <-- add this line
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    doctor_id = db.Column(db.Integer, nullable=False)
    appointment_type_id = db.Column(db.Integer, db.ForeignKey('appointment_type.id'), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default="pending")  # pending / confirmed / completed

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "doctor_id": self.doctor_id,
            "appointment_type_id": self.appointment_type_id,
            "date_time": self.date_time.isoformat(),
            "status": self.status
        }