"""icon table

Revision ID: de2a7ff224e5
Revises: 3051a6698c8a
Create Date: 2020-08-26 14:37:08.923741

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "de2a7ff224e5"
down_revision = "3051a6698c8a"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "icons",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("filename", sa.String),
        sa.Column("site", sa.String),
    )
    pass


def downgrade():
    op.drop_table("icons")
    pass
