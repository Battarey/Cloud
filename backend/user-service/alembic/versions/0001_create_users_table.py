"""create users table

Revision ID: 0001
Revises: 
Create Date: 2025-07-07
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Uuid(as_uuid=True), primary_key=True, index=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('email', sa.String, unique=True, index=True, nullable=False),
        sa.Column('username', sa.String(32), unique=True, index=True, nullable=False),
        sa.Column('hashed_password', sa.String, nullable=False),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('files_count', sa.Integer, nullable=False, server_default='0'),
        sa.Column('files_size', sa.BigInteger, nullable=False, server_default='0'),
        sa.Column('free_space', sa.BigInteger, nullable=False, server_default=str(10*1024*1024*1024)),  # 10 ГБ по умолчанию
    )

def downgrade():
    op.drop_table('users')
