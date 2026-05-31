-- This script will clear any old sample data first to avoid errors
-- and then insert a fresh set.

-- Clear old data (optional, but good for a clean start)
-- Note: This will fail if no data exists, which is okay. You can ignore the error.
TRUNCATE TABLE doctor_availability, doctors RESTART IDENTITY CASCADE;

-- Insert sample doctors
-- The RESTART IDENTITY CASCADE above will ensure their IDs start from 1 again.
INSERT INTO doctors (name, specialty) VALUES
('Dr. Evelyn Reed', 'Cardiology'),
('Dr. Marcus Chen', 'Orthopedics'),
('Dr. Alice Johnson', 'Dermatology'),
('Dr. Ben Carter', 'General Medicine');

-- Insert sample availability for Dr. Reed (Cardiology, ID=1)
-- IMPORTANT: Make sure these dates are in the future!
INSERT INTO doctor_availability (doctor_id, start_time, end_time) VALUES
(1, '2025-10-08 09:00:00+00', '2025-10-08 09:30:00+00'),
(1, '2025-10-08 09:30:00+00', '2025-10-08 10:00:00+00'),
(1, '2025-10-08 10:00:00+00', '2025-10-08 10:30:00+00');

-- Insert sample availability for Dr. Chen (Orthopedics, ID=2)
-- IMPORTANT: Make sure these dates are in the future!
INSERT INTO doctor_availability (doctor_id, start_time, end_time) VALUES
(2, '2025-10-10 11:00:00+00', '2025-10-10 11:30:00+00'),
(2, '2025-10-10 11:30:00+00', '2025-10-10 12:00:00+00');

-- Insert sample availability for Dr. Johnson (Dermatology, ID=3)
-- IMPORTANT: Make sure these dates are in the future!
INSERT INTO doctor_availability (doctor_id, start_time, end_time) VALUES
(3, '2025-10-09 14:00:00+00', '2025-10-09 14:30:00+00'),
(3, '2025-10-09 14:30:00+00', '2025-10-09 15:00:00+00');

-- A message to confirm the script ran
SELECT 'Sample data for doctors and availability has been inserted successfully.' as status;