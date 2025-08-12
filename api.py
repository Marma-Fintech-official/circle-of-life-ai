from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import uuid
import logging
import traceback

from embeddings.vector_store import show_all_entries, add_to_vector_store
from embeddings.embedding_service import create_embedding

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Vector Store API", version="1.0.0")


class EmbedRequest(BaseModel):
    text: str
    user_id: str
    doc_id: str | None = None
    doc_type: str | None = "unknown"
    extra_metadata: dict | None = None


@app.post("/embed")
async def embed(request: EmbedRequest):
    """
    Accepts text and metadata, stores embedding in ChromaDB.
    """
    doc_id = request.doc_id or str(uuid.uuid4())

    # Step 1: Create embedding safely
    try:
        embedding = create_embedding(request.text)
        if not embedding:
            raise ValueError("Embedding function returned empty result.")
    except Exception as e:
        logger.error(f"Embedding creation failed: {e}")
        logger.debug(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Embedding error: {str(e)}")

    # Step 2: Prepare metadata
    metadata = {
        "user_id": request.user_id,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "source": "mongodb",
        "type": request.doc_type
    }
    if request.extra_metadata:
        metadata.update(request.extra_metadata)

    # Step 3: Add to vector store safely
    try:
        add_to_vector_store(doc_id, request.text, embedding, metadata)
    except Exception as e:
        logger.error(f"Vector store insert failed: {e}")
        logger.debug(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Vector store error: {str(e)}")

    return {"status": "success", "doc_id": doc_id}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
