# VartaPravah - AI Broadcast News System 📡

A complete production-ready AI broadcast system for 24×7 Marathi YouTube News Channel with realistic AI anchors, professional graphics, and automated news generation.

## ✨ Features

### Core Capabilities
- 🧑‍💼 **Dual AI Anchors** - Alternating male/female anchors with realistic faces
- 🗣️ **Lip Sync Technology** - Wav2Lip integration for talking face videos
- 📺 **Professional Graphics** - TV-grade overlays (logo, ticker, lower third, breaking news)
- 🎙️ **Marathi TTS** - Natural speech synthesis in Marathi language
- 📰 **Automated News** - Scheduled or on-demand video generation
- 📡 **YouTube Live** - Continuous RTMP streaming with auto-recovery
- ⏱️ **Live Clock** - Real-time clock overlay
- 🎬 **Intro/Outro Support** - Smooth segment transitions
- 🔄 **Auto-Recovery** - Watchdog ensures 24/7 uptime
- 💾 **Fallback Content** - Automatic fallback if no new content

### Technical Features
- **Docker Orchestration** - Multi-container setup with docker-compose
- **GPU Acceleration** - Optional CUDA support for lip-sync
- **Modular Architecture** - Separate engines for each feature
- **RESTful API** - Full REST API for control and integration
- **Comprehensive Logging** - Complete visibility into operations
- **State Management** - Persistent anchor state tracking

## 🚀 Quick Start

### Prerequisites
- Docker Desktop
- YouTube Stream Key
- 4GB+ RAM (8GB+ recommended)

### 1. Setup (1 minute)
```bash
cp .env.example .env
# Edit .env and add YouTube Stream Key
```

### 2. Launch (30 seconds)
```bash
# Linux/Mac
chmod +x start.sh && ./start.sh

# Windows
start.bat
```

### 3. Generate News
```bash
curl -X POST http://localhost:8000/generate-news \
  -H "Content-Type: application/json" \
  -d '{
    "headline": "महाराष्ट्रातील मुख्य बातमी",
    "content": "बातमीचा तपशील येथे आहे।",
    "category": "राजकारण",
    "breaking": false
  }'
```

## 📚 Documentation

- **[Full Setup Guide](SETUP_GUIDE.md)** - Detailed configuration and deployment
- **[API Docs](http://localhost:8000/docs)** - Interactive API documentation
- **[Docker Compose](docker-compose.yml)** - Multi-service architecture

## 🐳 Docker Services

| Service | Purpose | Status |
|---------|---------|--------|
| **app** | FastAPI server, video generation | Port 8000 |
| **streamer** | FFmpeg RTMP broadcaster | Continuous |
| **watchdog** | Health monitoring & auto-restart | Active |

## 📡 API Endpoints

### Generate News Video
```bash
POST /generate-news
```
Request body:
```json
{
  "headline": "मुख्य बातमी",
  "content": "विस्तृत मजकूर",
  "category": "राजकारण",
  "breaking": false
}
```

### Streaming Control
```bash
POST /start-stream  # Start YouTube streaming
POST /stop-stream   # Stop streaming
GET /status         # Get system status
```

## ⚙️ Configuration

Edit `.env` to customize:
```bash
YOUTUBE_STREAM_KEY=your_key_here
VIDEO_BITRATE=3000k
AUDIO_BITRATE=128k
NEWS_INTERVAL=5
TTS_LANG=mr
```

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed configuration options.

## 📊 Monitoring

```bash
# View logs
docker-compose logs -f app

# Check status
docker-compose ps

# Access API
http://localhost:8000/docs

# Run FFmpeg stream monitor (Linux/Mac)
./stream-monitor.sh &

# Run FFmpeg stream monitor (Windows)
stream-monitor.bat
```

For detailed monitoring setup, see [STREAM_MONITORING_GUIDE.md](STREAM_MONITORING_GUIDE.md)

## 🎨 Customization

Replace assets in `app/assets/`:
- `logo.png` - Channel logo
- `studio.jpg` - Background image
- `anchors/male.png` - Male anchor
- `anchors/female.png` - Female anchor
- `intro.mp4`, `outro.mp4` - Clips

## 📈 System Requirements

- CPU: 2+ cores (4+ recommended)
- RAM: 2GB+ (8GB+ recommended)
- Storage: 5GB+ (50GB+ for production)
- Internet: 5+ Mbps upload
- GPU: Optional (NVIDIA CUDA for faster lip-sync)

## 🔧 Troubleshooting

See [SETUP_GUIDE.md](SETUP_GUIDE.md#troubleshooting) for detailed troubleshooting.

**Common issues:**
- Services won't start → Check `.env` exists
- Stream not visible → Verify YouTube Stream Key
- Lip sync failing → Check GPU or logs
- Videos not generating → Verify assets directory

## 📝 Project Structure

```
vartapravah/
├── app/encoder/          # Core engines
├── app/assets/           # Images, fonts, clips
├── main.py               # FastAPI app
├── docker-compose.yml    # Service orchestration
├── Dockerfile            # Container definition
├── requirements.txt      # Python packages
├── SETUP_GUIDE.md       # Detailed guide
└── README.md            # This file
```

## 🤝 Support

1. Check [SETUP_GUIDE.md](SETUP_GUIDE.md)
2. View logs: `docker-compose logs`
3. Test API: http://localhost:8000/docs

---

**Production Ready** | **24/7 Broadcasting** | **Marathi Support** | **AI Powered**