"""resize embeddings to 384

Revision ID: 5c9600c3562e
Revises: 70ad3fa32784
Create Date: 2025-09-29 11:31:40.153780

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c9600c3562e'
down_revision: Union[str, Sequence[str], None] = '70ad3fa32784'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema to 384-dim embeddings."""
    # Change journal_metadata.embeddings to VECTOR(384)
    op.execute(
        "ALTER TABLE journal_metadata ALTER COLUMN embeddings TYPE vector(384);"
    )


def downgrade() -> None:
    """Downgrade schema back to 1536-dim embeddings."""
    op.execute(
        "ALTER TABLE journal_metadata ALTER COLUMN embeddings TYPE vector(1536);"
    )
