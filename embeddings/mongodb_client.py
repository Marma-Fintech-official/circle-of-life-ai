import mongomock
from datetime import datetime
import uuid
from embeddings.embedding_service import create_embedding
from embeddings.vector_store import add_to_vector_store

client = mongomock.MongoClient()
db = client["journal_app"]

journal_entries_col = db["journal_entries"]
products_col = db["products"]

def _store_in_chroma(doc_id: str, text: str, user_id: str, doc_type: str, extra_metadata=None):
    embedding = create_embedding(text)
    metadata = {
        "user_id": user_id,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "source": "mongodb",
        "type": doc_type
    }
    if extra_metadata:
        metadata.update(extra_metadata)
    add_to_vector_store(doc_id, text, embedding, metadata)
