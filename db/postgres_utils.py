import os
import psycopg2
import asyncpg
from psycopg2 import OperationalError
from dotenv import load_dotenv

load_dotenv()

# ------------------ Sync Connection ------------------
def create_connection() -> psycopg2.extensions.connection | None:
    try:
        connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME", "circleoflife"),
            user=os.getenv("DB_USER", "admin"),
            password=os.getenv("DB_PASSWORD", "nimda"),
            host=os.getenv("DB_HOST", "postgres"),
            port=os.getenv("DB_PORT", "5432")
        )
        print("✅ PostgreSQL connection established!")
        return connection
    except OperationalError as e:
        print(f"❌ Failed to connect to the database:\n{e}")
        return None

def close_connection(connection: psycopg2.extensions.connection) -> None:
    if connection:
        connection.close()
        print("✅ Database connection closed.")

# ------------------ Async Connection ------------------
async def create_async_pool() -> asyncpg.pool.Pool:
    pool = await asyncpg.create_pool(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        host=os.getenv("DB_HOST"),  # Removed hardcoded 'localhost'
        port=int(os.getenv("DB_PORT", 5432)),
        min_size=1,
        max_size=10,
    )
    print("✅ Async PostgreSQL pool established!")
    return pool

async def close_async_pool(pool: asyncpg.pool.Pool) -> None:
    if pool:
        await pool.close()
        print("✅ Async PostgreSQL pool closed.")