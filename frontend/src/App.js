import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import StudentAnalysis from './pages/StudentAnalysis';
import Alerts from './pages/Alerts';
import './App.css';

function App() {
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Check API health on load
    fetch('http://localhost:8000/health')
      .then(res => res.json())
      .catch(err => console.log('API not available yet'));
  }, []);

  return (
    <Router>
      <div className="App">
        <nav className="navbar">
          <div className="navbar-container">
            <Link to="/" className="navbar-logo">
              🎓 LearnDrift
            </Link>
            <div className="navbar-links">
              <Link to="/" className="nav-link">Dashboard</Link>
              <Link to="/students" className="nav-link">Students</Link>
              <Link to="/alerts" className="nav-link">Alerts</Link>
            </div>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/students/:studentId" element={<StudentAnalysis />} />
            <Route path="/alerts" element={<Alerts />} />
          </Routes>
        </main>

        <footer className="footer">
          <p>&copy; 2026 LearnDrift - AI System for Detecting Concept Drift in Student Learning</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
