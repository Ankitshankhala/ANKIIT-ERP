// Shapes returned by the ANKIIT ERP API (backend/app/schemas). Decimals arrive as strings.

export interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  full_name?: string
  phone?: string | null
  organization_id: number
  role_id: number
  role_name?: string | null
  permissions?: string[] | null
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
}

export interface FinancialSummary {
  total_assets: string
  total_liabilities: string
  total_equity: string
  total_revenue: string
  total_expenses: string
  net_income: string
  cash_balance: string
  accounts_receivable: string
  accounts_payable: string
}

export interface Invoice {
  id: number
  invoice_number: string
  customer_name: string
  due_date: string
  status: string
  total_amount: string
  balance_due: string
  is_paid: boolean
}

export interface Customer {
  id: number
  name: string
  email?: string | null
  phone?: string | null
  is_active: boolean
}

export interface Product {
  id: number
  sku: string
  name: string
  category?: string | null
  unit_of_measure: string
  sale_price: string
  cost_price: string
  is_active: boolean
}

export interface Employee {
  id: number
  first_name: string
  last_name: string
  email: string
  department?: string | null
  title?: string | null
  status?: string | null
}

export interface DashboardStats {
  organization_name: string
  organization_users: number
}
