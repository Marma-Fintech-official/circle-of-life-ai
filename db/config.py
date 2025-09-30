from dotenv import load_dotenv
import os
import boto3

"""
S3 and Database configuration
"""
load_dotenv()  # Load .env variables

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DATABASE_URL = os.getenv("POSTGRES_URI")

