from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from db.s3_utils import upload_file_to_s3
from db.postgres_utils import create_connection, close_connection