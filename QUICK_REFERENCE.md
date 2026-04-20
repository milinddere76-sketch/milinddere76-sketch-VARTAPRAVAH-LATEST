# VartaPravah Quick Reference

## 🚀 Start/Stop Services

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View service status
docker-compose ps

# View real-time logs
docker-compose logs -f

# Restart specific service
docker-compose restart app
docker-compose restart streamer
```

## 📡 API Calls

### Generate News Video
```bash
curl -X POST http://localhost:8000/generate-news \
  -H "Content-Type: application/json" \
  -d '{
    "headline": "महत्वपूर्ण बातमी",
    "content": "बातमीचा विस्तृत मजकूर येथे.",
    "category": "राजकारण",
    "breaking": false
  }'
```

### Start Streaming
```bash
curl -X POST http://localhost:8000/start-stream
```

### Stop Streaming
```bash
curl -X POST http://localhost:8000/stop-stream
```

### Check Status
```bash
curl http://localhost:8000/status
```

### API Documentation (GUI)
```
http://localhost:8000/docs
```

## 🔍 Debugging

```bash
# View app logs
docker-compose logs app

# View streaming logs
docker-compose logs streamer

# View watchdog logs
docker-compose logs watchdog

# Follow logs in real-time
docker-compose logs -f [service]

# See last 50 lines
docker-compose logs --tail=50 app

# Monitor resource usage
docker stats

# Execute command in container
docker-compose exec app bash

# Test API from inside container
docker-compose exec app curl http://localhost:8000/status
```

## 📁 File Management

```bash
# List generated videos
ls -la app/videos/

# Check available assets
ls -la app/assets/

# Check temp files
ls -la app/temp/

# Clear temp files
docker-compose exec app rm -rf /app/temp/*

# Backup videos
cp -r app/videos backup/
```

## 🔧 Configuration

```bash
# Edit environment file
nano .env  # or use your preferred editor

# Set news generation interval (in minutes)
NEWS_INTERVAL=5

# Change video quality
VIDEO_BITRATE=3000k  # 3 Mbps
AUDIO_BITRATE=128k   # 128 kbps

# Update and apply changes
docker-compose up -d
```

## 🐳 Docker Compose Profiles

```bash
# Standard deployment
docker-compose up -d

# Production with health checks
docker-compose -f docker-compose.prod.yml up -d

# Development mode (hot reload)
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

## 🔄 Service Management

```bash
# Rebuild images
docker-compose build

# Full rebuild (no cache)
docker-compose build --no-cache

# Update and restart single service
docker-compose up -d --no-deps app

# Remove all containers and volumes
docker-compose down -v

# View service configuration
docker-compose config

# Validate docker-compose.yml
docker-compose config --quiet
```

## 🎬 Video Management

```bash
# Create fallback video (auto-created on startup)
docker-compose exec app python -c "from main import generate_news; generate_news({'headline': 'Test', 'content': 'Test', 'category': 'Test', 'breaking': False})"

# View video properties
docker-compose exec app ffprobe app/videos/fallback.mp4

# Convert video format
docker-compose exec app ffmpeg -i app/videos/input.mp4 app/videos/output.mkv
```

## 📊 Monitoring

```bash
# Real-time resource monitoring
watch -n 1 'docker stats --no-stream'

# Check disk usage
df -h

# Memory usage
free -h

# Stream monitoring (Linux/Mac)
./stream-monitor.sh

# Stream monitoring (Windows)
stream-monitor.bat

# Network connectivity test
docker-compose exec app ping 8.8.8.8

# YouTube RTMP connectivity test
docker-compose exec streamer curl -I rtmp://a.rtmp.youtube.com/live2/
```

## 🔐 Security

```bash
# View environment variables (from inside container)
docker-compose exec app env | grep YOUTUBE

# Secure .env file permissions
chmod 600 .env

# Check for exposed secrets
docker-compose config | grep -i secret

# Rotate YouTube Stream Key
# 1. Edit .env with new key
# 2. Restart streamer: docker-compose restart streamer
```

## 🚨 Emergency Procedures

```bash
# Hard stop (force kill)
docker-compose kill

# Full system reset
docker-compose down -v
docker-compose up -d

# View crash logs
docker-compose logs --tail=100 app

# Check disk space (if full)
du -sh app/videos/
docker-compose exec app find /app/videos -type f -mtime +7 -delete  # Remove files older than 7 days

# Check for zombie processes
docker ps -a | grep exited
docker container prune -f
```

## 📈 Performance Tuning

```bash
# CPU-intensive operation? Reduce FPS
VIDEO_FPS=15

# Low bandwidth? Reduce bitrate
VIDEO_BITRATE=1500k
AUDIO_BITRATE=64k

# Memory issues? Check limits
docker inspect vartapravah_app | grep -A 10 Memory

# Apply changes
docker-compose down
docker-compose up -d
```

## 🌐 Network Diagnostics

```bash
# Check if port 8000 is open
lsof -i :8000

# Test API connectivity
nc -zv localhost 8000

# Check DNS
docker-compose exec app nslookup google.com

# Test YouTube RTMP connectivity
telnet a.rtmp.youtube.com 1935
```

## 🎯 Common Scenarios

### Scenario 1: Video Not Generating
```bash
# Check logs
docker-compose logs app | grep ERROR

# Verify assets exist
ls -la app/assets/

# Test API directly
curl -X POST http://localhost:8000/generate-news \
  -H "Content-Type: application/json" \
  -d '{"headline": "Test", "content": "Test", "category": "Test", "breaking": false}'
```

### Scenario 2: Not Streaming to YouTube
```bash
# Verify Stream Key
docker-compose logs streamer | grep Stream

# Check RTMP connection
docker-compose exec streamer ffmpeg -f lavfi -i testsrc=duration=1:size=1280x720 -f lavfi -i sine=frequency=1000:duration=1 -c:v libx264 -c:a aac -f flv "rtmp://a.rtmp.youtube.com/live2/YOUR_KEY"

# Verify Stream Key in .env
grep YOUTUBE_STREAM_KEY .env
```

### Scenario 3: High CPU Usage
```bash
# Monitor CPU
docker stats vartapravah_app --no-stream

# Reduce encoding preset
# Edit docker-compose.yml and change -preset veryfast to -preset ultrafast

# Restart with new settings
docker-compose up -d
```

### Scenario 4: Out of Disk Space
```bash
# Check disk usage
du -sh app/videos/

# List videos by size
ls -laSh app/videos/ | head -20

# Remove old videos
find app/videos -type f -mtime +7 -delete

# Verify space freed
df -h
```

### Scenario 5: Services Keep Restarting
```bash
# Check logs for errors
docker-compose logs --tail=50

# View watchdog activity
docker-compose logs watchdog

# Check service health
curl http://localhost:8000/status

# Look for resource exhaustion
docker stats --no-stream
```

## 🔗 Useful Links

- **API Docs:** http://localhost:8000/docs
- **Status:** http://localhost:8000/status
- **YouTube Studio:** https://studio.youtube.com
- **FFmpeg Docs:** https://ffmpeg.org
- **Docker Docs:** https://docs.docker.com
- **Wav2Lip:** https://github.com/Rudrabha/Wav2Lip

## 💡 Pro Tips

1. **Keep logs readable:** `docker-compose logs --tail=50 -f`
2. **Test before deploying:** Use dev config
3. **Backup videos regularly:** `cp -r app/videos backup/`
4. **Monitor YouTube Studio:** Check stream health daily
5. **Review logs weekly:** `docker-compose logs | grep ERROR`
6. **Plan storage:** Videos = ~500MB/day
7. **Rotate Stream Key:** Every 3 months for security
8. **Test recovery:** Monthly full restart test