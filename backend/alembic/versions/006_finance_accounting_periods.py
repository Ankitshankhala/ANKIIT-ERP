"""Finance: add accounting periods table

Revision ID: 006
Revises: 005
Create Date: 2025-08-14 10:35:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '006'
down_revision = '005'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('accounting_periods',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('period', sa.String(length=7), nullable=False),
        sa.Column('start_date', sa.DateTime(), nullable=True),
        sa.Column('end_date', sa.DateTime(), nullable=True),
        sa.Column('is_closed', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('closed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('period')
    )
    op.create_index(op.f('ix_accounting_periods_period'), 'accounting_periods', ['period'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_accounting_periods_period'), table_name='accounting_periods')
    op.drop_table('accounting_periods')


