# 🚀 VARTAPRAVAH - How to Run

## Option 1: Using FastAPI Server + Web Endpoints (RECOMMENDED)

**Best for:** Scheduling, automation, remote control

```bash
# Start the server
python app/main.py

# Server runs on http://localhost:8000
# Open Swagger UI: http://localhost:8000/docs
```

**Then use any endpoint:**

```bash
# Fetch news
curl http://localhost:8000/news?limit=5

# Generate bulletin
curl -X POST http://localhost:8000/bulletin \
  -H "Content-Type: application/json" \
  -d '{"max_bullets": 5}'

# Full pipeline (News → Video → YouTube)
curl -X POST http://localhost:8000/bulletin-pipeline \
  -H "Content-Type: application/json" \
  -d '{
    "max_bullets": 5,
    "rtmp_url": "rtmp://a.rtmp.youtube.com/live2/YOUR_STREAM_KEY"
  }'
```

---

## Option 2: Direct Pipeline Execution (SIMPLE)

**Best for:** Quick testing, one-off runs, learning

```bash
# Run the complete pipeline directly
python app/pipeline_demo.py

# This will:
# 1. Fetch news
# 2. Generate Marathi script
# 3. Create audio
# 4. Generate video
# 5. (Optional) Stream to YouTube
```

---

## Option 3: Custom Python Script (ADVANCED)

**Best for:** Custom logic, integration with other systems

```python
from news_fetcher import NewsFetcher
from script_generator import generate_marathi_script
from tts_engine import generate_audio
from lipsync import run_lipsync

# 1. Fetch news
fetcher = NewsFetcher()
news = fetcher.fetch_all_news(limit=5)

# 2. Generate Marathi script (simple function)
script = generate_marathi_script(news_list, bulletin_type="सकाळ")

# 3. Generate audio
audio = generate_audio(script)

# 4. Generate video with lip-sync
video = run_lipsync(audio)

# 5. Stream to YouTube (optional)
from streamer import stream_to_youtube
stream_to_youtube(video, "rtmp://...")
```

---

## Setup Required

1. **Get NewsAPI Key** (Free)
   - Go to: https://newsapi.org/
   - Sign up and copy your API key

2. **Create .env file**
   ```bash
   NEWSAPI_KEY=your_api_key_here
   WORLDNEWS_API_KEY=your_api_key_here (optional)
   GOOGLE_APPLICATION_CREDENTIALS=/path/to/google_creds.json (optional)
   ```

3. **Install packages**
   ```bash
   pip install -r requirements.txt
   ```

---

## Bulletin Types (Marathi)

| Type | Marathi | English | Time |
|------|---------|---------|------|
| Morning | सकाळ | Morning | 6 AM |
| Noon | मध्य | Noon | 12 PM |
| Evening | संध्या | Evening | 5 PM |
| Prime Time | प्राइम | Prime Time | 8 PM |
| Night | रात्र | Night | 10 PM |

**Usage:**
```python
from script_generator import generate_marathi_script

# Morning bulletin
script = generate_marathi_script(news_list, "सकाळ")

# Noon bulletin
script = generate_marathi_script(news_list, "मध्य")

# Evening bulletin
script = generate_marathi_script(news_list, "संध्या")
```

---

## Scheduling 5 Bulletins Per Day

### On Linux/Mac (Crontab)
```bash
# Edit crontab
crontab -e

# Add these lines:
0 6 * * * cd /path/to/VARTAPRAVAH-LATEST && python app/pipeline_demo.py
0 12 * * * cd /path/to/VARTAPRAVAH-LATEST && python app/pipeline_demo.py
0 17 * * * cd /path/to/VARTAPRAVAH-LATEST && python app/pipeline_demo.py
0 20 * * * cd /path/to/VARTAPRAVAH-LATEST && python app/pipeline_demo.py
0 22 * * * cd /path/to/VARTAPRAVAH-LATEST && python app/pipeline_demo.py
```

### On Windows (Task Scheduler)
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger time (6 AM, 12 PM, etc.)
4. Set action:
   ```
   Program: python
   Arguments: C:\VARTAPRAVAH-LATEST\app\pipeline_demo.py
   Start in: C:\VARTAPRAVAH-LATEST
   ```
5. Repeat for each bulletin time

### Using FastAPI + Scheduler
```python
from apscheduler.schedulers.background import BackgroundScheduler
import requests

scheduler = BackgroundScheduler()

def run_bulletin():
    requests.post("http://localhost:8000/bulletin-pipeline", 
                  json={"max_bullets": 5})

# Schedule 5 bulletins
scheduler.add_job(run_bulletin, 'cron', hour=6, minute=0)
scheduler.add_job(run_bulletin, 'cron', hour=12, minute=0)
scheduler.add_job(run_bulletin, 'cron', hour=17, minute=0)
scheduler.add_job(run_bulletin, 'cron', hour=20, minute=0)
scheduler.add_job(run_bulletin, 'cron', hour=22, minute=0)

scheduler.start()
```

---

## YouTube Setup

1. Go to YouTube Studio
2. Click "Go Live" (or "Create" → "Go Live")
3. Choose "RTMP ingestion"
4. Copy your Stream URL (RTMP URL)
5. Set environment variable:
   ```bash
   export YOUTUBE_RTMP_URL='rtmp://a.rtmp.youtube.com/live2/YOUR_STREAM_KEY'
   ```

---

## Troubleshooting

**"ModuleNotFoundError"**
```bash
pip install -r requirements.txt
```

**"Invalid API Key"**
- Check .env file for correct NEWSAPI_KEY
- Verify at https://newsapi.org/account

**"FFmpeg not found"**
- Install FFmpeg: https://ffmpeg.org/download.html
- Add to PATH

**"No module named 'google.cloud'"**
- Google Cloud Translation is optional
- System works without it (uses fallback)
- To enable: `pip install google-cloud-translate`

**"No RTMP URL configured"**
- YouTube streaming is optional
- Set YOUTUBE_RTMP_URL to enable
- Video will still be created without it

---

## Quick Commands

```bash
# Start server
python app/main.py

# Run complete pipeline (one-off)
python app/pipeline_demo.py

# Test news fetcher only
python -c "from news_fetcher import NewsFetcher; f = NewsFetcher(); print(f.fetch_all_news(limit=2))"

# Test script generator only
python -c "
from script_generator import generate_marathi_script
news = [{'title': 'Test news', 'description': 'Test', 'source': 'PTI'}]
print(generate_marathi_script(news, 'सकाळ'))
"
```

---

## Architecture

```
┌─────────────────────────────────────────┐
│  VARTAPRAVAH - The Brain of Your Channel│
└────────────────────┬────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
   [Option 1]   [Option 2]   [Option 3]
   FastAPI      Pipeline     Custom
   Server       Demo Script   Python
   (Endpoints)  (Direct)      (Flexible)
        │            │            │
        └────────────┼────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
   News APIs          Processing Pipeline
   - NewsAPI          - Fetch news
   - WorldNews API    - Translate to Marathi
   - Custom sources   - Generate script
                      - Create audio (TTS)
                      - Create video (Lip-sync)
                      - Stream to YouTube
```

---

**Status:** ✅ Production Ready
**Version:** 1.0.0

Choose the option that fits your use case! 🚀
