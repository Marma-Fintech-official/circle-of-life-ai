"""create initial tables

Revision ID: 70ad3fa32784
Revises: 
Create Date: 2025-09-26 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '70ad3fa32784'
down_revision = None
branch_labels = None
depends_on = None

# Define enums
visibility_enum = postgresql.ENUM('public', 'personal', 'private', 'secure', name='visibilityenum')

def upgrade():
    # Create enum type
    visibility_enum.create(op.get_bind(), checkfirst=True)

    # --- Journals table ---
    op.create_table(
        'journals',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', sa.String, nullable=False),
        sa.Column('profile_id', sa.String, nullable=True),
        sa.Column('s3_key', sa.String, nullable=False),
        sa.Column('title', sa.String, nullable=True),
        sa.Column('content_summary', sa.String, nullable=True),
        sa.Column('visibility', visibility_enum, nullable=False, server_default='personal'),
        sa.Column('canonical_time', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('ingestion_source', sa.String, nullable=True),
        sa.Column('encryption_meta', sa.JSON, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )

    # --- Journal Metadata table ---
    op.create_table(
        'journal_metadata',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('journal_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('tags', postgresql.ARRAY(sa.String), nullable=True),
        sa.Column('mood', sa.String, nullable=True),
        sa.Column('feelings', sa.JSON, nullable=True),
        sa.Column('location', sa.JSON, nullable=True),
        sa.Column('device_info', sa.JSON, nullable=True),
        sa.Column('ingestion_source', sa.String, nullable=True),
        sa.Column('embeddings', postgresql.ARRAY(sa.String), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['journal_id'], ['journals.id'], ondelete='CASCADE')
    )

    # --- Placeholder tables ---
    op.create_table(
        'recommendations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        # Add other fields as needed
    )

    op.create_table(
        'insights',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        # Add other fields as needed
    )

    op.create_table(
        'notifications',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        # Add other fields as needed
    )

    op.create_table(
        'features',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        # Add other fields as needed
    )


def downgrade():
    # Drop tables first
    op.drop_table('features')
    op.drop_table('notifications')
    op.drop_table('insights')
    op.drop_table('recommendations')
    op.drop_table('journal_metadata')
    op.drop_table('journals')

    # Drop enum
    visibility_enum.drop(op.get_bind(), checkfirst=True)
