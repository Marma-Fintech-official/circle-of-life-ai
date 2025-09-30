"""resize embeddings to 384

Revision ID: 69dfefdbd0b5
Revises: f23a42f71191
Create Date: 2025-09-29 06:15:25.251129

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '69dfefdbd0b5'
down_revision: Union[str, Sequence[str], None] = 'f23a42f71191'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    """Resize embeddings column to 384."""
    op.execute("""
    ALTER TABLE journal_metadata 
    ALTER COLUMN embeddings TYPE vector(384);
    """)


def downgrade():
    """Revert embeddings column back to 1536."""
    op.execute("""
    ALTER TABLE journal_metadata 
    ALTER COLUMN embeddings TYPE vector(1536);
    """)