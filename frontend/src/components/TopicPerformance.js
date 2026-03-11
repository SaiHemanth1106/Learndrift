import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function TopicPerformance() {
  const data = [
    { topic: 'Algebra', attempts: 45, correct: 38, accuracy: 84 },
    { topic: 'Geometry', attempts: 38, correct: 32, accuracy: 84 },
    { topic: 'Trigonometry', attempts: 42, correct: 28, accuracy: 67 },
    { topic: 'Calculus', attempts: 35, correct: 22, accuracy: 63 },
    { topic: 'Statistics', attempts: 40, correct: 37, accuracy: 92 }
  ];

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="topic" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="attempts" fill="#3498db" name="Total Attempts" />
        <Bar dataKey="correct" fill="#27ae60" name="Correct Answers" />
      </BarChart>
    </ResponsiveContainer>
  );
}

export default TopicPerformance;
