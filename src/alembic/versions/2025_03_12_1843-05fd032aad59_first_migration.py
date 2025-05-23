"""first migration

Revision ID: 05fd032aad59
Revises:
Create Date: 2025-03-12 18:43:00.786523

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "05fd032aad59"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "authors",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "books",
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("published_year", sa.Integer(), nullable=False),
        sa.Column(
            "genre",
            sa.Enum(
                "FICTION",
                "NONFICTION",
                "SCIFI",
                "FANTASY",
                "MYSTERY",
                "BIOGRAPHY",
                "HISTORY",
                "OTHER",
                name="genreenum",
            ),
            nullable=False,
        ),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["authors.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("books")
    op.drop_table("authors")
    # ### end Alembic commands ###
