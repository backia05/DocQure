from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import jwt
from functools import wraps
from config import Config
from sqlalchemy import func, Date, cast
from datetime import date

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
CORS(app)

# --- Database Models ---
# Reflecting the tables needed for this service
class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, nullable=False)
    availability_id = db.Column(db.Integer, db.ForeignKey('doctor_availability.id'), nullable=False)

class DoctorAvailability(db.Model):
    __tablename__ = 'doctor_availability'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    start_time = db.Column(db.TIMESTAMP(timezone=True), nullable=False)

class Queue(db.Model):
    __tablename__ = 'queue'
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    token_number = db.Column(db.Integer, nullable=False)
    check_in_time = db.Column(db.TIMESTAMP(timezone=True), default=db.func.current_timestamp())
    status = db.Column(db.String(50), default='Waiting', nullable=False)


# --- JWT Authentication Decorator (Identical to scheduling-service) ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
            current_user_id = data['user_id']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user_id, *args, **kwargs)
    return decorated

# --- API Routes ---

@app.route('/api/queue/check-in', methods=['POST'])
@token_required
def check_in(current_user_id):
    data = request.get_json()
    appointment_id = data.get('appointment_id')

    if not appointment_id:
        return jsonify({'error': 'appointment_id is required'}), 400

    # 1. Verify this appointment belongs to the current user
    appointment = db.session.query(Appointment).filter_by(id=appointment_id, patient_id=current_user_id).first()
    if not appointment:
        return jsonify({'error': 'Appointment not found or does not belong to you'}), 404

    # 2. Check if the patient has already checked in for this appointment
    existing_queue_entry = db.session.query(Queue).filter_by(appointment_id=appointment_id).first()
    if existing_queue_entry:
        return jsonify({'message': 'You have already checked in.', 'token_number': existing_queue_entry.token_number}), 409

    # 3. Generate a new token number
    # This logic generates a token based on how many people have checked in today.
    today = date.today()
    # We need to join tables to find the doctor for this appointment to scope the queue
    slot = db.session.get(DoctorAvailability, appointment.availability_id)
    doctor_id_for_appt = slot.doctor_id
    
    # Count how many people have checked in for this specific doctor today
    count_for_doctor_today = db.session.query(Queue)\
        .join(Appointment, Queue.appointment_id == Appointment.id)\
        .join(DoctorAvailability, Appointment.availability_id == DoctorAvailability.id)\
        .filter(DoctorAvailability.doctor_id == doctor_id_for_appt)\
        .filter(cast(Queue.check_in_time, Date) == today).count()

    new_token_number = count_for_doctor_today + 1

    # 4. Create the new queue entry
    new_queue_entry = Queue(
        appointment_id=appointment_id,
        token_number=new_token_number
    )
    db.session.add(new_queue_entry)
    db.session.commit()

    return jsonify({
        'message': 'Check-in successful!',
        'token_number': new_token_number,
        'queue_id': new_queue_entry.id
    }), 201


@app.route('/api/queue/status/<int:doctor_id>', methods=['GET'])
def get_queue_status(doctor_id):
    # This is a public route anyone can see (e.g., on a hospital display)
    today = date.today()
    
    # Find all queue entries for a specific doctor for today, ordered by token number
    queue_today = db.session.query(Queue)\
        .join(Appointment, Queue.appointment_id == Appointment.id)\
        .join(DoctorAvailability, Appointment.availability_id == DoctorAvailability.id)\
        .filter(DoctorAvailability.doctor_id == doctor_id)\
        .filter(cast(Queue.check_in_time, Date) == today)\
        .order_by(Queue.token_number).all()
        
    # Find who is currently being seen
    current_consultation = next((q for q in queue_today if q.status == 'In Consultation'), None)
    
    # Calculate approximate waiting time (e.g., 15 minutes per patient)
    waiting_patients = [q for q in queue_today if q.status == 'Waiting']
    estimated_wait_time_minutes = len(waiting_patients) * 15 # Simple estimation

    return jsonify({
        'doctor_id': doctor_id,
        'current_token_in_consultation': current_consultation.token_number if current_consultation else None,
        'total_in_queue': len(queue_today),
        'estimated_wait_time_minutes': estimated_wait_time_minutes,
        'queue_list': [
            {'token': q.token_number, 'status': q.status} for q in queue_today
        ]
    })

# --- Run the Server ---
if __name__ == '__main__':
    # Run on yet another new port
    app.run(debug=True, port=5004)