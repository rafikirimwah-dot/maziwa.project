import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Navbar = () => {
    const { user, logout, isAdmin } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <nav style={{
            background: 'linear-gradient(135deg, #1a4b8c, #2c6ab0)',
            padding: '15px 20px',
            color: 'white',
            boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
        }}>
            <div style={{
                maxWidth: '1200px',
                margin: '0 auto',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                flexWrap: 'wrap',
                gap: '10px'
            }}>
                <div>
                    <h2 style={{ margin: 0, fontSize: '24px' }}>
                        <span style={{ color: '#ffd700' }}>MAZIWA</span> CO. FRESH
                    </h2>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '15px', flexWrap: 'wrap' }}>
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
                            padding: '5px 20px',
                            borderRadius: '20px',
                            cursor: 'pointer',
                            fontSize: '14px',
                            fontWeight: '500',
                            transition: 'all 0.3s'
                        }}
                        onMouseEnter={(e) => {
                            e.target.style.background = 'white';
                            e.target.style.color = '#1a4b8c';
                        }}
                        onMouseLeave={(e) => {
                            e.target.style.background = 'rgba(255,255,255,0.2)';
                            e.target.style.color = 'white';
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