"""migration

Revision ID: cb2c67efa291
Revises: 173554c57d41
Create Date: 2025-04-12 15:23:21.981693

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cb2c67efa291"
down_revision: Union[str, None] = "173554c57d41"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "books", sa.Column("file_path", sa.String(length=255), nullable=False)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("books", "file_path")
    # ### end Alembic commands ###
