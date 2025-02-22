"""add content column to posts table

Revision ID: dddef7c48b49
Revises: cf91bf7da30d
Create Date: 2025-02-22 12:45:33.655907

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "dddef7c48b49"
down_revision: Union[str, None] = "cf91bf7da30d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
