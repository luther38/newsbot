"""empty message

Revision ID: 8ad5918574d2
Revises: de2a7ff224e5
Create Date: 2020-09-01 20:51:55.238100

"""
from alembic import op
from sqlalchemy import Column, Boolean, String, Integer


# revision identifiers, used by Alembic.
revision = "8ad5918574d2"
down_revision = "de2a7ff224e5"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("DiscordQueue", Column("video", String()))
    op.add_column("DiscordQueue", Column("videoHeight", Integer()))
    op.add_column("DiscordQueue", Column("videoWidth", Integer()))

    op.add_column("Articles", Column("video", String()))
    op.add_column("Articles", Column("videoHeight", Integer()))
    op.add_column("Articles", Column("videoWidth", Integer()))
    op.add_column("Articles", Column("thumbnail", String()))
    op.add_column("Articles", Column("description", String()))


def downgrade():
    op.drop_column("DiscordQueue", "video")
    op.drop_column("DiscordQueue", "videoHeight")
    op.drop_column("DiscordQueue", "videoWidth")
    op.drop_column("Articles", "video")
    op.drop_column("Articles", "videoHeight")
    op.drop_column("Articles", "videoWidth")
    op.drop_column("Articles", "thumbnail")
    op.drop_column("Articles", "description")
