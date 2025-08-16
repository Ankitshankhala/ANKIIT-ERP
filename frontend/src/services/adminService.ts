import { api } from './authService'

export interface UserPayload {
  username: string
  email: string
  first_name: string
  last_name: string
  password: string
  organization_id: number
  role_id: number
}

export interface OrganizationPayload {
  name: string
  email?: string
}

class AdminService {
  async getUsers() {
    const response = await api.get('/users')
    return response.data
  }

  async createUser(data: UserPayload) {
    const response = await api.post('/users', data)
    return response.data
  }

  async getOrganizations() {
    const response = await api.get('/organizations')
    return response.data
  }

  async createOrganization(data: OrganizationPayload) {
    const response = await api.post('/organizations', data)
    return response.data
  }

  async getRoles() {
    const response = await api.get('/roles')
    return response.data
  }
}

export const adminService = new AdminService()
