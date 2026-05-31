// src/components/MyAppointments.js
import React, { useState, useEffect } from 'react';
import { getMyAppointments, checkInToQueue } from '../services/api';
import { useAppContext } from '../context/AppContext'; // Import our custom hook
import { Box, Typography, List, ListItem, ListItemText, Button, CircularProgress, Alert } from '@mui/material';
import TodayIcon from '@mui/icons-material/Today';

function MyAppointments() {
    const { refreshAppointments } = useAppContext(); // Get the refresh state from context
    const [appointments, setAppointments] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');
    const [checkInSuccess, setCheckInSuccess] = useState('');

    const isToday = (someDate) => {
        const today = new Date();
        const date = new Date(someDate);
        return date.getDate() === today.getDate() &&
               date.getMonth() === today.getMonth() &&
               date.getFullYear() === today.getFullYear();
    };

    const handleCheckIn = async (appointmentId) => {
        setError('');
        setCheckInSuccess('');
        try {
            const response = await checkInToQueue(appointmentId);
            setCheckInSuccess(`Successfully checked in! Your token number is ${response.data.token_number}.`);
        } catch (err) {
             setError(err.response?.data?.message || 'Check-in failed.');
        }
    };

    useEffect(() => {
        const fetchAppointments = async () => {
            setIsLoading(true);
            try {
                const response = await getMyAppointments();
                setAppointments(response.data);
            } catch (err) {
                setError('Could not fetch appointments.');
            } finally {
                setIsLoading(false);
            }
        };
        fetchAppointments();
    }, [refreshAppointments]); // <<<--- THIS IS THE MAGIC!

    return (
        <Box>
            <Typography variant="h5" component="h2" gutterBottom>
                My Appointments
            </Typography>
            {isLoading && <CircularProgress />}
            {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
            {checkInSuccess && <Alert severity="success" sx={{ mb: 2 }}>{checkInSuccess}</Alert>}

            {!isLoading && appointments.length > 0 ? (
                <List>
                    {appointments.map(appt => (
                        <ListItem key={appt.appointment_id}>
                            <ListItemText
                                primary={`Dr. ${appt.doctor_name} (${appt.specialty})`}
                                secondary={`On ${new Date(appt.start_time).toLocaleDateString()} at ${new Date(appt.start_time).toLocaleTimeString()}`}
                            />
                            {isToday(appt.start_time) && (
                                <Button
                                    variant="contained"
                                    color="secondary"
                                    startIcon={<TodayIcon />}
                                    onClick={() => handleCheckIn(appt.appointment_id)}
                                >
                                    Check-In
                                </Button>
                            )}
                        </ListItem>
                    ))}
                </List>
            ) : (
                !isLoading && <Typography>You have no upcoming appointments.</Typography>
            )}
        </Box>
    );
}

export default MyAppointments;