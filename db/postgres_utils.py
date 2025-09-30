from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from db.database import engine

SessionLocal = sessionmaker(bind=engine)

def insert_journal(journal_id, user_id, s3_key, title, content_summary="", profile_id=None):
    """ 
    Insert a new journal entry into the journals table.
    """
    session = SessionLocal()
    try:
        session.execute(
            text(
                """
                INSERT INTO journals (id, user_id, profile_id, s3_key, title, content_summary)
                VALUES (:id, :user_id, :profile_id, :s3_key, :title, :content_summary)
                """
            ),
            {
                "id": journal_id,
                "user_id": user_id,
                "profile_id": profile_id,
                "s3_key": s3_key,
                "title": title,
                "content_summary": content_summary
            },
        )
        # Insert empty row in journal_metadata for embeddings
        session.execute(
            text("INSERT INTO journal_metadata (journal_id) VALUES (:jid)"),
            {"jid": journal_id}
        )
        session.commit()
    finally:
        session.close()
