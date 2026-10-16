from decimal import Decimal
from typing import Dict, Optional

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.org_scope import get_session_organization, set_session_organization
from app.models.finance import Account, AccountCategory, AccountType

# Starter chart of accounts for a new organization. The accounts the finance service
# posts to are keyed by the ACCOUNTS_*_CODE settings.
DEFAULT_ACCOUNTS = [
    (settings.ACCOUNTS_CASH_CODE, "Cash", "Cash on hand and in bank",
     AccountType.ASSET, AccountCategory.CURRENT_ASSETS),
    (settings.ACCOUNTS_AR_CODE, "Accounts Receivable", "Amounts owed by customers",
     AccountType.ASSET, AccountCategory.CURRENT_ASSETS),
    (settings.ACCOUNTS_INVENTORY_CODE, "Inventory", "Stock on hand at cost",
     AccountType.ASSET, AccountCategory.CURRENT_ASSETS),
    ("1500_EQUIPMENT", "Equipment", "Office equipment and furniture",
     AccountType.ASSET, AccountCategory.FIXED_ASSETS),
    (settings.ACCOUNTS_AP_CODE, "Accounts Payable", "Amounts owed to suppliers",
     AccountType.LIABILITY, AccountCategory.CURRENT_LIABILITIES),
    ("3000_EQUITY", "Owner's Equity", "Owner's investment in the business",
     AccountType.EQUITY, AccountCategory.OWNERS_EQUITY),
    (settings.ACCOUNTS_REVENUE_CODE, "Sales Revenue", "Revenue from sales and services",
     AccountType.REVENUE, AccountCategory.OPERATING_REVENUE),
    (settings.ACCOUNTS_EXPENSE_CODE, "Operating Expenses", "General operating expenses",
     AccountType.EXPENSE, AccountCategory.OPERATING_EXPENSES),
    (settings.ACCOUNTS_COGS_CODE, "Cost of Goods Sold", "Cost of inventory sold",
     AccountType.EXPENSE, AccountCategory.OPERATING_EXPENSES),
]


def create_default_chart_of_accounts(
    db: Session,
    organization_id: int,
    opening_balances: Optional[Dict[str, Decimal]] = None,
) -> int:
    """Add the starter accounts to an organization that has none. Returns how many were added."""
    previous = get_session_organization(db)
    set_session_organization(db, organization_id)
    try:
        if db.query(Account).count() > 0:
            return 0
        balances = opening_balances or {}
        for code, name, description, account_type, category in DEFAULT_ACCOUNTS:
            balance = balances.get(code, Decimal("0.00"))
            db.add(Account(
                code=code,
                name=name,
                description=description,
                account_type=account_type,
                category=category,
                is_active=True,
                opening_balance=balance,
                current_balance=balance,
            ))
        db.flush()
        return len(DEFAULT_ACCOUNTS)
    finally:
        set_session_organization(db, previous)
