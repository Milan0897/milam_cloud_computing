import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { documentApi } from '../api';
import { useToast } from '../components/Toast';

const categoryOptions = [
  { value: 'marksheet', label: 'Marksheet' },
  { value: 'admin_card', label: 'Admin Card' },
  { value: 'registration_certificate', label: 'Registration Certificate' },
  { value: 'id_proof', label: 'ID Proof' },
  { value: 'other', label: 'Other' },
];

const ALLOWED_TYPES = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg', 'image/webp'];
const MAX_SIZE = 10 * 1024 * 1024;

export default function Upload() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [category, setCategory] = useState('other');
  const [loading, setLoading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);
  const { addToast } = useToast();
  const navigate = useNavigate();

  useEffect(() => {
    if (file) {
      const url = URL.createObjectURL(file);
      setPreview(url);
      return () => URL.revokeObjectURL(url);
    }
    setPreview(null);
  }, [file]);

  const validateFile = (f) => {
    if (!ALLOWED_TYPES.includes(f.type)) {
      addToast('Only PDF, JPEG, PNG, and WebP files allowed', 'error');
      return false;
    }
    if (f.size > MAX_SIZE) {
      addToast('File size must be less than 10MB', 'error');
      return false;
    }
    return true;
  };

  const handleFileSelect = (f) => {
    if (validateFile(f)) {
      setFile(f);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleInputChange = (e) => {
    if (e.target.files[0]) {
      handleFileSelect(e.target.files[0]);
    }
  };

  const removeFile = () => {
    setFile(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      addToast('Please select a file', 'error');
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('category', category);

      await documentApi.upload(formData);
      addToast('Document uploaded successfully!', 'success');
      navigate('/dashboard');
    } catch (error) {
      addToast(error.response?.data?.error || 'Upload failed', 'error');
    } finally {
      setLoading(false);
    }
  };

  const getFileIcon = () => {
    if (!file) return '📄';
    if (file.type === 'application/pdf') return '📄';
    if (file.type.startsWith('image/')) return '🖼️';
    return '📎';
  };

  return (
    <div>
      <div className="dashboard-header">
        <h1 className="dashboard-title">Upload Document</h1>
        <p className="dashboard-subtitle">Add a new document to your collection</p>
      </div>

      <div className="card" style={{maxWidth: '600px'}}>
        <form onSubmit={handleSubmit}>
          <div className="card" style={{padding: '1.5rem'}}>
            <div className="upload-zone" onClick={() => fileInputRef.current?.click()} style={dragActive ? {borderColor: 'var(--primary)', background: 'var(--primary-light)'} : {}}>
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf,.jpg,.jpeg,.png,.webp"
                onChange={handleInputChange}
                style={{display: 'none'}}
              />
              <div className="upload-icon">{file ? getFileIcon() : '📁'}</div>
              {file ? (
                <>
                  <p className="upload-text"><strong>{file.name}</strong></p>
                  <p className="upload-text">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                </>
              ) : (
                <>
                  <p className="upload-text">Drag & drop a file here, or <strong>click to browse</strong></p>
                  <p className="upload-text">PDF, JPG, PNG, WebP (max 10MB)</p>
                </>
              )}
            </div>

            {file && (
              <div style={{marginTop: '1rem', display: 'flex', gap: '1rem', alignItems: 'center', flexWrap: 'wrap'}}>
                <div style={{width: '60px', height: '60px', borderRadius: 'var(--radius)', background: 'var(--bg)', border: '1px solid var(--border)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.5rem'}}>
                  {preview && file.type.startsWith('image/') ? (
                    <img src={preview} alt="" style={{maxWidth: '100%', maxHeight: '100%', borderRadius: '4px'}} />
                  ) : (
                    getFileIcon()
                  )}
                </div>
                <div style={{flex: 1, minWidth: '150px'}}>
                  <p style={{fontWeight: 500}}>{file.name}</p>
                  <p style={{fontSize: '0.875rem', color: 'var(--text-muted)'}}>{(file.size / 1024 / 1024).toFixed(2)} MB • {file.type}</p>
                </div>
                <button type="button" onClick={removeFile} className="btn btn-outline btn-sm" disabled={loading}>Remove</button>
              </div>
            )}

            <div className="input-group" style={{marginTop: '1.5rem'}}>
              <label htmlFor="category">Category</label>
              <select
                id="category"
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                disabled={loading}
              >
                {categoryOptions.map((opt) => (
                  <option key={opt.value} value={opt.value}>{opt.label}</option>
                ))}
              </select>
            </div>
          </div>

          <div style={{padding: '1.5rem', borderTop: '1px solid var(--border)', display: 'flex', justifyContent: 'flex-end', gap: '0.75rem'}}>
            <button type="button" onClick={() => navigate('/dashboard')} className="btn btn-outline" disabled={loading}>Cancel</button>
            <button type="submit" className="btn btn-primary" disabled={loading || !file}>
              {loading ? 'Uploading...' : 'Upload Document'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}