# VartaPravah Fallback Video Cache System

## Overview

The **Fallback Video Cache System** ensures 24/7 streaming without crashes by:
- Always maintaining `/videos/final_news.mp4` as primary fallback
- Streaming old video if new video not ready (zero downtime)
- Automatic backup and recovery system
- Real-time health monitoring

---

## Architecture

### Fallback Video Structure

```
/app/videos/
├── final_news.mp4              ← Primary fallback (always available)
├── final_news_backup.mp4       ← Automatic backup
├── final_news_temp.mp4         ← Temporary (during update)
├── news_*.mp4                  ← New videos (temporary)
└── playlist_*.mp4              ← Generated playlists
```

### Streaming Strategy

```
┌─────────────────────────────────────────┐
│  Is New Video Ready?                    │
└──────────────┬──────────────────────────┘
               │
        ┌──────┴──────┐
        YES          NO
        │             │
        ▼             ▼
   Stream New    Stream Fallback
   + Update      (no downtime!)
     Cache
```

---

## Core Concepts

### 1. Primary Fallback (`final_news.mp4`)
- Always available for streaming
- Updated when new videos are ready
- Never deleted
- Always verified before stream starts

### 2. Backup Copy (`final_news_backup.mp4`)
- Automatic copy of previous `final_news.mp4`
- Used if primary gets corrupted
- Updated each time primary is replaced

### 3. Cache Update Process
1. New video validated
2. Current fallback backed up
3. New video copied to temp
4. Temp verified (size/integrity)
5. Atomic move to primary
6. Stats updated

### 4. Stream Continuity
- Stream never waits for new video
- If new video not ready → stream falls back
- Eliminates downtime completely
- Background cache updates

---

## Key Features

✅ **Zero Downtime**: Always have video to stream  
✅ **Atomic Updates**: Safe fallback replacement  
✅ **Auto Backup**: Previous version always saved  
✅ **Health Checks**: Verify fallback integrity  
✅ **Statistics**: Track usage patterns  
✅ **Error Recovery**: Fallback to backup if needed  
✅ **Thread Safe**: Async updates don't block stream  

---

## Usage Examples

### Example 1: Basic Fallback Management

```python
from encoder.fallback_manager import FallbackVideoManager

# Initialize
fallback = FallbackVideoManager(videos_dir="app/videos")

# Ensure fallback exists before streaming
if fallback.ensure_fallback_exists():
    print("Fallback ready!")
else:
    print("Warning: No fallback available")

# Get video to stream (new or fallback)
video = fallback.get_stream_video(new_video_path="app/videos/news_123.mp4")
# Returns: news_123.mp4 if ready, final_news.mp4 if not
```

### Example 2: Stream with Automatic Fallback

```python
from encoder.fallback_manager import StreamWithFallback

# Initialize
fallback = FallbackVideoManager()
stream = StreamWithFallback(fallback, streamer)

# Start stream - uses fallback if new video not ready
result = stream.start_stream(
    new_video_path="app/videos/news_latest.mp4",
    stream_key=os.getenv('YOUTUBE_STREAM_KEY')
)

print(f"Status: {result['status']}")
print(f"Using fallback: {result['using_fallback']}")
```

### Example 3: Cache Update

```python
# Update fallback cache when new video ready
if fallback.update_cache("app/videos/news_456.mp4"):
    print("Cache updated successfully")
else:
    print("Cache update failed (fallback still available)")
```

### Example 4: Health Check

```python
# Verify fallback integrity
status = fallback.get_status()

print(f"Status: {status['status']}")
print(f"Primary: {status['primary_video']}")
print(f"Backup: {status['backup_video']}")
print(f"Stats: {status['statistics']}")

# Output:
# Status: healthy
# Primary: {'exists': True, 'size_mb': 42.5, 'path': '.../final_news.mp4'}
# Backup: {'exists': True, 'size_mb': 40.2, 'path': '.../final_news_backup.mp4'}
# Stats: {'fallback_uses': 5, 'cache_updates': 3, ...}
```

---

## API Integration

### New Endpoints for Fallback Management

#### 1. Get Fallback Status

```bash
GET /fallback/status
```

**Response:**
```json
{
  "status": "healthy",
  "fallback_ready": true,
  "primary_video": {
    "exists": true,
    "size_mb": 42.5,
    "path": "app/videos/final_news.mp4"
  },
  "backup_video": {
    "exists": true,
    "size_mb": 40.2,
    "path": "app/videos/final_news_backup.mp4"
  },
  "message": "✓ Primary fallback ready",
  "statistics": {
    "fallback_uses": 5,
    "last_fallback_use": "2026-04-21T14:35:22.123456",
    "cache_updates": 3,
    "last_cache_update": "2026-04-21T14:30:15.654321"
  }
}
```

#### 2. Update Fallback Cache

```bash
POST /fallback/update
```

**Request:**
```json
{
  "video_path": "app/videos/news_latest.mp4"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Cache updated successfully",
  "new_size_mb": 42.5,
  "fallback_ready": true
}
```

#### 3. Verify Fallback Integrity

```bash
GET /fallback/verify
```

**Response:**
```json
{
  "primary_exists": true,
  "primary_size_mb": 42.5,
  "backup_exists": true,
  "backup_size_mb": 40.2,
  "is_healthy": true,
  "status": "✓ Primary fallback ready"
}
```

#### 4. Start Stream with Fallback

```bash
POST /stream/start-safe
```

**Request:**
```json
{
  "new_video_path": "app/videos/news_latest.mp4"
}
```

**Response:**
```json
{
  "status": "streaming",
  "video": "app/videos/final_news.mp4",
  "using_fallback": false,
  "fallback_ready": true,
  "message": "New video"
}
```

---

## Integration in main.py

### Step 1: Import and Initialize

```python
from encoder.fallback_manager import FallbackVideoManager, StreamWithFallback

# Global instances
fallback_manager = None
stream_with_fallback = None

@app.on_event("startup")
def startup():
    global fallback_manager, stream_with_fallback
    
    # Initialize fallback system
    fallback_manager = FallbackVideoManager(videos_dir=VIDEOS_DIR)
    stream_with_fallback = StreamWithFallback(fallback_manager, streamer)
    
    # Ensure fallback exists
    if not fallback_manager.ensure_fallback_exists():
        logger.warning("No fallback video. Creating placeholder...")
        from encoder.fallback_manager import create_placeholder_video
        create_placeholder_video(
            os.path.join(VIDEOS_DIR, "final_news.mp4"),
            duration=60
        )
```

### Step 2: Update Stream Start

```python
@app.post("/start-stream-safe")
def start_stream_safe(request: Dict = None):
    """Start streaming with fallback protection."""
    
    # Get latest video if available
    new_video = None
    if video_list:
        new_video = video_list[-1]
    
    # Start with fallback protection
    result = stream_with_fallback.start_stream(
        new_video_path=new_video,
        stream_key=os.getenv('YOUTUBE_STREAM_KEY')
    )
    
    return result
```

### Step 3: Add Fallback Endpoints

```python
@app.get("/fallback/status")
def get_fallback_status():
    """Get fallback system status."""
    return fallback_manager.get_status()

@app.get("/fallback/verify")
def verify_fallback():
    """Verify fallback integrity."""
    return fallback_manager.verify_fallback_integrity()

@app.post("/fallback/update")
def update_fallback(request: Dict):
    """Update fallback cache with new video."""
    video_path = request.get('video_path')
    
    if fallback_manager.update_cache(video_path):
        return {
            'status': 'success',
            'message': 'Cache updated',
            'fallback_ready': True
        }
    else:
        return {
            'status': 'error',
            'message': 'Cache update failed',
            'fallback_ready': fallback_manager.ensure_fallback_exists()
        }
```

---

## Fallback Scenarios

### Scenario 1: Normal Operation

```
Time 00:00 → News generated (news_001.mp4)
            → Stream new video
            → Update cache (final_news.mp4 = news_001.mp4)

Time 05:00 → News generation started
            → Stream continues (using final_news.mp4)
            → New video not ready yet (no downtime!)
            → Once ready → Update cache
            → Continue streaming new video
```

### Scenario 2: Video Generation Delay

```
Time 00:00 → News video ready (takes 5 minutes)
            → Request to stream new video
            → Video not ready yet!
            → System: Use fallback instead
            → Result: Stream fallback (no downtime)
            → Once new video ready → Update cache → Stream it
```

### Scenario 3: Network Interruption

```
Stream interrupted during broadcast

Option A: With Fallback
- Restart immediately with fallback
- No content loss
- Quality maintained

Option B: Without Fallback
- Stream stops
- Downtime occurs
- YouTube shows offline
```

### Scenario 4: Primary Corruption

```
Primary fallback corrupted (corrupt.mp4)

1. Fallback manager detects issue
2. System tries primary → fails
3. Falls back to backup copy
4. Broadcast continues seamlessly
5. Admin notified to regenerate
```

---

## Monitoring

### Check Fallback Health

```bash
# Quick status
curl http://localhost:8000/fallback/status

# Detailed verification
curl http://localhost:8000/fallback/verify

# View logs
docker-compose logs app | grep -i fallback
```

### Monitor Fallback Usage

```python
stats = fallback_manager.get_stats()

print(f"Fallback uses: {stats['fallback_uses']}")
print(f"Cache updates: {stats['cache_updates']}")
print(f"Last use: {stats['last_fallback_use']}")
```

### Real-time Monitoring

```bash
# Watch for fallback usage in logs
docker-compose logs -f app | grep "Streaming fallback"

# Monitor stream status
curl -s http://localhost:8000/stream/status | jq .
```

---

## Best Practices

### ✅ DO:
- Update cache after each new video
- Verify fallback before streaming
- Check health status regularly
- Monitor fallback usage patterns
- Maintain backup integrity
- Test fallback recovery monthly
- Archive old videos (don't delete fallback)

### ❌ DON'T:
- Manually delete final_news.mp4
- Skip cache updates
- Ignore fallback warnings
- Stream without fallback ready
- Let old videos accumulate
- Forget to set stream key
- Skip health checks

---

## Troubleshooting

### Issue: Fallback Not Found

**Symptoms:**
```
Error: No fallback available
```

**Solution:**
```bash
# Create placeholder
curl -X POST http://localhost:8000/fallback/create-placeholder

# Or manually
ffmpeg -f lavfi -i color=c=blue:s=1920x1080:d=60 \
       -f lavfi -i sine=f=1000:d=60 \
       -c:v libx264 -c:a aac \
       app/videos/final_news.mp4
```

### Issue: Fallback Corrupted

**Symptoms:**
```
Error: Fallback verification failed
Using backup instead
```

**Solution:**
```bash
# Restore from backup
cp app/videos/final_news_backup.mp4 app/videos/final_news.mp4

# Verify
curl http://localhost:8000/fallback/verify
```

### Issue: Cache Not Updating

**Symptoms:**
```
Streaming old content repeatedly
```

**Solution:**
```bash
# Manual cache update
curl -X POST http://localhost:8000/fallback/update \
  -H "Content-Type: application/json" \
  -d '{"video_path": "app/videos/news_latest.mp4"}'

# Check logs
docker-compose logs app | grep -i "cache"
```

---

## Statistics & Reporting

### Sample Statistics

```json
{
  "fallback_uses": 12,
  "last_fallback_use": "2026-04-21T14:35:22",
  "cache_updates": 45,
  "last_cache_update": "2026-04-21T14:30:15",
  "stream_starts": 180,
  "stream_interruptions": 0
}
```

### Analysis

- **Fallback Uses**: Times fallback was used (due to delayed new videos)
- **Cache Updates**: Successful cache updates
- **Stream Starts**: Total stream initiations
- **Stream Interruptions**: Total stream failures

---

## Production Checklist

- [ ] Fallback video exists
- [ ] Backup video exists
- [ ] Both videos verified
- [ ] Fallback size > 10 MB
- [ ] Health check passed
- [ ] Stats show normal usage
- [ ] Monitoring alerts configured
- [ ] Backup procedure tested
- [ ] Recovery procedure tested
- [ ] Team trained on system

---

## Summary

| Component | Purpose | Status |
|-----------|---------|--------|
| Primary Fallback | Always stream | Critical |
| Backup Copy | Disaster recovery | Important |
| Cache Manager | Update fallback | Core |
| Health Monitor | Verify system | Always on |
| Statistics | Track patterns | Passive |

**VartaPravah Fallback System = Zero-Downtime Broadcasting! 📡**