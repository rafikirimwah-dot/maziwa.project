import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Sidebar = ({ open }) => {
    const loc = useLocation();

    return (
        <aside style={{
            width: open ? 220 : 64,
            transition: 'width 200ms',
            background: '#0d2b4f',
            color: 'white',
            minHeight: 'calc(100vh - 80px)',
            paddingTop: 20,
            boxSizing: 'border-box'
        }}>
            <nav style={{ display: 'flex', flexDirection: 'column', gap: 6, padding: 10 }}>
                <NavLink to="/dashboard" active={loc.pathname === '/dashboard'} open={open} label="Dashboard" />
                <NavLink to="/add" active={loc.pathname === '/add'} open={open} label="Add" />
            </nav>
        </aside>
    );
};

const NavLink = ({ to, label, active, open }) => (
    <Link to={to} style={{ textDecoration: 'none' }}>
        <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: 10,
            padding: '10px 12px',
            borderRadius: 8,
            background: active ? 'rgba(255,255,255,0.08)' : 'transparent',
            color: 'white'
        }}>
            <div style={{ width: 28, textAlign: 'center' }}>●</div>
            {open && <div style={{ fontSize: 14 }}>{label}</div>}
        </div>
    </Link>
);

export default Sidebar;
