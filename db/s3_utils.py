import os
import io
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()  # Load .env variables

class MinIOClient:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            endpoint_url=os.getenv("S3_ENDPOINT"),
            aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("S3_SECRET_KEY")
        )

        self.bucket_name = os.getenv("S3_BUCKET")
        if not self.bucket_name:
            raise ValueError("S3_BUCKET is not set")
        # Ensure valid bucket name
        self.bucket_name = self.bucket_name.lower().replace("_", "-")
        self._create_bucket()

    def _create_bucket(self):
        try:
            existing_buckets = [b['Name'] for b in self.s3.list_buckets().get('Buckets', [])]
            if self.bucket_name not in existing_buckets:
                self.s3.create_bucket(Bucket=self.bucket_name)
        except ClientError as e:
            if e.response['Error']['Code'] not in ['BucketAlreadyOwnedByYou', 'BucketAlreadyExists']:
                raise

    # Upload a file from disk
    def upload_file(self, file_name, object_name=None):
        object_name = object_name or os.path.basename(file_name)
        self.s3.upload_file(file_name, self.bucket_name, object_name)
        return True

    # Upload bytes (in-memory)
    def upload_bytes(self, data: bytes, key: str):
        file_obj = io.BytesIO(data)
        self.s3.upload_fileobj(file_obj, self.bucket_name, key)
        return True

    # Download a file to disk
    def download_file(self, object_name, file_name=None):
        file_name = file_name or os.path.basename(object_name)
        self.s3.download_file(self.bucket_name, object_name, file_name)
        return True

    # Download to in-memory bytes
    def download_bytes(self, key: str) -> bytes:
        file_obj = io.BytesIO()
        self.s3.download_fileobj(self.bucket_name, key, file_obj)
        file_obj.seek(0)
        return file_obj.read()
