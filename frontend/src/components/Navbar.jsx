import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Navbar = ({ onToggleSidebar }) => {
    const { user, logout, isAdmin } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <nav style={{
            background: 'linear-gradient(135deg, #1a4b8c, #2c6ab0)',
            padding: '10px 14px',
            color: 'white',
            boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
        }}>
            <div style={{
                maxWidth: '1400px',
                margin: '0 auto',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                gap: '10px'
            }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                    <button
                        onClick={onToggleSidebar}
                        style={{
                            background: 'transparent',
                            border: 'none',
                            color: 'white',
                            fontSize: 20,
                            cursor: 'pointer'
                        }}
                        aria-label="Toggle sidebar"
                    >
                        ☰
                    </button>
                    <h2 style={{ margin: 0, fontSize: '20px' }}>
                        <span style={{ color: '#ffd700' }}>MAZIWA</span>
                    </h2>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <span style={{ fontSize: '14px' }}>
                        {isAdmin() ? '👑 ' : '🚛 '}
                        {user?.username}
                        {isAdmin() && ' (Admin)'}
                    </span>

                    <Link to="/dashboard" style={linkStyle}>Dashboard</Link>
                    <Link to="/add" style={linkStyle}>Add Record</Link>

                    {isAdmin() && (
                        <Link to="/admin-panel" style={linkStyle}>Admin Panel</Link>
                    )}

                    <button
                        onClick={handleLogout}
                        style={{
                            background: 'rgba(255,255,255,0.2)',
                            border: '2px solid white',
                            color: 'white',
                            padding: '6px 18px',
                            borderRadius: '20px',
                            cursor: 'pointer',
                            fontSize: '14px',
                            fontWeight: '500'
                        }}
                    >
                        Logout
                    </button>
                </div>
            </div>
        </nav>
    );
};

const linkStyle = {
    color: 'white',
    textDecoration: 'none',
    padding: '5px 10px',
    borderRadius: '5px',
    transition: 'background 0.3s',
    fontSize: '14px'
};

export default Navbar;