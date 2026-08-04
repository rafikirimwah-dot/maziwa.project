import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/axiosConfig';
import { useAuth } from '../contexts/AuthContext';

const RecordList = () => {
    const [records, setRecords] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const { isAdmin, user } = useAuth();

    useEffect(() => {
        fetchRecords();
    }, []);

    const fetchRecords = async () => {
        try {
            setLoading(true);
            const response = await api.get('/api/milk-records/');
            console.debug('GET /api/milk-records/ response:', response);
            const items = response.data?.results || response.data || [];
            console.debug('parsed items length:', items.length);
            setRecords(items);
            setError(null);
        } catch (err) {
            setError('Failed to load records');
            console.error('fetchRecords error:', err?.response || err);
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (id) => {
        if (window.confirm('Delete this record?')) {
            try {
                await api.delete(`/api/milk-records/${id}/`);
                setRecords(records.filter(r => r.id !== id));
            } catch (err) {
                if (err.response?.status === 403) {
                    setError('You don\'t have permission to delete this record');
                } else {
                    setError('Failed to delete record');
                }
            }
        }
    };

    if (loading) return <div style={loadingStyle}>Loading...</div>;
    if (error) return <div style={errorStyle}>{error}</div>;

    return (
        <div style={containerStyle}>
            <div style={headerStyle}>
                <h3>📋 Milk Records</h3>
                <span style={badgeStyle}>
                    {isAdmin() ? '👑 Admin View' : '🚛 Truck View'}
                </span>
            </div>

            {records.length === 0 ? (
                <div style={emptyStyle}>
                    <p>No records found</p>
                    <div style={{ fontSize: 12, color: '#666', marginTop: 8 }}>
                        <div>Current user: {user?.username || 'anonymous'}</div>
                        <div>Access token present: {Boolean(localStorage.getItem('access_token')) ? 'yes' : 'no'}</div>
                    </div>
                    <Link to="/add" style={addButtonStyle}>Add First Record</Link>
                </div>
            ) : (
                <div style={{ overflowX: 'auto' }}>
                    <table style={tableStyle}>
                        <thead>
                            <tr style={headerRowStyle}>
                                <th>Photo</th>
                                <th>Farmer</th>
                                <th>Location</th>
                                <th>Purity</th>
                                <th>Truck</th>
                                <th>Recorded By</th>
                                <th>Time</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {records.map((record) => (
                                <tr key={record.id} style={rowStyle}>
                                    <td>
                                        {record.farmer_photo_url ? (
                                            <img 
                                                src={record.farmer_photo_url} 
                                                alt={record.farmer_name}
                                                style={photoStyle}
                                            />
                                        ) : (
                                            <div style={noPhotoStyle}>📷</div>
                                        )}
                                    </td>
                                    <td><strong>{record.farmer_name}</strong></td>
                                    <td>{record.farmer_location}</td>
                                    <td>
                                        <span style={getPurityStyle(record.milk_purity)}>
                                            {record.purity_display || record.milk_purity}
                                        </span>
                                    </td>
                                    <td>
                                        <span style={getTruckStyle(record.truck)}>
                                            {record.truck}
                                        </span>
                                    </td>
                                    <td>
                                        {record.recorded_by_username}
                                        {record.recorded_by_role === 'admin' && ' 👑'}
                                    </td>
                                    <td>{new Date(record.collection_time).toLocaleString()}</td>
                                    <td>
                                        <Link to={`/detail/${record.id}`} style={actionButton('info')}>
                                            View
                                        </Link>
                                        <Link to={`/edit/${record.id}`} style={actionButton('warning')}>
                                            Edit
                                        </Link>
                                        {isAdmin() && (
                                            <button
                                                onClick={() => handleDelete(record.id)}
                                                style={actionButton('danger')}
                                            >
                                                Delete
                                            </button>
                                        )}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                    <div style={footerStyle}>
                        Total: {records.length} records
                    </div>
                </div>
            )}
        </div>
    );
};

// ============ STYLES ============

const containerStyle = {
    background: 'white',
    borderRadius: '15px',
    padding: '20px',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
};

const headerStyle = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '20px'
};

const badgeStyle = {
    padding: '5px 15px',
    borderRadius: '20px',
    background: '#1a4b8c',
    color: 'white',
    fontSize: '14px'
};

const photoStyle = {
    width: '50px',
    height: '50px',
    borderRadius: '50%',
    objectFit: 'cover',
    border: '2px solid #ddd'
};

const noPhotoStyle = {
    width: '50px',
    height: '50px',
    borderRadius: '50%',
    background: '#f0f0f0',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '24px',
    color: '#ccc'
};

const tableStyle = {
    width: '100%',
    borderCollapse: 'collapse'
};

const headerRowStyle = {
    background: '#1a4b8c',
    color: 'white'
};

const rowStyle = {
    borderBottom: '1px solid #eee'
};

const loadingStyle = {
    textAlign: 'center',
    padding: '50px'
};

const errorStyle = {
    color: 'red',
    textAlign: 'center',
    padding: '20px'
};

const emptyStyle = {
    textAlign: 'center',
    padding: '40px',
    color: '#666'
};

const addButtonStyle = {
    display: 'inline-block',
    padding: '10px 25px',
    background: 'linear-gradient(135deg, #1a4b8c, #2c6ab0)',
    color: 'white',
    textDecoration: 'none',
    borderRadius: '25px',
    marginTop: '10px'
};

const footerStyle = {
    marginTop: '15px',
    fontSize: '13px',
    color: '#666'
};

const getPurityStyle = (purity) => ({
    padding: '5px 12px',
    borderRadius: '20px',
    background: purity === 'GREAT' ? '#28a745' :
               purity === 'MID' ? '#ffc107' : '#dc3545',
    color: purity === 'MID' ? 'black' : 'white',
    display: 'inline-block',
    fontSize: '13px'
});

const getTruckStyle = (truck) => ({
    padding: '5px 12px',
    borderRadius: '20px',
    background: truck === 'TRUCK_A' ? '#1a4b8c' : '#28a745',
    color: 'white',
    display: 'inline-block',
    fontSize: '13px'
});

const actionButton = (type) => {
    const colors = {
        info: { bg: '#17a2b8', color: 'white' },
        warning: { bg: '#ffc107', color: 'black' },
        danger: { bg: '#dc3545', color: 'white' }
    };
    return {
        marginRight: '5px',
        padding: '5px 10px',
        background: colors[type].bg,
        color: colors[type].color,
        textDecoration: 'none',
        borderRadius: '5px',
        fontSize: '12px',
        border: 'none',
        cursor: 'pointer',
        display: 'inline-block'
    };
};

export default RecordList;