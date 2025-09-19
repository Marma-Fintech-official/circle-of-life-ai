## main.py
# app/fastmcp/main.py
### code owner: Saravanamuthu Muthusamy
### maintainer: Saravanamuthu Muthusamy
from fastapi import FastAPI
from app.fastmcp.routes import items, health
app = FastAPI()

### root level dummy endpoint
@app.get("/")
def read_root():
    "dummy Url endpoint for root"
    return {"message": "Welcome to the Circle of Life AI FastMCP Service!"}

### import and include health check router
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(items.router, prefix="/items", tags=["items"])