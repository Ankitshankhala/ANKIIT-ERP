"""Create CRM and HR tables

Revision ID: 003
Revises: 002
Create Date: 2024-01-15 13:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade():
    # CRM enums
    lead_status = sa.Enum('new', 'contacted', 'qualified', 'lost', name='leadstatus')
    opp_stage = sa.Enum('prospecting', 'qualification', 'proposal', 'negotiation', 'won', 'lost', name='opportunitystage')

    # Customers
    op.create_table('customers',
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
    op.create_index(op.f('ix_customers_email'), 'customers', ['email'], unique=False)

    # Leads
    op.create_table('leads',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('customer_id', sa.Integer(), nullable=True),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('email', sa.String(length=200), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('source', sa.String(length=100), nullable=True),
        sa.Column('status', lead_status, nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_leads_email'), 'leads', ['email'], unique=False)

    # Opportunities
    op.create_table('opportunities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('customer_id', sa.Integer(), nullable=True),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('value', sa.Numeric(12, 2), nullable=False),
        sa.Column('stage', opp_stage, nullable=False),
        sa.Column('close_date', sa.DateTime(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # HR enums
    emp_status = sa.Enum('active', 'inactive', 'on_leave', name='employmentstatus')

    # Employees
    op.create_table('employees',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=False),
        sa.Column('last_name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=200), nullable=False),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('department', sa.String(length=100), nullable=True),
        sa.Column('title', sa.String(length=100), nullable=True),
        sa.Column('status', emp_status, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_employees_email'), 'employees', ['email'], unique=True)

    # Attendance
    op.create_table('attendance',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('check_in', sa.DateTime(), nullable=True),
        sa.Column('check_out', sa.DateTime(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('attendance')
    op.drop_index(op.f('ix_employees_email'), table_name='employees')
    op.drop_table('employees')
    op.execute('DROP TYPE IF EXISTS employmentstatus')
    op.drop_table('opportunities')
    op.drop_index(op.f('ix_leads_email'), table_name='leads')
    op.drop_table('leads')
    op.drop_index(op.f('ix_customers_email'), table_name='customers')
    op.drop_table('customers')
    op.execute('DROP TYPE IF EXISTS opportunitystage')
    op.execute('DROP TYPE IF EXISTS leadstatus')


