# app/tests/test_documents_dao.py
# app/tests/test_documents_dao.py
import pytest
import uuid
import pytest_asyncio
from app.dao.documents_dao import DocumentsDAO
from db.postgres_utils import create_async_pool, close_async_pool

BUCKET_NAME = "documents-bucket"

@pytest_asyncio.fixture(scope="function")
async def pool():
    pool = await create_async_pool()
    yield pool
    await close_async_pool(pool)

@pytest_asyncio.fixture
async def dao(pool):
    return DocumentsDAO(pool, BUCKET_NAME)

@pytest.fixture
def sample_conversation():
    user_id = str(uuid.uuid4())
    # Use the unique user_id to create a unique username and email
    unique_suffix = user_id[:8]
    metadata = {
        "user_id": user_id,
        "username": f"mock_user_{unique_suffix}", # Make username unique
        "email": f"mock_{unique_suffix}@example.com", # Email is already unique, but this is a good pattern
        "password_hash": "mockhash123",
        "session_id": str(uuid.uuid4()),
        "role": "user"
    }
    conversation = [
        {"content": "What should I do today?", "role": "user"},
        {"content": "Go for a short walk or hike.", "role": "assistant"}
    ]
    return metadata, conversation

@pytest.mark.asyncio
async def test_create_conversation(dao, sample_conversation):
    metadata, conversation = sample_conversation
    conv_id = await dao.create_conversation(metadata, conversation)
    assert conv_id is not None

@pytest.mark.asyncio
async def test_get_conversation(dao, sample_conversation):
    metadata, conversation = sample_conversation
    conv_id = await dao.create_conversation(metadata, conversation)
    result = await dao.get_conversation(conv_id)
    assert result is not None
    assert result["conversation"][0]["content"] == "What should I do today?"

@pytest.mark.asyncio
async def test_list_conversations(dao, sample_conversation):
    metadata, conversation = sample_conversation
    conversation_ids = []
    for _ in range(2):
        conv_id = await dao.create_conversation(metadata, conversation)
        conversation_ids.append(conv_id)

    results = await dao.list_conversations(metadata["user_id"])
    assert len(results) >= 2
