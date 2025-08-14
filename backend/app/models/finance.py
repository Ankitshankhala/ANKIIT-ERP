from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from decimal import Decimal
import enum
from .base import BaseModel, Base

class AccountType(str, enum.Enum):
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    REVENUE = "revenue"
    EXPENSE = "expense"

class AccountCategory(str, enum.Enum):
    CURRENT_ASSETS = "current_assets"
    FIXED_ASSETS = "fixed_assets"
    CURRENT_LIABILITIES = "current_liabilities"
    LONG_TERM_LIABILITIES = "long_term_liabilities"
    OWNERS_EQUITY = "owners_equity"
    OPERATING_REVENUE = "operating_revenue"
    OPERATING_EXPENSES = "operating_expenses"
    NON_OPERATING = "non_operating"

class TransactionType(str, enum.Enum):
    SALE = "sale"
    PURCHASE = "purchase"
    PAYMENT = "payment"
    RECEIPT = "receipt"
    TRANSFER = "transfer"
    ADJUSTMENT = "adjustment"
    JOURNAL_ENTRY = "journal_entry"

class InvoiceStatus(str, enum.Enum):
    DRAFT = "draft"
    SENT = "sent"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class InvoiceType(str, enum.Enum):
    SALE = "sale"       # AR
    PURCHASE = "purchase"  # AP

class PaymentMethod(str, enum.Enum):
    CASH = "cash"
    BANK_TRANSFER = "bank_transfer"
    CREDIT_CARD = "credit_card"
    CHECK = "check"
    DIGITAL_WALLET = "digital_wallet"

class Account(BaseModel, Base):
    __tablename__ = "accounts"
    
    code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    account_type = Column(Enum(AccountType), nullable=False)
    category = Column(Enum(AccountCategory), nullable=False)
    parent_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    opening_balance = Column(Numeric(15, 2), default=Decimal('0.00'))
    current_balance = Column(Numeric(15, 2), default=Decimal('0.00'))
    is_locked = Column(Boolean, default=False)
    
    # Relationships
    parent_account = relationship("Account", remote_side=[id], backref="sub_accounts")
    transactions = relationship("Transaction", backref="account")
    
    def __repr__(self):
        return f"<Account(code='{self.code}', name='{self.name}', type='{self.account_type}')>"
    
    @property
    def full_name(self):
        if self.parent_account:
            return f"{self.parent_account.full_name} > {self.name}"
        return self.name

class Transaction(BaseModel, Base):
    __tablename__ = "transactions"
    
    transaction_number = Column(String(50), unique=True, nullable=False, index=True)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    description = Column(Text, nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    debit_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    credit_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    reference = Column(String(100), nullable=True)
    transaction_date = Column(DateTime, nullable=False, default=func.now())
    is_posted = Column(Boolean, default=False)
    posted_date = Column(DateTime, nullable=True)
    period = Column(String(7), nullable=True, index=True)  # e.g., 2025-08
    
    # Relationships
    debit_account = relationship("Account", foreign_keys=[debit_account_id])
    credit_account = relationship("Account", foreign_keys=[credit_account_id])
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=True)
    invoice = relationship("Invoice", back_populates="transactions", uselist=False)
    
    def __repr__(self):
        return f"<Transaction(number='{self.transaction_number}', amount={self.amount}, type='{self.transaction_type}')>"
    
    def post_transaction(self):
        """Post the transaction and update account balances"""
        if self.is_posted:
            return
        
        # Update account balances
        self.debit_account.current_balance += self.amount
        self.credit_account.current_balance -= self.amount
        
        self.is_posted = True
        self.posted_date = func.now()

class Invoice(BaseModel, Base):
    __tablename__ = "invoices"
    
    invoice_number = Column(String(50), unique=True, nullable=False, index=True)
    customer_name = Column(String(200), nullable=False)
    customer_email = Column(String(200), nullable=True)
    customer_address = Column(Text, nullable=True)
    invoice_date = Column(DateTime, nullable=False, default=func.now())
    due_date = Column(DateTime, nullable=False)
    subtotal = Column(Numeric(15, 2), nullable=False, default=Decimal('0.00'))
    discount_total = Column(Numeric(15, 2), nullable=False, default=Decimal('0.00'))
    tax_amount = Column(Numeric(15, 2), nullable=False, default=Decimal('0.00'))
    total_amount = Column(Numeric(15, 2), nullable=False, default=Decimal('0.00'))
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.DRAFT)
    notes = Column(Text, nullable=True)
    invoice_type = Column(Enum(InvoiceType), default=InvoiceType.SALE, nullable=False)
    
    # Relationships
    transactions = relationship("Transaction", back_populates="invoice")
    payments = relationship("Payment", back_populates="invoice")
    items = relationship("InvoiceLineItem", back_populates="invoice", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Invoice(number='{self.invoice_number}', customer='{self.customer_name}', amount={self.total_amount})>"
    
    @property
    def paid_amount(self):
        return sum(payment.amount for payment in self.payments if payment.status == "completed")
    
    @property
    def balance_due(self):
        return self.total_amount - self.paid_amount
    
    @property
    def is_paid(self):
        return self.balance_due <= 0
    
    def calculate_totals(self):
        """Calculate invoice totals from line items"""
        subtotal = Decimal('0.00')
        tax_total = Decimal('0.00')
        discount_total = Decimal('0.00')
        for item in getattr(self, 'items', []) or []:
            line_base = (item.quantity or Decimal('0')) * (item.unit_price or Decimal('0'))
            discount = item.discount_amount or Decimal('0')
            taxable_base = line_base - discount
            line_tax = (taxable_base * (item.tax_rate or Decimal('0'))) if item.tax_rate else Decimal('0')
            subtotal += taxable_base
            tax_total += line_tax
            discount_total += discount
            item.tax_amount = line_tax
            item.line_total = taxable_base + line_tax
        self.subtotal = subtotal
        self.discount_total = discount_total
        self.tax_amount = tax_total
        self.total_amount = subtotal + tax_total

    @property
    def accounting_period(self) -> str:
        # YYYY-MM from invoice_date
        dt = self.invoice_date
        return f"{dt.year:04d}-{dt.month:02d}"

class Payment(BaseModel, Base):
    __tablename__ = "payments"
    
    payment_number = Column(String(50), unique=True, nullable=False, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    payment_date = Column(DateTime, nullable=False, default=func.now())
    reference = Column(String(100), nullable=True)
    status = Column(String(20), default="pending")  # pending, completed, failed, cancelled
    notes = Column(Text, nullable=True)
    period = Column(String(7), nullable=True, index=True)
    
    # Relationships
    invoice = relationship("Invoice", back_populates="payments")
    
    def __repr__(self):
        return f"<Payment(number='{self.payment_number}', amount={self.amount}, method='{self.payment_method}')>"
    
    def process_payment(self):
        """Process the payment and update related records"""
        if self.status == "completed":
            return
        
        # Create transaction for the payment
        # This would be implemented in a service layer
        self.status = "completed"


class InvoiceLineItem(BaseModel, Base):
    __tablename__ = "invoice_line_items"

    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False, index=True)
    product_sku = Column(String(64), nullable=True)
    description = Column(String(255), nullable=False)
    quantity = Column(Numeric(15, 4), nullable=False, default=Decimal('0.0000'))
    unit_price = Column(Numeric(15, 2), nullable=False, default=Decimal('0.00'))
    discount_amount = Column(Numeric(15, 2), nullable=False, default=Decimal('0.00'))
    tax_rate = Column(Numeric(6, 4), nullable=False, default=Decimal('0.0000'))  # e.g. 0.1000 = 10%
    tax_amount = Column(Numeric(15, 2), nullable=False, default=Decimal('0.00'))
    line_total = Column(Numeric(15, 2), nullable=False, default=Decimal('0.00'))

    invoice = relationship("Invoice", back_populates="items")


class AccountingPeriod(BaseModel, Base):
    __tablename__ = "accounting_periods"

    # Period in format YYYY-MM
    period = Column(String(7), unique=True, nullable=False, index=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    is_closed = Column(Boolean, default=False, nullable=False)
    closed_at = Column(DateTime, nullable=True)
