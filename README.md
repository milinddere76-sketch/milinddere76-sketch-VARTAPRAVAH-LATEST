# VARTAPRAVAH - AI News Avatar Generator 🎬

Convert news text to professionally lip-synced video and stream live to YouTube in real-time.

## 🎯 Features

- ✅ **Multi-language Text-to-Speech** - Convert text to natural speech (Hindi, Marathi, English, etc.)
- ✅ **Automatic Lip-Syncing** - Wav2Lip deep learning model for perfect lip-sync
- ✅ **YouTube Live Streaming** - Direct RTMP streaming to YouTube Live
- ✅ **REST API** - FastAPI endpoints for all operations
- ✅ **Docker Containerized** - One-command deployment
- ✅ **Health Monitoring** - Automatic restart and health checks
- ✅ **Error Handling** - Graceful error recovery with detailed logging

## 📋 System Requirements

- **Docker Desktop** (Windows/Mac) or **Docker + Docker Compose** (Linux)
- **4GB+ RAM** minimum (8GB+ recommended for smooth processing)
- **20GB+ disk space** (for models and output)
- **YouTube Channel** with Live streaming enabled

## 🚀 Quick Start

### 1. Clone & Setup

```bash
cd VARTAPRAVAH-LATEST
copy .env.example .env
```

### 2. Configure YouTube RTMP Key

Edit `.env` and add your YouTube Stream Key:

```env
YOUTUBE_RTMP_KEY=your-stream-key-here
YOUTUBE_RTMP_URL=rtmp://a.rtmp.youtube.com/live2/
```

**Get your Stream Key:**
1. Go to [YouTube Studio Live](https://studio.youtube.com/channel/UC.../livestreaming/manage)
2. Click "Stream Settings"
3. Copy the Stream Key (e.g., `qcu7-xesd-m4sv-9zvv-e335`)

### 3. Add Anchor Video

Place your anchor video file:

```
VARTAPRAVAH-LATEST/
└── assets/
    └── anchor.mp4    (Your news anchor video - 1920x1080 recommended)
    └── logo.png      (Optional - Channel logo/branding)
```

### 4. Build & Run

```bash
# Build image and start container
docker-compose up --build

# View logs
docker-compose logs -f vartapravah

# Stop container
docker-compose down
```

## 🔌 API Usage

Once running, access the API at `http://localhost:8000`

### API Endpoints

#### Health Check
```bash
curl http://localhost:8000/health
```

#### 1️⃣ Text-to-Speech
```bash
curl -X POST http://localhost:8000/tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "नमस्कार, यह एक समाचार है।",
    "output_path": "output/audio.wav"
  }'
```

#### 2️⃣ Lip-Sync Video
```bash
curl -X POST http://localhost:8000/lipsync \
  -H "Content-Type: application/json" \
  -d '{
    "audio_path": "output/audio.wav",
    "video_path": "assets/anchor.mp4",
    "output_video": "output/video.mp4"
  }'
```

#### 3️⃣ Stream to YouTube
```bash
curl -X POST http://localhost:8000/stream \
  -H "Content-Type: application/json" \
  -d '{
    "video_path": "output/video.mp4",
    "rtmp_url": "rtmp://a.rtmp.youtube.com/live2/YOUR_STREAM_KEY"
  }'
```

#### 🎯 Complete Pipeline (All-in-One)
```bash
curl -X POST http://localhost:8000/pipeline \
  -H "Content-Type: application/json" \
  -d '{
    "text": "नमस्कार, वार्ताप्रवाह मध्ये आपले स्वागत आहे।",
    "rtmp_url": "rtmp://a.rtmp.youtube.com/live2/YOUR_STREAM_KEY"
  }'
```

### Interactive API Docs

Open `http://localhost:8000/docs` in your browser for Swagger UI - try endpoints interactively!

## 📁 Project Structure

```
VARTAPRAVAH-LATEST/
│
├── docker-compose.yml       # Container orchestration
├── Dockerfile              # Image definition
├── requirements.txt        # Python dependencies
├── .env.example           # Configuration template
├── README.md              # This file
│
├── app/
│   ├── main.py           # Entry point (FastAPI server)
│   ├── api.py            # REST API endpoints
│   ├── tts_engine.py     # Text-to-Speech (Coqui TTS)
│   ├── lipsync.py        # Lip-sync (Wav2Lip)
│   └── streamer.py       # YouTube RTMP streaming (FFmpeg)
│
├── assets/
│   ├── anchor.mp4        # Anchor video (you provide)
│   └── logo.png          # Channel logo (optional)
│
├── output/
│   ├── audio.wav         # Generated audio files
│   ├── video.mp4         # Lip-synced videos
│   └── final.mp4         # Final output
│
└── logs/
    └── vartapravah.log   # Application logs
```

## 🔧 Configuration

### Environment Variables (.env)

```env
# YouTube
YOUTUBE_RTMP_KEY=your-stream-key
YOUTUBE_RTMP_URL=rtmp://a.rtmp.youtube.com/live2/

# TTS
TTS_MODEL=tts_models/multilingual/multi-dataset/xtts_v2
TTS_GPU=false

# Paths
ANCHOR_VIDEO=assets/anchor.mp4
OUTPUT_DIR=output

# API
API_HOST=0.0.0.0
API_PORT=8000
API_LOG_LEVEL=info
```

## 🐛 Troubleshooting

### Issue: Container fails to start

**Check logs:**
```bash
docker-compose logs vartapravah
```

**Common causes:**
- Out of disk space → Clean up `output/` folder
- Out of RAM → Increase Docker memory limits
- Port 8000 already in use → Change port in docker-compose.yml

### Issue: TTS model fails to load

**Solution:**
```bash
# Delete cached models and retry
docker-compose down
docker system prune -a
docker-compose up --build
```

### Issue: Wav2Lip not generating video

**Ensure:**
- Audio file exists and is valid WAV format
- Anchor video is MP4 format at 1920x1080 resolution
- FFmpeg is properly installed (included in Docker)

**Debug:**
```bash
# Access container shell
docker exec -it vartapravah_ai bash

# Test Wav2Lip manually
python Wav2Lip/inference.py \
  --checkpoint_path Wav2Lip/checkpoints/wav2lip.pth \
  --face assets/anchor.mp4 \
  --audio output/audio.wav \
  --outfile output/test.mp4
```

### Issue: YouTube streaming fails

**Verify:**
1. Stream Key is correct (check YouTube Studio)
2. YouTube Live is enabled on your channel
3. RTMP URL format: `rtmp://a.rtmp.youtube.com/live2/STREAM_KEY`

**Check FFmpeg:**
```bash
docker exec -it vartapravah_ai ffmpeg -version
```

## 📊 Performance Tips

1. **Use GPU acceleration** (if available):
   - Update Dockerfile: Change `gpu=False` to `gpu=True`
   - Install NVIDIA Docker: https://github.com/NVIDIA/nvidia-docker

2. **Optimize Video Quality:**
   - For faster processing: Lower resolution anchor video
   - For better quality: Use 1080p anchor with high bitrate

3. **Memory Management:**
   - Clear output folder periodically: `rm -rf output/*.mp4`
   - Monitor disk usage: `docker-compose stats`

## 🔐 Security Best Practices

1. **Never commit .env** - Add to .gitignore
2. **Use environment secrets** - Don't hardcode stream keys
3. **Restrict API access** - Use firewall rules or proxy
4. **Update models regularly** - Keep TTS and Wav2Lip models current

## 📝 Logging

View application logs:

```bash
# Real-time logs
docker-compose logs -f vartapravah

# Last 100 lines
docker-compose logs --tail=100

# Specific time range
docker-compose logs --since 2024-01-15 --until 2024-01-16
```

Log file inside container: `/app/logs/vartapravah.log`

## 🤝 API Response Examples

### Success Response
```json
{
  "status": "success",
  "audio_path": "output/audio.wav",
  "video_path": "output/video.mp4",
  "timestamp": "2024-01-15T10:30:45.123456",
  "message": "✅ Complete pipeline executed successfully"
}
```

### Error Response
```json
{
  "detail": "Audio file not found: output/audio.wav"
}
```

## 📚 Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| API Framework | FastAPI | 0.104.1 |
| Text-to-Speech | Coqui TTS | 0.22.0 |
| Lip-Sync | Wav2Lip | Latest |
| Video Processing | FFmpeg | 8.1+ |
| ML Framework | PyTorch | Latest (CPU) |
| Container | Docker | Latest |
| Server | Uvicorn | 0.24.0 |

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Coqui TTS Documentation](https://github.com/coqui-ai/TTS)
- [Wav2Lip Repository](https://github.com/Rudrabha/Wav2Lip)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)

## 📝 License

This project is provided as-is for educational and personal use.

## ⚙️ System Architecture

```
┌─────────────────────────────────────────────┐
│         Client / External System            │
│  (News Feed, Scheduling System, etc.)       │
└──────────────┬──────────────────────────────┘
               │
               ▼
       ┌───────────────────┐
       │   FastAPI REST    │
       │      Server       │
       │  (Port 8000)      │
       └───────────────────┘
               │
      ┌────────┼────────┐
      ▼        ▼        ▼
  ┌────────────────────────────────┐
  │  TTS Engine (Coqui)            │
  │  Text → Audio (WAV)            │
  └────────────────────────────────┘
               │
               ▼
  ┌────────────────────────────────┐
  │  Lip-Sync Engine (Wav2Lip)     │
  │  Audio + Video → Sync Video    │
  └────────────────────────────────┘
               │
               ▼
  ┌────────────────────────────────┐
  │  Streamer (FFmpeg)             │
  │  MP4 → RTMP → YouTube Live     │
  └────────────────────────────────┘
               │
               ▼
       ┌─────────────────┐
       │  YouTube Live   │
       │   Broadcast     │
       └─────────────────┘
```

## 🆘 Support

For issues or questions:
1. Check logs: `docker-compose logs`
2. Review troubleshooting section above
3. Ensure Docker and dependencies are up-to-date

---

**Made with ❤️ for content creators & news organizations**

Version: 1.0.0 | Last Updated: 2024-01-15
