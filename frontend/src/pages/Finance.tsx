import React, { useState } from 'react';
import { 
  DollarSign, 
  TrendingUp, 
  TrendingDown, 
  CreditCard, 
  FileText, 
  BarChart3,
  Plus,
  Eye,
  Download
} from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const Finance: React.FC = () => {
  const [activeTab, setActiveTab] = useState('overview');

  // Mock data for charts
  const cashFlowData = [
    { month: 'Jan', cashIn: 45000, cashOut: 32000 },
    { month: 'Feb', cashIn: 52000, cashOut: 38000 },
    { month: 'Mar', cashIn: 48000, cashOut: 35000 },
    { month: 'Apr', cashIn: 61000, cashOut: 42000 },
    { month: 'May', cashIn: 55000, cashOut: 39000 },
    { month: 'Jun', cashIn: 67000, cashOut: 45000 },
  ];

  const accountDistribution = [
    { name: 'Assets', value: 65, color: '#10B981' },
    { name: 'Liabilities', value: 20, color: '#EF4444' },
    { name: 'Equity', value: 15, color: '#3B82F6' },
  ];

  const recentTransactions = [
    { id: 1, description: 'Client Payment - Project Alpha', amount: 15000, type: 'credit', date: '2024-01-15' },
    { id: 2, description: 'Office Supplies', amount: 250, type: 'debit', date: '2024-01-14' },
    { id: 3, description: 'Software License Renewal', amount: 1200, type: 'debit', date: '2024-01-13' },
    { id: 4, description: 'Consulting Fee', amount: 8000, type: 'credit', date: '2024-01-12' },
  ];

  const upcomingInvoices = [
    { id: 1, customer: 'TechCorp Inc.', amount: 25000, dueDate: '2024-01-25', status: 'pending' },
    { id: 2, customer: 'Global Solutions', amount: 18000, dueDate: '2024-01-28', status: 'pending' },
    { id: 3, customer: 'Innovation Labs', amount: 32000, dueDate: '2024-01-30', status: 'pending' },
  ];

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      case 'paid': return 'bg-green-100 text-green-800';
      case 'overdue': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Finance Dashboard</h1>
              <p className="text-gray-600">Manage your financial operations and track performance</p>
            </div>
            <div className="flex space-x-3">
              <button className="btn-primary">
                <Plus className="w-4 h-4 mr-2" />
                New Transaction
              </button>
              <button className="btn-secondary">
                <Download className="w-4 h-4 mr-2" />
                Export Report
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            {[
              { id: 'overview', label: 'Overview', icon: BarChart3 },
              { id: 'accounts', label: 'Chart of Accounts', icon: CreditCard },
              { id: 'transactions', label: 'Transactions', icon: TrendingUp },
              { id: 'invoices', label: 'Invoices', icon: FileText },
              { id: 'reports', label: 'Reports', icon: Download },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <tab.icon className="w-4 h-4 inline mr-2" />
                {tab.label}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'overview' && (
          <div className="space-y-8">
            {/* Key Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-green-100 rounded-lg">
                    <DollarSign className="w-6 h-6 text-green-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Total Revenue</p>
                    <p className="text-2xl font-bold text-gray-900">{formatCurrency(125000)}</p>
                  </div>
                </div>
                <div className="mt-4 flex items-center text-sm">
                  <TrendingUp className="w-4 h-4 text-green-500 mr-1" />
                  <span className="text-green-600">+12.5%</span>
                  <span className="text-gray-500 ml-1">from last month</span>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-red-100 rounded-lg">
                    <TrendingDown className="w-6 h-6 text-red-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Total Expenses</p>
                    <p className="text-2xl font-bold text-gray-900">{formatCurrency(89000)}</p>
                  </div>
                </div>
                <div className="mt-4 flex items-center text-sm">
                  <TrendingDown className="w-4 h-4 text-red-500 mr-1" />
                  <span className="text-red-600">+8.2%</span>
                  <span className="text-gray-500 ml-1">from last month</span>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <CreditCard className="w-6 h-6 text-blue-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Cash Balance</p>
                    <p className="text-2xl font-bold text-gray-900">{formatCurrency(36000)}</p>
                  </div>
                </div>
                <div className="mt-4 flex items-center text-sm">
                  <TrendingUp className="w-4 h-4 text-green-500 mr-1" />
                  <span className="text-green-600">+5.8%</span>
                  <span className="text-gray-500 ml-1">from last month</span>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-purple-100 rounded-lg">
                    <FileText className="w-6 h-6 text-purple-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Outstanding Invoices</p>
                    <p className="text-2xl font-bold text-gray-900">{formatCurrency(75000)}</p>
                  </div>
                </div>
                <div className="mt-4 flex items-center text-sm">
                  <TrendingDown className="w-4 h-4 text-red-500 mr-1" />
                  <span className="text-red-600">+2.1%</span>
                  <span className="text-gray-500 ml-1">from last month</span>
                </div>
              </div>
            </div>

            {/* Charts Row */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Cash Flow Chart */}
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Cash Flow Trend</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={cashFlowData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip formatter={(value) => formatCurrency(Number(value))} />
                    <Line type="monotone" dataKey="cashIn" stroke="#10B981" strokeWidth={2} name="Cash In" />
                    <Line type="monotone" dataKey="cashOut" stroke="#EF4444" strokeWidth={2} name="Cash Out" />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              {/* Account Distribution */}
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Account Distribution</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={accountDistribution}
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                      label={({ name, value }) => `${name}: ${value}%`}
                    >
                      {accountDistribution.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Recent Activity Row */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Recent Transactions */}
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">Recent Transactions</h3>
                  <button className="text-blue-600 hover:text-blue-800 text-sm font-medium">View All</button>
                </div>
                <div className="space-y-3">
                  {recentTransactions.map((transaction) => (
                    <div key={transaction.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div className="flex items-center">
                        <div className={`w-2 h-2 rounded-full mr-3 ${
                          transaction.type === 'credit' ? 'bg-green-500' : 'bg-red-500'
                        }`} />
                        <div>
                          <p className="text-sm font-medium text-gray-900">{transaction.description}</p>
                          <p className="text-xs text-gray-500">{transaction.date}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className={`text-sm font-semibold ${
                          transaction.type === 'credit' ? 'text-green-600' : 'text-red-600'
                        }`}>
                          {transaction.type === 'credit' ? '+' : '-'}{formatCurrency(transaction.amount)}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Upcoming Invoices */}
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">Upcoming Invoices</h3>
                  <button className="text-blue-600 hover:text-blue-800 text-sm font-medium">View All</button>
                </div>
                <div className="space-y-3">
                  {upcomingInvoices.map((invoice) => (
                    <div key={invoice.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div>
                        <p className="text-sm font-medium text-gray-900">{invoice.customer}</p>
                        <p className="text-xs text-gray-500">Due: {invoice.dueDate}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm font-semibold text-gray-900">{formatCurrency(invoice.amount)}</p>
                        <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(invoice.status)}`}>
                          {invoice.status}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <button className="flex flex-col items-center p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-400 hover:bg-blue-50 transition-colors">
                  <Plus className="w-8 h-8 text-gray-400 mb-2" />
                  <span className="text-sm font-medium text-gray-600">New Account</span>
                </button>
                <button className="flex flex-col items-center p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-400 hover:bg-blue-50 transition-colors">
                  <TrendingUp className="w-8 h-8 text-gray-400 mb-2" />
                  <span className="text-sm font-medium text-gray-600">New Transaction</span>
                </button>
                <button className="flex flex-col items-center p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-400 hover:bg-blue-50 transition-colors">
                  <FileText className="w-8 h-8 text-gray-400 mb-2" />
                  <span className="text-sm font-medium text-gray-600">Create Invoice</span>
                </button>
                <button className="flex flex-col items-center p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-400 hover:bg-blue-50 transition-colors">
                  <BarChart3 className="w-8 h-8 text-gray-400 mb-2" />
                  <span className="text-sm font-medium text-gray-600">Generate Report</span>
                </button>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'accounts' && (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Chart of Accounts</h2>
            <p className="text-gray-600">Chart of accounts management coming soon...</p>
          </div>
        )}

        {activeTab === 'transactions' && (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Transactions</h2>
            <p className="text-gray-600">Transaction management coming soon...</p>
          </div>
        )}

        {activeTab === 'invoices' && (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Invoices</h2>
            <p className="text-gray-600">Invoice management coming soon...</p>
          </div>
        )}

        {activeTab === 'reports' && (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Financial Reports</h2>
            <p className="text-gray-600">Financial reporting coming soon...</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Finance;
