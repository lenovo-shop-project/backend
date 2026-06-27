"""add favorite products

Revision ID: 51295b11b6bf
Revises: b182269644bd
Create Date: 2026-06-26 23:37:00.313485

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '51295b11b6bf'
down_revision: Union[str, Sequence[str], None] = 'b182269644bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "favorite_products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "user_id",
            "product_id",
            name="uq_favorite_products_user_product",
        ),
    )

    op.create_index(
        op.f("ix_favorite_products_user_id"),
        "favorite_products",
        ["user_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_favorite_products_product_id"),
        "favorite_products",
        ["product_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_favorite_products_product_id"),
        table_name="favorite_products",
    )

    op.drop_index(
        op.f("ix_favorite_products_user_id"),
        table_name="favorite_products",
    )

    op.drop_table("favorite_products")
