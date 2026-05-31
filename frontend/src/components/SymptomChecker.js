// src/components/SymptomChecker.js
import React, { useState } from 'react';
import { getSymptomPrediction, getDoctorsBySpecialty, getDoctorAvailability, bookAppointment } from '../services/api';
import { useAppContext } from '../context/AppContext'; // Import our custom hook
import { Box, TextField, Button, Typography, CircularProgress, Alert, List, ListItem, ListItemText, Divider } from '@mui/material';
import EventAvailableIcon from '@mui/icons-material/EventAvailable';
import BookOnlineIcon from '@mui/icons-material/BookOnline';

function SymptomChecker() {
    const { triggerRefresh } = useAppContext(); // Get the trigger function from context
    const [symptoms, setSymptoms] = useState('');
    const [recommendation, setRecommendation] = useState(null);
    const [doctors, setDoctors] = useState([]);
    const [availability, setAvailability] = useState([]);
    const [selectedDoctor, setSelectedDoctor] = useState(null);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [isBooking, setIsBooking] = useState(false);

    const handleSymptomSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');
        setSuccess('');
        setRecommendation(null);
        setDoctors([]);
        setAvailability([]);
        setSelectedDoctor(null);
        try {
            const response = await getSymptomPrediction(symptoms);
            const specialty = response.data.recommended_department;
            setRecommendation(specialty);
            const doctorsResponse = await getDoctorsBySpecialty(specialty);
            setDoctors(doctorsResponse.data);
        } catch (err) {
            setError('Could not get recommendation. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleViewSlots = async (doctor) => {
        setSuccess('');
        setSelectedDoctor(doctor);
        setAvailability([]); // Clear previous slots
        try {
            const response = await getDoctorAvailability(doctor.id);
            setAvailability(response.data);
        } catch (err) {
            setError('Could not fetch doctor availability.');
        }
    };

    const handleBookSlot = async (slotId) => {
        setIsBooking(true);
        try {
            await bookAppointment(slotId);
            setSuccess(`Appointment booked successfully!`);
            triggerRefresh(); // <<<--- THIS IS THE MAGIC!
            // Clear the availability for the booked doctor
            setAvailability([]);
            setSelectedDoctor(null);
        } catch (err) {
            setError(err.response?.data?.error || 'Failed to book appointment.');
        } finally {
            setIsBooking(false);
        }
    };

    return (
        <Box>
            <Typography variant="h5" component="h2" gutterBottom>
                Symptom Checker & Booking
            </Typography>
            <Box component="form" onSubmit={handleSymptomSubmit}>
                <TextField
                    fullWidth
                    multiline
                    rows={4}
                    value={symptoms}
                    onChange={(e) => setSymptoms(e.target.value)}
                    label="Describe your symptoms..."
                    required
                />
                <Button
                    type="submit"
                    variant="contained"
                    sx={{ mt: 2 }}
                    disabled={isLoading}
                    startIcon={isLoading ? <CircularProgress size={20} color="inherit" /> : null}
                >
                    {isLoading ? 'Getting Recommendation...' : 'Get Recommendation'}
                </Button>
            </Box>

            {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
            {success && <Alert severity="success" sx={{ mt: 2 }}>{success}</Alert>}

            {recommendation && (
                <Box sx={{ mt: 3 }}>
                    <Typography variant="h6">Recommended Department: {recommendation}</Typography>
                    <Typography sx={{ mt: 1 }}>Doctors Available:</Typography>
                    <List>
                        {doctors.map(doctor => (
                            <ListItem key={doctor.id} secondaryAction={
                                <Button variant="outlined" startIcon={<EventAvailableIcon />} onClick={() => handleViewSlots(doctor)}>
                                    View Slots
                                </Button>
                            }>
                                <ListItemText primary={doctor.name} secondary={doctor.specialty} />
                            </ListItem>
                        ))}
                    </List>
                </Box>
            )}

            {selectedDoctor && (
                <Box sx={{ mt: 2 }}>
                    <Divider sx={{ mb: 2 }} />
                    <Typography>Available slots for {selectedDoctor.name}:</Typography>
                    {availability.length > 0 ? (
                         <List>
                            {availability.map(slot => (
                                <ListItem key={slot.id} secondaryAction={
                                    <Button
                                        variant="contained"
                                        color="secondary"
                                        startIcon={isBooking ? <CircularProgress size={20} color="inherit" /> : <BookOnlineIcon />}
                                        onClick={() => handleBookSlot(slot.id)}
                                        disabled={isBooking}
                                    >
                                        Book Now
                                    </Button>
                                }>
                                    <ListItemText primary={new Date(slot.start_time).toLocaleString()} />
                                </ListItem>
                            ))}
                        </List>
                    ) : <Typography sx={{mt: 1, fontStyle: 'italic'}}>No available slots found for this doctor.</Typography>}
                </Box>
            )}
        </Box>
    );
}

export default SymptomChecker;