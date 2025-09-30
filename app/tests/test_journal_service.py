import pytest
from app.services.journal_service import JournalService
from db.s3_utils import MinIOClient
from db.config import DATABASE_URL
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# -------------------------------
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

@pytest.fixture(scope="module")
def s3_client():
    client = MinIOClient()
    return client

@pytest.fixture(scope="module")
def journal_service(s3_client):
    return JournalService(s3_client, bucket_name="test_bucket")

def test_create_journal_flow(journal_service, s3_client):
    user_id = "user_123"
    content = "This is a real test journal entry."
    title = "Integration Test Journal"

    # Create the journal
    journal_id = journal_service.create_journal(user_id, content, title, profile_id=None)
    print(f"Journal created with ID: {journal_id}")

    # ✅ Verify S3 content in-memory
    s3_data = s3_client.download_bytes(f"journals/{journal_id}.txt")
    assert s3_data.decode() == content

    # ✅ Verify metadata & embeddings in Postgres
    with SessionLocal() as session:
        row = session.execute(
            text("SELECT embeddings FROM journal_metadata WHERE journal_id = :jid"),
            {"jid": journal_id}
        ).mappings().fetchone()  # Use .mappings() to access columns by name
        assert row is not None, "Journal metadata not found"
        embedding = row['embeddings']
        assert embedding is not None, "Embedding not saved"
        print("Embedding length:", len(embedding))
        print("Sample values:", embedding[:5])
