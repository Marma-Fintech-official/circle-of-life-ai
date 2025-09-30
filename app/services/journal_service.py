import uuid
from .embedding_service import EmbeddingService
from db.s3_utils import MinIOClient
from db.postgres_utils import insert_journal

class JournalService:
    """
    Service to handle journal creation, storage, and embedding generation.
    """
    def __init__(self, s3_client: MinIOClient, bucket_name: str):
        self.s3_client = s3_client
        self.bucket_name = bucket_name
        self.embedder = EmbeddingService()

    def create_journal(self, user_id: str, content: str, title: str = None, profile_id: str = None):
        """
        Upload raw text to S3 (in-memory)
        Insert journal metadata into Postgres
        Generate and save embedding in Postgres
        """
        journal_id = str(uuid.uuid4())
        s3_key = f"journals/{journal_id}.txt"

        # Upload raw text as bytes
        self.s3_client.upload_bytes(content.encode(), s3_key)

        # Insert journal record
        insert_journal(
            journal_id=journal_id,
            user_id=user_id,
            profile_id=profile_id,
            s3_key=s3_key,
            title=title or "",
            content_summary=content[:255]
        )

        # Insert empty metadata row (needed for embedding update)
        # Save embedding
        self.embedder.save_embedding(journal_id, content)

        return journal_id
