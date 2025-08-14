"""
Add procurement (PO/GRN), outbound (SO/Shipment), valuation layers, and costing fields

Revision ID: 007_inventory_procurement_sales
Revises: 006_finance_accounting_periods
Create Date: 2025-08-14
"""

from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '007_inventory_procurement_sales'
down_revision = '006_finance_accounting_periods'
branch_labels = None
depends_on = None


def upgrade():
    # Enums
    valuation_method = postgresql.ENUM('fifo', 'average', name='valuationmethod', create_type=False)
    try:
        valuation_method.create(op.get_bind(), checkfirst=True)
    except Exception:
        pass

    po_status = postgresql.ENUM('draft', 'approved', 'received', 'closed', 'cancelled', name='purchaseorderstatus', create_type=False)
    try:
        po_status.create(op.get_bind(), checkfirst=True)
    except Exception:
        pass

    so_status = postgresql.ENUM('draft', 'confirmed', 'shipped', 'closed', 'cancelled', name='salesorderstatus', create_type=False)
    try:
        so_status.create(op.get_bind(), checkfirst=True)
    except Exception:
        pass

    valuation_source_type = postgresql.ENUM('grn', 'adjustment', 'opening', name='valuationsourcetype', create_type=False)
    try:
        valuation_source_type.create(op.get_bind(), checkfirst=True)
    except Exception:
        pass

    # Add columns to existing tables
    with op.batch_alter_table('products') as batch:
        batch.add_column(sa.Column('valuation_method', sa.Enum('fifo', 'average', name='valuationmethod'), nullable=False, server_default='fifo'))

    with op.batch_alter_table('stock_movements') as batch:
        batch.add_column(sa.Column('cost_amount', sa.Numeric(15, 2), nullable=True))

    # Create procurement tables
    op.create_table(
        'purchase_orders',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('po_number', sa.String(length=50), nullable=False),
        sa.Column('supplier_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.Enum('draft', 'approved', 'received', 'closed', 'cancelled', name='purchaseorderstatus'), nullable=False, server_default='draft'),
        sa.Column('order_date', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('expected_date', sa.DateTime(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('total_amount', sa.Numeric(15,2), nullable=False, server_default='0.00'),
        sa.UniqueConstraint('po_number'),
        sa.Index('ix_purchase_orders_po_number', 'po_number'),
        sa.ForeignKeyConstraint(['supplier_id'], ['suppliers.id'])
    )

    op.create_table(
        'purchase_order_lines',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('purchase_order_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('quantity', sa.Numeric(14,4), nullable=False, server_default='0.0000'),
        sa.Column('unit_price', sa.Numeric(12,2), nullable=False, server_default='0.00'),
        sa.Column('received_quantity', sa.Numeric(14,4), nullable=False, server_default='0.0000'),
        sa.Index('ix_purchase_order_lines_po', 'purchase_order_id'),
        sa.ForeignKeyConstraint(['purchase_order_id'], ['purchase_orders.id']),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'])
    )

    op.create_table(
        'goods_receipts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('grn_number', sa.String(length=50), nullable=False),
        sa.Column('Supplier_id', sa.Integer(), nullable=True),
        sa.Column('purchase_order_id', sa.Integer(), nullable=True),
        sa.Column('warehouse_id', sa.Integer(), nullable=False),
        sa.Column('receipt_date', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.UniqueConstraint('grn_number'),
        sa.Index('ix_goods_receipts_grn_number', 'grn_number'),
        sa.ForeignKeyConstraint(['Supplier_id'], ['suppliers.id']),
        sa.ForeignKeyConstraint(['purchase_order_id'], ['purchase_orders.id']),
        sa.ForeignKeyConstraint(['warehouse_id'], ['warehouses.id'])
    )

    op.create_table(
        'goods_receipt_lines',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('goods_receipt_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('po_line_id', sa.Integer(), nullable=True),
        sa.Column('quantity', sa.Numeric(14,4), nullable=False, server_default='0.0000'),
        sa.Column('unit_cost', sa.Numeric(12,2), nullable=False, server_default='0.00'),
        sa.Index('ix_goods_receipt_lines_grn', 'goods_receipt_id'),
        sa.ForeignKeyConstraint(['goods_receipt_id'], ['goods_receipts.id']),
        sa.ForeignKeyConstraint(['product_id'], ['products.id']),
        sa.ForeignKeyConstraint(['po_line_id'], ['purchase_order_lines.id'])
    )

    # Outbound
    op.create_table(
        'sales_orders',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('so_number', sa.String(length=50), nullable=False),
        sa.Column('customer_name', sa.String(length=200), nullable=False),
        sa.Column('customer_email', sa.String(length=200), nullable=True),
        sa.Column('status', sa.Enum('draft', 'confirmed', 'shipped', 'closed', 'cancelled', name='salesorderstatus'), nullable=False, server_default='draft'),
        sa.Column('order_date', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('expected_ship_date', sa.DateTime(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('total_amount', sa.Numeric(15,2), nullable=False, server_default='0.00'),
        sa.UniqueConstraint('so_number'),
        sa.Index('ix_sales_orders_so_number', 'so_number')
    )

    op.create_table(
        'sales_order_lines',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('sales_order_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('quantity', sa.Numeric(14,4), nullable=False, server_default='0.0000'),
        sa.Column('unit_price', sa.Numeric(12,2), nullable=False, server_default='0.00'),
        sa.Column('shipped_quantity', sa.Numeric(14,4), nullable=False, server_default='0.0000'),
        sa.Index('ix_sales_order_lines_so', 'sales_order_id'),
        sa.ForeignKeyConstraint(['sales_order_id'], ['sales_orders.id']),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'])
    )

    op.create_table(
        'shipments',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('ship_number', sa.String(length=50), nullable=False),
        sa.Column('sales_order_id', sa.Integer(), nullable=True),
        sa.Column('warehouse_id', sa.Integer(), nullable=False),
        sa.Column('ship_date', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.UniqueConstraint('ship_number'),
        sa.Index('ix_shipments_ship_number', 'ship_number'),
        sa.ForeignKeyConstraint(['sales_order_id'], ['sales_orders.id']),
        sa.ForeignKeyConstraint(['warehouse_id'], ['warehouses.id'])
    )

    op.create_table(
        'shipment_lines',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('shipment_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Numeric(14,4), nullable=False, server_default='0.0000'),
        sa.Column('unit_cost', sa.Numeric(12,2), nullable=True),
        sa.Column('stock_movement_id', sa.Integer(), nullable=True),
        sa.Index('ix_shipment_lines_shipment', 'shipment_id'),
        sa.ForeignKeyConstraint(['shipment_id'], ['shipments.id']),
        sa.ForeignKeyConstraint(['product_id'], ['products.id']),
        sa.ForeignKeyConstraint(['stock_movement_id'], ['stock_movements.id'])
    )

    # Valuation layers
    op.create_table(
        'inventory_valuation_layers',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('warehouse_id', sa.Integer(), nullable=False),
        sa.Column('quantity_remaining', sa.Numeric(14,4), nullable=False, server_default='0.0000'),
        sa.Column('unit_cost', sa.Numeric(12,2), nullable=False, server_default='0.00'),
        sa.Column('source_type', sa.Enum('grn', 'adjustment', 'opening', name='valuationsourcetype'), nullable=False),
        sa.Column('source_id', sa.Integer(), nullable=True),
        sa.Column('created_at_ts', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['product_id'], ['products.id']),
        sa.ForeignKeyConstraint(['warehouse_id'], ['warehouses.id'])
    )


def downgrade():
    op.drop_table('inventory_valuation_layers')
    op.drop_table('shipment_lines')
    op.drop_table('shipments')
    op.drop_table('sales_order_lines')
    op.drop_table('sales_orders')
    op.drop_table('goods_receipt_lines')
    op.drop_table('goods_receipts')
    op.drop_table('purchase_order_lines')
    op.drop_table('purchase_orders')

    with op.batch_alter_table('stock_movements') as batch:
        batch.drop_column('cost_amount')

    with op.batch_alter_table('products') as batch:
        batch.drop_column('valuation_method')

    try:
        postgresql.ENUM(name='valuationsourcetype').drop(op.get_bind(), checkfirst=True)
    except Exception:
        pass
    try:
        postgresql.ENUM(name='salesorderstatus').drop(op.get_bind(), checkfirst=True)
    except Exception:
        pass
    try:
        postgresql.ENUM(name='purchaseorderstatus').drop(op.get_bind(), checkfirst=True)
    except Exception:
        pass
    try:
        postgresql.ENUM(name='valuationmethod').drop(op.get_bind(), checkfirst=True)
    except Exception:
        pass


