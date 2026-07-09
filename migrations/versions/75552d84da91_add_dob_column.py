"""add dob column

Revision ID: 75552d84da91
Revises: dc78d152322c
Create Date: 2026-07-09 23:54:31.876636

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75552d84da91'
down_revision = 'dc78d152322c'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(
            sa.Column("dob", sa.Date(), nullable=True)
        )


def downgrade():
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column("dob")


