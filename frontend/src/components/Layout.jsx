import { Outlet, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="page">
      <header className="header">
        <div className="header-content">
          <Link to="/dashboard" className="logo">StudentDocs</Link>
          <nav className="nav">
            <Link to="/dashboard" className="btn btn-outline btn-sm">Dashboard</Link>
            <Link to="/upload" className="btn btn-primary btn-sm">Upload Document</Link>
            <div className="user-menu">
              <span style={{fontSize: '0.875rem', color: 'var(--text-muted)'}}>{user?.name}</span>
              <div className="user-avatar">{user?.name?.[0].toUpperCase()}</div>
              <button onClick={handleLogout} className="btn btn-outline btn-sm">Logout</button>
            </div>
          </nav>
        </div>
      </header>
      <main className="main">
        <div className="container">
          <Outlet />
        </div>
      </main>
    </div>
  );
}