# Use lightweight Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Install build dependencies and curl
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        python3-dev \
        libffi-dev \
        libssl-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and wheel to avoid build issues
RUN pip install --upgrade pip setuptools wheel

# Copy dependencies file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./app ./app
COPY ./db ./db
COPY .env .env

# Expose Uvicorn port
EXPOSE 8000

# Healthcheck – FastAPI readiness endpoint
HEALTHCHECK --interval=30s --timeout=5s --retries=5 CMD curl -f http://localhost:8000/health/ready || exit 1

# Run FastMCP backend with Uvicorn
CMD ["uvicorn", "app.fastmcp.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
