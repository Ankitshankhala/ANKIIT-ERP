from typing import List, Optional, Dict, Any, Tuple
from decimal import Decimal
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from sqlalchemy.exc import IntegrityError
import uuid

from ..models.finance import (
    Account,
    Transaction,
    Invoice,
    Payment,
    AccountType,
    TransactionType,
    InvoiceStatus,
    InvoiceType,
    InvoiceLineItem,
    AccountingPeriod,
    AccountCategory,
)
from ..models.inventory import Product, Shipment, ShipmentLine
from ..schemas.finance import (
    AccountCreate, AccountUpdate, TransactionCreate, TransactionUpdate,
    InvoiceCreate, InvoiceUpdate, PaymentCreate, PaymentUpdate,
    FinancialSummary, CashFlowSummary, FinancialMetrics
)
from ..core.exceptions import BusinessLogicError, ValidationError
from ..core.config import settings

class FinanceService:
    def __init__(self, db: Session):
        self.db = db
    
    # Account Management
    def create_account(self, account_data: AccountCreate) -> Account:
        """Create a new account with validation"""
        try:
            # Validate account code uniqueness
            if self.db.query(Account).filter(Account.code == account_data.code).first():
                raise ValidationError(f"Account code '{account_data.code}' already exists")
            
            # Validate parent account if specified
            if account_data.parent_account_id:
                parent = self.db.query(Account).filter(Account.id == account_data.parent_account_id).first()
                if not parent:
                    raise ValidationError("Parent account not found")
                if not parent.is_active:
                    raise ValidationError("Parent account is not active")
            
            account = Account(**account_data.dict())
            self.db.add(account)
            self.db.commit()
            self.db.refresh(account)
            return account
            
        except IntegrityError as e:
            self.db.rollback()
            raise ValidationError(f"Failed to create account: {str(e)}")
    
    def get_account(self, account_id: int) -> Optional[Account]:
        """Get account by ID"""
        return self.db.query(Account).filter(Account.id == account_id).first()
    
    def get_accounts(self, skip: int = 0, limit: int = 100, sort_by: Optional[str] = None, sort_dir: Optional[str] = None, **filters) -> List[Account]:
        """Get accounts with optional filtering"""
        query = self.db.query(Account)
        
        if filters.get('account_type'):
            query = query.filter(Account.account_type == filters['account_type'])
        if filters.get('category'):
            query = query.filter(Account.category == filters['category'])
        if filters.get('is_active') is not None:
            query = query.filter(Account.is_active == filters['is_active'])
        if filters.get('parent_account_id'):
            query = query.filter(Account.parent_account_id == filters['parent_account_id'])
        
        colmap = {
            "code": Account.code,
            "name": Account.name,
            "current_balance": Account.current_balance,
            "created_at": Account.created_at,
            "updated_at": Account.updated_at,
        }
        col = colmap.get((sort_by or "created_at"))
        if sort_dir == "asc":
            query = query.order_by(col.asc())
        else:
            query = query.order_by(col.desc())
        return query.offset(skip).limit(limit).all()
    
    def update_account(self, account_id: int, account_data: AccountUpdate) -> Optional[Account]:
        """Update account"""
        account = self.get_account(account_id)
        if not account:
            return None
        
        update_data = account_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(account, field, value)
        
        self.db.commit()
        self.db.refresh(account)
        return account

    # Transaction update
    def update_transaction(self, transaction_id: int, data: TransactionUpdate) -> Optional[Transaction]:
        txn = self.db.query(Transaction).filter(Transaction.id == transaction_id).first()
        if not txn:
            return None
        if txn.is_posted:
            raise BusinessLogicError("Cannot update a posted transaction")
        for field, value in data.dict(exclude_unset=True).items():
            setattr(txn, field, value)
        self.db.commit()
        self.db.refresh(txn)
        return txn
    
    def delete_account(self, account_id: int) -> bool:
        """Delete account if it has no transactions"""
        account = self.get_account(account_id)
        if not account:
            return False
        
        # Check if account has transactions
        if self.db.query(Transaction).filter(
            or_(Transaction.debit_account_id == account_id, Transaction.credit_account_id == account_id)
        ).first():
            raise BusinessLogicError("Cannot delete account with existing transactions")
        
        # Check if account has sub-accounts
        if account.sub_accounts:
            raise BusinessLogicError("Cannot delete account with sub-accounts")
        
        self.db.delete(account)
        self.db.commit()
        return True
    
    # Transaction Management
    def create_transaction(self, transaction_data: TransactionCreate) -> Transaction:
        """Create a new transaction with double-entry validation"""
        try:
            # Validate accounts exist and are active
            debit_account = self.get_account(transaction_data.debit_account_id)
            credit_account = self.get_account(transaction_data.credit_account_id)
            
            if not debit_account or not credit_account:
                raise ValidationError("One or both accounts not found")
            
            if not debit_account.is_active or not credit_account.is_active:
                raise ValidationError("One or both accounts are not active")
            
            # Validate double-entry principle
            if debit_account.id == credit_account.id:
                raise ValidationError("Debit and credit accounts must be different")
            
            # Generate transaction number
            transaction_number = f"TXN-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
            
            transaction = Transaction(
                **transaction_data.dict(),
                transaction_number=transaction_number
            )
            
            self.db.add(transaction)
            self.db.commit()
            self.db.refresh(transaction)
            return transaction
            
        except IntegrityError as e:
            self.db.rollback()
            raise ValidationError(f"Failed to create transaction: {str(e)}")
    
    def post_transaction(self, transaction_id: int) -> Transaction:
        """Post a transaction and update account balances"""
        transaction = self.db.query(Transaction).filter(Transaction.id == transaction_id).first()
        if not transaction:
            raise ValidationError("Transaction not found")
        
        if transaction.is_posted:
            raise BusinessLogicError("Transaction is already posted")
        
        # Update account balances
        transaction.debit_account.current_balance += transaction.amount
        transaction.credit_account.current_balance -= transaction.amount
        
        transaction.is_posted = True
        transaction.posted_date = datetime.now()
        
        self.db.commit()
        self.db.refresh(transaction)
        return transaction
    
    def get_transactions(self, skip: int = 0, limit: int = 100, sort_by: Optional[str] = None, sort_dir: Optional[str] = None, **filters) -> List[Transaction]:
        """Get transactions with optional filtering"""
        query = self.db.query(Transaction)
        
        if filters.get('transaction_type'):
            query = query.filter(Transaction.transaction_type == filters['transaction_type'])
        if filters.get('account_id'):
            query = query.filter(
                or_(Transaction.debit_account_id == filters['account_id'], 
                    Transaction.credit_account_id == filters['account_id'])
            )
        if filters.get('start_date'):
            query = query.filter(Transaction.transaction_date >= filters['start_date'])
        if filters.get('end_date'):
            query = query.filter(Transaction.transaction_date <= filters['end_date'])
        if filters.get('is_posted') is not None:
            query = query.filter(Transaction.is_posted == filters['is_posted'])
        
        colmap = {
            "transaction_date": Transaction.transaction_date,
            "amount": Transaction.amount,
            "created_at": Transaction.created_at,
        }
        col = colmap.get((sort_by or "transaction_date"))
        if sort_dir == "asc":
            query = query.order_by(col.asc())
        else:
            query = query.order_by(col.desc())
        return query.offset(skip).limit(limit).all()
    
    # Invoice Management
    def create_invoice(self, invoice_data: InvoiceCreate) -> Invoice:
        """Create a new invoice"""
        try:
            # Generate invoice number
            invoice_number = f"INV-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
            
            payload = invoice_data.dict()
            items_payload = payload.pop('items', [])
            invoice = Invoice(
                **payload,
                invoice_number=invoice_number,
            )
            # Build line items
            for item in items_payload:
                line = InvoiceLineItem(**item)
                invoice.items.append(line)
            # Calculate totals
            invoice.calculate_totals()
            
            self.db.add(invoice)
            self.db.commit()
            self.db.refresh(invoice)
            return invoice
            
        except IntegrityError as e:
            self.db.rollback()
            raise ValidationError(f"Failed to create invoice: {str(e)}")
    
    def get_invoices(self, skip: int = 0, limit: int = 100, sort_by: Optional[str] = None, sort_dir: Optional[str] = None, **filters) -> List[Invoice]:
        """Get invoices with optional filtering"""
        query = self.db.query(Invoice)
        
        if filters.get('status'):
            query = query.filter(Invoice.status == filters['status'])
        if filters.get('customer_name'):
            query = query.filter(Invoice.customer_name.ilike(f"%{filters['customer_name']}%"))
        if filters.get('start_date'):
            query = query.filter(Invoice.invoice_date >= filters['start_date'])
        if filters.get('end_date'):
            query = query.filter(Invoice.invoice_date <= filters['end_date'])
        if filters.get('is_paid') is not None:
            if filters['is_paid']:
                query = query.filter(Invoice.total_amount <= func.coalesce(
                    func.sum(Payment.amount), 0
                ))
            else:
                query = query.filter(Invoice.total_amount > func.coalesce(
                    func.sum(Payment.amount), 0
                ))
        
        colmap = {
            "invoice_date": Invoice.invoice_date,
            "total_amount": Invoice.total_amount,
            "customer_name": Invoice.customer_name,
            "created_at": Invoice.created_at,
        }
        col = colmap.get((sort_by or "invoice_date"))
        if sort_dir == "asc":
            query = query.order_by(col.asc())
        else:
            query = query.order_by(col.desc())
        return query.offset(skip).limit(limit).all()
    
    def update_invoice_status(self, invoice_id: int, status: InvoiceStatus) -> Invoice:
        """Update invoice status"""
        invoice = self.db.query(Invoice).filter(Invoice.id == invoice_id).first()
        if not invoice:
            raise ValidationError("Invoice not found")
        
        invoice.status = status
        self.db.commit()
        self.db.refresh(invoice)
        return invoice

    def update_invoice(self, invoice_id: int, data: InvoiceUpdate) -> Optional[Invoice]:
        invoice = self.db.query(Invoice).filter(Invoice.id == invoice_id).first()
        if not invoice:
            return None
        # Do not allow direct change of totals; prefer items recalculation (out of scope here)
        update_data = data.dict(exclude_unset=True)
        for key in ["customer_name", "customer_email", "customer_address", "due_date", "notes"]:
            if key in update_data:
                setattr(invoice, key, update_data[key])
        self.db.commit()
        self.db.refresh(invoice)
        return invoice

    # Posting Engine
    def _get_required_account(self, code: str) -> Account:
        acc = self.db.query(Account).filter(Account.code == code).first()
        if not acc:
            raise ValidationError(f"Required account '{code}' not found")
        if acc.is_locked:
            raise BusinessLogicError(f"Account '{code}' is locked")
        return acc

    def _current_period_locked(self, period: str) -> bool:
        period_row = self.db.query(AccountingPeriod).filter(AccountingPeriod.period == period).first()
        return bool(period_row and period_row.is_closed)

    def post_invoice(self, invoice_id: int) -> Invoice:
        """Post invoice to GL (AR/AP). Creates double-entry Transaction(s) and posts COGS if SALE with items containing COGS info in metadata (future)."""
        invoice = self.db.query(Invoice).filter(Invoice.id == invoice_id).first()
        if not invoice:
            raise ValidationError("Invoice not found")
        if invoice.status not in [InvoiceStatus.SENT, InvoiceStatus.PAID, InvoiceStatus.OVERDUE]:
            # Auto move from DRAFT to SENT on posting
            invoice.status = InvoiceStatus.SENT

        period = invoice.accounting_period
        if self._current_period_locked(period):
            raise BusinessLogicError(f"Period {period} is locked")

        amount = invoice.total_amount
        if amount <= 0:
            raise ValidationError("Invoice total must be > 0 to post")

        # Account codes expected to exist: AR/AP, Revenue/Expense
        if invoice.invoice_type == InvoiceType.SALE:
            debit_acc = self._get_required_account(settings.ACCOUNTS_AR_CODE)
            credit_acc = self._get_required_account(settings.ACCOUNTS_REVENUE_CODE)
            txn_type = TransactionType.SALE
            desc = f"Post AR for invoice {invoice.invoice_number}"
        else:
            # If purchase has inventory items, capitalize inventory; otherwise post to expense
            has_inventory = any((it.product_sku for it in invoice.items or []))
            debit_code = settings.ACCOUNTS_INVENTORY_CODE if has_inventory else settings.ACCOUNTS_EXPENSE_CODE
            debit_acc = self._get_required_account(debit_code)
            credit_acc = self._get_required_account(settings.ACCOUNTS_AP_CODE)
            txn_type = TransactionType.PURCHASE
            desc = f"Post AP for invoice {invoice.invoice_number}"

        txn_number = f"TXN-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        txn = Transaction(
            transaction_number=txn_number,
            transaction_type=txn_type,
            description=desc,
            amount=amount,
            debit_account_id=debit_acc.id,
            credit_account_id=credit_acc.id,
            reference=invoice.invoice_number,
            transaction_date=datetime.now(),
            is_posted=False,
            invoice_id=invoice.id,
            period=period,
        )
        self.db.add(txn)
        # Post the transaction to update balances
        self.db.flush()
        txn.debit_account.current_balance += amount
        txn.credit_account.current_balance -= amount
        txn.is_posted = True
        txn.posted_date = datetime.now()
        self.db.commit()
        self.db.refresh(invoice)

        # If SALE, also post COGS using shipment valuation if available, fallback to product cost_price
        if invoice.invoice_type == InvoiceType.SALE:
            total_cost = Decimal('0.00')
            # Try to detect shipment number in invoice notes: "Invoice for shipment SHP-..."
            ship_cost_used = False
            try:
                if invoice.notes and 'shipment ' in invoice.notes:
                    ship_number = invoice.notes.split('shipment ')[1].strip()
                    shp = self.db.query(Shipment).filter(Shipment.ship_number == ship_number).first()
                    if shp:
                        # Sum valuation costs from shipment lines
                        for sl in shp.lines or []:
                            line_cost = (sl.quantity or Decimal('0')) * (sl.unit_cost or Decimal('0'))
                            total_cost += line_cost
                        ship_cost_used = True
            except Exception:
                pass
            if not ship_cost_used:
                for item in invoice.items or []:
                    if item.product_sku:
                        prod = self.db.query(Product).filter(Product.sku == item.product_sku).first()
                        if prod and prod.cost_price is not None:
                            total_cost += (item.quantity or Decimal('0')) * (prod.cost_price or Decimal('0'))
            if total_cost > 0:
                cogs_acc = self._get_required_account(settings.ACCOUNTS_COGS_CODE)
                inv_acc = self._get_required_account(settings.ACCOUNTS_INVENTORY_CODE)
                txn_number2 = f"TXN-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
                cogs_txn = Transaction(
                    transaction_number=txn_number2,
                    transaction_type=TransactionType.JOURNAL_ENTRY,
                    description=f"COGS for invoice {invoice.invoice_number}",
                    amount=total_cost,
                    debit_account_id=cogs_acc.id,
                    credit_account_id=inv_acc.id,
                    reference=invoice.invoice_number,
                    transaction_date=datetime.now(),
                    is_posted=False,
                    invoice_id=invoice.id,
                    period=period,
                )
                self.db.add(cogs_txn)
                self.db.flush()
                cogs_txn.debit_account.current_balance += total_cost
                cogs_txn.credit_account.current_balance -= total_cost
                cogs_txn.is_posted = True
                cogs_txn.posted_date = datetime.now()
                self.db.commit()
                self.db.refresh(invoice)
        return invoice

    # Payments posting
    def process_payment(self, payment_id: int) -> Payment:
        payment = self.db.query(Payment).filter(Payment.id == payment_id).first()
        if not payment:
            raise ValidationError("Payment not found")
        if payment.status == "completed":
            return payment

        invoice = self.db.query(Invoice).filter(Invoice.id == payment.invoice_id).first()
        if not invoice:
            raise ValidationError("Invoice not found for payment")

        period = invoice.accounting_period
        if self._current_period_locked(period):
            raise BusinessLogicError(f"Period {period} is locked")

        # Determine cash/bank account and counter-account (AR/AP)
        cash_acc = self._get_required_account(settings.ACCOUNTS_CASH_CODE)
        if invoice.invoice_type == InvoiceType.SALE:
            # Receipt: Debit Cash, Credit AR
            ar_acc = self._get_required_account(settings.ACCOUNTS_AR_CODE)
            debit_acc, credit_acc = cash_acc, ar_acc
            txn_type = TransactionType.RECEIPT
            desc = f"AR receipt for invoice {invoice.invoice_number}"
        else:
            # Disbursement: Debit AP, Credit Cash
            ap_acc = self._get_required_account(settings.ACCOUNTS_AP_CODE)
            debit_acc, credit_acc = ap_acc, cash_acc
            txn_type = TransactionType.PAYMENT
            desc = f"AP payment for invoice {invoice.invoice_number}"

        amount = payment.amount
        if not amount or amount <= 0:
            raise ValidationError("Payment amount must be > 0")

        txn_number = f"TXN-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
        txn = Transaction(
            transaction_number=txn_number,
            transaction_type=txn_type,
            description=desc,
            amount=amount,
            debit_account_id=debit_acc.id,
            credit_account_id=credit_acc.id,
            reference=payment.payment_number,
            transaction_date=payment.payment_date or datetime.now(),
            is_posted=False,
            invoice_id=invoice.id,
            period=period,
        )
        self.db.add(txn)
        self.db.flush()
        txn.debit_account.current_balance += amount
        txn.credit_account.current_balance -= amount
        txn.is_posted = True
        txn.posted_date = datetime.now()

        payment.status = "completed"
        payment.period = period
        self.db.commit()
        self.db.refresh(payment)
        return payment

    # Financial Statements
    def get_balance_sheet(self) -> Dict[str, Any]:
        assets = self.db.query(func.sum(Account.current_balance)).filter(Account.account_type == AccountType.ASSET).scalar() or Decimal('0.00')
        liabilities = self.db.query(func.sum(Account.current_balance)).filter(Account.account_type == AccountType.LIABILITY).scalar() or Decimal('0.00')
        equity = self.db.query(func.sum(Account.current_balance)).filter(Account.account_type == AccountType.EQUITY).scalar() or Decimal('0.00')
        return {
            'assets': assets,
            'liabilities': liabilities,
            'equity': equity,
        }

    def get_profit_and_loss(self, start: Optional[datetime] = None, end: Optional[datetime] = None) -> Dict[str, Any]:
        q = self.db.query(Account.account_type, func.sum(Account.current_balance)).group_by(Account.account_type)
        rows = {k: v or Decimal('0.00') for k, v in q}
        revenue = rows.get(AccountType.REVENUE, Decimal('0.00'))
        expenses = rows.get(AccountType.EXPENSE, Decimal('0.00'))
        return {
            'revenue': revenue,
            'expenses': expenses,
            'net_income': revenue - expenses,
        }

    def get_cash_flow(self, period: str = 'month') -> CashFlowSummary:
        return self.get_cash_flow_summary(period)

    # Period management
    def list_periods(self) -> List[AccountingPeriod]:
        return self.db.query(AccountingPeriod).order_by(AccountingPeriod.period.desc()).all()

    def close_period(self, period: str) -> AccountingPeriod:
        row = self.db.query(AccountingPeriod).filter(AccountingPeriod.period == period).first()
        now = datetime.now()
        if not row:
            row = AccountingPeriod(period=period, start_date=None, end_date=None)
            self.db.add(row)
        row.is_closed = True
        row.closed_at = now
        self.db.commit()
        self.db.refresh(row)
        return row

    def open_period(self, period: str) -> AccountingPeriod:
        row = self.db.query(AccountingPeriod).filter(AccountingPeriod.period == period).first()
        if not row:
            row = AccountingPeriod(period=period)
            self.db.add(row)
        row.is_closed = False
        row.closed_at = None
        self.db.commit()
        self.db.refresh(row)
        return row
    
    # Payment Management
    def get_payments(
        self,
        skip: int = 0,
        limit: int = 100,
        sort_by: Optional[str] = None,
        sort_dir: Optional[str] = None,
        **filters,
    ) -> Tuple[List[Payment], int]:
        """Get payments with optional filtering"""
        query = self.db.query(Payment)

        if filters.get("invoice_id"):
            query = query.filter(Payment.invoice_id == filters["invoice_id"])
        if filters.get("status"):
            query = query.filter(Payment.status == filters["status"])

        colmap = {
            "payment_date": Payment.payment_date,
            "amount": Payment.amount,
            "created_at": Payment.created_at,
        }
        col = colmap.get(sort_by or "payment_date")
        if sort_dir == "asc":
            query = query.order_by(col.asc())
        else:
            query = query.order_by(col.desc())

        total = query.count()
        payments = query.offset(skip).limit(limit).all()
        return payments, total

    def create_payment(self, payment_data: PaymentCreate) -> Payment:
        """Create a new payment"""
        try:
            # Validate invoice exists
            invoice = self.db.query(Invoice).filter(Invoice.id == payment_data.invoice_id).first()
            if not invoice:
                raise ValidationError("Invoice not found")
            
            # Generate payment number
            payment_number = f"PAY-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
            
            payment = Payment(
                **payment_data.dict(),
                payment_number=payment_number
            )
            
            self.db.add(payment)
            self.db.commit()
            self.db.refresh(payment)
            return payment
            
        except IntegrityError as e:
            self.db.rollback()
            raise ValidationError(f"Failed to create payment: {str(e)}")

    def update_payment(self, payment_id: int, data: PaymentUpdate) -> Optional[Payment]:
        payment = self.db.query(Payment).filter(Payment.id == payment_id).first()
        if not payment:
            return None
        if payment.status == "completed":
            raise BusinessLogicError("Cannot update a completed payment")
        for field, value in data.dict(exclude_unset=True).items():
            setattr(payment, field, value)
        self.db.commit()
        self.db.refresh(payment)
        return payment

    # Financial Reporting
    def get_financial_summary(self) -> FinancialSummary:
        """Get overall financial summary"""
        # Get account balances by type
        assets = self.db.query(func.sum(Account.current_balance)).filter(
            Account.account_type == AccountType.ASSET
        ).scalar() or Decimal('0.00')
        
        liabilities = self.db.query(func.sum(Account.current_balance)).filter(
            Account.account_type == AccountType.LIABILITY
        ).scalar() or Decimal('0.00')
        
        equity = self.db.query(func.sum(Account.current_balance)).filter(
            Account.account_type == AccountType.EQUITY
        ).scalar() or Decimal('0.00')
        
        revenue = self.db.query(func.sum(Account.current_balance)).filter(
            Account.account_type == AccountType.REVENUE
        ).scalar() or Decimal('0.00')
        
        expenses = self.db.query(func.sum(Account.current_balance)).filter(
            Account.account_type == AccountType.EXPENSE
        ).scalar() or Decimal('0.00')
        
        # Calculate derived values
        net_income = revenue - expenses
        
        # Get specific account balances
        cash_accounts = self.db.query(Account).filter(
            and_(Account.account_type == AccountType.ASSET, 
                 Account.category.in_([AccountCategory.CURRENT_ASSETS]))
        ).all()
        cash_balance = sum(acc.current_balance for acc in cash_accounts)
        
        return FinancialSummary(
            total_assets=assets,
            total_liabilities=liabilities,
            total_equity=equity,
            total_revenue=revenue,
            total_expenses=expenses,
            net_income=net_income,
            cash_balance=cash_balance,
            accounts_receivable=Decimal('0.00'),  # Would calculate from AR accounts
            accounts_payable=Decimal('0.00')      # Would calculate from AP accounts
        )
    
    def get_cash_flow_summary(self, period: str = "month") -> CashFlowSummary:
        """Get cash flow summary for a period"""
        now = datetime.now()
        if period == "day":
            start = datetime(now.year, now.month, now.day)
        elif period == "week":
            start = datetime(now.year, now.month, now.day) - timedelta(days=now.weekday())
        elif period == "month":
            start = datetime(now.year, now.month, 1)
        elif period == "quarter":
            q_month = (now.month - 1) // 3 * 3 + 1
            start = datetime(now.year, q_month, 1)
        elif period == "year":
            start = datetime(now.year, 1, 1)
        else:
            raise ValidationError("Invalid period")

        cash_accounts = self.db.query(Account).filter(
            and_(
                Account.account_type == AccountType.ASSET,
                Account.category == AccountCategory.CURRENT_ASSETS,
            )
        ).all()
        cash_balance = sum(acc.current_balance for acc in cash_accounts)

        txns = (
            self.db.query(Transaction)
            .filter(
                Transaction.transaction_date >= start,
                Transaction.transaction_type.in_(
                    [TransactionType.RECEIPT, TransactionType.PAYMENT]
                ),
            )
            .all()
        )
        cash_in = sum(t.amount for t in txns if t.transaction_type == TransactionType.RECEIPT)
        cash_out = sum(t.amount for t in txns if t.transaction_type == TransactionType.PAYMENT)
        opening_balance = cash_balance - (cash_in - cash_out)
        closing_balance = cash_balance

        return CashFlowSummary(
            period=period,
            opening_balance=opening_balance,
            cash_in=cash_in,
            cash_out=cash_out,
            closing_balance=closing_balance,
        )
    
    def get_financial_metrics(self) -> FinancialMetrics:
        """Calculate key financial ratios"""
        summary = self.get_financial_summary()
        
        # Calculate ratios (simplified)
        current_ratio = summary.total_assets / summary.total_liabilities if summary.total_liabilities > 0 else Decimal('0.00')
        quick_ratio = (summary.total_assets - summary.total_assets) / summary.total_liabilities if summary.total_liabilities > 0 else Decimal('0.00')
        debt_to_equity = summary.total_liabilities / summary.total_equity if summary.total_equity > 0 else Decimal('0.00')
        profit_margin = summary.net_income / summary.total_revenue if summary.total_revenue > 0 else Decimal('0.00')
        return_on_equity = summary.net_income / summary.total_equity if summary.total_equity > 0 else Decimal('0.00')
        
        return FinancialMetrics(
            current_ratio=current_ratio,
            quick_ratio=quick_ratio,
            debt_to_equity=debt_to_equity,
            profit_margin=profit_margin,
            return_on_equity=return_on_equity
        )
