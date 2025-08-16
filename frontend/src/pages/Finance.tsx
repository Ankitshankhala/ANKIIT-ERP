import React, { useEffect, useState } from 'react';
import {
  financeService,
  Account,
  Transaction,
  Invoice,
  Payment,
  FinancialSummary,
  CashFlowSummary,
  FinancialMetrics,
} from '../services/financeService';

const tabs = ['overview', 'accounts', 'transactions', 'invoices', 'payments', 'reports'] as const;

type Tab = typeof tabs[number];

const Finance: React.FC = () => {
  const [activeTab, setActiveTab] = useState<Tab>('overview');
  const [summary, setSummary] = useState<FinancialSummary | null>(null);
  const [cashFlow, setCashFlow] = useState<CashFlowSummary | null>(null);
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [payments, setPayments] = useState<Payment[]>([]);
  const [metrics, setMetrics] = useState<FinancialMetrics | null>(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        if (activeTab === 'overview') {
          const [sum, flow] = await Promise.all([
            financeService.getFinancialSummary(),
            financeService.getCashFlowSummary(),
          ]);
          setSummary(sum);
          setCashFlow(flow);
        } else if (activeTab === 'accounts') {
          const res = await financeService.getAccounts();
          setAccounts(res.accounts);
        } else if (activeTab === 'transactions') {
          const res = await financeService.getTransactions();
          setTransactions(res.transactions);
        } else if (activeTab === 'invoices') {
          const res = await financeService.getInvoices();
          setInvoices(res.invoices);
        } else if (activeTab === 'payments') {
          const res = await financeService.getPayments();
          setPayments(res.payments);
        } else if (activeTab === 'reports') {
          const m = await financeService.getFinancialMetrics();
          setMetrics(m);
        }
      } catch (err) {
        console.error(err);
      }
    };
    loadData();
  }, [activeTab]);

  const formatCurrency = (amount: number) =>
    new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount);

  return (
    <div className="p-4">
      <div className="mb-4 space-x-2">
        {tabs.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-3 py-1 rounded ${activeTab === tab ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </div>

      {activeTab === 'overview' && summary && cashFlow && (
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="p-4 border rounded">
              <h3 className="font-semibold">Total Assets</h3>
              <p>{formatCurrency(summary.total_assets)}</p>
            </div>
            <div className="p-4 border rounded">
              <h3 className="font-semibold">Total Liabilities</h3>
              <p>{formatCurrency(summary.total_liabilities)}</p>
            </div>
            <div className="p-4 border rounded">
              <h3 className="font-semibold">Total Equity</h3>
              <p>{formatCurrency(summary.total_equity)}</p>
            </div>
            <div className="p-4 border rounded">
              <h3 className="font-semibold">Net Income</h3>
              <p>{formatCurrency(summary.net_income)}</p>
            </div>
          </div>
          <div className="p-4 border rounded">
            <h3 className="font-semibold mb-2">Cash Flow ({cashFlow.period})</h3>
            <p>Opening: {formatCurrency(cashFlow.opening_balance)}</p>
            <p>Cash In: {formatCurrency(cashFlow.cash_in)}</p>
            <p>Cash Out: {formatCurrency(cashFlow.cash_out)}</p>
            <p>Closing: {formatCurrency(cashFlow.closing_balance)}</p>
          </div>
        </div>
      )}

      {activeTab === 'accounts' && (
        <table className="min-w-full border">
          <thead>
            <tr className="bg-gray-100">
              <th className="p-2 text-left">Code</th>
              <th className="p-2 text-left">Name</th>
              <th className="p-2 text-right">Balance</th>
            </tr>
          </thead>
          <tbody>
            {accounts.map((acc) => (
              <tr key={acc.id} className="border-t">
                <td className="p-2">{acc.code}</td>
                <td className="p-2">{acc.name}</td>
                <td className="p-2 text-right">{formatCurrency(acc.current_balance)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {activeTab === 'transactions' && (
        <table className="min-w-full border">
          <thead>
            <tr className="bg-gray-100">
              <th className="p-2 text-left">Number</th>
              <th className="p-2 text-left">Type</th>
              <th className="p-2 text-right">Amount</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((txn) => (
              <tr key={txn.id} className="border-t">
                <td className="p-2">{txn.transaction_number}</td>
                <td className="p-2">{txn.transaction_type}</td>
                <td className="p-2 text-right">{formatCurrency(txn.amount)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {activeTab === 'invoices' && (
        <table className="min-w-full border">
          <thead>
            <tr className="bg-gray-100">
              <th className="p-2 text-left">Number</th>
              <th className="p-2 text-left">Customer</th>
              <th className="p-2 text-right">Total</th>
            </tr>
          </thead>
          <tbody>
            {invoices.map((inv) => (
              <tr key={inv.id} className="border-t">
                <td className="p-2">{inv.invoice_number}</td>
                <td className="p-2">{inv.customer_name}</td>
                <td className="p-2 text-right">{formatCurrency(inv.total_amount)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {activeTab === 'payments' && (
        <table className="min-w-full border">
          <thead>
            <tr className="bg-gray-100">
              <th className="p-2 text-left">Number</th>
              <th className="p-2 text-left">Method</th>
              <th className="p-2 text-right">Amount</th>
            </tr>
          </thead>
          <tbody>
            {payments.map((pay) => (
              <tr key={pay.id} className="border-t">
                <td className="p-2">{pay.payment_number}</td>
                <td className="p-2">{pay.payment_method}</td>
                <td className="p-2 text-right">{formatCurrency(pay.amount)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {activeTab === 'reports' && metrics && (
        <div className="grid grid-cols-2 gap-4">
          <div className="p-4 border rounded">
            <h3 className="font-semibold">Current Ratio</h3>
            <p>{metrics.current_ratio.toFixed(2)}</p>
          </div>
          <div className="p-4 border rounded">
            <h3 className="font-semibold">Debt to Equity</h3>
            <p>{metrics.debt_to_equity.toFixed(2)}</p>
          </div>
          <div className="p-4 border rounded">
            <h3 className="font-semibold">Profit Margin</h3>
            <p>{metrics.profit_margin.toFixed(2)}</p>
          </div>
          <div className="p-4 border rounded">
            <h3 className="font-semibold">Return on Equity</h3>
            <p>{metrics.return_on_equity.toFixed(2)}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Finance;
