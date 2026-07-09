"""add nutrition analysis columns

Revision ID: 8f7b1c2d3e4f
Revises: 75552d84da91
Create Date: 2026-07-10

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "8f7b1c2d3e4f"
down_revision = "75552d84da91"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("nutrition_analysis") as batch_op:

        batch_op.add_column(sa.Column("confidence", sa.Integer(), nullable=True))

        batch_op.add_column(sa.Column("meal_type_ai", sa.String(length=50), nullable=True))

        batch_op.add_column(sa.Column("serving_size", sa.String(length=100), nullable=True))

        batch_op.add_column(sa.Column("health_score", sa.Integer(), nullable=True))

        batch_op.add_column(sa.Column("health_tips", sa.JSON(), nullable=True))

        batch_op.add_column(sa.Column("warnings", sa.JSON(), nullable=True))

        batch_op.add_column(sa.Column("tags", sa.JSON(), nullable=True))


def downgrade():
    with op.batch_alter_table("nutrition_analysis") as batch_op:

        batch_op.drop_column("tags")

        batch_op.drop_column("warnings")

        batch_op.drop_column("health_tips")

        batch_op.drop_column("health_score")

        batch_op.drop_column("serving_size")

        batch_op.drop_column("meal_type_ai")

        batch_op.drop_column("confidence")