# Code owner: Shiva Palaksha
# Maintainer: Saravanamuthu Muthusamy

import os
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv

# Load .env.example explicitly
load_dotenv()

def create_connection() -> psycopg2.extensions.connection | None:
    """
    Create and return a connection to the PostgreSQL database.
    Uses Docker Compose service name as host if running in Docker.
    """
    try:
        connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME", "circleoflife"),
            user=os.getenv("DB_USER", "admin"),
            password=os.getenv("DB_PASSWORD", "nimda"),
            host=os.getenv("DB_HOST", "postgres"),  # Docker service name
            port=os.getenv("DB_PORT", "5432")
        )
        print("✅ PostgreSQL connection established!")
        return connection
    except OperationalError as e:
        print(f"❌ Failed to connect to the database:\n{e}")
        return None

def close_connection(connection: psycopg2.extensions.connection) -> None:
    """Safely close the database connection."""
    if connection:
        connection.close()
        print("✅ Database connection closed.")

if __name__ == "__main__":
    conn = create_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT datname FROM pg_database;")
        dbs = cur.fetchall()
        print("Databases available:", [db[0] for db in dbs])
        cur.close()
        close_connection(conn)
