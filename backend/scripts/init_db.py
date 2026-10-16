#!/usr/bin/env python3
"""
Database initialization script for ANKIIT ERP
Creates the database tables and seeds roles, an admin user and a starter chart of accounts.

Run from the backend/ directory:
    python scripts/init_db.py

The admin user is created from ADMIN_USERNAME / ADMIN_EMAIL / ADMIN_PASSWORD
(see config.env.example). It is skipped when ADMIN_PASSWORD is not set.
"""

import sys
from decimal import Decimal
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from app.core.config import settings
from app.core.database import SessionLocal, init_db
from app.models.finance import Account, AccountType, AccountCategory
from app.models.organization import Organization
from app.models.role import Role
from app.models.user import User


DEFAULT_ROLES = [
    {
        "name": "superuser",
        "display_name": "Super User",
        "description": "Full access to every module",
        "permissions": ["*"],
        "is_system_role": True,
    },
    {
        "name": "user",
        "display_name": "User",
        "description": "Default user role",
        "permissions": ["read:profile", "update:profile"],
        "is_system_role": True,
    },
]

# Codes for the accounts the finance service posts to come from settings (ACCOUNTS_*_CODE)
SAMPLE_ACCOUNTS = [
    (settings.ACCOUNTS_CASH_CODE, "Cash", "Cash on hand and in bank",
     AccountType.ASSET, AccountCategory.CURRENT_ASSETS, "10000.00"),
    (settings.ACCOUNTS_AR_CODE, "Accounts Receivable", "Amounts owed by customers",
     AccountType.ASSET, AccountCategory.CURRENT_ASSETS, "0.00"),
    (settings.ACCOUNTS_INVENTORY_CODE, "Inventory", "Stock on hand at cost",
     AccountType.ASSET, AccountCategory.CURRENT_ASSETS, "0.00"),
    ("1500_EQUIPMENT", "Equipment", "Office equipment and furniture",
     AccountType.ASSET, AccountCategory.FIXED_ASSETS, "5000.00"),
    (settings.ACCOUNTS_AP_CODE, "Accounts Payable", "Amounts owed to suppliers",
     AccountType.LIABILITY, AccountCategory.CURRENT_LIABILITIES, "0.00"),
    ("3000_EQUITY", "Owner's Equity", "Owner's investment in the business",
     AccountType.EQUITY, AccountCategory.OWNERS_EQUITY, "15000.00"),
    (settings.ACCOUNTS_REVENUE_CODE, "Sales Revenue", "Revenue from sales and services",
     AccountType.REVENUE, AccountCategory.OPERATING_REVENUE, "0.00"),
    (settings.ACCOUNTS_EXPENSE_CODE, "Operating Expenses", "General operating expenses",
     AccountType.EXPENSE, AccountCategory.OPERATING_EXPENSES, "0.00"),
    (settings.ACCOUNTS_COGS_CODE, "Cost of Goods Sold", "Cost of inventory sold",
     AccountType.EXPENSE, AccountCategory.OPERATING_EXPENSES, "0.00"),
]


def seed_roles(db) -> dict:
    roles = {}
    for spec in DEFAULT_ROLES:
        role = db.query(Role).filter(Role.name == spec["name"]).first()
        if role is None:
            role = Role(**spec)
            db.add(role)
            print(f"✓ Created role '{spec['name']}'")
        roles[spec["name"]] = role
    db.flush()
    return roles


def seed_admin(db, superuser_role: Role) -> None:
    if not settings.ADMIN_PASSWORD:
        print("• ADMIN_PASSWORD not set, skipping admin user")
        return
    existing = db.query(User).filter(
        (User.username == settings.ADMIN_USERNAME) | (User.email == settings.ADMIN_EMAIL)
    ).first()
    if existing:
        print(f"✓ Admin user '{existing.username}' already exists, skipping...")
        return

    organization = db.query(Organization).filter(Organization.slug == "ankiit-demo").first()
    if organization is None:
        organization = Organization(name="ANKIIT Demo", slug="ankiit-demo", email=settings.ADMIN_EMAIL)
        db.add(organization)
        db.flush()

    db.add(User(
        username=settings.ADMIN_USERNAME,
        email=settings.ADMIN_EMAIL,
        first_name="Admin",
        last_name="User",
        password=settings.ADMIN_PASSWORD,
        is_verified=True,
        organization_id=organization.id,
        role_id=superuser_role.id,
    ))
    print(f"✓ Created admin user '{settings.ADMIN_USERNAME}'")


def seed_accounts(db) -> None:
    if db.query(Account).count() > 0:
        print("✓ Accounts already exist, skipping...")
        return
    for code, name, description, account_type, category, balance in SAMPLE_ACCOUNTS:
        db.add(Account(
            code=code,
            name=name,
            description=description,
            account_type=account_type,
            category=category,
            is_active=True,
            opening_balance=Decimal(balance),
            current_balance=Decimal(balance),
        ))
    print(f"✓ Created {len(SAMPLE_ACCOUNTS)} sample accounts")


def init_database():
    """Initialize the database with tables and seed data"""
    print("Creating database tables...")
    init_db()
    print("✓ Database tables created successfully")

    db = SessionLocal()
    try:
        roles = seed_roles(db)
        seed_admin(db, roles["superuser"])
        seed_accounts(db)
        db.commit()
    except Exception as e:
        print(f"❌ Error creating seed data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def main():
    """Main function"""
    print("ANKIIT ERP Database Initialization")
    print("=" * 40)

    try:
        init_database()
        print("\n🎉 Database initialization completed successfully!")
        print("\nYou can now start the application with:")
        print("  uvicorn main:app --reload --port 8000")

    except Exception as e:
        print(f"\n❌ Database initialization failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
