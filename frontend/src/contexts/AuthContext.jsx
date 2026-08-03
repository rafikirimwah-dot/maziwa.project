import React, { createContext, useContext, useEffect, useState } from 'react';
import api from '../api/axiosConfig';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const token = localStorage.getItem('access_token');
        if (token) {
            fetchCurrentUser();
        } else {
            setLoading(false);
        }
    }, []);

    const fetchCurrentUser = async () => {
        try {
            const token = localStorage.getItem('access_token');
            if (token) {
                api.defaults.headers.common.Authorization = `Bearer ${token}`;
            }
            const response = await api.get('/api/current-user/');
            setUser(response.data);
        } catch (error) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            delete api.defaults.headers.common.Authorization;
            setUser(null);
        } finally {
            setLoading(false);
        }
    };

    const login = async (username, password) => {
        try {
            const response = await api.post('/api/token/', { username, password });
            const { access, refresh } = response.data;
            localStorage.setItem('access_token', access);
            localStorage.setItem('refresh_token', refresh);
            api.defaults.headers.common.Authorization = `Bearer ${access}`;
            const userResponse = await api.get('/api/current-user/');
            setUser(userResponse.data);
            return { success: true };
        } catch (error) {
            return {
                success: false,
                error: error.response?.data?.detail || 'Login failed',
            };
        }
    };

    const logout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setUser(null);
    };

    const isAdmin = () => user?.is_staff || user?.is_superuser;
    const isTruckA = () => user?.username === 'truck_a';
    const isTruckB = () => user?.username === 'truck_b';

    const value = {
        user,
        login,
        logout,
        isAdmin,
        isTruckA,
        isTruckB,
        loading,
        isAuthenticated: !!user,
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
