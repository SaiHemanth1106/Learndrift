import React, { useState, useEffect } from 'react';
import { analysisAPI } from '../services/api';

function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAlerts();
  }, []);

  const fetchAlerts = async () => {
    try {
      setLoading(true);
      const response = await analysisAPI.getAlerts();
      setAlerts(response.data);
      setError(null);
    } catch (err) {
      console.error('Error fetching alerts:', err);
      setError('Failed to load alerts');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading alerts...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="dashboard" style={{ gridColumn: '1 / -1' }}>
      <div className="chart-container">
        <h2>Drift Detection Alerts</h2>
        {alerts && alerts.length > 0 ? (
          <table className="table">
            <thead>
              <tr>
                <th>Student ID</th>
                <th>Topic</th>
                <th>Drift Score</th>
                <th>Stability Index</th>
                <th>Recommendation</th>
              </tr>
            </thead>
            <tbody>
              {alerts.map(alert => (
                <tr key={alert.id}>
                  <td>{alert.student_id}</td>
                  <td>{alert.topic}</td>
                  <td>
                    <div style={{
                      backgroundColor: alert.drift_score > 0.7 ? '#e74c3c' : alert.drift_score > 0.5 ? '#f39c12' : '#27ae60',
                      color: 'white',
                      padding: '0.25rem 0.5rem',
                      borderRadius: '4px',
                      display: 'inline-block'
                    }}>
                      {(alert.drift_score * 100).toFixed(1)}%
                    </div>
                  </td>
                  <td>{(alert.stability_index * 100).toFixed(1)}%</td>
                  <td>{alert.recommendation}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No alerts at this time - all students are progressing normally!</p>
        )}
      </div>
    </div>
  );
}

export default Alerts;
