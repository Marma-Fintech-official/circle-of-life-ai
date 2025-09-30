import pytest
from db.session import get_db
from sqlalchemy import text

def test_get_db_creates_and_closes_session():
    db_gen = get_db()
    db = next(db_gen)
    try:
        # Execute a simple query to check connection
        result = db.execute(text("SELECT 1"))
        assert result.scalar() == 1
    finally:
        db.close()
