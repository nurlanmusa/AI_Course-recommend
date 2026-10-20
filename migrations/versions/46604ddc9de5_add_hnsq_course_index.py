"""add hnsq course index

Revision ID: 46604ddc9de5
Revises: 6fff6f379539
Create Date: 2026-08-12 21:07:40.426507

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46604ddc9de5'
down_revision: Union[str, Sequence[str], None] = '6fff6f379539'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.execute(
        """
        CREATE INDEX courses_embedding_hnsw_idx
        ON courses
        USING hnsw (embedding vector_cosine_ops)
        WHERE embedding IS NOT NULL
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DROP INDEX IF EXISTS courses_embedding_hnsw_idx
        """
    )