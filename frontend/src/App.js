// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link as RouterLink, Navigate } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Button, Container, Box } from '@mui/material';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';

// A simple placeholder for a home page
const HomePage = () => (
    <Container>
        <Typography variant="h4" component="h1" gutterBottom sx={{ mt: 4 }}>
            Welcome to DocQure
        </Typography>
        <Typography>
            Your intelligent solution for seamless hospital appointments. Please log in or register to continue.
        </Typography>
    </Container>
);

function App() {
    const isLoggedIn = !!localStorage.getItem('accessToken');

    const handleLogout = () => {
        localStorage.removeItem('accessToken');
        // We use window.location to force a full refresh to clear all state
        window.location.href = '/login';
    };

    return (
        <Router>
            <Box sx={{ flexGrow: 1 }}>
                <AppBar position="static">
                    <Toolbar>
                        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                            <Button color="inherit" component={RouterLink} to="/">DocQure</Button>
                        </Typography>
                        {!isLoggedIn ? (
                            <>
                                <Button color="inherit" component={RouterLink} to="/login">Login</Button>
                                <Button color="inherit" component={RouterLink} to="/register">Register</Button>
                            </>
                        ) : (
                            <>
                                <Button color="inherit" component={RouterLink} to="/dashboard">Dashboard</Button>
                                <Button color="inherit" onClick={handleLogout}>Logout</Button>
                            </>
                        )}
                    </Toolbar>
                </AppBar>
                <main>
                    <Routes>
                        <Route path="/" element={<HomePage />} />
                        <Route path="/login" element={isLoggedIn ? <Navigate to="/dashboard" /> : <LoginPage />} />
                        <Route path="/register" element={isLoggedIn ? <Navigate to="/dashboard" /> : <RegisterPage />} />
                        <Route path="/dashboard" element={!isLoggedIn ? <Navigate to="/login" /> : <DashboardPage />} />
                        <Route path="*" element={<Navigate to="/" />} />
                    </Routes>
                </main>
            </Box>
        </Router>
    );
}

export default App;