-- Insert some sample availability for Dr. Marcus Chen (Orthopedics, assuming his ID is 2)
-- IMPORTANT: Make sure the dates are in the future!
INSERT INTO doctor_availability (doctor_id, start_time, end_time) VALUES
(2, '2025-10-10 11:00:00+00', '2025-10-10 11:30:00+00'),
(2, '2025-10-10 11:30:00+00', '2025-10-10 12:00:00+00'),
(2, '2025-10-10 12:00:00+00', '2025-10-10 12:30:00+00');