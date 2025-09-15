# Docker Services Guide

This guide explains how to start and manage the Circle-of-Life backend services using Docker Compose.

---

## 1. Navigate to the infra folder

```bash
cd infra

##  Start the services 
docker-compose up -d

##check running services

docker ps

## Access service UIs

pgAdmin → http://localhost:5050

MinIO Console → http://localhost:9001

Backend API → http://localhost:8000