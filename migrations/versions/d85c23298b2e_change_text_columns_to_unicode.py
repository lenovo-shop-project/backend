"""change text columns to unicode

Revision ID: d85c23298b2e
Revises: 9bb1b16bf2dc
Create Date: 2026-06-18 19:11:28.635145

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd85c23298b2e'
down_revision: Union[str, Sequence[str], None] = '9bb1b16bf2dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Change text columns from VARCHAR/TEXT to Unicode NVARCHAR."""


    # У категории name есть UNIQUE-ограничение.
    # Его имя SQL Server создал автоматически, поэтому сначала находим
    # его имя и удаляем перед изменением типа колонки.
    op.execute(
        """
        DECLARE @constraint_name NVARCHAR(128);
    
        SELECT @constraint_name = kc.name
        FROM sys.key_constraints AS kc
        INNER JOIN sys.index_columns AS ic
            ON kc.parent_object_id = ic.object_id
            AND kc.unique_index_id = ic.index_id
        INNER JOIN sys.columns AS c
            ON ic.object_id = c.object_id
            AND ic.column_id = c.column_id
        WHERE kc.parent_object_id = OBJECT_ID(N'categories')
          AND kc.type = 'UQ'
          AND c.name = N'name';
    
        IF @constraint_name IS NOT NULL
        BEGIN
            EXEC(
                N'ALTER TABLE categories DROP CONSTRAINT ['
                + @constraint_name
                + N']'
            );
        END;
        """
    )

    op.alter_column(
        "categories",
        "name",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.NVARCHAR(length=100),
        existing_nullable=False,
    )

    op.create_unique_constraint(
        "uq_categories_name",
        "categories",
        ["name"],
    )

    op.alter_column(
        "products",
        "name",
        existing_type=sa.VARCHAR(length=255),
        type_=sa.NVARCHAR(length=255),
        existing_nullable=False,
    )

    op.alter_column(
        "products",
        "description",
        existing_type=sa.TEXT(),
        type_=sa.NVARCHAR(length=None),
        existing_nullable=True,
    )

    op.alter_column(
        "reviews",
        "comment",
        existing_type=sa.TEXT(),
        type_=sa.NVARCHAR(length=None),
        existing_nullable=False,
    )

def downgrade() -> None:
    """Change Unicode columns back to VARCHAR/TEXT."""

    op.drop_constraint(
        "uq_categories_name",
        "categories",
        type_="unique",
    )

    op.alter_column(
        "categories",
        "name",
        existing_type=sa.NVARCHAR(length=100),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )

    op.create_unique_constraint(
        "uq_categories_name",
        "categories",
        ["name"],
    )

    op.alter_column(
        "products",
        "name",
        existing_type=sa.NVARCHAR(length=255),
        type_=sa.VARCHAR(length=255),
        existing_nullable=False,
    )

    op.alter_column(
        "products",
        "description",
        existing_type=sa.NVARCHAR(length=None),
        type_=sa.TEXT(),
        existing_nullable=True,
    )

    op.alter_column(
        "reviews",
        "comment",
        existing_type=sa.NVARCHAR(length=None),
        type_=sa.TEXT(),
        existing_nullable=False,
    )


