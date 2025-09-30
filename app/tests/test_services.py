import pytest
from app.services.embedding_service import EmbeddingService

@pytest.fixture
def embedding_service():
    """Fixture to initialize the EmbeddingService."""
    return EmbeddingService()

def test_single_embedding(embedding_service):
    text = "This is a test journal entry."
    embedding = embedding_service.embed_text(text)
    
    # Check the embedding is a list
    assert isinstance(embedding, list)
    
    # Check the dimension matches 384
    assert len(embedding) == 384
    
    # Check values are floats
    assert all(isinstance(x, float) for x in embedding)

def test_batch_embedding(embedding_service):
    texts = ["Entry one", "Entry two", "Entry three"]
    embeddings = embedding_service.embed_batch(texts)
    
    # Check it's a list of lists
    assert isinstance(embeddings, list)
    assert all(isinstance(vec, list) for vec in embeddings)
    
    # Check each embedding has correct dimension
    for vec in embeddings:
        assert len(vec) == 384
        assert all(isinstance(x, float) for x in vec)
