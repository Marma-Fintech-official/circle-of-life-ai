# Circle-of-Life Quick-Start Cheat Sheet

## 1️⃣ Start Services

```bash
cd infra
docker-compose up -d

# Check Running Containers
docker ps


You should see:

postgres → port 5432

pgadmin → port 5050

minio → ports 9000 / 9001

circle-of-life-backend → port 8000

3️⃣ Access UIs
Service	URL	Notes
pgAdmin	http://localhost:5050
	Manage Postgres databases
MinIO Console	http://localhost:9001
	Manage S3 buckets
Backend API	http://localhost:8000
	FastAPI endpoints
4️⃣ Test Backend Health
# Liveness
curl http://localhost:8000/health/ping

# Readiness (DB + S3)
curl http://localhost:8000/health/ready


Expected response: JSON with status ok or ready

5️⃣ Test Database Connection
# Enter backend container
docker exec -it circle-of-life-backend bash

# Inside container, test Postgres connection
python -c "from db.postgres_utils import create_connection, close_connection; conn=create_connection(); print(conn); close_connection(conn)"

6️⃣ Test S3 / MinIO Connection
# Inside backend container
python -c "from db.s3_utils import get_s3_client; s3=get_s3_client(); print(s3.list_buckets())"


Should list MinIO buckets (documents-bucket, etc.)

7️⃣ Stop All Services
docker-compose down


Remove volumes (optional, for fresh start):

docker-compose down -v