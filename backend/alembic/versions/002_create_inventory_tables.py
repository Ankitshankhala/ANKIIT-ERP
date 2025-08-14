"""Create inventory tables

Revision ID: 002
Revises: 001
Create Date: 2024-01-15 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # Enums
    stock_movement_type = sa.Enum('receipt', 'issue', 'transfer', 'adjustment', name='stockmovementtype')

    # Products
    op.create_table('products',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('sku', sa.String(length=64), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('unit_of_measure', sa.String(length=20), nullable=False),
        sa.Column('cost_price', sa.Numeric(12, 2), nullable=False),
        sa.Column('sale_price', sa.Numeric(12, 2), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_products_sku'), 'products', ['sku'], unique=True)

    # Suppliers
    op.create_table('suppliers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('email', sa.String(length=200), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('website', sa.String(length=200), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Warehouses
    op.create_table('warehouses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=20), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('location', sa.String(length=200), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_warehouses_code'), 'warehouses', ['code'], unique=True)

    # Stock Levels
    op.create_table('stock_levels',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('warehouse_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Numeric(14, 4), nullable=False),
        sa.Column('reorder_point', sa.Numeric(14, 4), nullable=False),
        sa.Column('reorder_quantity', sa.Numeric(14, 4), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
        sa.ForeignKeyConstraint(['warehouse_id'], ['warehouses.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_stock_levels_product_id'), 'stock_levels', ['product_id'], unique=False)
    op.create_index(op.f('ix_stock_levels_warehouse_id'), 'stock_levels', ['warehouse_id'], unique=False)

    # Stock Movements
    op.create_table('stock_movements',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('movement_number', sa.String(length=50), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Numeric(14, 4), nullable=False),
        sa.Column('movement_type', stock_movement_type, nullable=False),
        sa.Column('from_warehouse_id', sa.Integer(), nullable=True),
        sa.Column('to_warehouse_id', sa.Integer(), nullable=True),
        sa.Column('supplier_id', sa.Integer(), nullable=True),
        sa.Column('reference', sa.String(length=100), nullable=True),
        sa.Column('movement_date', sa.DateTime(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
        sa.ForeignKeyConstraint(['from_warehouse_id'], ['warehouses.id'], ),
        sa.ForeignKeyConstraint(['to_warehouse_id'], ['warehouses.id'], ),
        sa.ForeignKeyConstraint(['supplier_id'], ['suppliers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_stock_movements_movement_number'), 'stock_movements', ['movement_number'], unique=True)


def downgrade():
    op.drop_index(op.f('ix_stock_movements_movement_number'), table_name='stock_movements')
    op.drop_table('stock_movements')

    op.drop_index(op.f('ix_stock_levels_warehouse_id'), table_name='stock_levels')
    op.drop_index(op.f('ix_stock_levels_product_id'), table_name='stock_levels')
    op.drop_table('stock_levels')

    op.drop_index(op.f('ix_warehouses_code'), table_name='warehouses')
    op.drop_table('warehouses')

    op.drop_table('suppliers')

    op.drop_index(op.f('ix_products_sku'), table_name='products')
    op.drop_table('products')

    op.execute('DROP TYPE IF EXISTS stockmovementtype')


