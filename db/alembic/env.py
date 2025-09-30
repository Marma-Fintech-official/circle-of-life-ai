import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Add the db/ folder to sys.path so we can import models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Alembic Config object
config = context.config

# Override the sqlalchemy.url from environment variable
POSTGRES_URI = os.getenv("POSTGRES_URI")
if not POSTGRES_URI:
    raise Exception("POSTGRES_URI not found in environment variables")
config.set_main_option("sqlalchemy.url", POSTGRES_URI)

# Set up logging
fileConfig(config.config_file_name)

# Import your Base metadata
from models.models import Base  # this should import all your tables
target_metadata = Base.metadata

# --- Offline migration ---
def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# --- Online migration ---
def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

# --- Run the appropriate mode ---
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
