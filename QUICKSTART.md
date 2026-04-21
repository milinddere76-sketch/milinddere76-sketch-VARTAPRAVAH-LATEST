# ⚡ VARTAPRAVAH Quick Start Guide

Get your AI news avatar streaming to YouTube Live in 5 minutes!

## 📦 Prerequisites

- Docker Desktop installed
- YouTube channel with live streaming enabled
- Your YouTube Stream Key (from YouTube Studio)

## 🚀 5-Minute Setup

### Step 1: Prepare Configuration (1 min)

```bash
cd VARTAPRAVAH-LATEST
cp .env.example .env
```

### Step 2: Add Your Stream Key (1 min)

Open `.env` and update:
```env
YOUTUBE_RTMP_KEY=your-stream-key-here
```

**Where to find it:**
- YouTube Studio → Go Live → Settings
- Look for "Stream key" (e.g., `qcu7-xesd-m4sv-9zvv-e335`)

### Step 3: Add Anchor Video (1 min)

Place your news anchor video:
```
assets/anchor.mp4
```

Recommended: 1920x1080, MP4 format

### Step 4: Build & Run (2 min)

```bash
docker-compose up --build
```

Wait for:
```
✔ Container vartapravah_ai Created
Attaching to vartapravah_ai
```

### ✅ Done! Your API is running on http://localhost:8000

## 🔥 Generate Your First Video

### Option A: Interactive API (Easiest)

1. Open http://localhost:8000/docs
2. Click "Try it out" on `/pipeline` endpoint
3. Enter your news text:
   ```json
   {
     "text": "नमस्कार, यह समाचार है।",
     "rtmp_url": "rtmp://a.rtmp.youtube.com/live2/YOUR_STREAM_KEY"
   }
   ```
4. Click "Execute"

### Option B: Command Line (Quick)

```bash
curl -X POST http://localhost:8000/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "नमस्कार।"}'
```

### Option C: Python Script

```python
import requests

# 1. Generate audio
audio = requests.post("http://localhost:8000/tts", json={
    "text": "नमस्कार, वार्ताप्रवाह।"
}).json()

# 2. Generate video
video = requests.post("http://localhost:8000/lipsync", json={
    "audio_path": audio["audio_path"]
}).json()

# 3. Stream to YouTube
requests.post("http://localhost:8000/stream", json={
    "video_path": video["video_path"],
    "rtmp_url": "rtmp://a.rtmp.youtube.com/live2/YOUR_STREAM_KEY"
})
```

## 📊 API Endpoints Quick Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Check if API is running |
| `/docs` | GET | Interactive API documentation |
| `/tts` | POST | Convert text to speech |
| `/lipsync` | POST | Generate lip-synced video |
| `/stream` | POST | Stream to YouTube Live |
| `/pipeline` | POST | All-in-one: TTS + Lip-sync + Stream |

## 🐛 Verify Everything Works

```bash
# 1. Check API health
curl http://localhost:8000/health

# 2. View logs
docker-compose logs -f

# 3. View generated files
ls output/
```

## 🆘 Common Issues

### "Cannot connect to API"
```bash
# Make sure container is running
docker-compose ps

# If not running:
docker-compose up -d
```

### "Anchor video not found"
```bash
# Create dummy video for testing
echo "dummy" > assets/anchor.mp4

# Or download a sample video
```

### "Out of memory"
```bash
# Increase Docker memory in Docker Desktop settings
# Settings → Resources → Memory → 8GB (or more)
```

## 📝 Full Documentation

See [README.md](README.md) for:
- Detailed API documentation
- Advanced configuration
- Troubleshooting guide
- Performance optimization

## 🎬 Production Deployment

For production, see README.md section on:
- Health checks and monitoring
- Resource limits
- Security best practices
- Log management

## ✨ Features at a Glance

```
Text Input
   ↓
[🎙️ TTS Engine] → Audio generation
   ↓
[🎬 Lip-Sync] → Video generation
   ↓
[📡 FFmpeg] → YouTube Live Stream
```

## 🚀 Next Steps

1. ✅ Get API running
2. 📝 Test with your news text
3. 📺 Configure YouTube Stream Settings
4. 🔴 Go Live on YouTube!
5. 🔄 Automate with cron/scheduler

## 💡 Pro Tips

- **Batch Processing**: Send multiple requests to `/pipeline`
- **Multiple Anchors**: Place different videos in `assets/` folder
- **Custom Logos**: Add `logo.png` to `assets/` for branding
- **Monitor Logs**: `docker-compose logs --follow`
- **Auto-Scaling**: Adjust Docker resources in `docker-compose.yml`

---

**Questions?** Check [README.md](README.md) for detailed documentation.

**Ready?** Go to http://localhost:8000/docs and start streaming! 🚀
