"""Adding sourcelinks table

Revision ID: 1e72dcb284c9
Revises: 86fa6bab6bc0
Create Date: 2021-03-28 14:43:29.737553

"""

from alembic.op import add_column, drop_column, create_table, drop_table
from sqlalchemy import Column, String

# revision identifiers, used by Alembic.
revision = "1e72dcb284c9"
down_revision = "86fa6bab6bc0"
branch_labels = None
depends_on = None


def upgrade():
    create_table(
        "sourcelinks",
        Column("id", String, primary_key=True),
        Column("sourceName", String),
        Column("sourceType", String),
        Column("sourceID", String),
        Column('discordName', String),
        Column("discordID", String),
    )
    pass


def downgrade():
    drop_table("sourcelinks")
    pass
