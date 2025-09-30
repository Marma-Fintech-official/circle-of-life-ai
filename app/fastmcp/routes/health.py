# app/fastmcp/routes/health.py
### code owner: Saravanamuthu Muthusamy
### maintainer: Saravanamuthu Muthusamy

from fastapi import APIRouter
from fastapi.responses import JSONResponse
import asyncio
from db.postgres_utils import create_connection, close_connection
from db.s3_utils import get_s3_client

router = APIRouter()

async def check_database():
    """Check Postgres connectivity"""
    try:
        conn = create_connection()
        if not conn:
            raise Exception("Unable to connect")
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.fetchone()
        cur.close()
        close_connection(conn)
        return ("database", "ok")
    except Exception as e:
        return ("database", f"error: {str(e)}")

async def check_s3():
    """Check S3 connectivity"""
    try:
        s3 = get_s3_client()
        if not s3:
            raise Exception("Unable to create S3 client")
        s3.list_buckets()
        return ("s3", "ok")
    except Exception as e:
        return ("s3", f"error: {str(e)}")

@router.get("/ping", tags=["health"])
async def ping():
    """Basic liveness check"""
    return JSONResponse(content={"status": "ok", "service": "fastmcp"})

@router.get("/ready", tags=["health"])
async def readiness():
    """Readiness check for Postgres and S3"""
    results = await asyncio.gather(
        check_database(),
        check_s3(),
        return_exceptions=False
    )
    checks = dict(results)
    health = all(status == "ok" for status in checks.values())
    if health:
        return JSONResponse(content={"status": "ready", "checks": checks})
    else:
        return JSONResponse(status_code=503, content={"status": "error", "checks": checks})