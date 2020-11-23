"""Add Author information

Revision ID: 4230c4c200f0
Revises: b558571d13aa
Create Date: 2020-09-30 20:14:34.348607

"""
from alembic.op import add_column, drop_column
from sqlalchemy import Column, String


# revision identifiers, used by Alembic.
revision = "4230c4c200f0"
down_revision = "b558571d13aa"
branch_labels = None
depends_on = None


def upgrade():
    add_column("Articles", Column("authorName", String()))
    add_column("Articles", Column("authorImage", String()))
    add_column("DiscordQueue", Column("authorName", String()))
    add_column("DiscordQueue", Column("authorImage", String()))
    pass


def downgrade():
    drop_column("Articles", "authorName")
    drop_column("Articles", "authorImage")
    drop_column("DiscordQueue", "authorName")
    drop_column("DiscordQueue", "authorImage")
    pass
