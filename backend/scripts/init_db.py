#!/usr/bin/env python3
"""
Database initialization script for ANKIIT ERP
Creates the database tables and seeds roles, a demo organization with an admin user,
and that organization's starter chart of accounts.

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
from app.models.organization import Organization
from app.models.role import Role
from app.models.user import User
from app.services.organization_setup import create_default_chart_of_accounts


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

# Opening balances for the demo organization's starter accounts
DEMO_OPENING_BALANCES = {
    settings.ACCOUNTS_CASH_CODE: Decimal("10000.00"),
    "1500_EQUIPMENT": Decimal("5000.00"),
    "3000_EQUITY": Decimal("15000.00"),
}


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


def seed_demo_organization(db) -> Organization:
    organization = db.query(Organization).filter(Organization.slug == "ankiit-demo").first()
    if organization is None:
        organization = Organization(name="ANKIIT Demo", slug="ankiit-demo", email=settings.ADMIN_EMAIL)
        db.add(organization)
        db.flush()
        print("✓ Created organization 'ANKIIT Demo'")
    return organization


def seed_admin(db, superuser_role: Role, organization: Organization) -> None:
    if not settings.ADMIN_PASSWORD:
        print("• ADMIN_PASSWORD not set, skipping admin user")
        return
    existing = db.query(User).filter(
        (User.username == settings.ADMIN_USERNAME) | (User.email == settings.ADMIN_EMAIL)
    ).first()
    if existing:
        print(f"✓ Admin user '{existing.username}' already exists, skipping...")
        return

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


def seed_accounts(db, organization: Organization) -> None:
    created = create_default_chart_of_accounts(db, organization.id, DEMO_OPENING_BALANCES)
    if created:
        print(f"✓ Created {created} starter accounts for '{organization.name}'")
    else:
        print("✓ Accounts already exist, skipping...")


def init_database():
    """Initialize the database with tables and seed data"""
    print("Creating database tables...")
    init_db()
    print("✓ Database tables created successfully")

    db = SessionLocal()
    try:
        roles = seed_roles(db)
        organization = seed_demo_organization(db)
        seed_admin(db, roles["superuser"], organization)
        seed_accounts(db, organization)
        db.commit()
    except Exception as e:
        print(f"❌ Error creating seed data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def main():
    """Main function"""
    # Windows consoles (cp1252) cannot encode the status symbols; don't crash over them
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
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
