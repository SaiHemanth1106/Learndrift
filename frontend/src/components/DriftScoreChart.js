import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function DriftScoreChart() {
  const data = [
    { topic: 'Algebra', drift: 45, stability: 75 },
    { topic: 'Geometry', drift: 35, stability: 85 },
    { topic: 'Trigonometry', drift: 65, stability: 55 },
    { topic: 'Calculus', drift: 55, stability: 65 },
    { topic: 'Statistics', drift: 25, stability: 90 }
  ];

  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="topic" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="drift" stroke="#e74c3c" name="Drift Score (%)" />
        <Line type="monotone" dataKey="stability" stroke="#27ae60" name="Stability Index (%)" />
      </LineChart>
    </ResponsiveContainer>
  );
}

export default DriftScoreChart;
