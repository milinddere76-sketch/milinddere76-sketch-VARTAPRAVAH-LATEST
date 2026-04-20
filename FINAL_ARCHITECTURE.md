# VartaPravah Final Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    VARTAPRAVAH BROADCAST SYSTEM                         │
│                                                                          │
│  News API                                                                │
│     │                                                                    │
│     ├─→ Script Generator (Content Preparation)                         │
│     │      ├─→ News Validation (5-25 items)                           │
│     │      ├─→ Category Mapping                                        │
│     │      └─→ Breaking News Detection (25 items)                     │
│     │                                                                    │
│     ├─→ TTS Engine (Coqui XTTS v2)                                    │
│     │      ├─→ Marathi Language Support                               │
│     │      ├─→ Dual Anchor Voices (Male/Female)                       │
│     │      └─→ Audio Generation                                        │
│     │                                                                    │
│     ├─→ Lip Sync Generator (Wav2Lip)                                  │
│     │      ├─→ Anchor Image Selection                                  │
│     │      ├─→ Audio Synchronization                                   │
│     │      └─→ Talking Head Video                                      │
│     │                                                                    │
│     ├─→ Scene Builder (Composition)                                    │
│     │      ├─→ Background Image                                        │
│     │      ├─→ Overlay Graphics (Ticker, Logo, Clock)                 │
│     │      ├─→ Breaking News Banner                                    │
│     │      └─→ Video Composition                                       │
│     │                                                                    │
│     └─→ Final Output: final_news.mp4                                   │
│          ├─→ Cached in /videos/final_news.mp4                         │
│          ├─→ Backup: /videos/final_news_backup.mp4                    │
│          └─→ Always Available                                          │
│                                                                          │
│  FFmpeg Stream (Loop Mode)                                             │
│     ├─→ Source: final_news.mp4                                         │
│     ├─→ Loop: -stream_loop -1 (infinite)                              │
│     ├─→ Encoding: libx264 (h.264)                                      │
│     ├─→ Output: RTMP → YouTube Live                                    │
│     └─→ Result: 24/7 Broadcasting                                      │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### 1. News API (Input Layer)

**Purpose:** Accept news input and trigger generation

```
POST /generate-news
├─ Headline (str)
├─ Content (str)
├─ Category (str)
└─ Breaking (bool)

POST /bulletin/queue
├─ Batch news items
└─ Priority scheduling

GET /news/rules
└─ Validate before generation
```

**Validation:**
- Minimum 5 items per bulletin
- Maximum 25 items per bulletin
- At 25 items: Auto-breaking news flag

---

### 2. Script Generator (Content Preparation)

**Module:** `news_rules_engine.py`

```python
Input: News items (5-25)
  ├─ Validate each item
  ├─ Check required fields
  ├─ Enforce length rules
  ├─ Categorize volume
  └─ Apply breaking news format if 25 items

Output: Processed news array
  ├─ Standardized format
  ├─ Breaking news indicators
  └─ Ready for TTS
```

**Key Functions:**
- `validate_news_item()`: Verify individual news
- `validate_news_list()`: Batch validation
- `apply_breaking_news_format()`: Add special formatting
- `categorize_news_volume()`: Classify bulletin type

---

### 3. TTS Engine (Coqui XTTS v2)

**Module:** `tts_engine.py` (Updated for Coqui)

```
Input: Marathi text
  └─ Content string

Processing:
  ├─ Language: Marathi (mr)
  ├─ Model: tts_models/multilingual/multi-dataset/xtts_v2
  ├─ Voice: Anchor selection (male/female)
  └─ Quality: High-fidelity Marathi TTS

Output: Audio file
  ├─ Format: WAV/MP3
  ├─ Sample rate: 22050 Hz
  ├─ Duration: Dynamic (based on text)
  └─ Ready for lip-sync
```

**Configuration:**
```python
TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")
tts.tts_to_file(
    text=content,
    file_path="audio.wav",
    language="mr"
)
```

---

### 4. Lip Sync Generator (Wav2Lip)

**Module:** `lipsync_engine.py`

```
Input: 
  ├─ Anchor image (PNG/JPG)
  └─ Audio file (WAV)

Processing:
  ├─ Model: Wav2Lip pre-trained
  ├─ Face detection
  ├─ Audio-visual synchronization
  ├─ Realistic mouth movement
  └─ Video generation

Output: Talking head video
  ├─ Format: MP4 (H.264)
  ├─ Resolution: 1920x1080
  ├─ Duration: Audio duration
  └─ Ready for composition
```

**Anchor Selection:**
- Alternates male/female
- State maintained in JSON
- Professional images (1080p)

---

### 5. Scene Builder (Composition)

**Module:** `scene_builder.py` + `graphics_engine.py`

```
Input Components:
  ├─ Lip-sync video (anchor)
  ├─ Background image
  ├─ Headline text
  ├─ Category/Ticker text
  └─ Breaking news flag

Processing:
  ├─ Load background image (1920x1080)
  ├─ Overlay lip-sync video (center)
  ├─ Add TV graphics:
  │  ├─ Logo (top-right)
  │  ├─ Ticker (bottom - scrolling)
  │  ├─ Clock (top-right)
  │  └─ Breaking news banner (if breaking)
  ├─ Composite layers
  └─ Encode with FFmpeg

Output: Broadcast-ready video
  ├─ Format: MP4 (H.264 + AAC)
  ├─ Resolution: 1920x1080
  ├─ Frame rate: 30 FPS
  ├─ Bitrate: 3000 kbps
  └─ Quality: Professional broadcast
```

---

### 6. Fallback Cache (Storage)

**Module:** `fallback_manager.py`

```
Primary Fallback:
  └─ /videos/final_news.mp4
     ├─ Always available
     ├─ Updated with each new video
     └─ Atomic replacement

Backup Fallback:
  └─ /videos/final_news_backup.mp4
     ├─ Previous version
     ├─ Disaster recovery
     └─ Auto-managed

Guarantees:
  ├─ Never empty
  ├─ Always verified
  ├─ Instant streaming
  └─ Zero downtime
```

---

### 7. FFmpeg Stream (RTMP Loop)

**Module:** `ffmpeg_stream.py`

```
Command:
  ffmpeg -re \
    -stream_loop -1 \
    -i app/videos/final_news.mp4 \
    -c:v libx264 \
    -preset veryfast \
    -b:v 3000k \
    -c:a aac \
    -b:a 128k \
    -f flv \
    rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}

Features:
  ├─ Loop mode: Infinite (-stream_loop -1)
  ├─ Encoding: H.264 (libx264)
  ├─ Bitrate: 3000 kbps (configurable)
  ├─ Preset: veryfast (low CPU)
  ├─ Audio: AAC 128k
  ├─ Output: RTMP (YouTube Live)
  └─ Result: 24/7 streaming

Guarantees:
  ├─ Always streaming
  ├─ No gaps between videos
  ├─ Fallback if new not ready
  └─ YouTube compatible
```

---

## Data Flow Diagram

```
┌──────────────┐
│  News Input  │
│  (5-25 items)│
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│ Script Generator     │
│ ✓ Validate          │
│ ✓ Categorize        │
│ ✓ Process           │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ TTS Engine (Coqui)   │
│ Input: Marathi text  │
│ Output: Audio WAV    │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Lip Sync (Wav2Lip)   │
│ Input: Audio + Image │
│ Output: Video MP4    │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Scene Builder        │
│ ✓ Compose layers     │
│ ✓ Add graphics       │
│ Output: Broadcast MP4│
└──────┬───────────────┘
       │
       ▼
┌──────────────────────────┐
│ Fallback Cache Manager   │
│ Store: final_news.mp4    │
│ Backup: final_news_backup│
│ Always: Available        │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│ FFmpeg RTMP Stream       │
│ Loop: final_news.mp4     │
│ Output: YouTube Live     │
│ Status: 24/7 Broadcasting│
└──────────────────────────┘
```

---

## Bulletin Scheduling Integration

```
Bulletin Scheduler
├─ 05:00 AM: Morning    ──→ News Gen ──→ Stream ──→ YouTube
├─ 12:00 PM: Afternoon  ──→ News Gen ──→ Stream ──→ YouTube
├─ 05:00 PM: Evening    ──→ News Gen ──→ Stream ──→ YouTube
├─ 09:00 PM: Prime Time ──→ News Gen ──→ Stream ──→ YouTube
└─ 12:00 AM: Night      ──→ News Gen ──→ Stream ──→ YouTube

Each bulletin:
1. Generate news video (full pipeline)
2. Update fallback cache
3. Stream continuously (never stops)
4. Fallback to cached video if delayed
5. Repeat at next scheduled time
```

---

## Component Dependencies

```
News API
  ├─ bulletin_scheduler.py (scheduling)
  ├─ news_rules_engine.py (validation)
  ├─ tts_engine.py (Coqui XTTS)
  ├─ lipsync_engine.py (Wav2Lip)
  ├─ scene_builder.py (composition)
  ├─ graphics_engine.py (overlays)
  ├─ fallback_manager.py (cache)
  ├─ ffmpeg_stream.py (streaming)
  └─ anchor_engine.py (talent selection)

Python Dependencies:
  ├─ FastAPI (web framework)
  ├─ TTS (Coqui text-to-speech)
  ├─ ffmpeg-python (stream control)
  ├─ Pillow (image processing)
  ├─ torch (ML framework)
  └─ apscheduler (job scheduling)

External Tools:
  ├─ FFmpeg (video encoding)
  └─ YouTube RTMP (streaming endpoint)
```

---

## Configuration

### Environment Variables

```env
# YouTube
YOUTUBE_STREAM_KEY=your_rtmp_key

# TTS (Coqui)
TTS_LANG=mr                          # Marathi
TTS_MODEL=tts_models/multilingual/multi-dataset/xtts_v2

# Video Output
VIDEO_WIDTH=1920
VIDEO_HEIGHT=1080
VIDEO_FPS=30
VIDEO_BITRATE=3000k
AUDIO_BITRATE=128k

# Paths
VIDEOS_DIR=app/videos
ASSETS_DIR=app/assets
TEMP_DIR=app/temp

# Scheduling
NEWS_INTERVAL=5                      # Minutes (or use bulletin times)
```

---

## Deployment Topology

### Docker Services

```yaml
services:
  app:
    Image: vartapravah:latest
    Container: vartapravah_app
    Port: 8000
    Volumes:
      - videos/
      - assets/
      - temp/
    Environment:
      - PYTHONUNBUFFERED=1
      - All configuration

  streamer:
    Image: jrottenberg/ffmpeg:6.0-alpine
    Container: vartapravah_stream
    Command: ffmpeg loop stream
    Input: /videos/final_news.mp4
    Output: RTMP YouTube

  watchdog:
    Image: alpine:latest
    Container: vartapravah_watchdog
    Task: Monitor service health
    Action: Auto-restart on failure
```

---

## Production Flow

### Scenario: Evening Bulletin at 5 PM

```
Time: 16:59:00
  └─ System ready, streaming current video

Time: 17:00:00
  ├─ Bulletin scheduler triggers
  ├─ Queue news items from database/API
  ├─ Validate: 8 items ✓
  ├─ Generate: Script Generator
  ├─ Generate: TTS audio (Coqui)
  ├─ Generate: Lip-sync video (Wav2Lip)
  ├─ Generate: Scene composition
  ├─ Update: Fallback cache (final_news.mp4)
  └─ Stream: New video (seamless transition)

Time: 17:12:30
  └─ Video ends, loops (stream_loop -1)
  └─ Repeats until next bulletin

Time: 21:00:00
  └─ Prime Time bulletin starts
  └─ Repeat process
  └─ Stream updated
  └─ No downtime occurred
```

---

## Performance Metrics

| Component | Processing Time | Output |
|-----------|-----------------|--------|
| Script Validation | < 1 sec | Processed items |
| TTS (Coqui) | 2-5 sec/min | Audio WAV |
| Lip Sync (Wav2Lip) | 30-60 sec | Video MP4 |
| Scene Building | 10-20 sec | Final video |
| Cache Update | < 1 sec | Ready to stream |
| Stream Start | < 1 sec | YouTube Live |
| **Total Pipeline** | **1-2 minutes** | **Broadcasting** |

---

## Reliability Features

✅ **News Validation**: Enforced rules (5-25 items)  
✅ **TTS Reliability**: Coqui with fallback audio  
✅ **Lip Sync Quality**: Wav2Lip with CPU fallback  
✅ **Scene Composition**: Layered approach with error handling  
✅ **Fallback Cache**: Always available primary + backup  
✅ **Stream Continuity**: Loop mode infinite repetition  
✅ **Auto-Recovery**: Watchdog monitor with restart  
✅ **Health Checks**: Continuous verification  

---

## API Endpoints Summary

```
News Generation:
  POST /generate-news (manual)
  POST /bulletin/queue (batch)
  GET /news/rules (validation)
  POST /news/validate (pre-check)

Bulletin Scheduling:
  GET /bulletin/schedule
  GET /bulletin/status
  POST /bulletin/generate/{type}

Stream Control:
  POST /start-stream-safe
  POST /stop-stream
  GET /stream/status

Fallback Management:
  GET /fallback/status
  POST /fallback/update
  GET /fallback/verify
  GET /fallback/stats

Monitoring:
  GET /health
  GET /health/fallback
  GET /status
```

---

## Architecture Principles

1. **Separation of Concerns**: Each component has single responsibility
2. **Data Flow**: Linear progression through pipeline
3. **Fallback First**: Always have video to stream
4. **No Downtime**: Stream never stops
5. **Validation First**: Check before processing
6. **Atomic Updates**: Safe cache replacement
7. **Continuous Monitoring**: Health checks always running
8. **Professional Quality**: Broadcast-grade output

---

## Production Readiness Checklist

- ✅ News API endpoint
- ✅ Script generator with validation
- ✅ TTS engine (Coqui XTTS v2)
- ✅ Lip sync generator (Wav2Lip)
- ✅ Scene builder with graphics
- ✅ Fallback cache system
- ✅ FFmpeg RTMP stream
- ✅ Bulletin scheduler (5 daily times)
- ✅ Error handling & recovery
- ✅ Docker orchestration
- ✅ Health monitoring
- ✅ Stream monitoring
- ✅ Documentation
- ✅ Configuration templates

---

**VartaPravah Final Architecture: Production-Ready 24/7 Broadcasting System! 🎬📺**