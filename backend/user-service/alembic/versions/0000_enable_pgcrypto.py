"""enable pgcrypto extension for uuid generation

Revision ID: 0000
Revises: 
Create Date: 2025-07-07
"""
from alembic import op

def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto";')

def downgrade():
    op.execute('DROP EXTENSION IF EXISTS "pgcrypto";')
