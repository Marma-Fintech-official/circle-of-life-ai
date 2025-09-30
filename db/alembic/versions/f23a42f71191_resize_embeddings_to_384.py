"""resize embeddings to 384

Revision ID: f23a42f71191
Revises: 5c9600c3562e
Create Date: 2025-09-29 06:09:41.598007

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f23a42f71191'
down_revision: Union[str, Sequence[str], None] = '5c9600c3562e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
