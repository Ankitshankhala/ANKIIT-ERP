#!/usr/bin/env python3
"""
Database initialization script for ANKIIT ERP
This script creates the database tables and populates them with initial data.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models import Base
from app.models.finance import Account, AccountType, AccountCategory
from app.core.security import get_password_hash

def init_database():
    """Initialize the database with tables and sample data"""
    
    # Create database engine
    engine = create_engine(settings.DATABASE_URL)
    
    # Create all tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully")
    
    # Create session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if accounts already exist
        existing_accounts = db.query(Account).count()
        if existing_accounts > 0:
            print("✓ Sample accounts already exist, skipping...")
            return
        
        # Create sample chart of accounts
        print("Creating sample chart of accounts...")
        
        # Asset accounts
        cash_account = Account(
            code="1000",
            name="Cash",
            description="Cash on hand and in bank",
            account_type=AccountType.ASSET,
            category=AccountCategory.CURRENT_ASSETS,
            is_active=True,
            opening_balance=10000.00,
            current_balance=10000.00
        )
        
        accounts_receivable = Account(
            code="1100",
            name="Accounts Receivable",
            description="Amounts owed by customers",
            account_type=AccountType.ASSET,
            category=AccountCategory.CURRENT_ASSETS,
            is_active=True,
            opening_balance=0.00,
            current_balance=0.00
        )
        
        equipment_account = Account(
            code="1500",
            name="Equipment",
            description="Office equipment and furniture",
            account_type=AccountType.ASSET,
            category=AccountCategory.FIXED_ASSETS,
            is_active=True,
            opening_balance=5000.00,
            current_balance=5000.00
        )
        
        # Liability accounts
        accounts_payable = Account(
            code="2000",
            name="Accounts Payable",
            description="Amounts owed to suppliers",
            account_type=AccountType.LIABILITY,
            category=AccountCategory.CURRENT_LIABILITIES,
            is_active=True,
            opening_balance=0.00,
            current_balance=0.00
        )
        
        # Equity accounts
        owner_equity = Account(
            code="3000",
            name="Owner's Equity",
            description="Owner's investment in the business",
            account_type=AccountType.EQUITY,
            category=AccountCategory.OWNERS_EQUITY,
            is_active=True,
            opening_balance=15000.00,
            current_balance=15000.00
        )
        
        # Revenue accounts
        service_revenue = Account(
            code="4000",
            name="Service Revenue",
            description="Revenue from consulting services",
            account_type=AccountType.REVENUE,
            category=AccountCategory.OPERATING_REVENUE,
            is_active=True,
            opening_balance=0.00,
            current_balance=0.00
        )
        
        # Expense accounts
        office_supplies = Account(
            code="5000",
            name="Office Supplies",
            description="Office supplies and materials",
            account_type=AccountType.EXPENSE,
            category=AccountCategory.OPERATING_EXPENSES,
            is_active=True,
            opening_balance=0.00,
            current_balance=0.00
        )
        
        utilities_expense = Account(
            code="5100",
            name="Utilities",
            description="Electricity, water, internet, etc.",
            account_type=AccountType.EXPENSE,
            category=AccountCategory.OPERATING_EXPENSES,
            is_active=True,
            opening_balance=0.00,
            current_balance=0.00
        )
        
        # Add all accounts to session
        accounts = [
            cash_account,
            accounts_receivable,
            equipment_account,
            accounts_payable,
            owner_equity,
            service_revenue,
            office_supplies,
            utilities_expense
        ]
        
        for account in accounts:
            db.add(account)
        
        # Commit the changes
        db.commit()
        print(f"✓ Created {len(accounts)} sample accounts")
        
        # Verify the accounts were created
        total_accounts = db.query(Account).count()
        print(f"✓ Total accounts in database: {total_accounts}")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
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
        print("  uvicorn app.main:app --reload --port 8000")
        
    except Exception as e:
        print(f"\n❌ Database initialization failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
