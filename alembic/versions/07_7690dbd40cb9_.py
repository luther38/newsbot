"""Logging table

Revision ID: 7690dbd40cb9
Revises: 4230c4c200f0
Create Date: 2020-11-21 00:29:08.158281

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7690dbd40cb9"
down_revision = "4230c4c200f0"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "logs",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("date", sa.String),
        sa.Column("time", sa.String),
        sa.Column("type", sa.String),
        sa.Column("caller", sa.String),
        sa.Column("message", sa.String),
    )
    pass


def downgrade():
    op.drop_table("logs")
    pass
