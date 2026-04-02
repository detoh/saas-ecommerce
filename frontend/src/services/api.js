import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercepteur pour ajouter le token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Intercepteur pour gérer les erreurs
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
            refresh: refreshToken,
          });

          localStorage.setItem('access_token', response.data.access);
          originalRequest.headers.Authorization = `Bearer ${response.data.access}`;
          return api(originalRequest);
        } catch (refreshError) {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          window.location.href = '/login';
        }
      }
    }

    return Promise.reject(error);
  }
);

// Services
export const authService = {
  login: (credentials) => api.post('/auth/connexion/', credentials),
  register: (data) => api.post('/auth/inscription/', data),
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },
  getProfile: () => api.get('/auth/profil/'),
};

export const dashboardService = {
  getVendeur: () => api.get('/dashboard/vendeur/'),
  getAdmin: () => api.get('/dashboard/admin/'),
};

export const boutiqueService = {
  getMaBoutique: () => api.get('/boutiques/ma-boutique/'),
  createBoutique: (data) => api.post('/boutiques/ma-boutique/', data),
  updateBoutique: (id, data) => api.put(`/boutiques/${id}/`, data),
};

export const produitService = {
  getAll: () => api.get('/produits/'),
  getById: (id) => api.get(`/produits/${id}/`),
  create: (data) => api.post('/produits/', data),
  update: (id, data) => api.put(`/produits/${id}/`, data),
  delete: (id) => api.delete(`/produits/${id}/`),
};

export const commandeService = {
  getAll: () => api.get('/commandes/'),
  getById: (id) => api.get(`/commandes/${id}/`),
  create: (data) => api.post('/commandes/', data),
  updateStatut: (id, statut) => api.patch(`/commandes/${id}/statut/`, { statut }),
  getStats: () => api.get('/commandes/stats/'),
};

export const paiementService = {
  initier: (data) => api.post('/paiements/initier/', data),
  getById: (id) => api.get(`/paiements/${id}/`),
  getStatut: (id) => api.get(`/paiements/${id}/statut/`),
};

export const abonnementService = {
  getActif: () => api.get('/abonnements/actif/'),
  create: (data) => api.post('/abonnements/creer/', data),
  renouveler: (data) => api.post('/abonnements/renouveler/', data),
  getStats: () => api.get('/abonnements/stats/'),
};

export default api;