import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api from '../api/axiosConfig';

const RecordForm = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [previewImage, setPreviewImage] = useState(null);
    const [selectedFile, setSelectedFile] = useState(null);
    const [selectedCertificate, setSelectedCertificate] = useState(null);
    
    const [formData, setFormData] = useState({
        farmer_name: '',
        farmer_location: '',
        milk_purity: 'MID',
        truck: 'TRUCK_A',
        farmer_photo: null,
        milk_certificate: null,
        additional_notes: '',
    });

    useEffect(() => {
        if (id) {
            fetchRecord();
        }
    }, [id]);

    const fetchRecord = async () => {
        try {
            setLoading(true);
            const response = await api.get(`/api/milk-records/${id}/`);
            const record = response.data;
            
            setFormData({
                farmer_name: record.farmer_name || '',
                farmer_location: record.farmer_location || '',
                milk_purity: record.milk_purity || 'MID',
                truck: record.truck || 'TRUCK_A',
                farmer_photo: null,
                milk_certificate: null,
                additional_notes: record.additional_notes || '',
            });
            
            // Set preview if photo exists
            if (record.farmer_photo_url) {
                setPreviewImage(record.farmer_photo_url);
            }
        } catch (err) {
            setError('Failed to load record');
            console.error(err);
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

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        const fieldName = e.target.name;
        
        if (file) {
            // Update form data with file
            setFormData({
                ...formData,
                [fieldName]: file
            });
            
            // Preview image for photo
            if (fieldName === 'farmer_photo') {
                const reader = new FileReader();
                reader.onloadend = () => {
                    setPreviewImage(reader.result);
                };
                reader.readAsDataURL(file);
                setSelectedFile(file.name);
            } else if (fieldName === 'milk_certificate') {
                setSelectedCertificate(file.name);
            }
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            // Create FormData for file upload
            const formDataToSend = new FormData();
            
            // Add text fields
            formDataToSend.append('farmer_name', formData.farmer_name);
            formDataToSend.append('farmer_location', formData.farmer_location);
            formDataToSend.append('milk_purity', formData.milk_purity);
            formDataToSend.append('truck', formData.truck);
            formDataToSend.append('additional_notes', formData.additional_notes || '');
            
            // Add files if selected
            if (formData.farmer_photo) {
                formDataToSend.append('farmer_photo', formData.farmer_photo);
            }
            if (formData.milk_certificate) {
                formDataToSend.append('milk_certificate', formData.milk_certificate);
            }

            // Log FormData contents for debugging
            console.log('Sending FormData:');
            for (let pair of formDataToSend.entries()) {
                console.log(pair[0], pair[1]);
            }

            let response;
            if (id) {
                // Update - use PUT with FormData
                response = await api.put(`/api/milk-records/${id}/`, formDataToSend, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                });
            } else {
                // Create - use POST with FormData
                response = await api.post('/api/milk-records/', formDataToSend, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                });
            }

            navigate('/dashboard');
        } catch (err) {
            console.error('Submit error:', err);
            setError(err.response?.data?.message || 'Failed to save record');
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
                        {typeof error === 'string' ? error : JSON.stringify(error)}
                    </div>
                )}

                <form onSubmit={handleSubmit}>
                    {/* Basic Fields */}
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

                    {/* ============ FILE UPLOAD FIELDS ============ */}

                    {/* Farmer Photo Upload */}
                    <div style={fieldStyle}>
                        <label style={labelStyle}>Farmer Photo</label>
                        <input
                            type="file"
                            name="farmer_photo"
                            accept="image/*"
                            onChange={handleFileChange}
                            style={fileInputStyle}
                        />
                        <small style={helpTextStyle}>
                            Upload a photo of the farmer (JPG, PNG, etc.)
                        </small>
                        {selectedFile && (
                            <div style={fileInfoStyle}>📷 Selected: {selectedFile}</div>
                        )}
                        {previewImage && (
                            <div style={previewContainerStyle}>
                                <img 
                                    src={previewImage} 
                                    alt="Farmer preview" 
                                    style={previewImageStyle}
                                />
                                <p style={previewLabelStyle}>Farmer Photo Preview</p>
                            </div>
                        )}
                    </div>

                    {/* Milk Certificate Upload */}
                    <div style={fieldStyle}>
                        <label style={labelStyle}>Milk Certificate</label>
                        <input
                            type="file"
                            name="milk_certificate"
                            accept=".pdf,.jpg,.jpeg,.png,.doc,.docx"
                            onChange={handleFileChange}
                            style={fileInputStyle}
                        />
                        <small style={helpTextStyle}>
                            Upload milk quality certificate (PDF, JPG, PNG, DOC)
                        </small>
                        {selectedCertificate && (
                            <div style={fileInfoStyle}>📄 Selected: {selectedCertificate}</div>
                        )}
                    </div>

                    {/* Additional Notes */}
                    <div style={fieldStyle}>
                        <label style={labelStyle}>Additional Notes</label>
                        <textarea
                            name="additional_notes"
                            value={formData.additional_notes}
                            onChange={handleChange}
                            style={textareaStyle}
                            rows="3"
                            placeholder="Any additional notes about this milk collection..."
                        />
                    </div>

                    {/* Buttons */}
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

// ============ STYLES ============

const containerStyle = {
    maxWidth: '700px',
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
    marginBottom: '20px'
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
    fontSize: '16px'
};

const selectStyle = {
    width: '100%',
    padding: '10px',
    border: '2px solid #ddd',
    borderRadius: '8px',
    fontSize: '16px',
    background: 'white'
};

const textareaStyle = {
    width: '100%',
    padding: '10px',
    border: '2px solid #ddd',
    borderRadius: '8px',
    fontSize: '16px',
    resize: 'vertical'
};

const fileInputStyle = {
    display: 'block',
    width: '100%',
    padding: '10px',
    border: '2px dashed #ddd',
    borderRadius: '8px',
    cursor: 'pointer'
};

const helpTextStyle = {
    display: 'block',
    marginTop: '5px',
    color: '#666',
    fontSize: '13px'
};

const fileInfoStyle = {
    marginTop: '5px',
    color: '#1a4b8c',
    fontSize: '14px'
};

const previewContainerStyle = {
    marginTop: '10px',
    textAlign: 'center'
};

const previewImageStyle = {
    maxWidth: '150px',
    maxHeight: '150px',
    borderRadius: '10px',
    border: '2px solid #ddd'
};

const previewLabelStyle = {
    marginTop: '5px',
    fontSize: '12px',
    color: '#666'
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