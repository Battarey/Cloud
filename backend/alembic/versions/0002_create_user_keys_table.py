"""create user_keys table for encryption keys

Revision ID: 0002
Revises: 0001
Create Date: 2025-07-23
"""
revision = '0002'
down_revision = '0001'

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'user_keys',
        sa.Column('user_id', sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('encrypted_key', sa.Text, nullable=False),
    )
    op.create_index('ix_user_keys_user_id', 'user_keys', ['user_id'], unique=True)

def downgrade():
    op.drop_index('ix_user_keys_user_id', table_name='user_keys')
    op.drop_table('user_keys')
