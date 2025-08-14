import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add request interceptor to include auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Add response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refresh_token')
        if (refreshToken) {
          const response = await api.post('/auth/refresh', { refresh_token: refreshToken })
          const { access_token } = response.data
          
          localStorage.setItem('access_token', access_token)
          originalRequest.headers.Authorization = `Bearer ${access_token}`
          
          return api(originalRequest)
        }
      } catch (refreshError) {
        // Refresh failed, redirect to login
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export interface LoginRequest {
  email_or_username: string
  password: string
}

export interface LoginResponse {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
}

export interface RegisterRequest {
  username: string
  email: string
  first_name: string
  last_name: string
  password: string
  organization_name?: string
  phone?: string
}

export interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  phone?: string
  is_active: boolean
  is_verified: boolean
  avatar_url?: string
  bio?: string
  timezone: string
  language: string
  organization_id: number
  role_id: number
  created_at: string
  updated_at: string
}

class AuthService {
  async login(email: string, password: string): Promise<LoginResponse> {
    const response = await api.post<LoginResponse>('/auth/login', {
      email_or_username: email,
      password,
    })
    return response.data
  }

  async register(userData: RegisterRequest): Promise<User> {
    const response = await api.post<User>('/auth/register', userData)
    return response.data
  }

  async getCurrentUser(): Promise<User> {
    const response = await api.get<User>('/auth/me')
    return response.data
  }

  async refreshToken(refreshToken: string): Promise<LoginResponse> {
    const response = await api.post<LoginResponse>('/auth/refresh', {
      refresh_token: refreshToken,
    })
    return response.data
  }

  async logout(): Promise<void> {
    await api.post('/auth/logout')
  }

  async requestPasswordReset(email: string): Promise<{ message: string }> {
    const response = await api.post<{ message: string }>('/auth/password-reset', { email })
    return response.data
  }

  async confirmPasswordReset(token: string, newPassword: string): Promise<{ message: string }> {
    const response = await api.post<{ message: string }>('/auth/password-reset-confirm', {
      token,
      new_password: newPassword,
    })
    return response.data
  }
}

export const authService = new AuthService()
