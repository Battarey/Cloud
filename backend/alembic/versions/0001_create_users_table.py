"""create users table

Revision ID: 0001
Revises: 0000
Create Date: 2025-07-23
"""
revision = '0001'
down_revision = '0000'

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('email', sa.String, unique=True, nullable=False),
        sa.Column('username', sa.String(32), unique=True, nullable=False),
        sa.Column('hashed_password', sa.String, nullable=False),
        sa.Column('files_count', sa.Integer, nullable=False, server_default='0'),
        sa.Column('files_size', sa.BigInteger, nullable=False, server_default='0'),
        sa.Column('free_space', sa.BigInteger, nullable=False, server_default=str(10*1024*1024*1024)),
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_username', 'users', ['username'], unique=True)

def downgrade():
    op.drop_table('users')
