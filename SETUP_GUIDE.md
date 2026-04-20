# VartaPravah Setup & Deployment Guide

## Quick Start

### 1. Prerequisites
- Docker Desktop (includes Docker and Docker Compose)
- YouTube Live Stream Key (from YouTube Studio)
- 4GB+ RAM (8GB recommended)
- GPU optional but recommended for lip-sync

### 2. Setup Steps

#### Step 1: Clone or Download Project
```bash
cd f:\VARTAPRAVAH-LATEST
```

#### Step 2: Configure Environment
```bash
# Copy example to .env
cp .env.example .env

# Edit .env and add your YouTube Stream Key
# Open .env in text editor and replace:
# YOUTUBE_STREAM_KEY=your_stream_key_here
```

#### Step 3: Add Assets (Optional but Recommended)
Replace placeholder files:
- `app/assets/logo.png` - Your channel logo
- `app/assets/studio.jpg` - Background image
- `app/assets/anchors/male.png` - Male anchor face
- `app/assets/anchors/female.png` - Female anchor face

#### Step 4: Start Services

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Windows (PowerShell):**
```powershell
docker-compose build
docker-compose up -d
```

**Windows (Command Prompt):**
```cmd
start.bat
```

### 3. Verify Services

Check all services are running:
```bash
docker-compose ps
```

Expected output:
```
NAME                  COMMAND              SERVICE      STATUS
vartapravah_app       uvicorn main:app...  app          running
vartapravah_stream    -re -stream_loop...  streamer     running
vartapravah_watchdog  sh -c "while true"   watchdog     running
```

### 4. Access the System

- **API Dashboard:** http://localhost:8000/docs
- **API Root:** http://localhost:8000
- **View Logs:** `docker-compose logs -f app`

## API Usage

### Generate News (POST)
```bash
curl -X POST http://localhost:8000/generate-news \
  -H "Content-Type: application/json" \
  -d '{
    "headline": "महत्वपूर्ण बातमी",
    "content": "या बातमीचा तपशील येथे आहे।",
    "category": "राजकारण",
    "breaking": false
  }'
```

### Start Streaming (POST)
```bash
curl -X POST http://localhost:8000/start-stream
```

### Stop Streaming (POST)
```bash
curl -X POST http://localhost:8000/stop-stream
```

### Get Status (GET)
```bash
curl http://localhost:8000/status
```

## Docker Services Explained

### 1. **app** (FastAPI Server)
- Runs the main Python application
- Port: 8000
- Generates news videos
- Manages video queue
- Volumes: `/videos`, `/assets`, `/temp`

### 2. **streamer** (FFmpeg Service)
- Handles continuous streaming to YouTube
- Uses loop mode for uninterrupted service
- Auto-restarts on failure
- Reads from `/videos/fallback.mp4` by default

### 3. **watchdog** (Monitoring Service)
- Monitors app and streamer services
- Auto-restarts failed services
- Health checks every 30 seconds

## Advanced Configuration

### Change News Generation Interval
Edit `.env`:
```bash
NEWS_INTERVAL=10  # Generate new news every 10 minutes
```

### Adjust Video Bitrate
Edit `.env`:
```bash
VIDEO_BITRATE=5000k  # Higher quality
AUDIO_BITRATE=192k   # Better audio
```

### Enable GPU for Lip-Sync
Update `docker-compose.yml` in `app` service:
```yaml
app:
  ...
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            count: 1
            capabilities: [gpu]
```

Then build with:
```bash
docker-compose build --build-arg CUDA_AVAILABLE=true
```

## Troubleshooting

### Services not starting?
Check logs:
```bash
docker-compose logs
```

### Stream not appearing on YouTube?
1. Verify YOUTUBE_STREAM_KEY is correct
2. Check live stream is enabled in YouTube Studio
3. Check firewall allows outbound RTMP (port 1935)

### Lip-sync not working?
- Check GPU is available: `nvidia-smi`
- Falls back to static video if GPU unavailable
- Check Wav2Lip model downloaded: `ls app/assets/wav2lip/checkpoints/`

### Watchdog not restarting services?
The watchdog needs docker socket access. Ensure `/var/run/docker.sock` is available.

## Monitoring

### View Real-time Logs
```bash
docker-compose logs -f  # All services
docker-compose logs -f app  # Just app service
docker-compose logs -f streamer  # Just streamer
```

### FFmpeg Stream Monitor (Production)
For dedicated FFmpeg process monitoring, use the included stream-monitor scripts:

**Linux/Mac:**
```bash
chmod +x stream-monitor.sh
./stream-monitor.sh &  # Run in background
```

**Windows:**
```cmd
stream-monitor.bat
```

Features:
- Monitors FFmpeg process status every 15 seconds
- Auto-restarts streamer if process dies
- Logs all actions to `logs/stream-monitor.log`
- Provides extra layer of protection alongside Docker watchdog
- Useful for high-availability setups

### Check Service Status
```bash
docker-compose ps
```

### Inspect Network
```bash
docker network ls
docker network inspect vartapravah_network
```

## Maintenance

### Backup Videos
```bash
docker-compose cp vartapravah_app:/app/videos ./backup/videos
```

### Clean Old Videos
```bash
# Remove videos older than 7 days
docker-compose exec app find /app/videos -type f -mtime +7 -delete
```

### Update/Rebuild
```bash
docker-compose build --no-cache
docker-compose up -d
```

## Production Deployment

### On Cloud Server (AWS, GCP, Azure)

1. **Install Docker:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

2. **Clone and Setup:**
```bash
git clone <your-repo-url> vartapravah
cd vartapravah
cp .env.example .env
# Edit .env with Stream Key
```

3. **Start Services:**
```bash
docker-compose up -d
```

4. **Setup Auto-restart on Boot:**
```bash
sudo systemctl enable docker
# Add to crontab:
@reboot cd /path/to/vartapravah && docker-compose up -d
```

### Reverse Proxy (Nginx)
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Performance Tips

1. **Resource Allocation:**
   - App: 2 CPU cores, 2GB RAM
   - Streamer: 2 CPU cores, 1GB RAM
   - Total: 4 CPU cores, 3GB RAM minimum

2. **Network:**
   - 5Mbps upload for 1080p streaming
   - 10Mbps upload recommended

3. **Storage:**
   - ~500MB per day for generated videos
   - 10GB storage recommended

## Support & Issues

For issues:
1. Check logs: `docker-compose logs`
2. Verify .env configuration
3. Check Docker installation
4. Ensure YouTube Stream Key is active

## Next Steps

- Customize anchor images in `app/assets/anchors/`
- Add background in `app/assets/studio.jpg`
- Upload intro/outro in `app/assets/intro.mp4`
- Configure news generation schedule in code