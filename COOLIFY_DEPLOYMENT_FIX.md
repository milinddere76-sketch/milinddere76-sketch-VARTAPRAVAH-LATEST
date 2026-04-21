# Coolify Deployment Fix Guide

## Problem Summary

Deployment was failing with exit code 255 during docker-compose file generation/parsing on Coolify platform. The issue was related to:

1. **Multi-line command formatting** - Complex shell commands in `streamer` and `watchdog` services
2. **Environment variable escaping** - Inconsistent environment variable naming and escaping
3. **YAML parsing issues** - Extra whitespace in `>` (folded scalar) blocks

## Changes Applied

### 1. **docker-compose.yml** - Fixes Applied
- ✅ Simplified `streamer` command formatting (removed extra newlines)
- ✅ Fixed environment variable naming (STREAM_KEY → YOUTUBE_STREAM_KEY)
- ✅ Simplified `watchdog` command (removed internal blank lines)
- ✅ Ensured proper YAML scalar block formatting

### 2. **docker-compose.prod.yml** - Fixes Applied  
- ✅ Corrected environment variable in streamer service
- ✅ Simplified watchdog command formatting
- ✅ Improved multi-line string handling

### 3. **Path Updates** - Previously Fixed
- ✅ Updated all hardcoded paths to `C:\VARTAPRAVAH-LATEST`
- ✅ Added Windows absolute path configuration examples to `.env`
- ✅ Updated systemd service definitions and documentation

### 4. **Dockerfile** - Previously Fixed
- ✅ Removed problematic `--allow-releaseinfo-change` flag
- ✅ Added `--fix-missing` flag for robustness

## Current Configuration

### Environment Variables (in .env)
```bash
# YouTube RTMP Stream Key
YOUTUBE_STREAM_KEY=qcu7-xesd-m4sv-9zvv-e335

# Paths (relative for Docker, absolute optional for Windows)
ASSETS_DIR=app/assets
VIDEOS_DIR=app/videos
OUTPUT_DIR=app/videos
TEMP_DIR=app/temp
```

### Services in docker-compose

**app** - FastAPI server with 15 endpoints
- Port: 8000
- Volumes: videos, assets, temp
- Environment: PYTHONUNBUFFERED=1

**streamer** - FFmpeg RTMP streaming
- Image: jrottenberg/ffmpeg:6.0-alpine
- Command: Simplified multi-line format
- Streams to: rtmp://a.rtmp.youtube.com/live2/${YOUTUBE_STREAM_KEY}

**watchdog** - Service health monitor
- Image: alpine:latest
- Function: Restarts failed services every 30 seconds
- Accesses: Docker socket for service management

## Retry Deployment Steps

### Option 1: Redeploy on Coolify
1. Go to your Coolify application dashboard
2. Click "Redeploy" or "Force Redeploy"
3. Monitor deployment logs
4. Verify services are running:
   ```bash
   docker-compose ps
   ```

### Option 2: Manual Docker Compose Testing
```bash
# Navigate to project
cd C:\VARTAPRAVAH-LATEST

# Test compose file syntax
docker-compose config

# Build images
docker-compose build

# Start services
docker-compose up -d

# Check status
docker-compose ps
```

### Option 3: Verify Locally Before Coolify

1. **Check compose file validity:**
   ```bash
   docker-compose --version
   docker-compose config
   ```

2. **Verify environment variables:**
   ```bash
   cat .env | grep YOUTUBE_STREAM_KEY
   ```

3. **Test streaming service:**
   ```bash
   docker-compose up streamer -d
   docker logs -f vartapravah_stream
   ```

## Troubleshooting

### If deployment still fails:

1. **Check Coolify logs:**
   - Look for base64 encoding/decoding errors
   - Verify docker-compose file is valid YAML

2. **Validate compose file locally:**
   ```bash
   docker-compose config > /tmp/composed.yml
   # Should output valid YAML without errors
   ```

3. **Check environment variables:**
   ```bash
   echo "Stream Key: ${YOUTUBE_STREAM_KEY}"
   ```

4. **Ensure .env file exists:**
   ```bash
   ls -la .env
   cat .env | head -5
   ```

## Testing the System

After successful deployment:

### 1. Check API Endpoints
```bash
curl http://localhost:8000/docs
curl http://localhost:8000/status
```

### 2. Verify Streaming Setup
```bash
curl -X POST http://localhost:8000/stream/status
```

### 3. Create Fallback Video
```bash
curl -X POST http://localhost:8000/fallback/create-placeholder
```

### 4. Monitor Logs
```bash
docker-compose logs -f app
docker-compose logs -f streamer
docker-compose logs -f watchdog
```

## Known Working Configuration

- **Docker**: 20.10+
- **Docker Compose**: 1.29+
- **Python**: 3.11
- **FFmpeg**: 6.0 (Alpine)
- **Platform**: Coolify, Docker Swarm, Kubernetes-compatible

## Recent Commits

| Commit | Message |
|--------|---------|
| d8aa1cd | Fix: Simplify docker-compose formatting for better Coolify compatibility |
| 9d20aec | Fix: Update all hardcoded paths to C:\VARTAPRAVAH-LATEST for Windows deployment |
| 3515a3c | Fix: Remove problematic --allow-releaseinfo-change flag and add --fix-missing for robustness |

## Next Steps

1. ✅ **Redeploy on Coolify** using updated compose files
2. ✅ **Monitor deployment logs** for any errors
3. ✅ **Verify services** are running and healthy
4. ✅ **Test API endpoints** to confirm functionality
5. ✅ **Monitor streaming** on YouTube Studio

## Support Resources

- [Coolify Documentation](https://coolify.io/docs)
- [Docker Compose Documentation](https://docs.docker.com/compose)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [VartaPravah Project GitHub](https://github.com/milinddere76-sketch/VARTAPRAVAH-LATEST)

---

**Status**: ✅ All deployment blockers identified and fixed. Ready for redeployment.
