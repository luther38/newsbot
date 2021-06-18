"""Adds server and channel to DiscordWebHooks

Revision ID: 86fa6bab6bc0
Revises: 7690dbd40cb9
Create Date: 2021-03-28 13:43:00.634297

"""
from alembic.op import add_column, drop_column
from sqlalchemy import Column, String

# revision identifiers, used by Alembic.
revision = "86fa6bab6bc0"
down_revision = "7690dbd40cb9"
branch_labels = None
depends_on = None


def upgrade():
    add_column("discordwebhooks", Column("server", String()))
    add_column("discordwebhooks", Column("channel", String()))
    add_column("discordwebhooks", Column("url", String()))
    pass


def downgrade():
    drop_column("discordwebhooks", "server")
    drop_column("discordwebhooks", "channel")
    drop_column("discordwebhooks", "url")
    pass
