-- Table to store doctor information
CREATE TABLE doctors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    specialty VARCHAR(255) NOT NULL -- This will match the 'department' from the AI service
);

-- Table to store doctor's available time slots
CREATE TABLE doctor_availability (
    id SERIAL PRIMARY KEY,
    doctor_id INTEGER NOT NULL REFERENCES doctors(id),
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE NOT NULL,
    is_booked BOOLEAN DEFAULT FALSE NOT NULL
);

-- Table to store the actual booked appointments, linking users and doctors
CREATE TABLE appointments (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES users(id), -- This connects to our 'users' table
    availability_id INTEGER NOT NULL REFERENCES doctor_availability(id),
    booking_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Insert some sample doctors
INSERT INTO doctors (name, specialty) VALUES
('Dr. Evelyn Reed', 'Cardiology'),
('Dr. Marcus Chen', 'Orthopedics'),
('Dr. Alice Johnson', 'Dermatology'),
('Dr. Ben Carter', 'General Medicine');

-- Insert some sample availability for Dr. Reed (Cardiology)
-- NOTE: Adjust the dates to be in the future from when you are testing
INSERT INTO doctor_availability (doctor_id, start_time, end_time) VALUES
(1, '2025-10-08 09:00:00+00', '2025-10-08 09:30:00+00'),
(1, '2025-10-08 09:30:00+00', '2025-10-08 10:00:00+00'),
(1, '2025-10-08 10:00:00+00', '2025-10-08 10:30:00+00');

-- Insert some sample availability for Dr. Johnson (Dermatology)
INSERT INTO doctor_availability (doctor_id, start_time, end_time) VALUES
(3, '2025-10-09 14:00:00+00', '2025-10-09 14:30:00+00'),
(3, '2025-10-09 14:30:00+00', '2025-10-09 15:00:00+00');