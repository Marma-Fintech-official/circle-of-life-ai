# app/dao/documents_dao_async.py
import json
import uuid
import asyncio
from db.s3_utils import _get_s3_client, get_file_from_s3

class DocumentsDAO:
    def __init__(self, pool, bucket_name):
        self.pool = pool
        self.bucket_name = bucket_name
        self._bucket_ready = False
        self._bucket_lock = asyncio.Lock()

    async def _ensure_bucket_exists(self):
        async with self._bucket_lock:
            if self._bucket_ready:
                return
            async with await _get_s3_client() as s3:
                response = await s3.list_buckets()
                if self.bucket_name not in [b["Name"] for b in response.get("Buckets", [])]:
                    await s3.create_bucket(Bucket=self.bucket_name)
                    print(f"✅ S3 bucket created: {self.bucket_name}")
                else:
                    print(f"✅ S3 bucket exists: {self.bucket_name}")
            self._bucket_ready = True

    async def create_conversation(self, metadata, conversation):
        conversation_id = str(uuid.uuid4())
        s3_key = f"{conversation_id}/conversation.json"

        try:
            await self._ensure_bucket_exists()

            async with await _get_s3_client() as s3:
                await s3.put_object(
                    Bucket=self.bucket_name,
                    Key=s3_key,
                    Body=json.dumps(conversation).encode("utf-8")
                )
                print(f"✅ File uploaded to {self.bucket_name}/{s3_key}")

            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(
                        """
                        INSERT INTO users (id, username, email, password_hash)
                        VALUES ($1, $2, $3, $4)
                        ON CONFLICT (id) DO NOTHING
                        """,
                        metadata["user_id"],
                        metadata["username"],
                        metadata["email"],
                        metadata["password_hash"]
                    )
                    await conn.execute(
                        """
                        INSERT INTO conversations (id, user_id, session_id, s3_key, metadata)
                        VALUES ($1, $2, $3, $4, $5)
                        """,
                        conversation_id,
                        metadata["user_id"],
                        metadata["session_id"],
                        s3_key,
                        json.dumps(metadata)
                    )
            return conversation_id
        except Exception as e:
            print(f"❌ Error creating conversation: {e}")
            return None

    async def get_conversation(self, conversation_id):
        try:
            async with self.pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT s3_key FROM conversations WHERE id=$1",
                    conversation_id
                )
            if not row:
                return None
            s3_key = row["s3_key"]
            content = await get_file_from_s3(self.bucket_name, s3_key)
            return {"conversation": json.loads(content)}
        except Exception as e:
            print(f"❌ Error fetching conversation {conversation_id}: {e}")
            return None

    async def list_conversations(self, user_id):
        try:
            async with self.pool.acquire() as conn:
                rows = await conn.fetch(
                    "SELECT id FROM conversations WHERE user_id=$1",
                    user_id
                )
            return [r["id"] for r in rows]
        except Exception as e:
            print(f"❌ Error listing conversations for user {user_id}: {e}")
            return []