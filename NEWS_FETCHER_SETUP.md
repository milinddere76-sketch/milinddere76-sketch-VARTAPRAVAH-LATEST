# 🧠 VARTAPRAVAH - News Fetcher & Bulletin System

## Overview

This is the **BRAIN** of your VARTAPRAVAH channel - a complete automated system that:
- 🌐 Fetches news from multiple sources (India, Maharashtra, World)
- 🧠 Converts news to professional Marathi scripts
- 🎤 Generates audio via TTS
- 👁️ Creates lip-synced videos
- 📺 Streams to YouTube Live

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  NEWS API SOURCES                           │
│            NewsAPI, WorldNews API, etc.                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│         NEWS FETCHER (app/news_fetcher.py)                 │
│   • Fetches from India, Maharashtra, World categories      │
│   • Filters and deduplicates articles                       │
│   • Returns structured article data                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│      SCRIPT GENERATOR (app/script_generator.py)            │
│   • Translates to Marathi (English → Marathi)             │
│   • Creates professional news scripts                       │
│   • Generates full narration with intro/outro              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│          TTS ENGINE (tts_engine.py)                        │
│   • Converts Marathi text to audio                         │
│   • Uses Coqui TTS (high-quality Marathi voice)           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│       LIP-SYNC ENGINE (lipsync.py)                         │
│   • Creates video with lip-synced avatar                   │
│   • Uses Wav2Lip for realistic lip-sync                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│        YOUTUBE STREAMER (streamer.py)                      │
│   • Streams video to YouTube Live                          │
│   • Uses RTMP protocol                                      │
└─────────────────────────────────────────────────────────────┘
```

## 📁 New Files Added

### 1. **app/news_fetcher.py**
Fetches news from APIs

**Classes:**
- `NewsFetcher`: Main fetcher class
  - `fetch_india_news()`: India top headlines
  - `fetch_maharashtra_news()`: Maharashtra-specific news
  - `fetch_world_news()`: World headlines
  - `fetch_all_news()`: All categories combined

**Usage:**
```python
from news_fetcher import NewsFetcher

fetcher = NewsFetcher(newsapi_key="YOUR_KEY")
news = fetcher.fetch_all_news(limit=5)

# Returns:
# {
#   "India": [NewsArticle, ...],
#   "Maharashtra": [NewsArticle, ...],
#   "World": [NewsArticle, ...]
# }
```

### 2. **app/script_generator.py**
Converts news to Marathi scripts

**Classes:**
- `ScriptGenerator`: Main script generator
  - `translate_to_marathi()`: English → Marathi
  - `generate_bullet_script()`: Single bullet point
  - `generate_bulletin_script()`: Complete bulletin
  - `generate_full_narration()`: Full TTS text
  - `export_bulletin()`: Export in JSON/Text/SRT format

**Usage:**
```python
from script_generator import ScriptGenerator

generator = ScriptGenerator(use_google_translate=True)
bulletin = generator.generate_bulletin_script(news_data, max_bullets=5)
narration = generator.generate_full_narration(bulletin)
```

## 🔌 API Endpoints

### 1. **GET /news** - Fetch News
Fetch news from all categories

**Request:**
```bash
curl "http://localhost:8000/news?limit=5"
```

**Response:**
```json
{
  "status": "success",
  "total_articles": 15,
  "categories": {
    "India": [...],
    "Maharashtra": [...],
    "World": [...]
  },
  "timestamp": "2024-01-20T10:30:00"
}
```

### 2. **POST /bulletin** - Generate Bulletin
Generate complete Marathi bulletin script

**Request:**
```bash
curl -X POST "http://localhost:8000/bulletin" \
  -H "Content-Type: application/json" \
  -d '{
    "max_bullets": 5,
    "use_google_translate": true
  }'
```

**Response:**
```json
{
  "status": "success",
  "bulletin": {
    "intro": "नमस्कार, आपले वार्ताप्रवाह येथे।",
    "bullets": [...],
    "outro": "धन्यवाद देखने के लिए।",
    "total_bullets": 5,
    "timestamp": "2024-01-20T10:30:00"
  },
  "narration_text": "Full Marathi narration for TTS...",
  "message": "✅ Bulletin generated with 5 bullets"
}
```

### 3. **POST /bulletin-pipeline** - Full Pipeline 🧠
Complete pipeline: News → Marathi → TTS → Lip-sync → Stream

**Request:**
```bash
curl -X POST "http://localhost:8000/bulletin-pipeline" \
  -H "Content-Type: application/json" \
  -d '{
    "max_bullets": 5,
    "use_google_translate": true,
    "rtmp_url": "rtmp://a.rtmp.youtube.com/live2/STREAM_KEY"
  }'
```

**Response:**
```json
{
  "status": "success",
  "pipeline_steps": {
    "news_fetch": "✅ completed",
    "script_generation": "✅ completed",
    "tts": "✅ completed",
    "lipsync": "✅ completed",
    "streaming": "✅ scheduled"
  },
  "bulletin": {...},
  "audio_path": "output/bulletin_audio.wav",
  "video_path": "output/bulletin_video.mp4",
  "message": "✅ Complete pipeline executed: 5 bullets → video → stream"
}
```

## 🔐 Setup & Configuration

### 1. Get API Keys

#### NewsAPI Key (Free)
1. Go to https://newsapi.org/
2. Sign up for free account
3. Copy your API key
4. Add to `.env`:
```
NEWSAPI_KEY=your_newsapi_key_here
```

#### WorldNews API Key
1. Go to https://worldnewsapi.com/
2. Sign up for free account
3. Copy your API key
4. Add to `.env`:
```
WORLDNEWS_API_KEY=your_worldnews_key_here
```

#### Google Cloud Translation (Optional - for better Marathi translation)
1. Create Google Cloud project
2. Enable Translation API
3. Download service account JSON
4. Set environment variable:
```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

The new packages added:
- `requests==2.31.0` - For API calls
- `google-cloud-translate==3.14.0` - For Marathi translation (optional)

### 3. Create .env File
```bash
# NewsAPI
NEWSAPI_KEY=your_key_here

# WorldNews API
WORLDNEWS_API_KEY=your_key_here

# Optional: For Google Cloud Translation
GOOGLE_APPLICATION_CREDENTIALS=/path/to/google_credentials.json
```

### 4. Run the System
```bash
# Start FastAPI server
python app/main.py

# Server runs on http://localhost:8000

# Access Swagger UI
# http://localhost:8000/docs
```

## 🚀 Usage Examples

### Example 1: Quick News Fetch
```bash
# Fetch 3 articles per category
curl "http://localhost:8000/news?limit=3"
```

### Example 2: Generate Bulletin Only
```bash
# Generate Marathi bulletin (without streaming)
curl -X POST "http://localhost:8000/bulletin" \
  -H "Content-Type: application/json" \
  -d '{
    "max_bullets": 5,
    "use_google_translate": false
  }'
```

### Example 3: Full Automation (Pipeline)
```bash
# Complete automation: Fetch → Script → TTS → Video → YouTube
curl -X POST "http://localhost:8000/bulletin-pipeline" \
  -H "Content-Type: application/json" \
  -d '{
    "max_bullets": 5,
    "use_google_translate": true,
    "rtmp_url": "rtmp://a.rtmp.youtube.com/live2/YOUR_STREAM_KEY"
  }'
```

## 📊 Data Flow Examples

### Input Flow
```
NewsAPI Response:
{
  "title": "Maharashtra approves education policy",
  "description": "State govt announces comprehensive reform",
  "source": {"name": "PTI"},
  "url": "...",
  "urlToImage": "..."
}
        ↓
    NewsArticle Object:
{
  "title": "Maharashtra approves education policy",
  "description": "State govt announces comprehensive reform",
  "source": "PTI",
  "category": "Maharashtra",
  "timestamp": "10:30"
}
```

### Output Flow
```
News Article
  ↓
Translate to Marathi
  "महाराष्ट्र शिक्षा नीति मंजूर करते है"
  ↓
Generate Script
  "महाराष्ट्र शिक्षा नीति मंजूर करते है। राज्य सरकारने...।"
  ↓
Convert to Audio (Marathi TTS)
  output/bulletin_audio.wav
  ↓
Create Lip-Sync Video
  output/bulletin_video.mp4
  ↓
Stream to YouTube
  Live broadcast on YouTube!
```

## 🛠️ Customization

### Change News Categories
Edit `news_fetcher.py`:
```python
# Add custom categories
def fetch_sports_news(self, limit: int = 5):
    # Fetch sports news
    pass

def fetch_tech_news(self, limit: int = 5):
    # Fetch tech news
    pass
```

### Custom Marathi Translations
Edit `script_generator.py`:
```python
def translate_to_marathi(self, text: str) -> str:
    # Use your own translation service
    # API call to custom translation endpoint
    pass
```

### Custom TTS Settings
Edit `tts_engine.py`:
```python
# Change voice, speed, etc.
tts = TTS(
    model_name="tts_models/mr/guj_female/glow-tts",
    gpu=True,
    speed=1.1  # Adjust speed
)
```

## 🐳 Docker Integration

### Run in Docker
```bash
# Build Docker image
docker build -t vartapravah:latest .

# Run container
docker run -p 8000:8000 \
  -e NEWSAPI_KEY=your_key \
  -v $(pwd)/output:/app/output \
  vartapravah:latest

# Access
http://localhost:8000/docs
```

### Docker Compose
```bash
docker-compose up -d
```

## 📝 5 Bulletins System

Perfect for your 5 bulletins per day:

**Bulletin 1 (Morning 6 AM)**
- India news (top 5)
- Maharashtra news (top 5)
- World news (top 5)

**Bulletin 2 (Noon 12 PM)**
- Fresh India news
- State updates
- International news

**Bulletin 3 (Evening 5 PM)**
- Breaking India news
- Regional Maharashtra updates
- World headlines

**Bulletin 4 (Prime Time 8 PM)**
- Top news recap
- Business updates
- Global news

**Bulletin 5 (Night 10 PM)**
- End of day recap
- Tomorrow preview
- Weather forecast

**Automation:**
```bash
# Create cronjob for 5 bulletins
0 6 * * * curl -X POST http://localhost:8000/bulletin-pipeline ...
0 12 * * * curl -X POST http://localhost:8000/bulletin-pipeline ...
0 17 * * * curl -X POST http://localhost:8000/bulletin-pipeline ...
0 20 * * * curl -X POST http://localhost:8000/bulletin-pipeline ...
0 22 * * * curl -X POST http://localhost:8000/bulletin-pipeline ...
```

## ✅ Checklist for Setup

- [ ] Create `.env` file with API keys
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Test news fetcher: `python app/news_fetcher.py`
- [ ] Test script generator: `python app/script_generator.py`
- [ ] Start API server: `python app/main.py`
- [ ] Test endpoints via Swagger: http://localhost:8000/docs
- [ ] Configure YouTube RTMP URL
- [ ] Set up cronjobs for 5 bulletins
- [ ] Monitor logs and fine-tune

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'requests'"
```bash
pip install requests
```

### "Invalid API Key"
- Check `.env` file has correct NEWSAPI_KEY
- Verify key at https://newsapi.org/

### "Google Translate not available"
- Either set credentials for Google Cloud Translation
- Or set `use_google_translate=false` in requests

### "FFmpeg not found"
- Install FFmpeg: https://ffmpeg.org/download.html
- Add to PATH

## 📞 Support

For issues:
1. Check logs in terminal
2. Review `.env` configuration
3. Test individual components
4. Check API status (NewsAPI, YouTube)

---

**Made with ❤️ for VARTAPRAVAH - Automated News Broadcasting**
