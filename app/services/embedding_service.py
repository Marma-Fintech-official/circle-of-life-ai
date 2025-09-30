from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from db.config import DATABASE_URL

class EmbeddingService:
    """
    Service to handle text embedding generation and storage.
    Uses SentenceTransformer for embeddings and SQLAlchemy for DB operations."""
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.dim = 384  # Match pgVector column
        # Database setup
        self.engine = create_engine(DATABASE_URL)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def embed_text(self, text: str) -> list:
        """Convert text to vector"""
        vector = self.model.encode(text)
        if len(vector) != self.dim:
            raise ValueError(f"Expected {self.dim} dims, got {len(vector)}")
        return vector.tolist()

    def embed_batch(self, texts: list) -> list:
        """Convert multiple texts at once"""
        vectors = self.model.encode(texts)
        return [vec.tolist() for vec in vectors]

    def save_embedding(self, journal_id: str, content: str):
        """Generate and save embedding for a journal entry"""
        vector = self.embed_text(content)
        session = self.SessionLocal()
        try:
            session.execute(
                text(
                "UPDATE journal_metadata SET embeddings = :vec WHERE journal_id = :jid"
                ),
                {"vec": vector, "jid": journal_id},
            )
            session.commit()
        finally:
            session.close()

    def save_batch_embeddings(self, journal_vectors: list):
        """journal_vectors: List of (journal_id, content)
        """
        session = self.SessionLocal()
        try:
            for jid, content in journal_vectors:
                vec = self.embed_text(content)
                session.execute(
                    text(
                        "UPDATE journal_metadata SET embeddings = :vec WHERE journal_id = :jid"
                    ),
                    {"vec": vec, "jid": jid},
                )
            session.commit()
        finally:
            session.close()
