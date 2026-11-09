import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { documentApi } from '../api';
import { useToast } from '../components/Toast';

const categoryLabels = {
  marksheet: 'Marksheet',
  admin_card: 'Admin Card',
  registration_certificate: 'Registration Certificate',
  id_proof: 'ID Proof',
  other: 'Other',
};

const categoryColors = {
  marksheet: 'blue',
  admin_card: 'purple',
  registration_certificate: 'green',
  id_proof: 'orange',
  other: 'gray',
};

export default function Dashboard() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const [deleteId, setDeleteId] = useState(null);
  const [downloadingId, setDownloadingId] = useState(null);
  const { addToast } = useToast();

  const handleDownload = async (url, originalName, id) => {
    try {
      setDownloadingId(id);
      addToast('Starting download...', 'info');
      const response = await fetch(url);
      if (!response.ok) throw new Error('Failed to fetch file');
      const blob = await response.blob();
      const blobUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = blobUrl;
      link.download = originalName;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(blobUrl);
      addToast('Downloaded successfully!', 'success');
    } catch (error) {
      console.error('Download error:', error);
      window.open(url, '_blank');
      addToast('Opened document in new tab', 'info');
    } finally {
      setDownloadingId(null);
    }
  };

  const fetchDocuments = async () => {
    try {
      const { data } = await documentApi.getAll({ category: filter === 'all' ? '' : filter });
      setDocuments(data.documents);
    } catch (error) {
      addToast('Failed to load documents', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, [filter]);

  const handleDelete = async (id) => {
    try {
      await documentApi.delete(id);
      addToast('Document deleted', 'success');
      setDocuments((prev) => prev.filter((d) => d.id !== id));
      setDeleteId(null);
    } catch (error) {
      addToast('Failed to delete document', 'error');
    }
  };

  const confirmDelete = (id) => setDeleteId(id);

  const getFileIcon = (mimeType) => {
    if (mimeType === 'application/pdf') return '📄';
    if (mimeType.startsWith('image/')) return '🖼️';
    return '📎';
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  };

  const filteredDocuments = documents;

  if (loading) {
    return <div className="loading"><div className="spinner"></div></div>;
  }

  const stats = {
    total: documents.length,
    images: documents.filter((d) => d.mimeType.startsWith('image/')).length,
    pdfs: documents.filter((d) => d.mimeType === 'application/pdf').length,
  };

  return (
    <div>
      <div className="dashboard-header">
        <div>
          <h1 className="dashboard-title">My Documents</h1>
          <p className="dashboard-subtitle">Manage and organize your academic documents</p>
        </div>
        <Link to="/upload" className="btn btn-primary">
          <span>+</span> Upload Document
        </Link>
      </div>

      <div className="stats-grid">
        <div className="card stat-card">
          <div className="stat-icon blue">📁</div>
          <div className="stat-value">{stats.total}</div>
          <div className="stat-label">Total Documents</div>
        </div>
        <div className="card stat-card">
          <div className="stat-icon green">🖼️</div>
          <div className="stat-value">{stats.images}</div>
          <div className="stat-label">Images</div>
        </div>
        <div className="card stat-card">
          <div className="stat-icon orange">📄</div>
          <div className="stat-value">{stats.pdfs}</div>
          <div className="stat-label">PDFs</div>
        </div>
      </div>

      <div className="section-header">
        <h2 className="section-title">Documents</h2>
        <select value={filter} onChange={(e) => setFilter(e.target.value)} className="btn btn-outline btn-sm" style={{padding: '0.5rem 1rem'}}>
          <option value="all">All Categories</option>
          <option value="marksheet">Marksheet</option>
          <option value="admin_card">Admin Card</option>
          <option value="registration_certificate">Registration Certificate</option>
          <option value="id_proof">ID Proof</option>
          <option value="other">Other</option>
        </select>
      </div>

      {filteredDocuments.length === 0 ? (
        <div className="card empty-state">
          <div className="empty-icon">📂</div>
          <h3 className="empty-title">No documents yet</h3>
          <p>Upload your first document to get started</p>
          <Link to="/upload" className="btn btn-primary" style={{marginTop: '1rem', display: 'inline-block'}}>
            Upload Document
          </Link>
        </div>
      ) : (
        <div className="document-grid">
          {filteredDocuments.map((doc) => (
            <div key={doc.id} className="card document-card">
              <div className="document-preview">
                {doc.mimeType.startsWith('image/') ? (
                  <img src={doc.viewUrl} alt={doc.originalName} loading="lazy" />
                ) : (
                  <span className="document-icon">{getFileIcon(doc.mimeType)}</span>
                )}
              </div>
              <div className="document-info">
                <span className="document-name" title={doc.originalName}>{doc.originalName}</span>
                <div className="document-meta">
                  <span>{formatFileSize(doc.size)}</span>
                  <span>{new Date(doc.createdAt).toLocaleDateString()}</span>
                  <span className="document-category">{categoryLabels[doc.category] || doc.category}</span>
                </div>
              </div>
              <div className="document-actions">
                <a href={doc.viewUrl} target="_blank" rel="noopener noreferrer" className="btn btn-outline btn-sm" style={{flex: 1, textAlign: 'center'}}>
                  View
                </a>
                <button
                  onClick={() => handleDownload(doc.viewUrl, doc.originalName, doc.id)}
                  className="btn btn-primary btn-sm"
                  style={{flex: 1}}
                  disabled={downloadingId === doc.id}
                >
                  {downloadingId === doc.id ? 'Saving...' : 'Download'}
                </button>
                <button
                  onClick={() => confirmDelete(doc.id)}
                  className="btn btn-danger btn-sm"
                  style={{flex: 1}}
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {deleteId && (
        <div className="modal-overlay" onClick={() => setDeleteId(null)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3 className="modal-title">Delete Document</h3>
              <button className="modal-close" onClick={() => setDeleteId(null)}>&times;</button>
            </div>
            <div className="modal-body">
              <p>Are you sure you want to delete this document? This action cannot be undone.</p>
            </div>
            <div className="modal-footer">
              <button onClick={() => setDeleteId(null)} className="btn btn-outline">Cancel</button>
              <button onClick={() => handleDelete(deleteId)} className="btn btn-danger">Delete</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}