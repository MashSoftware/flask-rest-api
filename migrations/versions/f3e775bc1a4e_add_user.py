"""add user

Revision ID: f3e775bc1a4e
Revises: 20e61e1fff17
Create Date: 2021-08-23 15:54:25.578782

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "f3e775bc1a4e"
down_revision = "20e61e1fff17"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user_account",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("password", sa.LargeBinary(), nullable=False),
        sa.Column("email_address", sa.String(length=256), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_user_account_email_address"),
        "user_account",
        ["email_address"],
        unique=True,
    )
    op.add_column("thing", sa.Column("user_id", postgresql.UUID(), nullable=False))
    op.create_index(op.f("ix_thing_user_id"), "thing", ["user_id"], unique=False)
    op.create_foreign_key(None, "thing", "user_account", ["user_id"], ["id"], ondelete="CASCADE")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "thing", type_="foreignkey")
    op.drop_index(op.f("ix_thing_user_id"), table_name="thing")
    op.drop_column("thing", "user_id")
    op.drop_index(op.f("ix_user_account_email_address"), table_name="user_account")
    op.drop_table("user_account")
    # ### end Alembic commands ###
