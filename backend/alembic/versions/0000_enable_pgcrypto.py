"""enable pgcrypto extension

Revision ID: 0000
Revises: 
Create Date: 2025-07-23
"""
revision = '0000'
down_revision = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")

def downgrade():
    op.execute("DROP EXTENSION IF EXISTS pgcrypto;")
