"""Add audit_logs table

Revision ID: 004
Revises: 003
Create Date: 2025-08-14 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('audit_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('actor_user_id', sa.Integer(), nullable=True),
        sa.Column('actor_role', sa.String(length=100), nullable=True),
        sa.Column('tenant_id', sa.Integer(), nullable=True),
        sa.Column('organization_id', sa.Integer(), nullable=True),
        sa.Column('action', sa.String(length=100), nullable=False),
        sa.Column('resource_type', sa.String(length=100), nullable=False),
        sa.Column('resource_id', sa.String(length=100), nullable=True),
        sa.Column('ip_address', sa.String(length=64), nullable=True),
        sa.Column('user_agent', sa.String(length=255), nullable=True),
        sa.Column('method', sa.String(length=16), nullable=True),
        sa.Column('path', sa.String(length=512), nullable=True),
        sa.Column('status_code', sa.Integer(), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('before', sa.JSON(), nullable=True),
        sa.Column('after', sa.JSON(), nullable=True),
        sa.Column('error', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_logs_action'), 'audit_logs', ['action'], unique=False)
    op.create_index(op.f('ix_audit_logs_resource_type'), 'audit_logs', ['resource_type'], unique=False)
    op.create_index(op.f('ix_audit_logs_actor_user_id'), 'audit_logs', ['actor_user_id'], unique=False)
    op.create_index(op.f('ix_audit_logs_tenant_id'), 'audit_logs', ['tenant_id'], unique=False)
    op.create_index(op.f('ix_audit_logs_organization_id'), 'audit_logs', ['organization_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_audit_logs_organization_id'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_tenant_id'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_actor_user_id'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_resource_type'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_action'), table_name='audit_logs')
    op.drop_table('audit_logs')


