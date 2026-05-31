from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import jwt
from functools import wraps
from config import Config
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import ForeignKey

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
CORS(app)

# --- Database Models ---
# We use automap_base to reflect the tables we already created.
Base = declarative_base()

class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    specialty = db.Column(db.String(255), nullable=False)

class DoctorAvailability(db.Model):
    __tablename__ = 'doctor_availability'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    start_time = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    end_time = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    is_booked = db.Column(db.Boolean, default=False, nullable=False)

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    # We don't need a direct relationship to the 'users' table in this service's model,
    # as we are in a microservice architecture. We just store the ID.
    patient_id = db.Column(db.Integer, nullable=False) 
    availability_id = db.Column(db.Integer, db.ForeignKey('doctor_availability.id'), nullable=False)
    booking_time = db.Column(db.TIMESTAMP(timezone=True), default=db.func.current_timestamp())


# --- JWT Authentication Decorator ---
# This function will protect our routes
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            # Extract token from "Bearer <token>"
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # This is the key part: we use the shared secret to decode the token
            data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
            current_user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except Exception as e:
            return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 401
        
        # Pass the user ID to the decorated function
        return f(current_user_id, *args, **kwargs)
    return decorated

# --- API Routes ---

# Get a list of doctors, optionally filtered by specialty
@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    specialty = request.args.get('specialty')
    query = db.session.query(Doctor)
    if specialty:
        query = query.filter(Doctor.specialty.ilike(f"%{specialty}%"))
    
    doctors = query.all()
    return jsonify([{'id': d.id, 'name': d.name, 'specialty': d.specialty} for d in doctors])

# Get available slots for a specific doctor
@app.route('/api/doctors/<int:doctor_id>/availability', methods=['GET'])
def get_availability(doctor_id):
    available_slots = db.session.query(DoctorAvailability).filter_by(doctor_id=doctor_id, is_booked=False).all()
    return jsonify([{'id': slot.id, 'start_time': slot.start_time.isoformat(), 'end_time': slot.end_time.isoformat()} for slot in available_slots])

# Book a new appointment (Protected Route)
@app.route('/api/appointments', methods=['POST'])
@token_required
def book_appointment(current_user_id):
    data = request.get_json()
    availability_id = data.get('availability_id')

    if not availability_id:
        return jsonify({'error': 'availability_id is required'}), 400

    # Check if the slot is valid and not already booked
    slot = db.session.get(DoctorAvailability, availability_id)
    if not slot:
        return jsonify({'error': 'Availability slot not found'}), 404
    if slot.is_booked:
        return jsonify({'error': 'This time slot is already booked'}), 409 # Conflict

    # Mark the slot as booked
    slot.is_booked = True

    # Create the new appointment record
    new_appointment = Appointment(
        patient_id=current_user_id,
        availability_id=availability_id
    )
    
    db.session.add(new_appointment)
    db.session.commit()

    return jsonify({'message': 'Appointment booked successfully!', 'appointment_id': new_appointment.id}), 201

# Get appointments for the currently logged-in user (Protected Route)
@app.route('/api/appointments/me', methods=['GET'])
@token_required
def get_my_appointments(current_user_id):
    appointments = db.session.query(Appointment).filter_by(patient_id=current_user_id).all()
    
    results = []
    for appt in appointments:
        # For each appointment, find the details of the slot and the doctor
        slot = db.session.get(DoctorAvailability, appt.availability_id)
        doctor = db.session.get(Doctor, slot.doctor_id)
        results.append({
            'appointment_id': appt.id,
            'doctor_name': doctor.name,
            'specialty': doctor.specialty,
            'start_time': slot.start_time.isoformat(),
            'end_time': slot.end_time.isoformat(),
            'booked_at': appt.booking_time.isoformat()
        })

    return jsonify(results)

# --- Run the Server ---
if __name__ == '__main__':
    # Run on a new port
    app.run(debug=True, port=5003)