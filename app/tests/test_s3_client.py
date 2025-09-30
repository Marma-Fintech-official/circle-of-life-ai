import os
import pytest
from db.s3_utils import MinIOClient

TEST_FILE = "test_file.txt"
DOWNLOAD_FILE = "test_file_download.txt"
TEST_CONTENT = "Hello from pytest!"

@pytest.fixture(scope="module")
def s3_client():
    # Initialize MinIO client (bucket will be auto-created)
    client = MinIOClient()
    yield client

    # Cleanup files after tests
    for f in [TEST_FILE, DOWNLOAD_FILE]:
        if os.path.exists(f):
            os.remove(f)

def test_upload_download(s3_client):
    # Step 1: Create a test file
    with open(TEST_FILE, "w") as f:
        f.write(TEST_CONTENT)

    # Step 2: Upload the file
    assert s3_client.upload_file(TEST_FILE), "Upload failed"

    # Step 3: Download the file back
    assert s3_client.download_file(TEST_FILE, DOWNLOAD_FILE), "Download failed"

    # Step 4: Verify content
    with open(DOWNLOAD_FILE, "r") as f:
        content = f.read()
    assert content == TEST_CONTENT, "Downloaded file content mismatch"
