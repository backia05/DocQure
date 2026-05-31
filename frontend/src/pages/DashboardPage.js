// src/pages/DashboardPage.js
import React from 'react';
import { Container, Grid, Typography, Paper } from '@mui/material';
import SymptomChecker from '../components/SymptomChecker';
import MyAppointments from '../components/MyAppointments';

function DashboardPage() {
    // Note: The auth check is now handled in App.js, so we can simplify this page.
    return (
        <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <Typography variant="h4" component="h1" gutterBottom>
                Patient Dashboard
            </Typography>
            <Grid container spacing={3}>
                {/* Symptom Checker and Booking */}
                <Grid item xs={12} md={7} lg={8}>
                    <Paper>
                        <SymptomChecker />
                    </Paper>
                </Grid>
                {/* My Appointments */}
                <Grid item xs={12} md={5} lg={4}>
                    <Paper>
                        <MyAppointments />
                    </Paper>
                </Grid>
            </Grid>
        </Container>
    );
}

export default DashboardPage;