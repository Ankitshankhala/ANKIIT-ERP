# Finance Module - ANKIIT ERP

## Overview

The Finance Module is the first complete ERP module implemented in ANKIIT ERP, providing comprehensive financial management capabilities including Chart of Accounts, Double-Entry Bookkeeping, Transaction Management, Invoice Management, and Financial Reporting.

## 🏗️ Architecture

### Backend Components

#### 1. Database Models (`backend/app/models/finance.py`)
- **Account**: Chart of accounts with hierarchical structure
- **Transaction**: Double-entry bookkeeping transactions
- **Invoice**: Customer invoice management
- **Payment**: Payment tracking and processing

#### 2. Data Schemas (`backend/app/schemas/finance.py`)
- Request/Response validation schemas
- Data transfer objects (DTOs)
- Query parameter schemas
- Financial reporting schemas

#### 3. Business Logic (`backend/app/services/finance_service.py`)
- Account management with validation
- Transaction processing with double-entry rules
- Invoice lifecycle management
- Payment processing
- Financial calculations and reporting

#### 4. API Endpoints (`backend/app/api/v1/endpoints/finance.py`)
- RESTful API for all financial operations
- Permission-based access control
- Comprehensive error handling
- Financial reporting endpoints

### Frontend Components

#### 1. Finance Dashboard (`frontend/src/pages/Finance.tsx`)
- Interactive financial overview
- Real-time charts and metrics
- Navigation between financial modules
- Quick action buttons

#### 2. Financial Service (`frontend/src/services/financeService.ts`)
- TypeScript interfaces for all financial entities
- API client methods for backend communication
- Error handling and data transformation

## 📊 Features

### Chart of Accounts
- **Hierarchical Structure**: Parent-child account relationships
- **Account Types**: Asset, Liability, Equity, Revenue, Expense
- **Account Categories**: Detailed categorization for reporting
- **Balance Tracking**: Opening and current balance management
- **Active/Inactive Status**: Account lifecycle management

### Transaction Management
- **Double-Entry Bookkeeping**: Ensures accounting equation balance
- **Transaction Types**: Sale, Purchase, Payment, Receipt, Transfer, Adjustment, Journal Entry
- **Validation Rules**: Account existence, active status, different debit/credit accounts
- **Posting System**: Manual transaction posting with balance updates
- **Reference Tracking**: External reference numbers and descriptions

### Invoice Management
- **Customer Information**: Name, email, address management
- **Invoice Lifecycle**: Draft → Sent → Paid/Overdue/Cancelled
- **Tax Calculation**: Subtotal, tax amount, and total amount
- **Payment Tracking**: Automatic balance due calculations
- **Status Management**: Invoice status updates and workflow

### Payment Processing
- **Multiple Payment Methods**: Cash, Bank Transfer, Credit Card, Check, Digital Wallet
- **Payment Status**: Pending, Completed, Failed, Cancelled
- **Reference Tracking**: Payment reference numbers and notes
- **Invoice Linking**: Direct connection to invoice records

### Financial Reporting
- **Financial Summary**: Assets, Liabilities, Equity, Revenue, Expenses, Net Income
- **Cash Flow Analysis**: Period-based cash flow tracking
- **Financial Ratios**: Current Ratio, Quick Ratio, Debt-to-Equity, Profit Margin, ROE
- **Real-time Data**: Live financial metrics and calculations

## 🔐 Security & Permissions

### Permission System
- **Account Management**: `finance:account:create`, `finance:account:read`, `finance:account:update`, `finance:account:delete`
- **Transaction Management**: `finance:transaction:create`, `finance:transaction:read`, `finance:transaction:post`
- **Invoice Management**: `finance:invoice:create`, `finance:invoice:read`, `finance:invoice:update`
- **Payment Management**: `finance:payment:create`, `finance:payment:read`, `finance:payment:process`
- **Financial Reporting**: `finance:report:read`

### Data Validation
- **Input Validation**: Pydantic schemas with field constraints
- **Business Rule Validation**: Double-entry principles, account status checks
- **Data Integrity**: Foreign key constraints, unique constraints
- **Error Handling**: Comprehensive error messages and HTTP status codes

## 🗄️ Database Schema

### Core Tables
```sql
-- Chart of Accounts
accounts (
    id, code, name, description, account_type, category,
    parent_account_id, is_active, opening_balance, current_balance,
    created_at, updated_at
)

-- Financial Transactions
transactions (
    id, transaction_number, transaction_type, description, amount,
    debit_account_id, credit_account_id, reference, transaction_date,
    is_posted, posted_date, created_at, updated_at
)

-- Customer Invoices
invoices (
    id, invoice_number, customer_name, customer_email, customer_address,
    invoice_date, due_date, subtotal, tax_amount, total_amount,
    status, notes, created_at, updated_at
)

-- Payment Records
payments (
    id, payment_number, invoice_id, amount, payment_method,
    payment_date, reference, status, notes, created_at, updated_at
)
```

### Enums
- **AccountType**: asset, liability, equity, revenue, expense
- **AccountCategory**: current_assets, fixed_assets, current_liabilities, long_term_liabilities, owners_equity, operating_revenue, operating_expenses, non_operating
- **TransactionType**: sale, purchase, payment, receipt, transfer, adjustment, journal_entry
- **InvoiceStatus**: draft, sent, paid, overdue, cancelled
- **PaymentMethod**: cash, bank_transfer, credit_card, check, digital_wallet

## 🚀 Getting Started

### 1. Database Setup
```bash
# Run database migration
cd backend
alembic upgrade head

# Initialize with sample data
python scripts/init_db.py
```

### 2. Start the Application
```bash
# Backend
cd backend
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm run dev
```

### 3. Access Finance Module
- Navigate to `/finance` in the frontend
- Use the sidebar navigation to access different financial sections
- API endpoints available at `/api/v1/finance/*`

## 📈 Sample Data

The system comes pre-loaded with a sample Chart of Accounts:

### Asset Accounts
- **1000 - Cash**: $10,000 (Current Assets)
- **1100 - Accounts Receivable**: $0 (Current Assets)
- **1500 - Equipment**: $5,000 (Fixed Assets)

### Liability Accounts
- **2000 - Accounts Payable**: $0 (Current Liabilities)

### Equity Accounts
- **3000 - Owner's Equity**: $15,000 (Owner's Equity)

### Revenue Accounts
- **4000 - Service Revenue**: $0 (Operating Revenue)

### Expense Accounts
- **5000 - Office Supplies**: $0 (Operating Expenses)
- **5100 - Utilities**: $0 (Operating Expenses)

## 🔧 API Endpoints

### Accounts
- `POST /api/v1/finance/accounts` - Create account
- `GET /api/v1/finance/accounts` - List accounts with filtering
- `GET /api/v1/finance/accounts/{id}` - Get account details
- `PUT /api/v1/finance/accounts/{id}` - Update account
- `DELETE /api/v1/finance/accounts/{id}` - Delete account

### Transactions
- `POST /api/v1/finance/transactions` - Create transaction
- `POST /api/v1/finance/transactions/{id}/post` - Post transaction
- `GET /api/v1/finance/transactions` - List transactions with filtering
- `GET /api/v1/finance/transactions/{id}` - Get transaction details

### Invoices
- `POST /api/v1/finance/invoices` - Create invoice
- `GET /api/v1/finance/invoices` - List invoices with filtering
- `GET /api/v1/finance/invoices/{id}` - Get invoice details
- `PUT /api/v1/finance/invoices/{id}/status` - Update invoice status

### Payments
- `POST /api/v1/finance/payments` - Create payment
- `POST /api/v1/finance/payments/{id}/process` - Process payment
- `GET /api/v1/finance/payments` - List payments

### Financial Reporting
- `GET /api/v1/finance/reports/summary` - Financial summary
- `GET /api/v1/finance/reports/cash-flow` - Cash flow analysis
- `GET /api/v1/finance/reports/metrics` - Financial ratios

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest tests/ -v
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 📝 Development Notes

### Business Logic Implementation
- **Double-Entry Validation**: Ensures debit and credit accounts are different
- **Account Balance Updates**: Automatic balance updates when transactions are posted
- **Invoice Calculations**: Automatic balance due and payment status calculations
- **Permission Checks**: Role-based access control for all financial operations

### Error Handling
- **Custom Exceptions**: Business logic and validation errors
- **HTTP Status Codes**: Appropriate status codes for different error types
- **User-Friendly Messages**: Clear error messages for end users
- **Logging**: Comprehensive logging for debugging and monitoring

### Performance Considerations
- **Database Indexing**: Proper indexes on frequently queried fields
- **Query Optimization**: Efficient database queries with proper joins
- **Pagination**: Large dataset handling with skip/limit pagination
- **Caching**: Redis integration ready for future performance improvements

## 🔮 Future Enhancements

### Phase 2 Features
- **Invoice Line Items**: Detailed product/service line items
- **Recurring Invoices**: Automated invoice generation
- **Multi-Currency Support**: International business support
- **Advanced Reporting**: Custom financial reports and dashboards
- **Audit Trail**: Complete transaction history and changes tracking

### Phase 3 Features
- **Bank Reconciliation**: Bank statement matching
- **Budget Management**: Budget planning and variance analysis
- **Tax Management**: Automated tax calculations and reporting
- **Financial Forecasting**: Cash flow and profit projections
- **Integration APIs**: Third-party accounting software integration

## 🤝 Contributing

When contributing to the Finance Module:

1. **Follow Accounting Principles**: Ensure all changes maintain proper accounting standards
2. **Test Business Logic**: Verify double-entry bookkeeping rules are maintained
3. **Update Documentation**: Keep this documentation current with any changes
4. **Add Tests**: Include comprehensive tests for new features
5. **Code Review**: Ensure all changes are reviewed by team members

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [React Documentation](https://reactjs.org/docs/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

## 📞 Support

For questions about the Finance Module:
1. Check the API documentation at `/docs`
2. Review the code comments and docstrings
3. Open an issue in the repository
4. Contact the development team

---

**Last Updated**: January 2024  
**Version**: 1.0.0  
**Status**: ✅ Complete and Production Ready
