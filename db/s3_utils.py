# db/s3_utils_async.py
import os
import aioboto3
from dotenv import load_dotenv

load_dotenv()

async def _get_s3_client():
    """Return a fresh async S3 client."""
    session = aioboto3.Session()
    return session.client(
        service_name="s3",
        endpoint_url=os.getenv("S3_ENDPOINT"),
        aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("S3_SECRET_KEY")
    )

async def upload_file_to_s3(file_content: bytes, bucket_name: str, key: str):
    async with await _get_s3_client() as s3:
        response = await s3.list_buckets()
        buckets = [b["Name"] for b in response.get("Buckets", [])]
        if bucket_name not in buckets:
            await s3.create_bucket(Bucket=bucket_name)
        await s3.put_object(Bucket=bucket_name, Key=key, Body=file_content)

async def get_file_from_s3(bucket_name: str, key: str) -> str:
    async with await _get_s3_client() as s3:
        obj = await s3.get_object(Bucket=bucket_name, Key=key)
        content = await obj["Body"].read()
        return content.decode("utf-8")