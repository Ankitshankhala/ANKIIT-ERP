"""Create finance tables

Revision ID: 001
Revises: 
Create Date: 2024-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create accounts table
    op.create_table('accounts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=20), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('account_type', sa.Enum('asset', 'liability', 'equity', 'revenue', 'expense', name='accounttype'), nullable=False),
        sa.Column('category', sa.Enum('current_assets', 'fixed_assets', 'current_liabilities', 'long_term_liabilities', 'owners_equity', 'operating_revenue', 'operating_expenses', 'non_operating', name='accountcategory'), nullable=False),
        sa.Column('parent_account_id', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('opening_balance', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('current_balance', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['parent_account_id'], ['accounts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_accounts_code'), 'accounts', ['code'], unique=True)
    op.create_index(op.f('ix_accounts_id'), 'accounts', ['id'], unique=False)

    # Create transactions table
    op.create_table('transactions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('transaction_number', sa.String(length=50), nullable=False),
        sa.Column('transaction_type', sa.Enum('sale', 'purchase', 'payment', 'receipt', 'transfer', 'adjustment', 'journal_entry', name='transactiontype'), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('amount', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('debit_account_id', sa.Integer(), nullable=False),
        sa.Column('credit_account_id', sa.Integer(), nullable=False),
        sa.Column('reference', sa.String(length=100), nullable=True),
        sa.Column('transaction_date', sa.DateTime(), nullable=False),
        sa.Column('is_posted', sa.Boolean(), nullable=True),
        sa.Column('posted_date', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['credit_account_id'], ['accounts.id'], ),
        sa.ForeignKeyConstraint(['debit_account_id'], ['accounts.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transactions_id'), 'transactions', ['id'], unique=False)
    op.create_index(op.f('ix_transactions_transaction_number'), 'transactions', ['transaction_number'], unique=True)

    # Create invoices table
    op.create_table('invoices',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('invoice_number', sa.String(length=50), nullable=False),
        sa.Column('customer_name', sa.String(length=200), nullable=False),
        sa.Column('customer_email', sa.String(length=200), nullable=True),
        sa.Column('customer_address', sa.Text(), nullable=True),
        sa.Column('invoice_date', sa.DateTime(), nullable=False),
        sa.Column('due_date', sa.DateTime(), nullable=False),
        sa.Column('subtotal', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('tax_amount', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('total_amount', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('status', sa.Enum('draft', 'sent', 'paid', 'overdue', 'cancelled', name='invoicestatus'), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_invoices_id'), 'invoices', ['id'], unique=False)
    op.create_index(op.f('ix_invoices_invoice_number'), 'invoices', ['invoice_number'], unique=True)

    # Create payments table
    op.create_table('payments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('payment_number', sa.String(length=50), nullable=False),
        sa.Column('invoice_id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('payment_method', sa.Enum('cash', 'bank_transfer', 'credit_card', 'check', 'digital_wallet', name='paymentmethod'), nullable=False),
        sa.Column('payment_date', sa.DateTime(), nullable=False),
        sa.Column('reference', sa.String(length=100), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['invoice_id'], ['invoices.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_payments_id'), 'payments', ['id'], unique=False)
    op.create_index(op.f('ix_payments_payment_number'), 'payments', ['payment_number'], unique=True)

    # Create base tables for other modules
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('first_name', sa.String(length=50), nullable=False),
        sa.Column('last_name', sa.String(length=50), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_superuser', sa.Boolean(), nullable=True),
        sa.Column('organization_id', sa.Integer(), nullable=True),
        sa.Column('role_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    op.create_table('organizations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('slug', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('contact_email', sa.String(length=200), nullable=True),
        sa.Column('contact_phone', sa.String(length=50), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('website', sa.String(length=200), nullable=True),
        sa.Column('industry', sa.String(length=100), nullable=True),
        sa.Column('size', sa.String(length=50), nullable=True),
        sa.Column('founded_year', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('settings', sa.JSON(), nullable=True),
        sa.Column('enabled_modules', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_organizations_id'), 'organizations', ['id'], unique=False)
    op.create_index(op.f('ix_organizations_slug'), 'organizations', ['slug'], unique=True)

    op.create_table('roles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('permissions', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_roles_id'), 'roles', ['id'], unique=False)

    op.create_table('tenants',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('organization_id', sa.Integer(), nullable=False),
        sa.Column('schema_name', sa.String(length=100), nullable=False),
        sa.Column('settings', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tenants_id'), 'tenants', ['id'], unique=False)

    op.create_table('permissions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('resource', sa.String(length=100), nullable=False),
        sa.Column('action', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_permissions_id'), 'permissions', ['id'], unique=False)

    # Add foreign key constraints
    op.create_foreign_key(None, 'users', 'organizations', ['organization_id'], ['id'])
    op.create_foreign_key(None, 'users', 'roles', ['role_id'], ['id'])


def downgrade():
    # Drop foreign key constraints
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_constraint(None, 'users', type_='foreignkey')
    
    # Drop tables
    op.drop_index(op.f('ix_permissions_id'), table_name='permissions')
    op.drop_table('permissions')
    
    op.drop_index(op.f('ix_tenants_id'), table_name='tenants')
    op.drop_table('tenants')
    
    op.drop_index(op.f('ix_roles_id'), table_name='roles')
    op.drop_table('roles')
    
    op.drop_index(op.f('ix_organizations_id'), table_name='organizations')
    op.drop_table('organizations')
    
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    
    op.drop_index(op.f('ix_payments_payment_number'), table_name='payments')
    op.drop_index(op.f('ix_payments_id'), table_name='payments')
    op.drop_table('payments')
    
    op.drop_index(op.f('ix_invoices_invoice_number'), table_name='invoices')
    op.drop_index(op.f('ix_invoices_id'), table_name='invoices')
    op.drop_table('invoices')
    
    op.drop_index(op.f('ix_transactions_transaction_number'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_id'), table_name='transactions')
    op.drop_table('transactions')
    
    op.drop_index(op.f('ix_accounts_id'), table_name='accounts')
    op.drop_index(op.f('ix_accounts_code'), table_name='accounts')
    op.drop_table('accounts')
    
    # Drop enums
    op.execute('DROP TYPE IF EXISTS accounttype')
    op.execute('DROP TYPE IF EXISTS accountcategory')
    op.execute('DROP TYPE IF EXISTS transactiontype')
    op.execute('DROP TYPE IF EXISTS invoicestatus')
    op.execute('DROP TYPE IF EXISTS paymentmethod')
