import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api from '../api/axiosConfig';

const RecordForm = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [formData, setFormData] = useState({
        farmer_name: '',
        farmer_location: '',
        milk_purity: 'MID',
        truck: 'TRUCK_A',
        collection_time: new Date(new Date().getTime() - new Date().getTimezoneOffset() * 60000)
            .toISOString()
            .slice(0, 16),
    });

    const formatForDateTimeLocal = (dateString) => {
        if (!dateString) return '';
        const date = new Date(dateString);
        const offset = date.getTimezoneOffset();
        const localDate = new Date(date.getTime() - offset * 60000);
        return localDate.toISOString().slice(0, 16);
    };

    useEffect(() => {
        if (id) {
            fetchRecord();
        }
    }, [id]);

    const fetchRecord = async () => {
        try {
            setLoading(true);
            const response = await api.get(`/api/milk-records/${id}/`);
            setFormData(response.data);
        } catch (err) {
            setError('Failed to load record');
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            if (id) {
                await api.put(`/api/milk-records/${id}/`, formData);
            } else {
                await api.post('/api/milk-records/', formData);
            }
            navigate('/dashboard');
        } catch (err) {
            setError(err.response?.data?.message || 'Failed to save');
        } finally {
            setLoading(false);
        }
    };

    if (loading && id) return <div style={loadingStyle}>Loading...</div>;

    return (
        <div style={containerStyle}>
            <div style={cardStyle}>
                <h3 style={titleStyle}>
                    {id ? '✏️ Edit Milk Record' : '📝 Add New Milk Record'}
                </h3>

                {error && (
                    <div style={errorBoxStyle}>
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit}>
                    <div style={fieldStyle}>
                        <label style={labelStyle}>Farmer Name</label>
                        <input
                            type="text"
                            name="farmer_name"
                            value={formData.farmer_name}
                            onChange={handleChange}
                            required
                            style={inputStyle}
                            placeholder="Enter farmer name"
                        />
                    </div>

                    <div style={fieldStyle}>
                        <label style={labelStyle}>Farmer Location</label>
                        <input
                            type="text"
                            name="farmer_location"
                            value={formData.farmer_location}
                            onChange={handleChange}
                            required
                            style={inputStyle}
                            placeholder="Enter location"
                        />
                    </div>

                    <div style={fieldStyle}>
                        <label style={labelStyle}>Milk Purity</label>
                        <select
                            name="milk_purity"
                            value={formData.milk_purity}
                            onChange={handleChange}
                            style={selectStyle}
                        >
                            <option value="LOW">Low</option>
                            <option value="MID">Medium</option>
                            <option value="GREAT">Great</option>
                        </select>
                    </div>

                    <div style={fieldStyle}>
                        <label style={labelStyle}>Truck</label>
                        <select
                            name="truck"
                            value={formData.truck}
                            onChange={handleChange}
                            style={selectStyle}
                        >
                            <option value="TRUCK_A">Truck A</option>
                            <option value="TRUCK_B">Truck B</option>
                        </select>
                    </div>

                    <div style={fieldStyle}>
                        <label style={labelStyle}>Collection Time</label>
                        <input
                            type="datetime-local"
                            name="collection_time"
                            value={formData.collection_time}
                            onChange={handleChange}
                            required
                            style={inputStyle}
                        />
                    </div>

                    <div style={buttonGroupStyle}>
                        <button
                            type="submit"
                            disabled={loading}
                            style={submitButtonStyle}
                        >
                            {loading ? 'Saving...' : (id ? 'Update Record' : 'Save Record')}
                        </button>
                        <button
                            type="button"
                            onClick={() => navigate('/dashboard')}
                            style={cancelButtonStyle}
                        >
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

// Styles
const containerStyle = {
    maxWidth: '600px',
    margin: '0 auto'
};

const cardStyle = {
    background: 'white',
    borderRadius: '15px',
    padding: '30px',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
};

const titleStyle = {
    marginBottom: '20px',
    color: '#1a4b8c'
};

const fieldStyle = {
    marginBottom: '15px'
};

const labelStyle = {
    display: 'block',
    marginBottom: '5px',
    fontWeight: '500'
};

const inputStyle = {
    width: '100%',
    padding: '10px',
    border: '2px solid #ddd',
    borderRadius: '8px',
    fontSize: '16px',
    transition: 'border-color 0.3s'
};

const selectStyle = {
    width: '100%',
    padding: '10px',
    border: '2px solid #ddd',
    borderRadius: '8px',
    fontSize: '16px',
    background: 'white'
};

const buttonGroupStyle = {
    display: 'flex',
    gap: '10px',
    marginTop: '20px'
};

const submitButtonStyle = {
    flex: 1,
    padding: '12px',
    background: 'linear-gradient(135deg, #1a4b8c, #2c6ab0)',
    color: 'white',
    border: 'none',
    borderRadius: '25px',
    fontSize: '16px',
    cursor: 'pointer'
};

const cancelButtonStyle = {
    padding: '12px 25px',
    background: '#6c757d',
    color: 'white',
    border: 'none',
    borderRadius: '25px',
    cursor: 'pointer'
};

const errorBoxStyle = {
    background: '#f8d7da',
    color: '#721c24',
    padding: '10px',
    borderRadius: '8px',
    marginBottom: '20px'
};

const loadingStyle = {
    textAlign: 'center',
    padding: '50px'
};

export default RecordForm;