"""empty message

Revision ID: e07dac09ecad
Revises: 
Create Date: 2020-08-02 22:04:10.002940

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e07dac09ecad"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "articles",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("title", sa.String),
        sa.Column("url", sa.String),
        sa.Column("pubDate", sa.String)
    )
    op.create_table(
        "pso2news",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("title", sa.String),
        sa.Column('url', sa.String),
    )
    pass


def downgrade():
    op.drop_table("articles")
    pass
