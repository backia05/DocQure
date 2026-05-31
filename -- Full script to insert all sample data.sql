-- Full script to insert all sample data for testing

-- Insert sample doctors
INSERT INTO doctors (name, specialty) VALUES
('Dr. Evelyn Reed', 'Cardiology'),
('Dr. Marcus Chen', 'Orthopedics'),
('Dr. Alice Johnson', 'Dermatology'),
('Dr. Ben Carter', 'General Medicine');

-- Insert sample availability for Dr. Reed (Cardiology, ID=1)
-- IMPORTANT: Make sure these dates are in the future!
INSERT INTO doctor_availability (doctor_id, start_time, end_time) VALUES
(1, '2025-10-08 09:00:00+00', '2025-10-08 09:30:00+00'),
(1, '2025-10-08 09:30:00+00', '2025-10-08 10:00:00+00');

-- Insert sample availability for Dr. Chen (Orthopedics, ID=2)
-- IMPORTANT: Make sure these dates are in the future!
INSERT INTO doctor_availability (doctor_id, start_time, end_time) VALUES
(2, '2025-10-10 11:00:00+00', '2025-10-10 11:30:00+00'),
(2, '2025-10-10 11:30:00+00', '2025-10-10 12:00:00+00');

-- Insert sample availability for Dr. Johnson (Dermatology, ID=3)
-- IMPORTANT: Make sure these dates are in the future!
INSERT INTO doctor_availability (doctor_id, start_time, end_time) VALUES
(3, '2025-10-09 14:00:00+00', '2025-10-09 14:30:00+00');

-- A message to confirm the script ran
SELECT 'All sample data has been inserted successfully.' as status;