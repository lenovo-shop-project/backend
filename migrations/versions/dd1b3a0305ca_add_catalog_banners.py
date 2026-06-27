"""add catalog banners

Revision ID: dd1b3a0305ca
Revises: 910f54ffb63b
Create Date: 2026-06-26 22:16:31.024260

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd1b3a0305ca'
down_revision: Union[str, Sequence[str], None] = '910f54ffb63b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "catalog_banners",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.Unicode(length=255), nullable=True),
        sa.Column("image_url", sa.String(length=1000), nullable=False),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("1"),
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("catalog_banners")
