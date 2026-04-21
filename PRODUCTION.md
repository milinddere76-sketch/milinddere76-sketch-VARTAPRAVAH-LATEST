# Production Deployment Guide

## Overview

VARTAPRAVAH can be deployed to production using Docker and container orchestration platforms.

## Local Production Setup

### 1. Build Optimized Image

```bash
# Use build cache for faster builds
docker build -t vartapravah:latest --cache-from vartapravah:latest .

# Tag for registry
docker tag vartapravah:latest myregistry.azurecr.io/vartapravah:latest
```

### 2. Production docker-compose.yml

```yaml
version: "3.9"

services:
  vartapravah:
    image: vartapravah:latest
    container_name: vartapravah_prod
    restart: always
    
    environment:
      - PYTHONUNBUFFERED=1
      - LOG_LEVEL=INFO
      - YOUTUBE_RTMP_KEY=${YOUTUBE_RTMP_KEY}
    
    volumes:
      - vartapravah_output:/app/output
      - vartapravah_logs:/app/logs
    
    ports:
      - "8000:8000"
    
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G

volumes:
  vartapravah_output:
  vartapravah_logs:
```

### 3. Secure .env.production

```bash
# .env.production
YOUTUBE_RTMP_KEY=<your-secure-key>
LOG_LEVEL=WARNING
```

## AWS Deployment

### Option 1: EC2 + Docker

```bash
# 1. Launch EC2 instance (t3.large or larger)
# 2. Install Docker & Docker Compose
sudo yum update -y
sudo yum install -y docker docker-compose
sudo systemctl start docker
sudo usermod -aG docker ec2-user

# 3. Clone and deploy
git clone <your-repo>
cd VARTAPRAVAH-LATEST
docker-compose up -d

# 4. Monitor
docker-compose logs -f
```

### Option 2: ECS + Fargate

Create ECS task definition:

```json
{
  "family": "vartapravah",
  "containerDefinitions": [
    {
      "name": "vartapravah",
      "image": "your-registry/vartapravah:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "hostPort": 8000,
          "protocol": "tcp"
        }
      ],
      "memory": 4096,
      "cpu": 1024,
      "essential": true,
      "environment": [
        {
          "name": "YOUTUBE_RTMP_KEY",
          "value": "your-key-here"
        }
      ],
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"],
        "interval": 30,
        "timeout": 10,
        "retries": 3,
        "startPeriod": 40
      }
    }
  ]
}
```

## Google Cloud Deployment

### Option 1: Cloud Run

```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/vartapravah:latest

# Deploy to Cloud Run
gcloud run deploy vartapravah \
  --image gcr.io/PROJECT_ID/vartapravah:latest \
  --platform managed \
  --region us-central1 \
  --memory 4Gi \
  --cpu 2 \
  --set-env-vars YOUTUBE_RTMP_KEY=your-key \
  --allow-unauthenticated
```

### Option 2: GKE (Kubernetes)

```bash
# Create deployment
kubectl create deployment vartapravah \
  --image=gcr.io/PROJECT_ID/vartapravah:latest

# Expose service
kubectl expose deployment vartapravah \
  --type=LoadBalancer \
  --port=8000

# Scale
kubectl scale deployment vartapravah --replicas=3
```

## Azure Deployment

### Container Instances

```bash
# Create resource group
az group create -n vartapravah-rg -l eastus

# Deploy container
az container create \
  --resource-group vartapravah-rg \
  --name vartapravah \
  --image myregistry.azurecr.io/vartapravah:latest \
  --cpu 2 \
  --memory 4 \
  --port 8000 \
  --environment-variables YOUTUBE_RTMP_KEY=your-key \
  --registry-login-server myregistry.azurecr.io \
  --registry-username username \
  --registry-password password
```

## Kubernetes Deployment

### Helm Chart (Optional)

```yaml
# values.yaml
image:
  repository: vartapravah
  tag: latest
  pullPolicy: IfNotPresent

replicaCount: 3

resources:
  limits:
    cpu: 2
    memory: 4Gi
  requests:
    cpu: 1
    memory: 2Gi

env:
  YOUTUBE_RTMP_KEY: "your-key"
  LOG_LEVEL: "INFO"

service:
  type: LoadBalancer
  port: 8000

healthCheck:
  enabled: true
  initialDelaySeconds: 40
  periodSeconds: 30
```

## Monitoring & Logging

### Prometheus Metrics

Add to main.py:

```python
from prometheus_client import Counter, Histogram, generate_latest
import time

# Metrics
request_count = Counter('api_requests_total', 'Total API requests')
request_duration = Histogram('api_request_duration_seconds', 'API request duration')

@app.middleware("http")
async def add_metrics(request, call_next):
    request_count.inc()
    start = time.time()
    response = await call_next(request)
    request_duration.observe(time.time() - start)
    return response

@app.get("/metrics")
async def metrics():
    return generate_latest()
```

### Cloud Logging

```python
# Google Cloud Logging
from google.cloud import logging as cloud_logging
client = cloud_logging.Client()
client.setup_logging()

# Azure Application Insights
from opencensus.ext.azure.log_exporter import AzureLogHandler
logger.addHandler(AzureLogHandler())
```

## Security Best Practices

### 1. Environment Secrets

```bash
# AWS Secrets Manager
aws secretsmanager create-secret \
  --name vartapravah/youtube-key \
  --secret-string your-key

# Azure Key Vault
az keyvault secret set \
  --vault-name vartapravah \
  --name youtube-key \
  --value your-key
```

### 2. Network Security

```yaml
# docker-compose.yml with network isolation
networks:
  internal:
    driver: bridge
    internal: true
  external:
    driver: bridge

services:
  vartapravah:
    networks:
      - internal
      - external
    # Only external network is accessible from outside
```

### 3. Image Scanning

```bash
# Scan for vulnerabilities
trivy image vartapravah:latest

# Use minimal base image
FROM python:3.10-slim-bullseye as builder
# ... build steps ...
FROM python:3.10-slim-bullseye
COPY --from=builder /app /app
```

## Backup & Recovery

### Volume Backup

```bash
# AWS S3
aws s3 sync ./output s3://vartapravah-backup/output/
aws s3 sync ./logs s3://vartapravah-backup/logs/

# Google Cloud Storage
gsutil -m cp -r ./output gs://vartapravah-backup/output/
```

### Database Backup (if using)

```bash
# Schedule with cron
0 2 * * * docker-compose exec db mysqldump -u user -p password db > backup.sql
0 3 * * * aws s3 cp backup.sql s3://backups/
```

## Auto-Scaling

### Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Deploy service
docker service create \
  --name vartapravah \
  --publish 8000:8000 \
  --replicas 3 \
  vartapravah:latest
```

### Kubernetes Auto-scaling

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: vartapravah-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: vartapravah
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## Continuous Integration/Deployment

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build image
        run: docker build -t vartapravah:${{ github.sha }} .
      
      - name: Push to registry
        run: |
          docker tag vartapravah:${{ github.sha }} registry.example.com/vartapravah:latest
          docker push registry.example.com/vartapravah:latest
      
      - name: Deploy
        run: |
          docker-compose -f docker-compose.prod.yml pull
          docker-compose -f docker-compose.prod.yml up -d
```

## Troubleshooting Production

### Check Container Health

```bash
docker-compose ps
docker-compose logs --tail=100
docker stats
```

### Performance Tuning

```bash
# Increase worker processes
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000

# Or in Dockerfile
ENV WORKERS=4
CMD python -m gunicorn app.main:app --workers $WORKERS
```

---

For more details, see main [README.md](README.md)
