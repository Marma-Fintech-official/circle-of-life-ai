# Setup Guide

## Prerequisites
- Python 3.11+
- uv (for dependency + environment management)
- Docker & Docker Compose
- Git

## Local Development Setup (optional)
```bash
# Clone repo
git clone <your-repo-url>
cd circle-of-life-backend

# Initialize local environment
uv init
source .venv/bin/activate   # or `source .venv/bin/activate.fish` if using fish shell

# Install dependencies
uv sync
