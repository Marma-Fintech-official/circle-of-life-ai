# Code owner Yazeen Rizwan  
# Maintainer Saravanamuthu Muthu
import boto3

print("Starting connection test...")

try:
    s3 = boto3.client(
        "s3",
        endpoint_url="http://minio:9000",
        aws_access_key_id="minioadmin",
        aws_secret_access_key="minioadmin",
    )
    response = s3.list_buckets()
    print("Buckets available:", [b["Name"] for b in response.get("Buckets", [])])
    print("✅ Connection establishment completed")
except Exception as e:
    print("❌ Connection failed:", e)