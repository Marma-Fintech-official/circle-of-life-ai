# app/dao/documents_dao.py
### code owner: Saravanamuthu Muthusamy, shiva palaksha, yazeen rizwan
### maintainer: Saravanamuthu Muthusamy

import os
import uuid
import json
from dotenv import load_dotenv
from db.postgres_utils import create_connection, close_connection
from db.s3_utils import get_s3_client

class DocumentsDAO:
    def __init__(self):
        load_dotenv()
        self.conn = create_connection()
        self.s3_client = get_s3_client()
        self.bucket_name = os.getenv("S3_BUCKET", "documents-bucket")

        if self.s3_client:
            self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """Ensure the S3 bucket exists; create it if it doesn't."""
        try:
            existing_buckets = self.s3_client.list_buckets().get('Buckets', [])
            if not any(b['Name'] == self.bucket_name for b in existing_buckets):
                self.s3_client.create_bucket(Bucket=self.bucket_name)
                print(f"✅ Bucket '{self.bucket_name}' created.")
            else:
                print(f"✅ Bucket '{self.bucket_name}' already exists.")
        except Exception as e:
            print(f"❌ Error ensuring bucket exists:\n{e}")

    def create_document(self, file_path: str, metadata: dict) -> str | None:
        """Upload a document to S3 and store metadata in PostgreSQL."""
        if not self.conn or not self.s3_client:
            print("❌ Database or S3 client not initialized.")
            return None

        document_id = str(uuid.uuid4())
        s3_key = f"{document_id}_{os.path.basename(file_path)}"

        try:
            # Upload to S3
            with open(file_path, "rb") as file_data:
                self.s3_client.upload_fileobj(file_data, self.bucket_name, s3_key)
            print(f"✅ Document uploaded to S3 with key: {s3_key}")

            # Ensure user exists in DB
            with self.conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO users (id, username, email, password_hash)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                    """,
                    (
                        metadata.get("user_id"),
                        metadata.get("username", "testuser"),
                        metadata.get("email", "test@example.com"),
                        metadata.get("password_hash", "dummyhash")
                    )
                )

                # Insert conversation
                cursor.execute(
                    """
                    INSERT INTO conversations (id, user_id, session_id, s3_key, metadata)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        document_id,
                        metadata.get("user_id"),
                        metadata.get("session_id"),
                        s3_key,
                        json.dumps(metadata)
                    )
                )
                self.conn.commit()

            print(f"✅ Document metadata stored in PostgreSQL with ID: {document_id}")
            return document_id

        except Exception as e:
            print(f"❌ Error creating document:\n{e}")
            return None

    def get_document(self, document_id: str) -> dict | None:
        """Retrieve a document's metadata from PostgreSQL."""
        if not self.conn:
            return None

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, user_id, session_id, s3_key, metadata, created_at FROM conversations WHERE id=%s",
                    (document_id,)
                )
                row = cursor.fetchone()
                if not row:
                    return None
                keys = ["id", "user_id", "session_id", "s3_key", "metadata", "created_at"]
                return dict(zip(keys, row))
        except Exception as e:
            print(f"❌ Error fetching document:\n{e}")
            return None

    def close(self):
        """Close DB connection."""
        if self.conn:
            close_connection(self.conn)
