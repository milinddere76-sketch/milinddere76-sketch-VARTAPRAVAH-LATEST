# VartaPravah Docker Compose Guide

## Overview

VartaPravah uses **docker-compose** to orchestrate three services:

1. **app** - FastAPI application for news generation
2. **streamer** - FFmpeg service for YouTube RTMP streaming  
3. **watchdog** - Monitoring service for health checks and auto-restart

## Available Configurations

### 1. Standard Configuration (docker-compose.yml)
Default setup for general use. Balanced between features and resource usage.

```bash
docker-compose up -d
```

### 2. Production Configuration (docker-compose.prod.yml)
Enhanced monitoring, resource limits, health checks, and logging for production deployment.

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 3. Development Configuration (docker-compose.dev.yml)
Development mode with hot-reload, debug logging, and disabled streaming.

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

## Service Details

### App Service

**Container:** `vartapravah_app`  
**Image:** Custom (built from Dockerfile)  
**Port:** 8000  
**Volumes:**
- `/app/videos` - Generated videos
- `/app/assets` - Images, fonts, clips
- `/app/temp` - Temporary files

**Health Check:**
```
GET http://localhost:8000/status → 200 OK
Every 30 seconds, timeout 10s, retry 3 times
```

**Environment:** 
- Reads from `.env` file
- `PYTHONUNBUFFERED=1` for log streaming

### Streamer Service

**Container:** `vartapravah_stream`  
**Image:** `jrottenberg/ffmpeg:6.0-alpine`  
**Input:** `/videos/fallback.mp4`  
**Output:** YouTube RTMP stream  

**Command:**
```
ffmpeg -re -stream_loop -1 -i /videos/fallback.mp4 
  -c:v libx264 -preset veryfast -b:v 3000k 
  -c:a aac -b:a 128k 
  -f flv rtmp://a.rtmp.youtube.com/live2/STREAM_KEY
```

**Features:**
- Continuous loop mode (`-stream_loop -1`)
- Preset `veryfast` for minimal CPU overhead
- Adaptive bitrate from `.env`
- RTMP protocol for YouTube compatibility

### Watchdog Service

**Container:** `vartapravah_watchdog`  
**Image:** `alpine:latest`  
**Purpose:** Monitor and auto-restart services

**Checks:**
- App container running
- Streamer container running
- Checks every 30 seconds
- Logs to `/logs/watchdog.log`

**Auto-restart:**
- Automatically restarts failed services
- Waits 5 seconds before restart
- Prevents service restart loops

## Network Configuration

**Network Name:** `vartapravah_network`  
**Type:** Bridge  
**Subnet:** `172.25.0.0/16`

### Service IPs (Bridge mode)
- `app` service: Dynamic (discover with `docker-compose exec app hostname -i`)
- `streamer` service: Dynamic
- Services communicate by container name

## Volumes

### Persistent Volumes
```
videos/   - Stores generated news videos
assets/   - Images, fonts, music files
temp/     - Temporary processing files
```

### Volume Mapping

**App Service:**
```yaml
volumes:
  - ./videos:/app/videos          # Mount local videos folder
  - ./assets:/app/assets          # Mount local assets
  - ./temp:/app/temp              # Mount temp directory
```

**Streamer Service:**
```yaml
volumes:
  - ./videos:/videos:ro           # Read-only mount for video input
```

**Watchdog Service:**
```yaml
volumes:
  - /var/run/docker.sock:/var/run/docker.sock  # Docker access
  - ./logs:/logs                                # Log directory
```

## Commands Reference

### Basic Operations

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View running services
docker-compose ps

# View logs (all services)
docker-compose logs

# View logs (specific service)
docker-compose logs -f app
docker-compose logs -f streamer
docker-compose logs -f watchdog

# Follow logs in real-time
docker-compose logs -f

# Show service status
docker-compose config

# List networks
docker network ls

# Inspect network
docker network inspect vartapravah_network
```

### Service Management

```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart app
docker-compose restart streamer

# Stop specific service
docker-compose stop app

# Start specific service
docker-compose start app

# Remove all containers (keeps volumes)
docker-compose down

# Remove all containers and volumes
docker-compose down -v

# Rebuild images
docker-compose build

# Rebuild specific service
docker-compose build app
```

### Debugging

```bash
# Execute command in running container
docker-compose exec app bash
docker-compose exec app python -c "import sys; print(sys.version)"

# Check container logs
docker-compose logs app --tail=100

# Inspect app service
docker-compose exec app cat .env

# View container details
docker inspect vartapravah_app

# Monitor container resource usage
docker stats vartapravah_app vartapravah_stream vartapravah_watchdog
```

### Testing

```bash
# Test API endpoint
docker-compose exec app curl http://localhost:8000/status

# Test streaming (from inside container)
docker-compose exec streamer ps aux

# Verify video file
docker-compose exec app ls -lah /app/videos/
```

## Environment Variables

### From `.env` File
```bash
YOUTUBE_STREAM_KEY         # YouTube RTMP key
VIDEO_WIDTH                # Default: 1920
VIDEO_HEIGHT               # Default: 1080
VIDEO_FPS                  # Default: 30
VIDEO_BITRATE              # Default: 3000k
AUDIO_BITRATE              # Default: 128k
NEWS_INTERVAL              # Default: 5 (minutes)
TTS_LANG                   # Default: mr (Marathi)
ASSETS_DIR                 # Default: app/assets
VIDEOS_DIR                 # Default: app/videos
TEMP_DIR                   # Default: app/temp
```

### Service Environment Variables
```bash
PYTHONUNBUFFERED=1         # Unbuffered Python output
LOG_LEVEL=INFO             # Logging level
STREAM_KEY=${YOUTUBE_STREAM_KEY}  # Passed to streamer
```

## Resource Limits (Production)

### App Service
```yaml
limits:
  cpus: '2'        # Maximum 2 CPU cores
  memory: 2G       # Maximum 2GB RAM
reservations:
  cpus: '1'        # Reserve 1 CPU core
  memory: 1G       # Reserve 1GB RAM
```

### Streamer Service
```yaml
limits:
  cpus: '2'
  memory: 1G
reservations:
  cpus: '1'
  memory: 512M
```

### Watchdog Service
```yaml
limits:
  cpus: '0.5'
  memory: 256M
reservations:
  cpus: '0.25'
  memory: 128M
```

## Logging Configuration

### Default (JSON Driver)
```yaml
logging:
  driver: "json-file"
  options:
    max-size: "100m"       # Max file size
    max-file: "10"         # Keep 10 files
```

### Production Logging
```bash
# View logs with JSON formatting
docker-compose logs app | jq .

# Follow specific service logs
docker-compose logs -f app --tail=50

# Analyze log file directly
cat logs/watchdog.log
```

## Networking

### Service Communication
Services communicate using container names:
- App → Streamer: Not needed (separate)
- Watchdog → All services: Via docker socket

### External Access
```bash
# Access API
http://localhost:8000

# Direct to container
docker exec vartapravah_app curl http://localhost:8000/status

# From another container
docker-compose exec watchdog wget -q -O- http://app:8000/status
```

## Health Checks

### App Service
```bash
# Healthy if returns 200 OK
GET http://localhost:8000/status

# Manual check
curl http://localhost:8000/status
```

### Streamer Service
```bash
# Check if ffmpeg process running
docker-compose exec streamer ps aux | grep ffmpeg
```

### Watchdog Service
```bash
# Check watchdog logs
docker-compose exec watchdog tail -f /logs/watchdog.log
```

## Troubleshooting

### Services won't start
```bash
# Check for port conflicts
netstat -an | grep 8000

# View detailed logs
docker-compose logs

# Check docker daemon
docker ps
```

### Connection refused on API
```bash
# Verify container is running
docker-compose ps

# Check port mapping
docker port vartapravah_app

# Test from inside container
docker-compose exec app curl http://localhost:8000/status
```

### Streamer not streaming
```bash
# Verify STREAM_KEY is set
docker-compose exec streamer env | grep STREAM_KEY

# Check FFmpeg process
docker-compose exec streamer ps aux

# View streamer logs
docker-compose logs streamer
```

### High memory usage
```bash
# Monitor resources
docker stats

# Reduce VIDEO_BITRATE in .env
# Restart services
docker-compose restart app
```

## Performance Tuning

### CPU Optimization
```bash
# For low-CPU systems
VIDEO_FPS=15              # Reduce FPS
ffmpeg preset=ultrafast  # Use faster preset (modify code)
```

### Memory Optimization
```bash
# Docker resource limits
docker-compose -f docker-compose.prod.yml up -d

# Monitor with stats
watch -n 1 'docker stats'
```

### Network Optimization
```bash
# For limited bandwidth
VIDEO_BITRATE=1500k      # Reduce video bitrate
AUDIO_BITRATE=64k        # Reduce audio bitrate
```

## Scaling & Load Balancing

For multiple channels:
```bash
# Create separate docker-compose files
docker-compose -f docker-compose-channel1.yml up -d
docker-compose -f docker-compose-channel2.yml up -d

# Use different ports
PORT=8001 docker-compose up -d
PORT=8002 docker-compose up -d
```

## Cloud Deployment

### AWS EC2
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Clone repo
git clone <repo> vartapravah
cd vartapravah

# Start services
docker-compose -f docker-compose.prod.yml up -d
```

### Google Cloud Run (App only)
Convert app service to Cloud Run compatible format.

### Kubernetes
Convert docker-compose to Kubernetes manifests using `kompose`.

## Best Practices

1. ✅ Use `docker-compose.prod.yml` for production
2. ✅ Set resource limits
3. ✅ Monitor logs regularly
4. ✅ Backup videos directory
5. ✅ Use read-only volumes where possible
6. ✅ Keep `.env` file secure
7. ✅ Regular health checks
8. ✅ Test recovery procedures

## Emergency Procedures

### Service Recovery
```bash
# If everything hangs
docker-compose down
docker-compose up -d

# Full system reset (loses current videos)
docker-compose down -v
docker-compose up -d
```

### Data Backup
```bash
# Backup videos
docker-compose cp vartapravah_app:/app/videos ./backup/

# Backup assets
docker-compose cp vartapravah_app:/app/assets ./backup/
```

### Logs Cleanup
```bash
# Remove old logs
docker-compose exec watchdog rm -f /logs/*.log

# Clear container logs
docker container prune -f
```