import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Students endpoints
export const studentsAPI = {
  getAll: (skip = 0, limit = 100) => api.get(`/students`, { params: { skip, limit } }),
  getById: (id) => api.get(`/students/${id}`),
  create: (data) => api.post(`/students`, data),
  update: (id, data) => api.put(`/students/${id}`, data),
  delete: (id) => api.delete(`/students/${id}`),
};

// Interactions endpoints
export const interactionsAPI = {
  getStudentInteractions: (studentId) => api.get(`/interactions/student/${studentId}`),
  getTopicInteractions: (studentId, topic) => api.get(`/interactions/student/${studentId}/topic/${topic}`),
  recordInteraction: (data) => api.post(`/interactions`, data),
};

// Analysis endpoints
export const analysisAPI = {
  triggerAnalysis: (studentId) => api.post(`/analysis/analyze/${studentId}`),
  getStudentAnalysis: (studentId) => api.get(`/analysis/student/${studentId}`),
  getAlerts: () => api.get(`/analysis/alerts`),
  getTopicAnalysis: (topic) => api.get(`/analysis/topic/${topic}`),
};

// Dashboard endpoints
export const dashboardAPI = {
  getOverview: () => api.get(`/dashboard/overview`),
  getStudentSummary: (studentId) => api.get(`/dashboard/student/${studentId}/summary`),
  getTopicPerformance: () => api.get(`/dashboard/topic-performance`),
  getRecentAlerts: (hours = 24) => api.get(`/dashboard/recent-alerts`, { params: { hours } }),
};
