import axios from 'axios';
import { Todo, Tag, Statistics, AuthResponse } from '../types';

export const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('jwt_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('jwt_token');
      localStorage.removeItem('user');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

// Auth API methods
export const authApi = {
  login: (email: string, password: string) =>
    api.post<AuthResponse>('/auth/login', { email, password }),
  register: (email: string, password: string, name?: string, username?: string) =>
    api.post<AuthResponse>('/auth/register', { email, password, name, username }),
};

// Todo API methods
export const todoApi = {
  getTodos: () => api.get<Todo[]>('/todos'),
  createTodo: (todo: { title: string; description?: string; tagId?: string; priority?: string }) =>
    api.post<Todo>('/todos', todo),
  updateTodo: (id: string, todo: Partial<{ title: string; description?: string; tagId?: string; priority?: string }>) =>
    api.put<Todo>(`/todos/${id}`, todo),
  deleteTodo: (id: string) => api.delete(`/todos/${id}`),
  toggleComplete: (id: string) => api.patch<Todo>(`/todos/${id}/complete`),
  getStatistics: () => api.get<Statistics>('/todos/statistics'),
};

// Tag API methods
export const tagApi = {
  getTags: () => api.get<Tag[]>('/tags'),
  createTag: (tag: { name: string; color?: string }) => api.post<Tag>('/tags', tag),
};