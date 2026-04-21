# 🧠 VARTAPRAVAH - Quick Start Guide (Now with Groq AI!)

## 5 Minutes Setup

### 1. Get API Keys (Free)

**NewsAPI** - https://newsapi.org/
```
Sign up → Copy API key
```

**Groq AI** - https://console.groq.com/ (NEW!)
```
Sign up → Create API Key → Copy key (gsk_...)
```

### 2. Create .env File
```bash
NEWSAPI_KEY=your_newsapi_key_here
GROQ_API_KEY=gsk_your_groq_key_here
```

### 3. Install Packages
```bash
pip install -r requirements.txt
```

### 4. Start Server
```bash
python app/main.py
```

### 5. Test It!
```bash
# Test news fetcher
curl http://localhost:8000/news?limit=3

# Generate AI bulletin (with Groq!)
curl -X POST http://localhost:8000/bulletin \
  -H "Content-Type: application/json" \
  -d '{"max_bullets": 5}'

# Full pipeline (News → AI → TTS → Video → YouTube)
curl -X POST http://localhost:8000/bulletin-pipeline \
  -H "Content-Type: application/json" \
  -d '{
    "max_bullets": 5,
    "rtmp_url": "rtmp://a.rtmp.youtube.com/live2/YOUR_STREAM_KEY"
  }'
```

---

## ⭐ What's New: Groq AI

### AI-Generated Marathi Scripts
- Professional news anchor quality
- Native Marathi (not translation)
- Fast & accurate
- FREE tier available

### Before vs After
**Template (Before):**
```
1. Title।
   Description।
   ही बातमी PTI कडून प्राप्त झाली आहे।
```

**AI (Now):**
```
महाराष्ट्रातील शिक्षणक्षेत्रात मोठा बदल होणार आहे...
```

Much better! 🎯

---

## API Endpoints

| Endpoint | Method | Purpose | 
|----------|--------|---------|
| `/health` | GET | Health check |
| `/info` | GET | System info |
| `/news` | GET | Fetch news |
| `/bulletin` | POST | Generate AI bulletin ⭐ |
| `/bulletin-pipeline` | POST | Full automation 🧠 |
| `/docs` | GET | Swagger UI |

---

## File Structure

```
app/
├── news_fetcher.py       (Fetch news from APIs)
├── script_generator.py   (🧠 AI Marathi generator - NOW WITH GROQ!)
├── api.py                (FastAPI endpoints)
├── main.py               (Entry point)
├── tts_engine.py         (Audio generation)
├── lipsync.py            (Video generation)
├── streamer.py           (YouTube streaming)
└── __init__.py

output/
├── marathi_script.txt    (Generated script)
├── bulletin_audio.wav    (Generated audio)
└── bulletin_video.mp4    (Generated video)
```

---

## Typical Workflow

### Step 1: Fetch News
```bash
curl http://localhost:8000/news?limit=5
```

### Step 2: Generate AI Script (with Groq!)
```bash
curl -X POST http://localhost:8000/bulletin \
  -H "Content-Type: application/json" \
  -d '{"max_bullets": 5}'
```

### Step 3: Complete Pipeline
```bash
curl -X POST http://localhost:8000/bulletin-pipeline \
  -H "Content-Type: application/json" \
  -d '{
    "max_bullets": 5,
    "rtmp_url": "rtmp://a.rtmp.youtube.com/live2/STREAM_KEY"
  }'
```

All done! Video will be streamed to YouTube! 📺

---

## Schedule 5 Bulletins Per Day

Add to crontab (Linux/Mac):
```bash
# 6 AM
0 6 * * * cd /path/to/VARTAPRAVAH-LATEST && python app/pipeline_demo.py

# 12 PM
0 12 * * * cd /path/to/VARTAPRAVAH-LATEST && python app/pipeline_demo.py

# 5 PM
0 17 * * * cd /path/to/VARTAPRAVAH-LATEST && python app/pipeline_demo.py

# 8 PM
0 20 * * * cd /path/to/VARTAPRAVAH-LATEST && python app/pipeline_demo.py

# 10 PM
0 22 * * * cd /path/to/VARTAPRAVAH-LATEST && python app/pipeline_demo.py
```

Windows Task Scheduler: Create tasks for each time

---

## Features

✅ Auto news fetching from multiple sources
✅ 3 news categories (India, Maharashtra, World)
✅ 🧠 AI Marathi script generation (Groq)
✅ Professional script quality
✅ Lip-synced avatar videos
✅ Direct YouTube streaming
✅ Fully automated pipeline

---

## Bulletin Types

```python
"सकाळ"   # Morning (6 AM)
"मध्य"   # Noon (12 PM)
"संध्या"  # Evening (5 PM)
"प्राइम" # Prime Time (8 PM)
"रात्र"   # Night (10 PM)
```

---

## Environment Variables

```
NEWSAPI_KEY              - NewsAPI key (required)
GROQ_API_KEY            - Groq API key (required for AI)
WORLDNEWS_API_KEY       - WorldNews API key (optional)
GOOGLE_APPLICATION_CREDENTIALS - Google Cloud credentials (optional)
```

---

## Documentation

- 🧠 **AI Setup:** [GROQ_AI_SETUP.md](GROQ_AI_SETUP.md) ⭐ NEW
- 🎯 **AI Upgrade:** [GROQ_AI_UPGRADE.md](GROQ_AI_UPGRADE.md) ⭐ NEW
- 🚀 **How to Run:** [HOW_TO_RUN.md](HOW_TO_RUN.md)
- 📰 **Full Setup:** [NEWS_FETCHER_SETUP.md](NEWS_FETCHER_SETUP.md)

---

**Status:** ✅ Production Ready
**Version:** 2.0 (AI-Powered)
**AI Engine:** Groq (Llama 3.1 8B)
**Last Updated:** 2024-01-20

🧠 Now with AI brain! Your channel is ready to shine! ✨

