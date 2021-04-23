"""initial migration

Revision ID: a7384b7d2aef
Revises:
Create Date: 2021-04-21 23:27:23.088107

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "a7384b7d2aef"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "thing",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("name", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_thing_created_at"), "thing", ["created_at"], unique=False)
    op.create_index(op.f("ix_thing_name"), "thing", ["name"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_thing_name"), table_name="thing")
    op.drop_index(op.f("ix_thing_created_at"), table_name="thing")
    op.drop_table("thing")
    # ### end Alembic commands ###