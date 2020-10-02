"""empty message

Revision ID: 8ad5918574d2
Revises: de2a7ff224e5
Create Date: 2020-09-01 20:51:55.238100

"""
from alembic.op import add_column, drop_column
from sqlalchemy import Column, Boolean, String, Integer


# revision identifiers, used by Alembic.
revision = "8ad5918574d2"
down_revision = "de2a7ff224e5"
branch_labels = None
depends_on = None


def upgrade():
    add_column("DiscordQueue", Column("video", String()))
    add_column("DiscordQueue", Column("videoHeight", Integer()))
    add_column("DiscordQueue", Column("videoWidth", Integer()))
    add_column("Articles", Column("video", String()))
    add_column("Articles", Column("videoHeight", Integer()))
    add_column("Articles", Column("videoWidth", Integer()))
    add_column("Articles", Column("thumbnail", String()))
    add_column("Articles", Column("description", String()))

def downgrade():
    drop_column("DiscordQueue", "video")
    drop_column("DiscordQueue", "videoHeight")
    drop_column("DiscordQueue", "videoWidth")
    drop_column("Articles", "video")
    drop_column("Articles", "videoHeight")
    drop_column("Articles", "videoWidth")
    drop_column("Articles", "thumbnail")
    drop_column("Articles", "description")
