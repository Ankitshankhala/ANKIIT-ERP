from typing import Optional, List
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, Field, validator
from .common import PaginationParams

# Account Schemas
class AccountBase(BaseModel):
    code: str = Field(..., min_length=1, max_length=20, description="Account code")
    name: str = Field(..., min_length=1, max_length=100, description="Account name")
    description: Optional[str] = Field(None, max_length=500, description="Account description")
    account_type: str = Field(..., description="Account type (asset, liability, equity, revenue, expense)")
    category: str = Field(..., description="Account category")
    parent_account_id: Optional[int] = Field(None, description="Parent account ID for hierarchical structure")
    is_active: bool = Field(True, description="Whether the account is active")
    opening_balance: Decimal = Field(Decimal('0.00'), ge=Decimal('0.00'), description="Opening balance")

class AccountCreate(AccountBase):
    pass

class AccountUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    category: Optional[str] = Field(None)
    is_active: Optional[bool] = Field(None)
    opening_balance: Optional[Decimal] = Field(None, ge=Decimal('0.00'))

class AccountResponse(AccountBase):
    id: int
    current_balance: Decimal
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class AccountList(BaseModel):
    accounts: List[AccountResponse]
    total: int
    page: int
    size: int

# Transaction Schemas
class TransactionBase(BaseModel):
    transaction_type: str = Field(..., description="Transaction type")
    description: str = Field(..., min_length=1, max_length=500, description="Transaction description")
    amount: Decimal = Field(..., gt=Decimal('0.00'), description="Transaction amount")
    debit_account_id: int = Field(..., description="Debit account ID")
    credit_account_id: int = Field(..., description="Credit account ID")
    reference: Optional[str] = Field(None, max_length=100, description="Reference number")
    transaction_date: datetime = Field(default_factory=datetime.now, description="Transaction date")

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    amount: Optional[Decimal] = Field(None, gt=Decimal('0.00'))
    reference: Optional[str] = Field(None, max_length=100)
    transaction_date: Optional[datetime] = Field(None)

class TransactionResponse(TransactionBase):
    id: int
    transaction_number: str
    is_posted: bool
    posted_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class TransactionList(BaseModel):
    transactions: List[TransactionResponse]
    total: int
    page: int
    size: int

# Invoice Schemas
class InvoiceLineItemBase(BaseModel):
    description: str = Field(..., min_length=1, max_length=255)
    quantity: Decimal = Field(..., ge=Decimal('0'))
    unit_price: Decimal = Field(..., ge=Decimal('0'))
    discount_amount: Decimal = Field(Decimal('0.00'), ge=Decimal('0.00'))
    tax_rate: Decimal = Field(Decimal('0.0000'), ge=Decimal('0.00'))

class InvoiceLineItemCreate(InvoiceLineItemBase):
    product_sku: Optional[str] = Field(None, max_length=64)

class InvoiceLineItemResponse(InvoiceLineItemBase):
    id: int
    tax_amount: Decimal
    line_total: Decimal
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class InvoiceBase(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=200, description="Customer name")
    customer_email: Optional[str] = Field(None, max_length=200, description="Customer email")
    customer_address: Optional[str] = Field(None, max_length=1000, description="Customer address")
    invoice_date: datetime = Field(default_factory=datetime.now, description="Invoice date")
    due_date: datetime = Field(..., description="Due date")
    invoice_type: str = Field("sale", description="Invoice type: sale (AR) or purchase (AP)")
    notes: Optional[str] = Field(None, max_length=1000, description="Invoice notes")

class InvoiceCreate(InvoiceBase):
    items: List[InvoiceLineItemCreate]

class InvoiceUpdate(BaseModel):
    customer_name: Optional[str] = Field(None, min_length=1, max_length=200)
    customer_email: Optional[str] = Field(None, max_length=200)
    customer_address: Optional[str] = Field(None, max_length=1000)
    due_date: Optional[datetime] = Field(None)
    subtotal: Optional[Decimal] = Field(None, ge=Decimal('0.00'))
    tax_amount: Optional[Decimal] = Field(None, ge=Decimal('0.00'))
    total_amount: Optional[Decimal] = Field(None, ge=Decimal('0.00'))
    notes: Optional[str] = Field(None, max_length=1000)

class InvoiceResponse(InvoiceBase):
    id: int
    invoice_number: str
    status: str
    subtotal: Decimal
    discount_total: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    paid_amount: Decimal
    balance_due: Decimal
    is_paid: bool
    items: List[InvoiceLineItemResponse]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class InvoiceList(BaseModel):
    invoices: List[InvoiceResponse]
    total: int
    page: int
    size: int

# Payment Schemas
class PaymentBase(BaseModel):
    invoice_id: int = Field(..., description="Invoice ID")
    amount: Decimal = Field(..., gt=Decimal('0.00'), description="Payment amount")
    payment_method: str = Field(..., description="Payment method")
    payment_date: datetime = Field(default_factory=datetime.now, description="Payment date")
    reference: Optional[str] = Field(None, max_length=100, description="Payment reference")
    notes: Optional[str] = Field(None, max_length=500, description="Payment notes")

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    amount: Optional[Decimal] = Field(None, gt=Decimal('0.00'))
    payment_method: Optional[str] = Field(None)
    payment_date: Optional[datetime] = Field(None)
    reference: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = Field(None, max_length=500)

class PaymentResponse(PaymentBase):
    id: int
    payment_number: str
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class PaymentList(BaseModel):
    payments: List[PaymentResponse]
    total: int
    page: int
    size: int

# Financial Dashboard Schemas
class FinancialSummary(BaseModel):
    total_assets: Decimal
    total_liabilities: Decimal
    total_equity: Decimal
    total_revenue: Decimal
    total_expenses: Decimal
    net_income: Decimal
    cash_balance: Decimal
    accounts_receivable: Decimal
    accounts_payable: Decimal

class CashFlowSummary(BaseModel):
    period: str
    opening_balance: Decimal
    cash_in: Decimal
    cash_out: Decimal
    closing_balance: Decimal

class FinancialMetrics(BaseModel):
    current_ratio: Decimal
    quick_ratio: Decimal
    debt_to_equity: Decimal
    profit_margin: Decimal
    return_on_equity: Decimal

# Query Parameters
class AccountQueryParams(PaginationParams):
    account_type: Optional[str] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None
    parent_account_id: Optional[int] = None

class TransactionQueryParams(PaginationParams):
    transaction_type: Optional[str] = None
    account_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_posted: Optional[bool] = None

class InvoiceQueryParams(PaginationParams):
    status: Optional[str] = None
    customer_name: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_paid: Optional[bool] = None
