-- Table to manage the daily patient queue
CREATE TABLE queue (
    id SERIAL PRIMARY KEY,
    appointment_id INTEGER NOT NULL REFERENCES appointments(id),
    token_number INTEGER NOT NULL,
    check_in_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'Waiting' NOT NULL -- e.g., Waiting, In Consultation, Completed
);