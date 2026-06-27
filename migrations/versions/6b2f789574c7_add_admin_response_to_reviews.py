"""add admin response to reviews

Revision ID: 6b2f789574c7
Revises: 51295b11b6bf
Create Date: 2026-06-27 13:38:12.316322

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b2f789574c7'
down_revision: Union[str, Sequence[str], None] = '51295b11b6bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "reviews",
        sa.Column(
            "admin_response",
            sa.UnicodeText(),
            nullable=True,
        ),
    )

    op.add_column(
        "reviews",
        sa.Column(
            "admin_response_created_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column(
        "reviews",
        "admin_response_created_at",
    )

    op.drop_column(
        "reviews",
        "admin_response",
    )
