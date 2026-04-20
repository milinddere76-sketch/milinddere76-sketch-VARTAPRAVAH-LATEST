# VartaPravah Deployment Checklist

## Pre-Deployment

### System Requirements
- [ ] Docker installed and running
- [ ] Docker Compose installed (v1.29+)
- [ ] 4GB+ RAM available
- [ ] 10GB+ free disk space
- [ ] Stable internet connection (5+ Mbps upload)
- [ ] YouTube account with live streaming enabled

### Configuration
- [ ] YouTube Stream Key obtained from YouTube Studio
- [ ] `.env` file created from `.env.example`
- [ ] YOUTUBE_STREAM_KEY added to `.env`
- [ ] All required assets placed:
  - [ ] `app/assets/logo.png`
  - [ ] `app/assets/studio.jpg`
  - [ ] `app/assets/anchors/male.png`
  - [ ] `app/assets/anchors/female.png`
  - [ ] `app/assets/fonts/NotoSansDevanagari-Bold.ttf`
  - [ ] `app/assets/intro.mp4` (optional)
  - [ ] `app/assets/outro.mp4` (optional)

### Code Verification
- [ ] All Python files present and syntactically correct
- [ ] requirements.txt has all dependencies
- [ ] Dockerfile builds without errors
- [ ] docker-compose.yml is valid YAML

## Deployment Steps

### 1. Initial Build (First Time Only)
```bash
# Verify .env exists
ls -la .env

# Build Docker images
docker-compose build

# Expected output: Successfully tagged vartapravah:latest
```
- [ ] Build successful
- [ ] No build errors

### 2. Start Services
```bash
# Start all services in background
docker-compose up -d

# Wait 30 seconds for services to initialize
sleep 30

# Check service status
docker-compose ps

# Should show 3 services as "running"
```
- [ ] All 3 services running
- [ ] No error messages

### 3. Verify App Service
```bash
# Check API is responding
curl http://localhost:8000/status

# Expected output: {"streaming": false, "videos_count": 1, "news_queue": 0}
```
- [ ] API returns 200 OK
- [ ] Status endpoint works

### 4. Verify Streaming Service
```bash
# Check FFmpeg process
docker-compose exec streamer ps aux | grep ffmpeg

# Should show ffmpeg process running
```
- [ ] FFmpeg process visible
- [ ] Correct RTMP URL in command

### 5. Verify Watchdog Service
```bash
# Check watchdog logs
docker-compose logs watchdog --tail=10

# Should show recent health checks
```
- [ ] Watchdog running
- [ ] No errors in logs

### 6. Test Video Generation
```bash
# Generate test news video
curl -X POST http://localhost:8000/generate-news \
  -H "Content-Type: application/json" \
  -d '{
    "headline": "परीक्षण",
    "content": "परीक्षण बातमी",
    "category": "परीक्षण",
    "breaking": false
  }'

# Check for generated video
ls -la app/videos/
```
- [ ] Video generated successfully
- [ ] File size > 100MB
- [ ] No errors in logs

### 7. Test YouTube Streaming (Optional)
```bash
# Verify YouTube Studio shows active stream
# Open YouTube Studio > Go Live > Check for stream from RTMP_KEY
# Stream should show "Streaming" status
```
- [ ] YouTube shows "Connected" status
- [ ] No connection errors
- [ ] Bitrate matches expected value

### 8. Monitor System
```bash
# Monitor resource usage
docker stats

# Check all logs
docker-compose logs

# Monitor for 5 minutes, should be stable
```
- [ ] CPU usage reasonable (< 50% for app)
- [ ] Memory usage stable
- [ ] No error messages in logs

## Health Checks Post-Deployment

### Daily Checks
```bash
# 1. Services running
docker-compose ps
# Expected: 3 services, all "Up"

# 2. API responding
curl http://localhost:8000/status
# Expected: HTTP 200

# 3. Recent logs
docker-compose logs --tail=20
# Expected: No ERROR or CRITICAL messages

# 4. Disk space
df -h
# Expected: > 5% free space

# 5. Videos generated
ls -la app/videos/ | wc -l
# Expected: Increasing number of files
```

### Weekly Checks
```bash
# 1. YouTube streaming status
# Check YouTube Studio for 24h streaming continuity

# 2. Backup videos
cp -r app/videos backup/videos_$(date +%Y%m%d)

# 3. Check logs for errors
docker-compose logs | grep ERROR | wc -l
# Expected: < 10 errors

# 4. Memory analysis
docker stats --no-stream | head -10
```

### Monthly Checks
```bash
# 1. Clean old videos (>30 days)
find app/videos -type f -mtime +30 -delete

# 2. Rebuild images
docker-compose build --no-cache

# 3. Test recovery
docker-compose down
docker-compose up -d
# Expected: Full recovery within 2 minutes

# 4. Performance review
docker stats --no-stream
# Compare with baseline
```

## Rollback Procedure

If deployment fails:

### Step 1: Stop Services
```bash
docker-compose down
# All containers and networks removed
```
- [ ] All services stopped

### Step 2: Check Logs
```bash
docker-compose logs
# Review error messages
```
- [ ] Identified root cause

### Step 3: Fix Issue
```bash
# Common fixes:
# 1. Missing .env: cp .env.example .env
# 2. Missing assets: Download required files
# 3. Port conflict: Change port in docker-compose.yml
# 4. Build error: docker-compose build --no-cache
```
- [ ] Issue resolved

### Step 4: Restart
```bash
docker-compose up -d
# Verify with checks above
```
- [ ] Services running
- [ ] API responding

## Troubleshooting Guide

| Issue | Cause | Solution |
|-------|-------|----------|
| Services won't start | Port 8000 in use | Change PORTS in compose file |
| API returns 500 | Missing assets | Verify assets directory |
| Streaming not visible | Invalid Stream Key | Check YouTube Studio |
| High CPU usage | Video encoding issue | Reduce VIDEO_BITRATE |
| Out of memory | Container limits exceeded | Increase available RAM |
| Watchdog restarting | Service unstable | Check service logs |

## Escalation Procedures

### Level 1: Service Restart
```bash
docker-compose restart app
# Wait 30 seconds
docker-compose logs app --tail=20
```

### Level 2: Service Rebuild
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Level 3: Full System Reset
```bash
docker-compose down -v
docker-compose up -d
# This removes all data, requires re-initialization
```

### Level 4: Infrastructure Investigation
```bash
# Check system resources
free -h
df -h

# Check Docker
docker system df
docker system prune -a

# Check network
netstat -an | grep 8000
```

## Success Criteria

Your deployment is successful when:

✅ All 3 services show "Up" status  
✅ API responds to status endpoint  
✅ Videos are being generated  
✅ No ERROR messages in logs  
✅ CPU usage < 60%  
✅ Memory usage stable  
✅ YouTube streaming shows as active  
✅ Watchdog is monitoring services  

## Post-Deployment Configuration

### Customize News Generation Interval
Edit `.env`:
```bash
NEWS_INTERVAL=10  # Generate every 10 minutes instead of 5
docker-compose restart app
```

### Adjust Video Quality
Edit `.env`:
```bash
VIDEO_BITRATE=5000k    # Higher quality
AUDIO_BITRATE=192k     # Better audio
docker-compose restart app
```

### Enable GPU Acceleration (if available)
Edit `.env`:
```bash
CUDA_AVAILABLE=true
docker-compose up -d --build
```

### Change Streaming Parameters
Edit `docker-compose.yml` streamer service command and restart.

## Support Resources

- 📖 [SETUP_GUIDE.md](SETUP_GUIDE.md) - Detailed setup instructions
- 🐳 [DOCKER_COMPOSE_GUIDE.md](DOCKER_COMPOSE_GUIDE.md) - Docker Compose documentation
- 📚 [README.md](README.md) - Project overview
- 🔗 [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- 🎬 [YouTube Live Documentation](https://developers.google.com/youtube/v3)

## Contact & Issues

For issues:
1. Check relevant documentation files
2. Review docker-compose logs
3. Verify YouTube Stream Key is active
4. Ensure all assets are present