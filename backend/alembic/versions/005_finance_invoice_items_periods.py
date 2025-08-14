"""Finance: add invoice line items, invoice type, discounts, periods, and links

Revision ID: 005
Revises: 004
Create Date: 2025-08-14 10:20:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '005'
down_revision = '004'
branch_labels = None
depends_on = None


def upgrade():
    # Enums
    invoice_type = sa.Enum('sale', 'purchase', name='invoicetype')
    invoice_type.create(op.get_bind(), checkfirst=True)

    # Invoices: add discount_total, invoice_type, and items relation exists via FK in items table
    op.add_column('invoices', sa.Column('discount_total', sa.Numeric(15, 2), nullable=False, server_default='0.00'))
    op.add_column('invoices', sa.Column('invoice_type', invoice_type, nullable=False, server_default='sale'))

    # Transactions: link to invoice and add period
    op.add_column('transactions', sa.Column('invoice_id', sa.Integer(), nullable=True))
    op.add_column('transactions', sa.Column('period', sa.String(length=7), nullable=True))
    op.create_foreign_key(None, 'transactions', 'invoices', ['invoice_id'], ['id'])
    op.create_index(op.f('ix_transactions_period'), 'transactions', ['period'], unique=False)

    # Accounts: lock flag
    op.add_column('accounts', sa.Column('is_locked', sa.Boolean(), nullable=True, server_default=sa.false()))

    # Payments: add period
    op.add_column('payments', sa.Column('period', sa.String(length=7), nullable=True))
    op.create_index(op.f('ix_payments_period'), 'payments', ['period'], unique=False)

    # Invoice Line Items
    op.create_table('invoice_line_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('invoice_id', sa.Integer(), nullable=False),
        sa.Column('product_sku', sa.String(length=64), nullable=True),
        sa.Column('description', sa.String(length=255), nullable=False),
        sa.Column('quantity', sa.Numeric(15, 4), nullable=False),
        sa.Column('unit_price', sa.Numeric(15, 2), nullable=False),
        sa.Column('discount_amount', sa.Numeric(15, 2), nullable=False),
        sa.Column('tax_rate', sa.Numeric(6, 4), nullable=False),
        sa.Column('tax_amount', sa.Numeric(15, 2), nullable=False),
        sa.Column('line_total', sa.Numeric(15, 2), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['invoice_id'], ['invoices.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_invoice_line_items_invoice_id'), 'invoice_line_items', ['invoice_id'], unique=False)

    # Clean server defaults
    op.alter_column('invoices', 'discount_total', server_default=None)
    op.alter_column('invoices', 'invoice_type', server_default=None)


def downgrade():
    op.drop_index(op.f('ix_invoice_line_items_invoice_id'), table_name='invoice_line_items')
    op.drop_table('invoice_line_items')

    op.drop_index(op.f('ix_payments_period'), table_name='payments')
    op.drop_column('payments', 'period')

    op.drop_index(op.f('ix_transactions_period'), table_name='transactions')
    op.drop_constraint(None, 'transactions', type_='foreignkey')
    op.drop_column('transactions', 'period')
    op.drop_column('transactions', 'invoice_id')

    op.drop_column('accounts', 'is_locked')

    op.drop_column('invoices', 'invoice_type')
    op.drop_column('invoices', 'discount_total')
    op.execute('DROP TYPE IF EXISTS invoicetype')


