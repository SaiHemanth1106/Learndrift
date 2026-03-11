import React, { useState, useEffect } from 'react';
import { dashboardAPI } from '../services/api';
import DriftScoreChart from '../components/DriftScoreChart';
import TopicPerformance from '../components/TopicPerformance';

function Dashboard() {
  const [overview, setOverview] = useState(null);
  const [alerts, setAlerts] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [overviewRes, alertsRes] = await Promise.all([
        dashboardAPI.getOverview(),
        dashboardAPI.getRecentAlerts(24)
      ]);
      
      setOverview(overviewRes.data);
      setAlerts(alertsRes.data);
      setError(null);
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
      setError('Failed to load dashboard data. Make sure the API is running.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading dashboard...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="dashboard">
      <div className="card alert-high" style={{ color: 'white' }}>
        <div className="card-label">Total Students</div>
        <div className="card-value">{overview?.total_students || 0}</div>
      </div>

      <div className="card alert-medium" style={{ color: 'white' }}>
        <div className="card-label">Total Interactions</div>
        <div className="card-value">{overview?.total_interactions || 0}</div>
      </div>

      <div className="card alert-high" style={{ color: 'white' }}>
        <div className="card-label">Students at Risk</div>
        <div className="card-value">{overview?.students_at_risk || 0}</div>
      </div>

      <div className="card">
        <div className="card-label">Recent Alerts (24h)</div>
        <div className="card-value">{alerts?.alert_count || 0}</div>
      </div>

      <div className="chart-container" style={{ gridColumn: '1 / -1' }}>
        <h3>Concept Drift Detection Overview</h3>
        <DriftScoreChart />
      </div>

      <div className="chart-container" style={{ gridColumn: '1 / -1' }}>
        <h3>Topic Performance Metrics</h3>
        <TopicPerformance />
      </div>
    </div>
  );
}

export default Dashboard;
