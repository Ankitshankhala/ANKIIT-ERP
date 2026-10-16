"""Per-organization data isolation: organization_id on every ERP table

Revision ID: 008
Revises: 007_inventory_procurement_sales
Create Date: 2026-10-16 13:30:00.000000

- Creates communications, payrolls and leaves, which earlier migrations never created.
- Adds a NOT NULL organization_id (FK organizations.id, indexed) to every other ERP table.
  Existing rows are assigned to the oldest organization.
- Replaces globally unique codes/numbers with per-organization unique constraints.

Downgrade restores the global unique indexes, which fails if two organizations
already use the same code or number.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = '008'
down_revision = '007_inventory_procurement_sales'
branch_labels = None
depends_on = None


# ERP tables that already exist at revision 007
EXISTING_TABLES = [
    'accounts', 'transactions', 'invoices', 'payments', 'invoice_line_items', 'accounting_periods',
    'products', 'suppliers', 'warehouses', 'stock_levels', 'stock_movements',
    'purchase_orders', 'purchase_order_lines', 'goods_receipts', 'goods_receipt_lines',
    'sales_orders', 'sales_order_lines', 'shipments', 'shipment_lines', 'inventory_valuation_layers',
    'customers', 'leads', 'opportunities',
    'employees', 'attendance',
]

# Columns that were unique across all organizations and become unique per organization.
# Value: how the global uniqueness was enforced at revision 007.
PER_ORG_UNIQUE = {
    ('accounts', 'code'): 'index',
    ('transactions', 'transaction_number'): 'index',
    ('invoices', 'invoice_number'): 'index',
    ('payments', 'payment_number'): 'index',
    ('products', 'sku'): 'index',
    ('warehouses', 'code'): 'index',
    ('stock_movements', 'movement_number'): 'index',
    ('employees', 'email'): 'index',
    ('accounting_periods', 'period'): 'constraint',
    ('purchase_orders', 'po_number'): 'constraint',
    ('goods_receipts', 'grn_number'): 'constraint',
    ('sales_orders', 'so_number'): 'constraint',
    ('shipments', 'ship_number'): 'constraint',
}

# Enum labels match what the models persist (member names)
communication_type = postgresql.ENUM('CALL', 'EMAIL', 'MEETING', 'NOTE', name='communicationtype', create_type=False)
payroll_status = postgresql.ENUM('PENDING', 'PAID', name='payrollstatus', create_type=False)
leave_type = postgresql.ENUM('SICK', 'VACATION', 'UNPAID', name='leavetype', create_type=False)
leave_status = postgresql.ENUM('PENDING', 'APPROVED', 'REJECTED', name='leavestatus', create_type=False)
NEW_ENUMS = [communication_type, payroll_status, leave_type, leave_status]


def _base_columns():
    return [
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('organization_id', sa.Integer(), sa.ForeignKey('organizations.id'), nullable=False),
    ]


def _create_missing_tables():
    bind = op.get_bind()
    for enum in NEW_ENUMS:
        enum.create(bind, checkfirst=True)

    op.create_table(
        'communications',
        *_base_columns(),
        sa.Column('customer_id', sa.Integer(), sa.ForeignKey('customers.id'), nullable=True),
        sa.Column('lead_id', sa.Integer(), sa.ForeignKey('leads.id'), nullable=True),
        sa.Column('opportunity_id', sa.Integer(), sa.ForeignKey('opportunities.id'), nullable=True),
        sa.Column('type', communication_type, nullable=False),
        sa.Column('subject', sa.String(length=200), nullable=True),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('occurred_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'payrolls',
        *_base_columns(),
        sa.Column('employee_id', sa.Integer(), sa.ForeignKey('employees.id'), nullable=False),
        sa.Column('period_start', sa.Date(), nullable=False),
        sa.Column('period_end', sa.Date(), nullable=False),
        sa.Column('base_salary', sa.Numeric(12, 2), nullable=False),
        sa.Column('allowances', sa.Numeric(12, 2), nullable=False),
        sa.Column('deductions', sa.Numeric(12, 2), nullable=False),
        sa.Column('net_pay', sa.Numeric(12, 2), nullable=False),
        sa.Column('status', payroll_status, nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'leaves',
        *_base_columns(),
        sa.Column('employee_id', sa.Integer(), sa.ForeignKey('employees.id'), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('type', leave_type, nullable=False),
        sa.Column('status', leave_status, nullable=False),
        sa.Column('reason', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    for table in ('communications', 'payrolls', 'leaves'):
        op.create_index(f'ix_{table}_id', table, ['id'], unique=False)
        op.create_index(f'ix_{table}_organization_id', table, ['organization_id'], unique=False)


def upgrade():
    _create_missing_tables()

    for table in EXISTING_TABLES:
        op.add_column(table, sa.Column('organization_id', sa.Integer(), nullable=True))
        # Rows created before isolation belong to the oldest organization
        op.execute(f'UPDATE {table} SET organization_id = (SELECT MIN(id) FROM organizations)')
        op.alter_column(table, 'organization_id', nullable=False)
        op.create_foreign_key(f'{table}_organization_id_fkey', table, 'organizations', ['organization_id'], ['id'])
        op.create_index(f'ix_{table}_organization_id', table, ['organization_id'], unique=False)

    for (table, column), kind in PER_ORG_UNIQUE.items():
        if kind == 'index':
            op.drop_index(f'ix_{table}_{column}', table_name=table)
            op.create_index(f'ix_{table}_{column}', table, [column], unique=False)
        else:
            op.drop_constraint(f'{table}_{column}_key', table, type_='unique')
        op.create_unique_constraint(f'uq_{table}_org_{column}', table, ['organization_id', column])


def downgrade():
    for (table, column), kind in PER_ORG_UNIQUE.items():
        op.drop_constraint(f'uq_{table}_org_{column}', table, type_='unique')
        if kind == 'index':
            op.drop_index(f'ix_{table}_{column}', table_name=table)
            op.create_index(f'ix_{table}_{column}', table, [column], unique=True)
        else:
            op.create_unique_constraint(f'{table}_{column}_key', table, [column])

    for table in reversed(EXISTING_TABLES):
        op.drop_index(f'ix_{table}_organization_id', table_name=table)
        op.drop_constraint(f'{table}_organization_id_fkey', table, type_='foreignkey')
        op.drop_column(table, 'organization_id')

    for table in ('leaves', 'payrolls', 'communications'):
        op.drop_table(table)
    bind = op.get_bind()
    for enum in reversed(NEW_ENUMS):
        enum.drop(bind, checkfirst=True)
