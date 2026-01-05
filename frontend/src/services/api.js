import axios from 'axios';

const API_URL = 'http://localhost:8000';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const userService = {
    getAll: () => api.get('/users/'),
    getById: (id) => api.get(`/users/${id}`),
    create: (data) => api.post('/users/', data),
    update: (id, data) => api.put(`/users/${id}`, data),
    delete: (id) => api.delete(`/users/${id}`),
};

export const postService = {
    getAll: () => api.get('/posts/'),
    getById: (id) => api.get(`/posts/${id}`),
    create: (data) => api.post('/posts/', data),
    update: (id, data) => api.put(`/posts/${id}`, data),
    delete: (id) => api.delete(`/posts/${id}`),
};

export const roleService = {
    getAll: () => api.get('/roles/'),
    create: (data) => api.post('/roles/', data),
};

export default api;
