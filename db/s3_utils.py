# Code owner: Yazeen Rizwan
# Maintainer: Saravanamuthu Muthu

import os
import boto3
from dotenv import load_dotenv

# Load .env.example explicitly
load_dotenv(dotenv_path="../.env.example")

def get_s3_client():
    """
    Initialize and return a Boto3 S3 client.
    Works with MinIO or AWS S3.
    """
    try:
        s3 = boto3.client(
            "s3",
            endpoint_url=os.getenv("S3_ENDPOINT", "http://minio:9000"),
            aws_access_key_id=os.getenv("S3_ACCESS_KEY", "minioadmin"),
            aws_secret_access_key=os.getenv("S3_SECRET_KEY", "minioadmin"),
        )
        print("✅ S3 connection established!")
        return s3
    except Exception as e:
        print(f"❌ Failed to connect to S3:\n{e}")
        return None

if __name__ == "__main__":
    client = get_s3_client()
    if client:
        response = client.list_buckets()
        buckets = [b["Name"] for b in response.get("Buckets", [])]
        print("Buckets available:", buckets)
