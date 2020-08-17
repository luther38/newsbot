"""Discord WebHook Table

Revision ID: ea9cf2966ab1
Revises: e07dac09ecad
Create Date: 2020-08-06 01:37:06.601844

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ea9cf2966ab1"
down_revision = "e07dac09ecad"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "sources",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("name", sa.String),
        sa.Column("url", sa.String),
        sa.Column("enabled", sa.BOOLEAN),
    )

    op.create_table(
        "discordwebhooks",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("name", sa.String),
        sa.Column("key", sa.String),
        sa.Column("enabled", sa.String),
    )


def downgrade():
    op.drop_table("sites")
    op.drop_table("discordwebhooks")
