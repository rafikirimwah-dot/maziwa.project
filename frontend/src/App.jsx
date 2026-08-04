import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './contexts/AuthContext';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import RecordList from './components/Recordlist';
import RecordForm from './components/Recordform';
import Login from './components/login';

const ProtectedRoute = ({ children }) => {
    const { isAuthenticated, loading } = useAuth();
    
    if (loading) return <div style={loadingStyle}>Loading...</div>;
    
    if (!isAuthenticated) {
        return <Navigate to="/login" />;
    }
    
    return children;
};

const AppContent = () => {
    const { isAuthenticated } = useAuth();
    const [sidebarOpen, setSidebarOpen] = React.useState(true);

    return (
        <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
            <div style={appStyle}>
                {isAuthenticated && <Navbar onToggleSidebar={() => setSidebarOpen(s => !s)} />}
                <div style={layoutStyle}>
                    {isAuthenticated && <Sidebar open={sidebarOpen} />}
                    <main style={mainStyle}>
                        <Routes>
                        <Route path="/login" element={<Login />} />
                        <Route path="/" element={<Navigate to="/dashboard" />} />
                        <Route path="/dashboard" element={
                            <ProtectedRoute>
                                <RecordList />
                            </ProtectedRoute>
                        } />
                        <Route path="/add" element={
                            <ProtectedRoute>
                                <RecordForm />
                            </ProtectedRoute>
                        } />
                        <Route path="/edit/:id" element={
                            <ProtectedRoute>
                                <RecordForm />
                            </ProtectedRoute>
                        } />
                        <Route path="/detail/:id" element={
                            <ProtectedRoute>
                                <div style={cardStyle}>
                                    <h3>📄 Record Details</h3>
                                    <p>Select "Dashboard" to view all records</p>
                                    <button
                                        onClick={() => window.location.href = '/dashboard'}
                                        style={buttonStyle}
                                    >
                                        Back to Dashboard
                                    </button>
                                </div>
                            </ProtectedRoute>
                        } />
                    </Routes>
                    </main>
                </div>
                {isAuthenticated && (
                    <footer style={footerStyle}>
                        <p style={{ margin: 0 }}>MAZIWA RIGHTS AND REGULATIONS RESERVED</p>
                        <p style={{ margin: 0, opacity: 0.7, fontSize: '12px' }}>
                            © 2024 MAZIWA Co. All rights reserved.
                        </p>
                    </footer>
                )}
            </div>
        </Router>
    );
};

// Styles
const appStyle = {
    minHeight: '100vh',
    background: '#e8f0fe',
    display: 'flex',
    flexDirection: 'column'
};

const layoutStyle = {
    display: 'flex',
    flex: 1,
    minHeight: 'calc(100vh - 80px)'
};

const mainStyle = {
    flex: 1,
    padding: '20px',
    width: '100%',
    boxSizing: 'border-box'
};

const footerStyle = {
    background: 'linear-gradient(135deg, #0d2b4f, #1a4b8c)',
    color: 'white',
    padding: '20px',
    textAlign: 'center'
};

const loadingStyle = {
    textAlign: 'center',
    padding: '50px'
};

const cardStyle = {
    background: 'white',
    borderRadius: '15px',
    padding: '30px',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
    textAlign: 'center'
};

const buttonStyle = {
    padding: '10px 25px',
    background: 'linear-gradient(135deg, #1a4b8c, #2c6ab0)',
    color: 'white',
    border: 'none',
    borderRadius: '25px',
    cursor: 'pointer',
    marginTop: '15px'
};

function App() {
    return <AppContent />;
}

export default App;