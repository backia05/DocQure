// src/context/AppContext.js
import React, { createContext, useState, useContext } from 'react';

// 1. Create the context
const AppContext = createContext();

// 2. Create a custom hook to easily use the context
export const useAppContext = () => {
    return useContext(AppContext);
};

// 3. Create the Provider component that will wrap our app
export const AppProvider = ({ children }) => {
    // This state is what we will share
    const [refreshAppointments, setRefreshAppointments] = useState(false);

    // This function will be called by SymptomChecker to trigger a refresh
    const triggerRefresh = () => {
        setRefreshAppointments(prev => !prev); // Toggle the value to trigger useEffect
    };

    const value = {
        refreshAppointments,
        triggerRefresh,
    };

    return (
        <AppContext.Provider value={value}>
            {children}
        </AppContext.Provider>
    );
};