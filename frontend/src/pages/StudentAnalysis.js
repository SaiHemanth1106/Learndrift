import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { dashboardAPI, interactionsAPI } from '../services/api';

function StudentAnalysis() {
  const { studentId } = useParams();
  const [summary, setSummary] = useState(null);
  const [interactions, setInteractions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStudentData();
  }, [studentId]);

  const fetchStudentData = async () => {
    try {
      setLoading(true);
      const [summaryRes, interactionsRes] = await Promise.all([
        dashboardAPI.getStudentSummary(studentId),
        interactionsAPI.getStudentInteractions(studentId)
      ]);
      
      setSummary(summaryRes.data);
      setInteractions(interactionsRes.data);
      setError(null);
    } catch (err) {
      console.error('Error fetching student data:', err);
      setError('Failed to load student data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading student analysis...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="dashboard">
      {summary && (
        <>
          <div className="card alert-low" style={{ color: 'white' }}>
            <div className="card-label">Student Name</div>
            <div className="card-value">{summary.student_name}</div>
          </div>

          <div className="card alert-medium" style={{ color: 'white' }}>
            <div className="card-label">Total Attempts</div>
            <div className="card-value">{summary.total_attempts}</div>
          </div>

          <div className="card alert-low" style={{ color: 'white' }}>
            <div className="card-label">Accuracy</div>
            <div className="card-value">{(summary.accuracy * 100).toFixed(1)}%</div>
          </div>

          <div className="card alert-medium" style={{ color: 'white' }}>
            <div className="card-label">Avg Time (sec)</div>
            <div className="card-value">{summary.average_time_seconds.toFixed(1)}</div>
          </div>
        </>
      )}

      <div className="chart-container" style={{ gridColumn: '1 / -1' }}>
        <h3>Recent Interactions</h3>
        {interactions.length > 0 ? (
          <table className="table">
            <thead>
              <tr>
                <th>Question ID</th>
                <th>Timestamp</th>
                <th>Correct</th>
                <th>Time (sec)</th>
                <th>Retries</th>
              </tr>
            </thead>
            <tbody>
              {interactions.slice(0, 10).map(interaction => (
                <tr key={interaction.id}>
                  <td>{interaction.question_id}</td>
                  <td>{new Date(interaction.timestamp).toLocaleDateString()}</td>
                  <td>{interaction.is_correct ? '✓' : '✗'}</td>
                  <td>{interaction.time_taken_seconds.toFixed(1)}</td>
                  <td>{interaction.retry_count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No interactions found</p>
        )}
      </div>
    </div>
  );
}

export default StudentAnalysis;
