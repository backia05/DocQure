import axios from 'axios';

// --- Base URLs for our services ---
const IDENTITY_SERVICE_URL = 'http://localhost:5001/api';
const AI_TRIAGE_SERVICE_URL = 'http://localhost:5002/api';
const SCHEDULING_SERVICE_URL = 'http://localhost:5003/api';
const QUEUE_SERVICE_URL = 'http://localhost:5004/api';

// --- Helper to get the auth token from localStorage ---
const getAuthHeader = () => {
    const token = localStorage.getItem('accessToken');
    return token ? { Authorization: `Bearer ${token}` } : {};
};

// --- Identity Service Methods ---
export const registerUser = (userData) => {
    return axios.post(`${IDENTITY_SERVICE_URL}/register`, userData);
};

export const loginUser = (credentials) => {
    return axios.post(`${IDENTITY_SERVICE_URL}/login`, credentials);
};

// --- AI Triage Service Methods ---
export const getSymptomPrediction = (symptoms) => {
    return axios.post(`${AI_TRIAGE_SERVICE_URL}/predict`, { symptoms });
};

// --- Scheduling Service Methods ---
export const getDoctorsBySpecialty = (specialty) => {
    return axios.get(`${SCHEDULING_SERVICE_URL}/doctors?specialty=${specialty}`);
};

export const getDoctorAvailability = (doctorId) => {
    return axios.get(`${SCHEDULING_SERVICE_URL}/doctors/${doctorId}/availability`);
};

export const bookAppointment = (availabilityId) => {
    return axios.post(`${SCHEDULING_SERVICE_URL}/appointments`, { availability_id: availabilityId }, { headers: getAuthHeader() });
};

export const getMyAppointments = () => {
    return axios.get(`${SCHEDULING_SERVICE_URL}/appointments/me`, { headers: getAuthHeader() });
};

// --- Queue Management Service Methods ---
export const checkInToQueue = (appointmentId) => {
    return axios.post(`${QUEUE_SERVICE_URL}/queue/check-in`, { appointment_id: appointmentId }, { headers: getAuthHeader() });
};

export const getQueueStatus = (doctorId) => {
    return axios.get(`${QUEUE_SERVICE_URL}/queue/status/${doctorId}`);
};