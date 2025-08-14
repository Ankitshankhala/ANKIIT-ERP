import { apiClient } from './authService';

export interface Account {
  id: number;
  code: string;
  name: string;
  description?: string;
  account_type: string;
  category: string;
  parent_account_id?: number;
  is_active: boolean;
  opening_balance: number;
  current_balance: number;
  created_at: string;
  updated_at: string;
}

export interface Transaction {
  id: number;
  transaction_number: string;
  transaction_type: string;
  description: string;
  amount: number;
  debit_account_id: number;
  credit_account_id: number;
  reference?: string;
  transaction_date: string;
  is_posted: boolean;
  posted_date?: string;
  created_at: string;
  updated_at: string;
}

export interface Invoice {
  id: number;
  invoice_number: string;
  customer_name: string;
  customer_email?: string;
  customer_address?: string;
  invoice_date: string;
  due_date: string;
  subtotal: number;
  tax_amount: number;
  total_amount: number;
  status: string;
  notes?: string;
  paid_amount: number;
  balance_due: number;
  is_paid: boolean;
  created_at: string;
  updated_at: string;
}

export interface Payment {
  id: number;
  payment_number: string;
  invoice_id: number;
  amount: number;
  payment_method: string;
  payment_date: string;
  reference?: string;
  status: string;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface FinancialSummary {
  total_assets: number;
  total_liabilities: number;
  total_equity: number;
  total_revenue: number;
  total_expenses: number;
  net_income: number;
  cash_balance: number;
  accounts_receivable: number;
  accounts_payable: number;
}

export interface CashFlowSummary {
  period: string;
  opening_balance: number;
  cash_in: number;
  cash_out: number;
  closing_balance: number;
}

export interface FinancialMetrics {
  current_ratio: number;
  quick_ratio: number;
  debt_to_equity: number;
  profit_margin: number;
  return_on_equity: number;
}

export interface AccountCreate {
  code: string;
  name: string;
  description?: string;
  account_type: string;
  category: string;
  parent_account_id?: number;
  is_active: boolean;
  opening_balance: number;
}

export interface TransactionCreate {
  transaction_type: string;
  description: string;
  amount: number;
  debit_account_id: number;
  credit_account_id: number;
  reference?: string;
  transaction_date: string;
}

export interface InvoiceCreate {
  customer_name: string;
  customer_email?: string;
  customer_address?: string;
  invoice_date: string;
  due_date: string;
  subtotal: number;
  tax_amount: number;
  total_amount: number;
  notes?: string;
}

export interface PaymentCreate {
  invoice_id: number;
  amount: number;
  payment_method: string;
  payment_date: string;
  reference?: string;
  notes?: string;
}

class FinanceService {
  // Account Management
  async getAccounts(params?: {
    skip?: number;
    limit?: number;
    account_type?: string;
    category?: string;
    is_active?: boolean;
    parent_account_id?: number;
    sort_by?: string;
    sort_dir?: 'asc'|'desc';
  }): Promise<{ accounts: Account[]; total: number; page: number; size: number }> {
    const response = await apiClient.get('/finance/accounts', { params });
    return response.data;
  }

  async getAccount(id: number): Promise<Account> {
    const response = await apiClient.get(`/finance/accounts/${id}`);
    return response.data;
  }

  async createAccount(accountData: AccountCreate): Promise<Account> {
    const response = await apiClient.post('/finance/accounts', accountData);
    return response.data;
  }

  async updateAccount(id: number, accountData: Partial<AccountCreate>): Promise<Account> {
    const response = await apiClient.put(`/finance/accounts/${id}`, accountData);
    return response.data;
  }

  async deleteAccount(id: number): Promise<void> {
    await apiClient.delete(`/finance/accounts/${id}`);
  }

  // Transaction Management
  async getTransactions(params?: {
    skip?: number;
    limit?: number;
    transaction_type?: string;
    account_id?: number;
    start_date?: string;
    end_date?: string;
    is_posted?: boolean;
    sort_by?: string;
    sort_dir?: 'asc'|'desc';
  }): Promise<{ transactions: Transaction[]; total: number; page: number; size: number }> {
    const response = await apiClient.get('/finance/transactions', { params });
    return response.data;
  }

  async getTransaction(id: number): Promise<Transaction> {
    const response = await apiClient.get(`/finance/transactions/${id}`);
    return response.data;
  }

  async createTransaction(transactionData: TransactionCreate): Promise<Transaction> {
    const response = await apiClient.post('/finance/transactions', transactionData);
    return response.data;
  }

  async postTransaction(id: number): Promise<Transaction> {
    const response = await apiClient.post(`/finance/transactions/${id}/post`);
    return response.data;
  }

  // Invoice Management
  async getInvoices(params?: {
    skip?: number;
    limit?: number;
    status?: string;
    customer_name?: string;
    start_date?: string;
    end_date?: string;
    is_paid?: boolean;
    sort_by?: string;
    sort_dir?: 'asc'|'desc';
  }): Promise<{ invoices: Invoice[]; total: number; page: number; size: number }> {
    const response = await apiClient.get('/finance/invoices', { params });
    return response.data;
  }

  async getInvoice(id: number): Promise<Invoice> {
    const response = await apiClient.get(`/finance/invoices/${id}`);
    return response.data;
  }

  async createInvoice(invoiceData: InvoiceCreate): Promise<Invoice> {
    const response = await apiClient.post('/finance/invoices', invoiceData);
    return response.data;
  }

  async updateInvoiceStatus(id: number, status: string): Promise<Invoice> {
    const response = await apiClient.put(`/finance/invoices/${id}/status`, { status });
    return response.data;
  }

  // Payment Management
  async getPayments(params?: {
    skip?: number;
    limit?: number;
  }): Promise<{ payments: Payment[]; total: number; page: number; size: number }> {
    const response = await apiClient.get('/finance/payments', { params });
    return response.data;
  }

  async createPayment(paymentData: PaymentCreate): Promise<Payment> {
    const response = await apiClient.post('/finance/payments', paymentData);
    return response.data;
  }

  async processPayment(id: number): Promise<Payment> {
    const response = await apiClient.post(`/finance/payments/${id}/process`);
    return response.data;
  }

  // Financial Reporting
  async getFinancialSummary(): Promise<FinancialSummary> {
    const response = await apiClient.get('/finance/reports/summary');
    return response.data;
  }

  async getCashFlowSummary(period: string = 'month'): Promise<CashFlowSummary> {
    const response = await apiClient.get('/finance/reports/cash-flow', { params: { period } });
    return response.data;
  }

  async getFinancialMetrics(): Promise<FinancialMetrics> {
    const response = await apiClient.get('/finance/reports/metrics');
    return response.data;
  }
}

export const financeService = new FinanceService();
