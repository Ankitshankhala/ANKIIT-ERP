import { apiClient } from './authService'

export interface Product {
  id: number
  sku: string
  name: string
  description?: string
  category?: string
  unit_of_measure: string
  cost_price: number
  sale_price: number
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface Supplier {
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

export interface Warehouse {
  id: number
  code: string
  name: string
  location?: string
  description?: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface StockMovement {
  id: number
  movement_number: string
  product_id: number
  quantity: number
  movement_type: 'receipt' | 'issue' | 'transfer' | 'adjustment'
  from_warehouse_id?: number
  to_warehouse_id?: number
  supplier_id?: number
  reference?: string
  movement_date: string
  notes?: string
  created_at: string
  updated_at: string
}

export interface ProductCreate {
  sku: string
  name: string
  description?: string
  category?: string
  unit_of_measure?: string
  cost_price?: number
  sale_price?: number
  is_active?: boolean
}

export interface SupplierCreate {
  name: string
  email?: string
  phone?: string
  address?: string
  website?: string
  is_active?: boolean
}

export interface WarehouseCreate {
  code: string
  name: string
  location?: string
  description?: string
  is_active?: boolean
}

class InventoryService {
  async getProducts(params?: { skip?: number; limit?: number; q?: string; sort_by?: string; sort_dir?: 'asc'|'desc' }) {
    const { data } = await apiClient.get('/inventory/products', { params })
    return data
  }

  async createProduct(payload: ProductCreate) {
    const { data } = await apiClient.post('/inventory/products', payload)
    return data
  }

  async deleteProduct(id: number) {
    await apiClient.delete(`/inventory/products/${id}`)
  }

  async getSuppliers(params?: { skip?: number; limit?: number; q?: string; sort_by?: string; sort_dir?: 'asc'|'desc' }) {
    const { data } = await apiClient.get('/inventory/suppliers', { params })
    return data
  }

  async createSupplier(payload: SupplierCreate) {
    const { data } = await apiClient.post('/inventory/suppliers', payload)
    return data
  }

  async deleteSupplier(id: number) {
    await apiClient.delete(`/inventory/suppliers/${id}`)
  }

  async getWarehouses(params?: { skip?: number; limit?: number; q?: string; sort_by?: string; sort_dir?: 'asc'|'desc' }) {
    const { data } = await apiClient.get('/inventory/warehouses', { params })
    return data
  }

  async createWarehouse(payload: WarehouseCreate) {
    const { data } = await apiClient.post('/inventory/warehouses', payload)
    return data
  }

  async deleteWarehouse(id: number) {
    await apiClient.delete(`/inventory/warehouses/${id}`)
  }

  async receiveStock(payload: { product_id: number; to_warehouse_id: number; quantity: number; supplier_id?: number; reference?: string; notes?: string }) {
    const { data } = await apiClient.post('/inventory/stock/receive', payload)
    return data
  }

  async issueStock(payload: { product_id: number; from_warehouse_id: number; quantity: number; reference?: string; notes?: string }) {
    const { data } = await apiClient.post('/inventory/stock/issue', payload)
    return data
  }

  async transferStock(payload: { product_id: number; from_warehouse_id: number; to_warehouse_id: number; quantity: number; reference?: string; notes?: string }) {
    const { data } = await apiClient.post('/inventory/stock/transfer', payload)
    return data
  }

  async adjustStock(payload: { product_id: number; quantity: number; to_warehouse_id?: number; from_warehouse_id?: number; reference?: string; notes?: string }) {
    const { data } = await apiClient.post('/inventory/stock/adjust', payload)
    return data
  }

  // Procurement
  async createPO(payload: { supplier_id: number; expected_date?: string; notes?: string; lines: Array<{ product_id: number; description?: string; quantity: number; unit_price: number }> }) {
    const { data } = await apiClient.post('/inventory/purchase-orders', payload)
    return data
  }

  async createGRN(payload: { purchase_order_id?: number; warehouse_id: number; receipt_date?: string; notes?: string; lines: Array<{ product_id: number; po_line_id?: number; quantity: number; unit_cost: number }> }) {
    const { data } = await apiClient.post('/inventory/goods-receipts', payload)
    return data
  }

  // Outbound
  async createSO(payload: { customer_name: string; customer_email?: string; expected_ship_date?: string; notes?: string; lines: Array<{ product_id: number; description?: string; quantity: number; unit_price: number }> }) {
    const { data } = await apiClient.post('/inventory/sales-orders', payload)
    return data
  }

  async createShipment(payload: { sales_order_id?: number; warehouse_id: number; ship_date?: string; lines: Array<{ product_id: number; quantity: number }> }) {
    const { data } = await apiClient.post('/inventory/shipments', payload)
    return data
  }
}

export const inventoryService = new InventoryService()
