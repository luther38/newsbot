"""discord queue

Revision ID: 3051a6698c8a
Revises: ea9cf2966ab1
Create Date: 2020-08-16 02:01:26.259611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3051a6698c8a"
down_revision = "ea9cf2966ab1"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "discordQueue",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("siteName", sa.String),
        sa.Column("title", sa.String),
        sa.Column("link", sa.String),
        sa.Column("tags", sa.String),
        sa.Column("thumbnail", sa.String),
        sa.Column("description", sa.String),
    )
    pass


def downgrade():
    op.drop_table("discordQueue")
    pass
