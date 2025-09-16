# app/tests/test_documents_dao.py
import os
import json
import pytest
from app.dao.documents_dao import DocumentsDAO

SAMPLE_FILE = "sample_conversation.json"

@pytest.fixture(scope="function")
def dao():
    return DocumentsDAO()

@pytest.fixture(scope="function")
def sample_file(tmp_path):
    file_path = tmp_path / SAMPLE_FILE
    sample_data = {
        "user_id": "11111111-1111-1111-1111-111111111111",
        "session_id": "22222222-2222-2222-2222-222222222222",
        "username": "testuser",
        "email": "test@example.com",
        "password_hash": "dummyhash",
        "content": [
            {"role": "user", "message": "Hello"},
            {"role": "assistant", "message": "Hi there!"}
        ]
    }
    with open(file_path, "w") as f:
        json.dump(sample_data, f)
    return file_path, sample_data

def test_create_document(dao, sample_file):
    file_path, metadata = sample_file
    document_id = dao.create_document(str(file_path), metadata)
    assert document_id is not None
    print(f"Document created with ID: {document_id}")

    # Verify get_document works
    doc = dao.get_document(document_id)
    assert doc is not None
    assert doc["id"] == document_id
    assert doc["user_id"] == metadata["user_id"]