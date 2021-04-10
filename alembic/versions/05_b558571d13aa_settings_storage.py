"""settings storage

Revision ID: b558571d13aa
Revises: 8ad5918574d2
Create Date: 2020-09-27 16:06:49.580178

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b558571d13aa"
down_revision = "8ad5918574d2"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "settings",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("key", sa.String),
        sa.Column("value", sa.String),
        sa.Column("options", sa.String),
        sa.Column("notes", sa.String),
    )
    pass


def downgrade():
    op.drop_table("settings")
    pass
