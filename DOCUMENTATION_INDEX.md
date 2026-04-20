# VartaPravah Documentation Index

Welcome to **VartaPravah** - The AI Broadcast News System for 24×7 Marathi YouTube streaming.

## 📚 Documentation Structure

### 🚀 Start Here!
0. **[START_HERE.md](START_HERE.md)** - Quick navigation guide
   - 30-second summary
   - Reading order by use case
   - Common commands
   - Troubleshooting

1. **[COMPLETE_DELIVERY_SUMMARY.md](COMPLETE_DELIVERY_SUMMARY.md)** - Full delivery information
   - Complete file listing
   - All features delivered
   - Specifications
   - Quick start guide
   - Success metrics

### Quick Start (Start Here!)
2. **[SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md)** - High-level system summary
   - Complete pipeline overview
   - Feature summary
   - Quick deployment guide
   - Performance metrics

3. **[README.md](README.md)** - Project overview and features
   - Feature overview
   - Quick start (2 minutes)
   - API endpoints
   - System requirements

### Detailed Architecture
4. **[FINAL_ARCHITECTURE.md](FINAL_ARCHITECTURE.md)** - Complete technical architecture
   - System component diagram
   - Data flow pipeline
   - Bulletin scheduling
   - Performance metrics
   - Production topology

### Delivery Information
5. **[DELIVERY_STATUS.md](DELIVERY_STATUS.md)** - Complete delivery summary
   - What you received
   - Feature checklist
   - Specifications
   - Deployment checklist

### Detailed Guides
6. **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete setup and deployment
   - Prerequisites and setup steps
   - Docker usage and services
   - API usage examples
   - Configuration options
   - Troubleshooting guide
   - Production deployment

7. **[DOCKER_COMPOSE_GUIDE.md](DOCKER_COMPOSE_GUIDE.md)** - Docker Compose reference
   - Service architecture
   - Available configurations (standard, production, dev)
   - Commands reference
   - Networking and volumes
   - Resource limits
   - Debugging techniques

### Operations & Deployment
8. **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Pre and post-deployment
   - Pre-deployment checklist
   - Step-by-step deployment
   - Health checks
   - Rollback procedures
   - Escalation guides

9. **[STREAM_MONITORING_GUIDE.md](STREAM_MONITORING_GUIDE.md)** - FFmpeg stream monitoring
   - stream-monitor script features
   - Installation and usage
   - Configuration options
   - Deployment scenarios
   - Troubleshooting

10. **[BULLETIN_SCHEDULER_GUIDE.md](BULLETIN_SCHEDULER_GUIDE.md)** - Daily bulletin scheduling
   - Bulletin schedule (5 daily bulletins)
   - Integration steps
   - API endpoints for scheduling
   - Configuration and customization
   - Production setup

11. **[NEWS_GENERATION_RULES.md](NEWS_GENERATION_RULES.md)** - News generation rules enforcement
   - Minimum/maximum rules (5-25 items)
   - Breaking news threshold (25 items)
   - News validation system
   - Volume categorization
   - Error handling and best practices

12. **[FALLBACK_CACHE_SYSTEM.md](FALLBACK_CACHE_SYSTEM.md)** - Zero-downtime fallback system
   - Always-available video caching
   - Automatic fallback switching
   - Backup and recovery
   - Health monitoring
   - Production deployment

13. **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick command reference
   - Start/stop commands
   - API call examples
   - Debugging commands
   - Common scenarios
   - Pro tips

### Integration Code Examples
14. **[BULLETIN_SCHEDULER_INTEGRATION.md](BULLETIN_SCHEDULER_INTEGRATION.md)** - Scheduler integration code
   - Code snippets for main.py
   - Import statements
   - Initialization code
   - API endpoint examples

15. **[NEWS_RULES_INTEGRATION.md](NEWS_RULES_INTEGRATION.md)** - Rules engine integration code
   - Code snippets for main.py
   - Validation integration
   - Rule enforcement
   - Error handling

16. **[FALLBACK_INTEGRATION.md](FALLBACK_INTEGRATION.md)** - Fallback system integration code
   - Code snippets for main.py
   - Cache management
   - Stream integration
   - Health monitoring

17. **[LIPSYNC_INTEGRATION.md](LIPSYNC_INTEGRATION.md)** - Lip-sync & TTS integration code
   - Coqui TTS configuration
   - Wav2Lip integration
   - Complete pipeline usage
   - API endpoints
   - Error handling

18. **[NEWS_FETCHER_INTEGRATION.md](NEWS_FETCHER_INTEGRATION.md)** - News fetching & aggregation code
   - Multi-source fetching (NewsAPI + RSS)
   - Priority scoring system
   - Marathi conversion (basic + AI)
   - Ticker generation
   - API endpoints
   - Complete examples

## 🚀 Getting Started

### Path 1: Quick Deploy (5 minutes)
1. Copy `.env.example` → `.env`
2. Add YouTube Stream Key to `.env`
3. Run `./start.sh` (Linux/Mac) or `start.bat` (Windows)
4. Access API at http://localhost:8000/docs

### Path 2: Complete Setup (15 minutes)
1. Read [SETUP_GUIDE.md](SETUP_GUIDE.md) - Prerequisites section
2. Follow setup steps in [SETUP_GUIDE.md](SETUP_GUIDE.md)
3. Use [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) to verify
4. Reference [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for common tasks

### Path 3: Production Deployment (30 minutes)
1. Read [SETUP_GUIDE.md](SETUP_GUIDE.md) - Production deployment section
2. Use `docker-compose.prod.yml` instead of standard
3. Follow [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
4. Monitor with [DOCKER_COMPOSE_GUIDE.md](DOCKER_COMPOSE_GUIDE.md) - Monitoring section

## 📁 Project Structure

```
vartapravah/
├── 📖 README.md                      ← Start here
├── 📖 SETUP_GUIDE.md                 ← Detailed instructions
├── 📖 DOCKER_COMPOSE_GUIDE.md        ← Docker reference
├── 📖 DEPLOYMENT_CHECKLIST.md        ← Deployment verification
├── 📖 QUICK_REFERENCE.md             ← Command cheatsheet
├── 📖 DOCUMENTATION_INDEX.md          ← This file
│
├── 🐳 docker-compose.yml             ← Standard config
├── 🐳 docker-compose.prod.yml        ← Production config
├── 🐳 docker-compose.dev.yml         ← Development config
├── 🐳 Dockerfile                     ← Container definition
│
├── 📝 main.py                        ← FastAPI application
├── 📝 requirements.txt                ← Python dependencies
├── .env.example                       ← Config template
├── .env                               ← Your config (create from template)
│
├── 📁 app/
│   ├── encoder/                       ← Core engines
│   │   ├── anchor_engine.py           ← Anchor selection
│   │   ├── lipsync_engine.py          ← Wav2Lip integration
│   │   ├── graphics_engine.py         ← TV graphics
│   │   ├── scene_builder.py           ← Video composition
│   │   ├── ffmpeg_stream.py           ← Streaming engine
│   │   ├── tts_engine.py              ← Marathi TTS
│   │   ├── ticker.py                  ← Scrolling ticker
│   │   └── scheduler.py               ← News scheduling
│   │
│   └── assets/                        ← Media files
│       ├── anchors/                   ← Face images
│       ├── graphics/                  ← TV graphics
│       ├── fonts/                     ← Devanagari font
│       ├── intro.mp4                  ← Intro clip
│       └── outro.mp4                  ← Outro clip
│
├── 📁 logs/                           ← Watchdog logs
├── 📁 videos/                         ← Generated videos
└── 📁 temp/                           ← Temporary files
```

## 🎯 Quick Command Reference

### Start Services
```bash
./start.sh                          # Linux/Mac
start.bat                           # Windows
docker-compose up -d                # Manual
```

### Generate News
```bash
curl -X POST http://localhost:8000/generate-news \
  -H "Content-Type: application/json" \
  -d '{"headline": "बातमी", "content": "...", "category": "...", "breaking": false}'
```

### Manage Services
```bash
docker-compose ps                   # View status
docker-compose logs -f              # View logs
docker-compose down                 # Stop services
docker-compose build                # Rebuild images
```

### Debugging
```bash
docker-compose logs app             # App logs
docker-compose logs streamer        # Streamer logs
docker stats                        # Monitor resources
curl http://localhost:8000/status   # Check status
```

## 🔗 Key Features

✅ **Dual AI Anchors** - Alternating male/female with realistic faces  
✅ **Lip Sync Technology** - Wav2Lip for talking videos  
✅ **Professional Graphics** - TV-grade overlays and ticker  
✅ **Marathi TTS** - Natural Marathi speech synthesis  
✅ **Auto-Scheduling** - Configurable news generation intervals  
✅ **YouTube Live** - Direct RTMP streaming  
✅ **24/7 Uptime** - Watchdog monitors and restarts services  
✅ **Docker Orchestration** - Multi-container production setup  

## 🔧 Configuration Files

| File | Purpose |
|------|---------|
| `.env` | Your configuration (YouTube key, bitrate, etc.) |
| `docker-compose.yml` | Standard service setup |
| `docker-compose.prod.yml` | Production with health checks & limits |
| `docker-compose.dev.yml` | Development with hot reload |
| `Dockerfile` | Container build instructions |
| `requirements.txt` | Python package dependencies |

## 📊 Service Architecture

```
┌──────────────────────────────────────────┐
│   VartaPravah Broadcast System           │
├──────────────────────────────────────────┤
│                                          │
│  ┌─ app (FastAPI)                        │
│  │  └─ News generation, composition      │
│  │                                       │
│  ├─ streamer (FFmpeg)                    │
│  │  └─ YouTube RTMP broadcasting         │
│  │                                       │
│  └─ watchdog (Monitor)                   │
│     └─ Service health & auto-restart     │
│                                          │
└──────────────────────────────────────────┘
```

## 🚨 Common Issues & Solutions

| Issue | Solution | Documentation |
|-------|----------|---|
| Services won't start | Check `.env` exists | [SETUP_GUIDE.md](SETUP_GUIDE.md#troubleshooting) |
| API not responding | Verify app is running | [DOCKER_COMPOSE_GUIDE.md](DOCKER_COMPOSE_GUIDE.md#service-communication) |
| Stream not visible | Check YouTube Stream Key | [SETUP_GUIDE.md](SETUP_GUIDE.md#troubleshooting) |
| Videos not generating | Verify assets exist | [QUICK_REFERENCE.md](QUICK_REFERENCE.md#scenario-1-video-not-generating) |
| High CPU usage | Reduce video bitrate | [DOCKER_COMPOSE_GUIDE.md](DOCKER_COMPOSE_GUIDE.md#cpu-optimization) |

## 📱 API Documentation

### Interactive API Docs
Once running, visit: **http://localhost:8000/docs**

### Available Endpoints
- `POST /generate-news` - Generate video
- `POST /start-stream` - Start streaming
- `POST /stop-stream` - Stop streaming
- `GET /status` - Get system status

See [QUICK_REFERENCE.md](QUICK_REFERENCE.md#-api-calls) for examples.

## 🏆 Best Practices

1. **Always use docker-compose** - Ensures proper service orchestration
2. **Keep videos backed up** - At least weekly
3. **Monitor resources** - Check CPU/memory regularly
4. **Use production config** - For public deployments
5. **Test before going live** - Use dev environment first
6. **Review logs weekly** - Check for errors
7. **Rotate Stream Key** - Every 3 months for security
8. **Test recovery** - Monthly restart procedures

## 📞 Need Help?

### For Different Situations:

**Just want to run it?**  
→ Start with [README.md](README.md) and run `./start.sh`

**Need detailed setup?**  
→ Follow [SETUP_GUIDE.md](SETUP_GUIDE.md)

**Understanding Docker Compose?**  
→ Read [DOCKER_COMPOSE_GUIDE.md](DOCKER_COMPOSE_GUIDE.md)

**Deploying to production?**  
→ Use [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

**Quick command lookup?**  
→ Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

**Troubleshooting issues?**  
→ See [QUICK_REFERENCE.md](QUICK_REFERENCE.md#-common-scenarios) or [SETUP_GUIDE.md](SETUP_GUIDE.md#troubleshooting)

## 🎯 Your Next Steps

1. **Read**: [README.md](README.md) (5 minutes)
2. **Setup**: Follow [SETUP_GUIDE.md](SETUP_GUIDE.md) (15 minutes)
3. **Deploy**: Use [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) (5 minutes)
4. **Generate**: First news video via API (2 minutes)
5. **Monitor**: Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for ongoing operations

## 📚 Additional Resources

- **FFmpeg Docs:** https://ffmpeg.org/documentation.html
- **YouTube Live:** https://support.google.com/youtube/answer/2474026
- **Docker Docs:** https://docs.docker.com/
- **Python FastAPI:** https://fastapi.tiangolo.com/
- **Wav2Lip:** https://github.com/Rudrabha/Wav2Lip

## 🎬 Project Status

✅ **Production Ready**  
✅ **24/7 Streaming Capable**  
✅ **Fully Documented**  
✅ **Docker Optimized**  
✅ **AI Powered**  

---

**VartaPravah** - Broadcasting Marathi News 24/7 with AI  
*Built with FastAPI, FFmpeg, Wav2Lip, and Docker*