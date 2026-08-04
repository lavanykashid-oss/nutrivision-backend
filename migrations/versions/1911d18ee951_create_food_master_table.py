"""create food master table

Revision ID: 1911d18ee951
Revises: 0c3e18474c41
Create Date: 2026-08-04 21:20:14.440232

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1911d18ee951'
down_revision = '0c3e18474c41'
branch_labels = None
depends_on = None




def upgrade():
    op.create_table(
        "food_master",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("parameter_id", sa.Integer(), nullable=False),
        sa.Column("condition", sa.String(length=20), nullable=False),
        sa.Column("food_name", sa.String(length=150), nullable=False),
        sa.Column("meal_type", sa.String(length=50)),
        sa.Column("reason", sa.Text()),
        sa.Column("priority", sa.Integer(), server_default="1"),
        sa.ForeignKeyConstraint(
            ["parameter_id"],
            ["parameter_master.id"]
        )
    )

def downgrade():
    op.drop_table("food_master")