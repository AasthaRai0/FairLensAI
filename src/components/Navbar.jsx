import './Navbar.css'

function Navbar({ navigate, currentPage }) {
  return (
    <nav className="navbar">
      <div className="navbar-logo" onClick={() => navigate('landing')}>
        <div className="logo-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="#000" strokeWidth="2.5" strokeLinecap="round">
            <circle cx="12" cy="12" r="3" />
            <path d="M12 2v3M12 19v3M2 12h3M19 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1" />
          </svg>
        </div>
        <span className="logo-text">Fair<span>Lens</span></span>
      </div>

      <div className="navbar-links">
        <button
          className={`nav-link ${currentPage === 'landing' ? 'active' : ''}`}
          onClick={() => navigate('landing')}
        >Home</button>
        <button
          className={`nav-link ${currentPage === 'analyze' || currentPage === 'loading' || currentPage === 'results' ? 'active' : ''}`}
          onClick={() => navigate('analyze')}
        >Audit</button>
        <button
          className={`nav-link ${currentPage === 'history' ? 'active' : ''}`}
          onClick={() => navigate('history')}
        >History</button>
        <button
          className={`nav-link ${currentPage === 'history' ? 'active' : ''}`}
          onClick={() => navigate('history')}
        >Docs</button>
      </div>

      <div className="navbar-right">
        <button className="nav-run-btn" onClick={() => navigate('analyze')}>
          Run Audit
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M3 7h8M8 4l3 3-3 3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
      </div>
    </nav>
  )
}

export default Navbar