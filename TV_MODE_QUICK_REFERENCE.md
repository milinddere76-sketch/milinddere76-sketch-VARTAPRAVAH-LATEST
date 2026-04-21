# 📺 VARTAPRAVAH TV Mode - Quick Reference

## Two Operating Modes

### 🌐 API Server Mode (Manual Control)
```bash
python app/main.py api

# Access dashboard: http://localhost:8000/docs
# Use HTTP endpoints for on-demand bulletins
# Perfect for: Testing, development, manual control
```

### 📺 TV Mode (24×7 Automated)
```bash
python app/main.py tv

# Auto runs 5 bulletins per day
# Streams continuously to YouTube
# Perfect for: Production, channel broadcasting
```

---

## ⚡ Quick Start (TV Mode)

### 1. Set Environment Variables
```bash
export NEWSAPI_KEY="your_key"
export GROQ_API_KEY="gsk_your_key"
export YOUTUBE_RTMP_URL="rtmp://a.rtmp.youtube.com/live2/YOUR_KEY"
```

Or create `.env`:
```
NEWSAPI_KEY=your_key
GROQ_API_KEY=gsk_your_key
YOUTUBE_RTMP_URL=rtmp://a.rtmp.youtube.com/live2/YOUR_KEY
```

### 2. Place Promo Video
```bash
mkdir -p assets
# Copy your 5-30 second promo video to:
# assets/promo.mp4
```

### 3. Start TV Mode
```bash
python app/main.py tv
```

### 4. Watch Dashboard
YouTube Live → Your channel will show the livestream

---

## 📅 Bulletin Schedule

| Time | Bulletin | Type |
|------|----------|------|
| **05:00** | सकाळ | Morning |
| **12:00** | दुपार | Afternoon |
| **17:00** | संध्याकाळ | Evening |
| **20:00** | प्राइम टाइम | Prime Time |
| **23:00** | रात्री | Night |

---

## 🎯 What Happens

```
05:00 AM
  ↓
📰 Fetch news (all categories)
  ↓
🧠 AI generates Marathi scripts (Groq)
  ↓
🎤 Convert to audio (TTS)
  ↓
📹 Create lip-sync videos (Wav2Lip)
  ↓
📺 Stream to YouTube
  ↓
📢 Play promo every 5 stories
  ↓
🔁 Loop all stories until 12:00
  ↓
12:00 → Auto switch to Afternoon bulletin
  ↓
Repeat...
```

---

## 🔧 Components

| Component | Role |
|-----------|------|
| **News Fetcher** | Fetches from NewsAPI |
| **Script Generator** | AI creates Marathi (Groq) |
| **TTS Engine** | Converts to audio (Coqui) |
| **Lip-Sync** | Creates video (Wav2Lip) |
| **Streamer** | Sends to YouTube (RTMP) |
| **Scheduler** | Manages timing & loops |

---

## 📊 News Handling

- **Normal**: ≤25 stories → All in bulletin
- **Overflow**: >25 stories
  - First 25 → Main bulletin
  - Rest → Breaking News queue
  - Top 5 breaking stories → Stream separately

---

## 🎬 Story Processing (Per Article)

```
News Article
    ↓
Groq AI (3-5 sec)
    ↓
TTS Audio (5-10 sec)
    ↓
Lip-Sync Video (10 sec)
    ↓
YouTube Stream (Real-time)
    
Total: ~20-30 seconds per story
```

---

## 📈 Timeline Example

```
05:00:00 - Bulletin starts (सकाळ)
05:00:20 - Story 1 streams
05:00:50 - Story 2 streams
05:01:20 - Story 3 streams
05:01:50 - Story 4 streams
05:02:20 - Story 5 streams
05:02:50 - 📢 PROMO (30 sec)
05:03:20 - Story 6 streams
...
11:55:00 - Still looping stories
11:58:00 - Prep next bulletin
12:00:00 - ⏰ Switch to दुपार (Afternoon)
12:00:20 - New bulletin starts
```

---

## 🛑 Stop/Control

### Stop Running Instance
```bash
# Press: Ctrl + C
# To resume: python app/main.py tv
```

### Background Execution
```bash
# Run in background
nohup python app/main.py tv > vartapravah.log 2>&1 &

# View logs
tail -f vartapravah.log

# Kill
pkill -f "python app/main.py tv"
```

---

## 📋 Logs to Watch For

```
✅ OK:
- "📺 STARTING BULLETIN: सकाळ (Morning)"
- "📖 Processing story: ..."
- "✅ Story streamed successfully"
- "🔁 Looping current bulletin"

⚠️ Warning:
- "⚠️ Groq not available"
- "⚠️ Promo video not found"
- "⚠️ Using fallback translation"

❌ Error (will retry):
- "❌ News fetch failed"
- "❌ Script generation failed"
- "❌ Streaming failed"
```

---

## 🐛 Common Issues

### No News Showing
```bash
# Check API key
echo $NEWSAPI_KEY

# Test manually
python -c "from news_fetcher import NewsFetcher; f = NewsFetcher(); print(f.fetch_all_news(limit=2))"
```

### Not Streaming to YouTube
```bash
# Check RTMP URL
echo $YOUTUBE_RTMP_URL

# Ensure YouTube channel is live-enabled
# YouTube Studio → Settings → Live
```

### Promo Not Playing
```bash
# Check file exists
ls -la assets/promo.mp4

# Or disable in scheduler.py (comment out play_promo() calls)
```

### Scripts Not in Marathi
```bash
# Check Groq API
echo $GROQ_API_KEY

# Falls back to template if Groq unavailable (English still works)
```

---

## 📊 Production Checklist

- [ ] NEWSAPI_KEY set and valid
- [ ] GROQ_API_KEY set and valid
- [ ] YOUTUBE_RTMP_URL set
- [ ] promo.mp4 placed in assets/
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Test API server: `python app/main.py api`
- [ ] Test news fetcher: Works?
- [ ] Test script generator: Marathi output?
- [ ] YouTube channel live-enabled
- [ ] Internet connection stable
- [ ] Server has enough disk space
- [ ] FFmpeg installed and in PATH

---

## 🎯 Modes Comparison

| Feature | API Mode | TV Mode |
|---------|----------|---------|
| Manual control | ✅ Yes | ❌ No |
| HTTP endpoints | ✅ Yes | ❌ No |
| 24×7 automation | ❌ No | ✅ Yes |
| YouTube streaming | ❌ Manual | ✅ Auto |
| News fetching | On-demand | Scheduled |
| Bulletin timing | Any time | Fixed 5× |
| Promo loops | ❌ No | ✅ Yes |
| Breaking news | ❌ No | ✅ Auto |
| Best for | Development | Production |

---

## 🚀 Next Upgrades

Future features:
- 📰 Live ticker at bottom
- 🎬 Story-by-story switching
- 🎙️ Intro/outro videos
- 📊 Analytics dashboard
- 🎨 Custom branding
- 🎛️ Remote control API

---

## 📞 Quick Help

```bash
# Show help
python app/main.py help

# Start API server
python app/main.py api

# Start TV mode
python app/main.py tv

# One-time demo
python app/pipeline_demo.py

# Test components
python -c "from news_fetcher import NewsFetcher; print('✅ News OK')"
python -c "from script_generator import generate_marathi_script; print('✅ Script OK')"
python -c "from groq import Groq; print('✅ Groq OK')"
```

---

**Status:** ✅ Production Ready | 📺 TV Mode Active | 🧠 AI Powered | 📊 24×7 Ready

Your channel is now ready for 24×7 broadcasting! 🎬📺✨
