# 📺 VARTAPRAVAH - TV Mode (24×7 Automated Bulletins)

## Overview

**TV Mode** runs your channel 24×7 with automated bulletins on a fixed schedule:
- 🕔 5 bulletins per day at fixed times
- 🔁 Loops with promo videos between cycles
- 🚨 Handles breaking news automatically
- 📺 Direct YouTube streaming
- 🧠 AI-powered Marathi script generation

---

## 📅 Bulletin Schedule

| Time | Marathi | English |
|------|---------|---------|
| 05:00 | सकाळ | Morning |
| 12:00 | दुपार | Afternoon |
| 17:00 | संध्याकाळ | Evening |
| 20:00 | प्राइम टाइम | Prime Time |
| 23:00 | रात्री | Night |

---

## 🎯 How It Works

```
05:00 AM
   ↓
Generate all news (max 25 per bulletin)
   ↓
Process Each Story:
   1. Fetch news
   2. Generate Marathi script (Groq AI)
   3. Convert to audio (TTS)
   4. Create video (Lip-sync)
   5. Stream to YouTube
   6. Play promo after every 5 stories
   ↓
If >25 news → Breaking News Queue
   Stream top 5 breaking news stories
   ↓
Loop until next bulletin time (12:00)
   Reset story queue
   Repeat all stories continuously
   Play promos every ~5 min
   ↓
12:00 PM → Switch to Afternoon bulletin
   ↓
Repeat cycle...
```

---

## 🚀 Setup

### 1. Environment Variables

Create `.env` file:
```bash
# Required
NEWSAPI_KEY=your_newsapi_key
GROQ_API_KEY=gsk_your_groq_key

# YouTube streaming (required for TV mode)
YOUTUBE_RTMP_URL=rtmp://a.rtmp.youtube.com/live2/YOUR_STREAM_KEY

# Optional
WORLDNEWS_API_KEY=optional_key
```

### 2. YouTube Setup

1. Go to YouTube Studio
2. Click "Go Live" → "RTMP Ingestion"
3. Copy your **Stream URL** (RTMP URL)
4. Set in environment: `export YOUTUBE_RTMP_URL="rtmp://..."`

### 3. Promo Video

Place promo video at: `assets/promo.mp4`
- Duration: 5-30 seconds
- Format: MP4, H.264
- Will play between story cycles

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🎬 Running TV Mode

### Start TV Mode

```bash
python app/main.py tv
```

### What You'll See

```
2024-01-20 05:00:15 - INFO - ======================================================================
2024-01-20 05:00:15 - INFO - 🚀 VARTAPRAVAH 24×7 TV ENGINE STARTED
2024-01-20 05:00:15 - INFO - ======================================================================
2024-01-20 05:00:15 - INFO - 📺 Streaming to: rtmp://a.rtmp.youtube.com/...
2024-01-20 05:00:15 - INFO - ⏰ Bulletin schedule:
2024-01-20 05:00:15 - INFO -     05:00 → सकाळ (Morning)
2024-01-20 05:00:15 - INFO -     12:00 → दुपार (Afternoon)
...

2024-01-20 05:00:20 - INFO - ======================================================================
2024-01-20 05:00:20 - INFO - 📺 STARTING BULLETIN: सकाळ (Morning)
2024-01-20 05:00:20 - INFO - 🕒 Time Slot: 05:00
2024-01-20 05:00:20 - INFO - ======================================================================
2024-01-20 05:00:22 - INFO - 📰 Fetching news from all sources...
2024-01-20 05:00:25 - INFO - 📊 News overflow: 30 articles
2024-01-20 05:00:25 - INFO -    Main bulletin: 25 articles
2024-01-20 05:00:25 - INFO -    Breaking news: 5 articles
2024-01-20 05:00:25 - INFO - ✅ Loaded 25 main + 5 breaking

2024-01-20 05:00:25 - INFO - ======================================================================
2024-01-20 05:00:25 - INFO - 📖 Processing story: Maharashtra announces education policy...
2024-01-20 05:00:25 - INFO -     Category: Maharashtra
2024-01-20 05:00:25 - INFO -     Source: PTI
2024-01-20 05:00:25 - INFO - Step 1/4: Generating Marathi script...
2024-01-20 05:00:28 - INFO - 🧠 Generating Marathi script with Groq AI...
2024-01-20 05:00:30 - INFO - ✅ Generated AI script: 245 characters
2024-01-20 05:00:30 - INFO - Step 2/4: Converting to audio...
2024-01-20 05:00:35 - INFO - ✅ Audio generated: output/story_audio.wav
2024-01-20 05:00:35 - INFO - Step 3/4: Creating lip-sync video...
2024-01-20 05:00:45 - INFO - ✅ Video created: output/story_video.mp4
2024-01-20 05:00:45 - INFO - Step 4/4: Streaming to YouTube...
2024-01-20 05:00:46 - INFO - 📺 Streaming: output/story_video.mp4
2024-01-20 05:00:47 - INFO - ✅ Story streamed successfully

[Story 2, 3, 4... processing...]

2024-01-20 05:02:15 - INFO - ⏸️ Promo break...
2024-01-20 05:02:15 - INFO - 📢 Playing promo video...

[Continues looping stories until 12:00]

2024-01-20 12:00:00 - INFO - ⏰ Time for next bulletin!
2024-01-20 12:00:00 - INFO - ======================================================================
2024-01-20 12:00:00 - INFO - 📺 STARTING BULLETIN: दुपार (Afternoon)
...
```

---

## 🎮 Two Modes of Operation

### Mode 1: API Server
```bash
python app/main.py api

# Access: http://localhost:8000
# Use: Manual control via HTTP endpoints
# Bulletins: On-demand
```

### Mode 2: TV Mode (24×7)
```bash
python app/main.py tv

# Automatic: Runs 24 hours
# Bulletins: Fixed schedule
# Streaming: Continuous to YouTube
```

---

## 🎛️ Advanced Configuration

### Custom Bulletin Schedule

Edit `app/scheduler.py`:
```python
BULLETIN_SCHEDULE = [
    ("05:00", "सकाळ", "Morning"),
    ("12:00", "दुपार", "Afternoon"),
    ("17:00", "संध्याकाळ", "Evening"),
    ("20:00", "प्राइम टाइम", "Prime Time"),
    ("23:00", "रात्री", "Night"),
]
```

### Adjust News Limits

```python
MAX_NEWS_PER_BULLETIN = 25       # Stories per bulletin
BREAKING_NEWS_LIMIT = 5          # Breaking news stories
PROMO_INTERVAL = 300             # 5 minutes
LOOP_DELAY = 10                  # Seconds between loops
```

### Custom Promo Video

```python
PROMO_VIDEO = "assets/promo.mp4"  # Change path
```

---

## 📊 System Flow

```
┌─────────────────────────────────────┐
│    VARTAPRAVAH 24×7 TV ENGINE       │
└─────────────┬───────────────────────┘
              │
              ├─→ Check Current Time
              │
              ├─→ Load Correct Bulletin
              │
              ├─→ Fetch All News
              │        ↓
              │    Split: Main (≤25) + Breaking (>25)
              │
              ├─→ Process Each Story:
              │    1. AI Marathi Script (Groq)
              │    2. TTS Audio
              │    3. Lip-Sync Video
              │    4. YouTube Stream
              │    5. Promo Every 5 Stories
              │
              ├─→ Handle Breaking News
              │    (If >25 articles)
              │
              ├─→ Loop Until Next Bulletin
              │    Repeat stories with promos
              │
              └─→ Auto Switch Bulletin
                  12:00 → Afternoon
                  17:00 → Evening
                  etc...
```

---

## 🔍 Monitoring & Logs

All events are logged to console:
- 📺 Bulletin starts/switches
- 📰 News fetching status
- 🧠 AI script generation
- 🎤 Audio/Video processing
- 📊 Stream status
- 🚨 Breaking news detection
- ⚠️ Error/warning messages

### Redirect Logs to File

```bash
# Save logs
python app/main.py tv > vartapravah.log 2>&1

# View live
tail -f vartapravah.log
```

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'news_fetcher'"
```bash
pip install -r requirements.txt
cd app
python main.py tv
```

### "YOUTUBE_RTMP_URL not found"
```bash
export YOUTUBE_RTMP_URL="rtmp://a.rtmp.youtube.com/live2/YOUR_KEY"
python app/main.py tv
```

### "Promo video not found"
- Place video at: `assets/promo.mp4`
- Or disable promos by removing `play_promo()` calls

### "No news fetched"
- Check `NEWSAPI_KEY` environment variable
- Verify API key is valid at newsapi.org

### "Streaming fails"
- Check YouTube RTMP URL is correct
- Ensure YouTube channel is live-enabled
- Check internet connection

---

## 🎯 Real-World Usage

### Production Setup

```bash
# Start on server
ssh user@server
cd /path/to/VARTAPRAVAH-LATEST
export NEWSAPI_KEY="..."
export GROQ_API_KEY="..."
export YOUTUBE_RTMP_URL="..."

# Run in background
nohup python app/main.py tv > /var/log/vartapravah.log 2>&1 &
```

### Monitor with Screen

```bash
# Start in screen session
screen -S vartapravah

# Inside screen
python app/main.py tv

# Detach: Ctrl+A, D
# Reattach: screen -r vartapravah
```

### Docker Deployment

```bash
docker run -d \
  -e NEWSAPI_KEY="..." \
  -e GROQ_API_KEY="..." \
  -e YOUTUBE_RTMP_URL="..." \
  -v $(pwd)/output:/app/output \
  vartapravah:latest \
  python app/main.py tv
```

---

## 📈 Performance Tips

1. **Fresh News**: Fetches all bulletins at slot time
2. **AI Speed**: Groq AI takes ~3-5 seconds per story
3. **TTS**: ~5-10 seconds depending on text length
4. **Video**: Lip-sync takes ~10 seconds
5. **Streaming**: Real-time to YouTube

**Total per story**: ~20-30 seconds

**Per bulletin (25 stories)**: ~10-12 minutes

---

## 🎥 Future Upgrades (Roadmap)

Planned improvements:
- 📰 Ticker running at bottom of screen
- 🎬 Story-by-story segmentation
- 🎙️ Intro video before each bulletin
- 📊 Analytics dashboard
- 🤖 Voice quality improvements
- 🎨 Custom graphics & branding

---

## 📞 Support

For issues:
1. Check logs: `tail -f vartapravah.log`
2. Verify all env variables are set
3. Test news fetcher: `python app/news_fetcher.py`
4. Test script generator: `python app/script_generator.py`
5. Test manually: `python app/main.py api` (use /docs)

---

**Status:** ✅ Production Ready
**Version:** 2.0 (24×7 TV Mode)
**Engine:** Groq AI + Coqui TTS + Wav2Lip
**Streaming:** YouTube Live RTMP

🎬 Your channel is now live 24×7! 📺✨
