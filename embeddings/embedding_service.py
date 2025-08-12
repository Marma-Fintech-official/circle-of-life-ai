import logging
from chromadb.utils import embedding_functions

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

def create_embedding(text: str):
    try:
        if not text or not isinstance(text, str):
            raise ValueError("Input text must be a non-empty string.")

        logger.info(f"Creating embedding for text: {text[:50]}...")

        embedding = embedding_func([text])
        if not embedding or len(embedding) == 0:
            raise ValueError("Embedding creation returned empty result.")

        return embedding[0].tolist()

    except Exception as e:
        logger.error(f"Failed to create embedding: {e}", exc_info=True)
        return None  # Or raise the error if you want the API to fail
