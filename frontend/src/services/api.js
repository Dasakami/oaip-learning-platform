import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authService = {
  register: (data) => api.post('/auth/register', data),
  login: async (data) => {
    const response = await api.post('/auth/login', data);
    localStorage.setItem('token', response.data.access_token);
    return response;
  },
  logout: () => {
    localStorage.removeItem('token');
  },
  getMe: () => api.get('/auth/me'),
};

export const moduleService = {
  getAll: () => api.get('/modules/'),
  getById: (id) => api.get(`/modules/${id}`),
};

export const taskService = {
  getModuleTasks: (moduleId) => api.get(`/tasks/module/${moduleId}`),
  getById: (id) => api.get(`/tasks/${id}`),
  submitCode: (data) => api.post('/tasks/submit', data),
};

export const progressService = {
  getStats: () => api.get('/progress/stats'),
};

export default api;