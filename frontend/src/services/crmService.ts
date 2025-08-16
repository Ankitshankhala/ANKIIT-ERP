import { apiClient } from './authService'

export interface Customer {
  id: number
  name: string
  email?: string
  phone?: string
  address?: string
  website?: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface Lead {
  id: number
  customer_id?: number
  name: string
  email?: string
  phone?: string
  source?: string
  status: string
  notes?: string
  created_at: string
  updated_at: string
}

export interface Opportunity {
  id: number
  customer_id?: number
  name: string
  value: number
  stage: string
  close_date?: string
  notes?: string
  created_at: string
  updated_at: string
}

class CRMService {
  async getCustomers(params?: { skip?: number; limit?: number; q?: string }) {
    const { data } = await apiClient.get('/crm/customers', { params })
    return data
  }

  async createCustomer(payload: Partial<Customer>) {
    const { data } = await apiClient.post('/crm/customers', payload)
    return data
  }

  async deleteCustomer(id: number) {
    await apiClient.delete(`/crm/customers/${id}`)
  }

  async getLeads(params?: { skip?: number; limit?: number; q?: string }) {
    const { data } = await apiClient.get('/crm/leads', { params })
    return data
  }

  async createLead(payload: Partial<Lead>) {
    const { data } = await apiClient.post('/crm/leads', payload)
    return data
  }

  async deleteLead(id: number) {
    await apiClient.delete(`/crm/leads/${id}`)
  }

  async getOpportunities(params?: { skip?: number; limit?: number; q?: string }) {
    const { data } = await apiClient.get('/crm/opportunities', { params })
    return data
  }

  async createOpportunity(payload: Partial<Opportunity>) {
    const { data } = await apiClient.post('/crm/opportunities', payload)
    return data
  }

  async deleteOpportunity(id: number) {
    await apiClient.delete(`/crm/opportunities/${id}`)
  }

  async getOpportunityPipeline() {
    const { data } = await apiClient.get('/crm/opportunities/pipeline')
    return data
  }

  async advanceOpportunity(id: number) {
    const { data } = await apiClient.post(`/crm/opportunities/${id}/advance`)
    return data
  }

  async getCommunications(params?: { skip?: number; limit?: number; customer_id?: number; lead_id?: number; opportunity_id?: number }) {
    const { data } = await apiClient.get('/crm/communications', { params })
    return data
  }

  async createCommunication(payload: any) {
    const { data } = await apiClient.post('/crm/communications', payload)
    return data
  }
}

export const crmService = new CRMService()


