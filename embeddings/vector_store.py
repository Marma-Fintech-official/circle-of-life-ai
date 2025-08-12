import chromadb
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize CloudClient with your credentials
try:
    client = chromadb.CloudClient(
        api_key="ck-AqzRAwNJex6T29n3Qh3ewtVRiV1dZWjqPZfzzgTurdBz",
        tenant="1b8e5050-0598-4e6c-9bef-2f0039d232e4",
        database="jorunal_entries"  # make sure this is the correct DB name
    )
    collection = client.get_or_create_collection(name="journal_embeddings")
except Exception as e:
    logger.exception("Failed to initialize ChromaDB client or collection.")
    collection = None


def add_to_vector_store(doc_id: str, text: str, embedding: list, metadata: dict):
    if collection is None:
        raise RuntimeError("ChromaDB collection is not initialized.")
    try:
        collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata]
        )
        logger.info(f"Document {doc_id} added successfully.")
    except Exception as e:
        logger.exception(f"Failed to add document {doc_id} to ChromaDB.")
        raise


def show_all_entries():
    if collection is None:
        logger.error("ChromaDB collection is not initialized.")
        return

    try:
        data = collection.get()
        if not data["ids"]:
            logger.info("No entries found in Chroma Cloud collection.")
            return

        logger.info("\n=== ChromaDB Cloud Stored Entries ===")
        for i in range(len(data["ids"])):
            logger.info(f"ID: {data['ids'][i]}")
            logger.info(f"Document: {data['documents'][i]}")
            logger.info(f"Metadata: {data['metadatas'][i]}")
            logger.info("-" * 40)
    except Exception as e:
        logger.exception("Failed to fetch entries from ChromaDB.")
