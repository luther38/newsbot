"""update sources table

Revision ID: c77ad08fa772
Revises: 1e72dcb284c9
Create Date: 2021-04-04 15:48:07.364376

"""
from alembic.op import add_column, drop_column, create_table, drop_table
from sqlalchemy import Column, String, Boolean


# revision identifiers, used by Alembic.
revision = 'c77ad08fa772'
down_revision = '1e72dcb284c9'
branch_labels = None
depends_on = None


def upgrade():
    # dropping it so we can rebuild it.
    # This is not a user table as is and all values are generated from env or soon, ui
    drop_table("sources")

    create_table(
        "sources"
        ,Column("id", String, primary_key=True)
        ,Column("name", String)
        ,Column("source", String)
        ,Column("type", String)
        ,Column("value", String)
        ,Column('enabled', Boolean)
        ,Column('url', String)
        ,Column('tags', String)
    )
    pass


def downgrade():
    # Drop the new table
    drop_table("sources")

    #Generate the old 
    create_table(
        "sources",
        Column("id", String, primary_key=True),
        Column("name", String),
        Column("url", String),
        Column("enabled", Boolean)
    )
    pass
