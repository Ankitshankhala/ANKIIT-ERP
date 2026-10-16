"""Align the migrated schema with the SQLAlchemy models

Revision ID: 009
Revises: 008
Create Date: 2026-10-16 14:30:00.000000

Migrations 001-007 never matched the models, so a database built with
`alembic upgrade head` could not be used by the app. This revision closes the gap:

- Enum labels: the models persist enum member NAMES ('ASSET'), the old migrations
  created lowercase VALUES ('asset'). Labels are renamed in place, which keeps
  existing rows and needs no model change.
- created_at / updated_at become timezone-aware, NOT NULL and default to now()
  (the app relies on the database to fill them).
- organizations, users, roles, permissions and tenants get the columns the models
  define. Old organization columns are copied into their replacements where one
  exists (contact_email -> email, contact_phone -> phone, address -> address_line1,
  size -> company_size). organizations.description, organizations.settings and
  users.is_superuser have no counterpart in the models and are dropped
  (superuser status comes from the "superuser" role).
- Missing indexes are added and four index names from 007 are renamed to the
  names the models generate.

New NOT NULL columns keep a server default matching the model's default so
existing rows stay valid.
"""
from alembic import op
import sqlalchemy as sa


revision = '009'
down_revision = '008'
branch_labels = None
depends_on = None


# Old lowercase labels; the models use the same words upper-cased
ENUM_LABELS = {
    'accountcategory': ['current_assets', 'fixed_assets', 'current_liabilities', 'long_term_liabilities',
                        'owners_equity', 'operating_revenue', 'operating_expenses', 'non_operating'],
    'accounttype': ['asset', 'liability', 'equity', 'revenue', 'expense'],
    'employmentstatus': ['active', 'inactive', 'on_leave'],
    'invoicestatus': ['draft', 'sent', 'paid', 'overdue', 'cancelled'],
    'invoicetype': ['sale', 'purchase'],
    'leadstatus': ['new', 'contacted', 'qualified', 'lost'],
    'opportunitystage': ['prospecting', 'qualification', 'proposal', 'negotiation', 'won', 'lost'],
    'paymentmethod': ['cash', 'bank_transfer', 'credit_card', 'check', 'digital_wallet'],
    'purchaseorderstatus': ['draft', 'approved', 'received', 'closed', 'cancelled'],
    'salesorderstatus': ['draft', 'confirmed', 'shipped', 'closed', 'cancelled'],
    'stockmovementtype': ['receipt', 'issue', 'transfer', 'adjustment'],
    'transactiontype': ['sale', 'purchase', 'payment', 'receipt', 'transfer', 'adjustment', 'journal_entry'],
    'valuationmethod': ['fifo', 'average'],
    'valuationsourcetype': ['grn', 'adjustment', 'opening'],
}

# Tables whose created_at/updated_at were nullable TIMESTAMP columns without a default
TIMESTAMPS_NULLABLE_NO_DEFAULT = [
    'accounting_periods', 'accounts', 'attendance', 'audit_logs', 'customers', 'employees',
    'invoice_line_items', 'invoices', 'leads', 'opportunities', 'organizations', 'payments',
    'permissions', 'products', 'roles', 'stock_levels', 'stock_movements', 'suppliers',
    'tenants', 'transactions', 'users', 'warehouses',
]
# Tables from 007 whose timestamps were already NOT NULL DEFAULT now(), only lacking a time zone
TIMESTAMPS_NOT_NULL_WITH_DEFAULT = [
    'goods_receipt_lines', 'goods_receipts', 'purchase_order_lines', 'purchase_orders',
    'sales_order_lines', 'sales_orders', 'shipment_lines', 'shipments',
]
# inventory_valuation_layers.created_at stays a plain DateTime in the model; only updated_at changes

ID_INDEX_TABLES = [
    'accounting_periods', 'attendance', 'audit_logs', 'customers', 'employees', 'goods_receipt_lines',
    'goods_receipts', 'inventory_valuation_layers', 'invoice_line_items', 'leads', 'opportunities',
    'products', 'purchase_order_lines', 'purchase_orders', 'sales_order_lines', 'sales_orders',
    'shipment_lines', 'shipments', 'stock_levels', 'stock_movements', 'suppliers', 'warehouses',
]
INDEX_RENAMES = {
    'ix_goods_receipt_lines_grn': 'ix_goods_receipt_lines_goods_receipt_id',
    'ix_purchase_order_lines_po': 'ix_purchase_order_lines_purchase_order_id',
    'ix_sales_order_lines_so': 'ix_sales_order_lines_sales_order_id',
    'ix_shipment_lines_shipment': 'ix_shipment_lines_shipment_id',
}


def _new_organization_columns():
    return [
        sa.Column('display_name', sa.String(255), nullable=True),
        sa.Column('email', sa.String(255), nullable=True),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('address_line1', sa.String(255), nullable=True),
        sa.Column('address_line2', sa.String(255), nullable=True),
        sa.Column('city', sa.String(100), nullable=True),
        sa.Column('state', sa.String(100), nullable=True),
        sa.Column('postal_code', sa.String(20), nullable=True),
        sa.Column('country', sa.String(100), nullable=True),
        sa.Column('company_size', sa.String(50), nullable=True),
        sa.Column('tax_id', sa.String(100), nullable=True),
        sa.Column('timezone', sa.String(50), nullable=False, server_default='UTC'),
        sa.Column('currency', sa.String(3), nullable=False, server_default='USD'),
        sa.Column('language', sa.String(10), nullable=False, server_default='en'),
        sa.Column('date_format', sa.String(20), nullable=False, server_default='YYYY-MM-DD'),
        sa.Column('subscription_plan', sa.String(50), nullable=False, server_default='basic'),
        sa.Column('max_users', sa.Integer(), nullable=False, server_default='10'),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('trial_ends_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('logo_url', sa.String(500), nullable=True),
        sa.Column('primary_color', sa.String(7), nullable=False, server_default='#3B82F6'),
        sa.Column('secondary_color', sa.String(7), nullable=False, server_default='#1F2937'),
    ]


# (column, type) of the organization columns from 001 that this revision drops
OLD_ORGANIZATION_COLUMNS = [
    ('description', sa.Text()),
    ('contact_email', sa.String(200)),
    ('contact_phone', sa.String(50)),
    ('address', sa.Text()),
    ('size', sa.String(50)),
    ('settings', sa.JSON()),
]


def _new_user_columns():
    return [
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('email_verified_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('avatar_url', sa.String(500), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('timezone', sa.String(50), nullable=False, server_default='UTC'),
        sa.Column('language', sa.String(10), nullable=False, server_default='en'),
    ]


def _new_role_columns():
    return [
        sa.Column('display_name', sa.String(255), nullable=True),
        sa.Column('is_system_role', sa.Boolean(), nullable=False, server_default=sa.false()),
    ]


def _new_permission_columns():
    return [
        sa.Column('display_name', sa.String(255), nullable=True),
        sa.Column('is_global', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('is_system', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('module', sa.String(100), nullable=True),
    ]


def _new_tenant_columns():
    return [
        sa.Column('database_url', sa.String(500), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('is_primary', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('custom_fields', sa.JSON(), nullable=False, server_default=sa.text("'{}'::json")),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=False, server_default=sa.text("'[]'::json")),
    ]


def _timestamps_to_tz(table, columns):
    for column in columns:
        op.alter_column(table, column, type_=sa.DateTime(timezone=True),
                        postgresql_using=f"{column} AT TIME ZONE 'UTC'")


def upgrade():
    # Enum labels: 'asset' -> 'ASSET'
    for type_name, labels in ENUM_LABELS.items():
        for label in labels:
            op.execute(f"ALTER TYPE {type_name} RENAME VALUE '{label}' TO '{label.upper()}'")

    # Timestamps
    for table in TIMESTAMPS_NULLABLE_NO_DEFAULT:
        for column in ('created_at', 'updated_at'):
            op.execute(f"UPDATE {table} SET {column} = now() WHERE {column} IS NULL")
        _timestamps_to_tz(table, ('created_at', 'updated_at'))
        for column in ('created_at', 'updated_at'):
            op.alter_column(table, column, nullable=False, server_default=sa.func.now())
    for table in TIMESTAMPS_NOT_NULL_WITH_DEFAULT:
        _timestamps_to_tz(table, ('created_at', 'updated_at'))
    _timestamps_to_tz('inventory_valuation_layers', ('updated_at',))
    op.drop_column('inventory_valuation_layers', 'created_at_ts')

    # organizations
    for column in _new_organization_columns():
        op.add_column('organizations', column)
    op.execute("""
        UPDATE organizations SET
            email = contact_email,
            phone = left(contact_phone, 20),
            address_line1 = left(address, 255),
            company_size = size
    """)
    for column, _type in OLD_ORGANIZATION_COLUMNS:
        op.drop_column('organizations', column)
    op.alter_column('organizations', 'founded_year', type_=sa.String(4), postgresql_using='founded_year::text')
    op.alter_column('organizations', 'name', type_=sa.String(255))
    op.alter_column('organizations', 'slug', type_=sa.String(100))
    op.alter_column('organizations', 'website', type_=sa.String(500))
    op.execute("UPDATE organizations SET enabled_modules = '[]' WHERE enabled_modules IS NULL")
    op.execute("UPDATE organizations SET is_active = true WHERE is_active IS NULL")
    op.alter_column('organizations', 'enabled_modules', nullable=False)
    op.alter_column('organizations', 'is_active', nullable=False)
    op.create_index('ix_organizations_name', 'organizations', ['name'], unique=False)

    # users
    for column in _new_user_columns():
        op.add_column('users', column)
    op.drop_column('users', 'is_superuser')
    op.alter_column('users', 'email', type_=sa.String(255))
    op.alter_column('users', 'first_name', type_=sa.String(100))
    op.alter_column('users', 'last_name', type_=sa.String(100))
    op.execute("UPDATE users SET is_active = true WHERE is_active IS NULL")
    op.alter_column('users', 'is_active', nullable=False)
    op.alter_column('users', 'organization_id', nullable=False)
    op.alter_column('users', 'role_id', nullable=False)

    # roles
    for column in _new_role_columns():
        op.add_column('roles', column)
    op.create_index('ix_roles_name', 'roles', ['name'], unique=True)

    # permissions
    op.add_column('permissions', sa.Column('name', sa.String(100), nullable=True))
    op.execute("UPDATE permissions SET name = action || ':' || resource WHERE name IS NULL")
    op.alter_column('permissions', 'name', nullable=False)
    for column in _new_permission_columns():
        op.add_column('permissions', column)
    op.alter_column('permissions', 'action', type_=sa.String(50))
    op.create_index('ix_permissions_name', 'permissions', ['name'], unique=True)

    # tenants
    op.add_column('tenants', sa.Column('name', sa.String(255), nullable=True))
    op.add_column('tenants', sa.Column('slug', sa.String(100), nullable=True))
    op.execute("UPDATE tenants SET name = schema_name, slug = schema_name WHERE name IS NULL")
    op.alter_column('tenants', 'name', nullable=False)
    op.alter_column('tenants', 'slug', nullable=False)
    for column in _new_tenant_columns():
        op.add_column('tenants', column)
    op.execute("UPDATE tenants SET settings = '{}' WHERE settings IS NULL")
    op.alter_column('tenants', 'settings', nullable=False)
    op.create_unique_constraint('tenants_schema_name_key', 'tenants', ['schema_name'])
    op.create_index('ix_tenants_name', 'tenants', ['name'], unique=False)
    op.create_index('ix_tenants_slug', 'tenants', ['slug'], unique=True)

    # Indexes
    for table in ID_INDEX_TABLES:
        op.create_index(f'ix_{table}_id', table, ['id'], unique=False)
    for old, new in INDEX_RENAMES.items():
        op.execute(f'ALTER INDEX {old} RENAME TO {new}')
    for column in ('product_id', 'warehouse_id'):
        op.create_index(f'ix_inventory_valuation_layers_{column}', 'inventory_valuation_layers', [column], unique=False)


def _timestamps_to_naive(table, columns):
    for column in columns:
        op.alter_column(table, column, type_=sa.DateTime(),
                        postgresql_using=f"{column} AT TIME ZONE 'UTC'")


def downgrade():
    # Indexes
    for column in ('warehouse_id', 'product_id'):
        op.drop_index(f'ix_inventory_valuation_layers_{column}', table_name='inventory_valuation_layers')
    for old, new in INDEX_RENAMES.items():
        op.execute(f'ALTER INDEX {new} RENAME TO {old}')
    for table in ID_INDEX_TABLES:
        op.drop_index(f'ix_{table}_id', table_name=table)

    # tenants
    op.drop_index('ix_tenants_slug', table_name='tenants')
    op.drop_index('ix_tenants_name', table_name='tenants')
    op.drop_constraint('tenants_schema_name_key', 'tenants', type_='unique')
    op.alter_column('tenants', 'settings', nullable=True)
    for column in reversed(_new_tenant_columns()):
        op.drop_column('tenants', column.name)
    op.drop_column('tenants', 'slug')
    op.drop_column('tenants', 'name')

    # permissions
    op.drop_index('ix_permissions_name', table_name='permissions')
    op.alter_column('permissions', 'action', type_=sa.String(100))
    for column in reversed(_new_permission_columns()):
        op.drop_column('permissions', column.name)
    op.drop_column('permissions', 'name')

    # roles
    op.drop_index('ix_roles_name', table_name='roles')
    for column in reversed(_new_role_columns()):
        op.drop_column('roles', column.name)

    # users
    op.alter_column('users', 'role_id', nullable=True)
    op.alter_column('users', 'organization_id', nullable=True)
    op.alter_column('users', 'is_active', nullable=True)
    op.alter_column('users', 'last_name', type_=sa.String(50))
    op.alter_column('users', 'first_name', type_=sa.String(50))
    op.alter_column('users', 'email', type_=sa.String(100))
    op.add_column('users', sa.Column('is_superuser', sa.Boolean(), nullable=True))
    op.execute("""
        UPDATE users SET is_superuser = EXISTS (
            SELECT 1 FROM roles WHERE roles.id = users.role_id AND roles.name = 'superuser'
        )
    """)
    for column in reversed(_new_user_columns()):
        op.drop_column('users', column.name)

    # organizations
    op.drop_index('ix_organizations_name', table_name='organizations')
    op.alter_column('organizations', 'is_active', nullable=True)
    op.alter_column('organizations', 'enabled_modules', nullable=True)
    op.alter_column('organizations', 'website', type_=sa.String(200))
    op.alter_column('organizations', 'slug', type_=sa.String(200))
    op.alter_column('organizations', 'name', type_=sa.String(200))
    op.alter_column('organizations', 'founded_year', type_=sa.Integer(),
                    postgresql_using="CASE WHEN founded_year ~ '^[0-9]+$' THEN founded_year::integer END")
    for column, type_ in OLD_ORGANIZATION_COLUMNS:
        op.add_column('organizations', sa.Column(column, type_, nullable=True))
    op.execute("""
        UPDATE organizations SET
            contact_email = left(email, 200),
            contact_phone = phone,
            address = address_line1,
            size = company_size
    """)
    for column in reversed(_new_organization_columns()):
        op.drop_column('organizations', column.name)

    # Timestamps
    op.add_column('inventory_valuation_layers',
                  sa.Column('created_at_ts', sa.DateTime(), nullable=False, server_default=sa.func.now()))
    _timestamps_to_naive('inventory_valuation_layers', ('updated_at',))
    for table in TIMESTAMPS_NOT_NULL_WITH_DEFAULT:
        _timestamps_to_naive(table, ('created_at', 'updated_at'))
    for table in TIMESTAMPS_NULLABLE_NO_DEFAULT:
        for column in ('created_at', 'updated_at'):
            op.alter_column(table, column, nullable=True, server_default=None)
        _timestamps_to_naive(table, ('created_at', 'updated_at'))

    # Enum labels: 'ASSET' -> 'asset'
    for type_name, labels in ENUM_LABELS.items():
        for label in labels:
            op.execute(f"ALTER TYPE {type_name} RENAME VALUE '{label.upper()}' TO '{label}'")
