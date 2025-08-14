import { apiClient } from './authService'

export interface Employee {
  id: number
  first_name: string
  last_name: string
  email: string
  phone?: string
  department?: string
  title?: string
  status: string
  created_at: string
  updated_at: string
}

export interface Attendance {
  id: number
  employee_id: number
  date: string
  check_in?: string
  check_out?: string
  notes?: string
  created_at: string
  updated_at: string
}

class HRService {
  async getEmployees(params?: { skip?: number; limit?: number; q?: string }) {
    const { data } = await apiClient.get('/hr/employees', { params })
    return data
  }

  async createEmployee(payload: Partial<Employee>) {
    const { data } = await apiClient.post('/hr/employees', payload)
    return data
  }

  async getAttendance(params?: { employee_id?: number; skip?: number; limit?: number }) {
    const { data } = await apiClient.get('/hr/attendance', { params })
    return data
  }

  async createAttendance(payload: Partial<Attendance>) {
    const { data } = await apiClient.post('/hr/attendance', payload)
    return data
  }
}

export const hrService = new HRService()


