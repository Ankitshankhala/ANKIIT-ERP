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

export interface Payroll {
  id: number
  employee_id: number
  period_start: string
  period_end: string
  base_salary: number
  allowances: number
  deductions: number
  net_pay: number
  status: string
  created_at: string
  updated_at: string
}

export interface Leave {
  id: number
  employee_id: number
  start_date: string
  end_date: string
  type: string
  status: string
  reason?: string
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

  async getPayrolls(params?: { employee_id?: number; skip?: number; limit?: number }) {
    const { data } = await apiClient.get('/hr/payrolls', { params })
    return data
  }

  async createPayroll(payload: Partial<Payroll>) {
    const { data } = await apiClient.post('/hr/payrolls', payload)
    return data
  }

  async getLeaves(params?: { employee_id?: number; skip?: number; limit?: number }) {
    const { data } = await apiClient.get('/hr/leaves', { params })
    return data
  }

  async createLeave(payload: Partial<Leave>) {
    const { data } = await apiClient.post('/hr/leaves', payload)
    return data
  }
}

export const hrService = new HRService()


