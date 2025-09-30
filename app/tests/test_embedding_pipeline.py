import uuid
from app.services.embedding_service import EmbeddingService
from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker
from db.config import DATABASE_URL

# -------------------------------
# DATABASE SETUP
# -------------------------------
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# -------------------------------
# Helper functions
# -------------------------------
def create_dummy_journal(user_id="user_123", title="Test Journal", content_summary="Sample content"):
    journal_id = str(uuid.uuid4())
    s3_key = f"dummy/{journal_id}.txt"

    with engine.connect() as conn:
        conn.execute(
            text(
                """
                INSERT INTO journals (id, user_id, s3_key, title, content_summary)
                VALUES (:id, :user_id, :s3_key, :title, :summary)
                """
            ),
            {"id": journal_id, "user_id": user_id, "s3_key": s3_key, "title": title, "summary": content_summary},
        )
        conn.commit()
    return journal_id

# -------------------------------
# Test embedding service
# -------------------------------
def test_embedding_pipeline():
    service = EmbeddingService()

    # Step 1: Create dummy journal
    journal_id = create_dummy_journal()
    text_to_embed = "This is a sample journal entry for embedding."

    # Step 2: Generate and save embedding
    service.save_embedding(journal_id, text_to_embed)
    print(f"Embedding saved for journal_id: {journal_id}")

    # Step 3: Fetch embedding from DB to verify
    with SessionLocal() as session:
        result = session.execute(
            text("SELECT embeddings FROM journal_metadata WHERE journal_id = :jid"),
            {"jid": journal_id},
        ).fetchone()
        if result is None:
            print("No metadata row found. Inserting dummy metadata first.")
            # Insert dummy metadata row
            session.execute(
                text(
                    "INSERT INTO journal_metadata (journal_id) VALUES (:jid)"
                ),
                {"jid": journal_id}
            )
            session.commit()
            # Retry saving embedding
            service.save_embedding(journal_id, text_to_embed)
            result = session.execute(
                text("SELECT embeddings FROM journal_metadata WHERE journal_id = :jid"),
                {"jid": journal_id},
            ).fetchone()

        embedding = result[0]
        print("Embedding length:", len(embedding))
        print("Sample values:", embedding[:5])

if __name__ == "__main__":
    test_embedding_pipeline()
