from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from decimal import Decimal

from ....core.database import get_db
from ....core.security import get_current_active_user, require_permission
from ....models.user import User
from ....services.finance_service import FinanceService
from ....schemas.finance import (
    AccountCreate, AccountUpdate, AccountResponse, AccountList, AccountQueryParams,
    TransactionCreate, TransactionUpdate, TransactionResponse, TransactionList, TransactionQueryParams,
    InvoiceCreate, InvoiceUpdate, InvoiceResponse, InvoiceList, InvoiceQueryParams,
    PaymentCreate, PaymentUpdate, PaymentResponse, PaymentList,
    FinancialSummary, CashFlowSummary, FinancialMetrics
)
from ....core.exceptions import BusinessLogicError, ValidationError

router = APIRouter()

# Account Endpoints
@router.post("/accounts", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
async def create_account(
    account_data: AccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("finance:account:create"))
):
    """Create a new account"""
    try:
        finance_service = FinanceService(db)
        return finance_service.create_account(account_data)
    except (BusinessLogicError, ValidationError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/accounts", response_model=AccountList)
async def get_accounts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    account_type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    parent_account_id: Optional[int] = Query(None),
    sort_by: Optional[str] = Query(None),
    sort_dir: Optional[str] = Query("desc"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("finance:account:read"))
):
    """Get accounts with optional filtering"""
    finance_service = FinanceService(db)
    accounts = finance_service.get_accounts(
        skip=skip, 
        limit=limit,
        account_type=account_type,
        category=category,
        is_active=is_active,
        parent_account_id=parent_account_id,
        sort_by=sort_by,
        sort_dir=sort_dir
    )
    
    # Get total count for pagination
    total = len(accounts)  # Simplified - in production, you'd use a separate count query
    
    return AccountList(
        accounts=accounts,
        total=total,
        page=skip // limit + 1,
        size=limit
    )

@router.get("/accounts/{account_id}", response_model=AccountResponse)
async def get_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("finance:account:read"))
):
    """Get account by ID"""
    finance_service = FinanceService(db)
    account = finance_service.get_account(account_id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return account

@router.put("/accounts/{account_id}", response_model=AccountResponse)
async def update_account(
    account_id: int,
    account_data: AccountUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("finance:account:update"))
):
    """Update account"""
    finance_service = FinanceService(db)
    account = finance_service.update_account(account_id, account_data)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return account

@router.delete("/accounts/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("finance:account:delete"))
):
    """Delete account"""
    try:
        finance_service = FinanceService(db)
        success = finance_service.delete_account(account_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    except BusinessLogicError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Transaction Endpoints
@router.post("/transactions", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_data: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("finance:transaction:create"))
):
    """Create a new transaction"""
    try:
        finance_service = FinanceService(db)
        return finance_service.create_transaction(transaction_data)
    except (BusinessLogicError, ValidationError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/transactions/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: int,
    payload: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("finance:transaction:update"))
):
    svc = FinanceService(db)
    try:
        txn = svc.update_transaction(transaction_id, payload)
        if not txn:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
        return txn
    except (BusinessLogicError, ValidationError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/transactions/{transaction_id}/post", response_model=TransactionResponse)
async def post_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("finance:transaction:post"))
):
    """Post a transaction and update account balances"""
    try:
        finance_service = FinanceService(db)
        return finance_service.post_transaction(transaction_id)
    except (BusinessLogicError, ValidationError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/transactions", response_model=TransactionList)
async def get_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    transaction_type: Optional[str] = Query(None),
    account_id: Optional[int] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    is_posted: Optional[bool] = Query(None),
    sort_by: Optional[str] = Query(None),
    sort_dir: Optional[str] = Query("desc"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("finance:transaction:read"))
):
    """Get transactions with optional filtering"""
    finance_service = FinanceService(db)
    transactions = finance_service.get_transactions(
        skip=skip,
        limit=limit,
        transaction_type=transaction_type,
        account_id=account_id,
        start_date=start_date,
        end_date=end_date,
        is_posted=is_posted,
        sort_by=sort_by,
        sort_dir=sort_dir
    )
    
    total = len(transactions)  # Simplified count
    
    return TransactionList(
        transactions=transactions,
        total=total,
        page=skip // limit + 1,
        size=limit
    )

@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("finance:transaction:read"))
):
    """Get transaction by ID"""
    finance_service = FinanceService(db)
    transaction = finance_service.get_transactions(limit=1, **{"id": transaction_id})
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transaction[0]

# Invoice Endpoints
@router.post("/invoices", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
async def create_invoice(
    invoice_data: InvoiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("finance:invoice:create"))
):
    """Create a new invoice"""
    try:
        finance_service = FinanceService(db)
        return finance_service.create_invoice(invoice_data)
    except (BusinessLogicError, ValidationError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/invoices", response_model=InvoiceList)
async def get_invoices(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None),
    customer_name: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    is_paid: Optional[bool] = Query(None),
    sort_by: Optional[str] = Query(None),
    sort_dir: Optional[str] = Query("desc"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("finance:invoice:read"))
):
    """Get invoices with optional filtering"""
    finance_service = FinanceService(db)
    invoices = finance_service.get_invoices(
        skip=skip,
        limit=limit,
        status=status,
        customer_name=customer_name,
        start_date=start_date,
        end_date=end_date,
        is_paid=is_paid,
        sort_by=sort_by,
        sort_dir=sort_dir
    )
    
    total = len(invoices)  # Simplified count
    
    return InvoiceList(
        invoices=invoices,
        total=total,
        page=skip // limit + 1,
        size=limit
    )

@router.get("/invoices/{invoice_id}", response_model=InvoiceResponse)
async def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("finance:invoice:read"))
):
    """Get invoice by ID"""
    finance_service = FinanceService(db)
    invoices = finance_service.get_invoices(limit=1, **{"id": invoice_id})
    if not invoices:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    return invoices[0]

@router.put("/invoices/{invoice_id}", response_model=InvoiceResponse)
async def update_invoice(
    invoice_id: int,
    invoice_data: InvoiceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("finance:invoice:update"))
):
    """Update invoice header fields"""
    svc = FinanceService(db)
    inv = svc.update_invoice(invoice_id, invoice_data)
    if not inv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    return inv

@router.put("/invoices/{invoice_id}/status")
async def update_invoice_status(
    invoice_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("finance:invoice:update"))
):
    """Update invoice status"""
    try:
        finance_service = FinanceService(db)
        return finance_service.update_invoice_status(invoice_id, status)
    except (BusinessLogicError, ValidationError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/invoices/{invoice_id}/post", response_model=InvoiceResponse)
async def post_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("finance:invoice:post"))
):
    """Post an invoice to GL (creates accounting transactions)."""
    try:
        finance_service = FinanceService(db)
        return finance_service.post_invoice(invoice_id)
    except (BusinessLogicError, ValidationError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Payment Endpoints
@router.post("/payments", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(
    payment_data: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("finance:payment:create"))
):
    """Create a new payment"""
    try:
        finance_service = FinanceService(db)
        return finance_service.create_payment(payment_data)
    except (BusinessLogicError, ValidationError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/payments/{payment_id}", response_model=PaymentResponse)
async def update_payment(
    payment_id: int,
    payload: PaymentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("finance:payment:update"))
):
    svc = FinanceService(db)
    try:
        payment = svc.update_payment(payment_id, payload)
        if not payment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
        return payment
    except (BusinessLogicError, ValidationError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/payments/{payment_id}/process", response_model=PaymentResponse)
async def process_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("finance:payment:process"))
):
    """Process a payment"""
    try:
        finance_service = FinanceService(db)
        return finance_service.process_payment(payment_id)
    except (BusinessLogicError, ValidationError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/payments", response_model=PaymentList)
async def get_payments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    sort_by: Optional[str] = Query(None),
    sort_dir: Optional[str] = Query("desc"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("finance:payment:read"))
):
    """Get payments"""
    finance_service = FinanceService(db)
    payments, total = finance_service.get_payments(
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_dir=sort_dir,
    )
    return PaymentList(
        payments=payments,
        total=total,
        page=skip // limit + 1,
        size=limit,
    )

# Financial Reporting Endpoints
@router.get("/reports/summary", response_model=FinancialSummary)
async def get_financial_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("finance:report:read"))
):
    """Get financial summary"""
    finance_service = FinanceService(db)
    return finance_service.get_financial_summary()

@router.get("/reports/cash-flow", response_model=CashFlowSummary)
async def get_cash_flow_summary(
    period: str = Query("month", description="Period for cash flow (day, week, month, quarter, year)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("finance:report:read"))
):
    """Get cash flow summary"""
    finance_service = FinanceService(db)
    return finance_service.get_cash_flow_summary(period)

@router.get("/reports/metrics", response_model=FinancialMetrics)
async def get_financial_metrics(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("finance:report:read"))
):
    """Get financial metrics and ratios"""
    finance_service = FinanceService(db)
    return finance_service.get_financial_metrics()

@router.get("/reports/balance-sheet")
async def get_balance_sheet(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("finance:report:read"))
):
    svc = FinanceService(db)
    return svc.get_balance_sheet()

@router.get("/reports/profit-and-loss")
async def get_profit_and_loss(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("finance:report:read"))
):
    svc = FinanceService(db)
    return svc.get_profit_and_loss()

# Accounting Periods
@router.get("/periods")
async def list_periods(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("finance:period:read"))
):
    svc = FinanceService(db)
    return svc.list_periods()

@router.post("/periods/{period}/close")
async def close_period(
    period: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("finance:period:close"))
):
    svc = FinanceService(db)
    try:
        return svc.close_period(period)
    except (BusinessLogicError, ValidationError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/periods/{period}/open")
async def open_period(
    period: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("finance:period:open"))
):
    svc = FinanceService(db)
    try:
        return svc.open_period(period)
    except (BusinessLogicError, ValidationError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
