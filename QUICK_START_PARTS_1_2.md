# 🚀 QUICK START - Parts 1 & 2 (Overlays + Recovery)

## ⏱️ 5-Minute Setup

### 1. Download Font (1 min)
```powershell
# PowerShell (Windows)
cd c:\VARTAPRAVAH-LATEST
Invoke-WebRequest -Uri 'https://github.com/notofonts/devanagari/raw/main/fonts/NotoSansDevanagari/unhinted/NotoSansDevanagari-Regular.ttf' -OutFile 'assets/font.ttf'

# OR Linux/Mac
wget https://github.com/notofonts/devanagari/raw/main/fonts/NotoSansDevanagari/unhinted/NotoSansDevanagari-Regular.ttf -O assets/font.ttf
```

### 2. Verify Setup (1 min)
```bash
python setup_verify.py

# Should show ✅ for all critical items
```

### 3. Set Environment (1 min)
```bash
# PowerShell
$env:NEWSAPI_KEY="your_key"
$env:GROQ_API_KEY="gsk_your_key"
$env:YOUTUBE_RTMP_URL="rtmp://..."

# Or Linux/Mac
export NEWSAPI_KEY="your_key"
export GROQ_API_KEY="gsk_your_key"
export YOUTUBE_RTMP_URL="rtmp://..."
```

### 4. Start TV Mode (1 min)
```bash
python app/main.py tv
```

### 5. Watch It Work (1 min)
```bash
# In another terminal
tail -f vartapravah.log

# Look for:
# ✅ Adding overlays to:
# 📡 Starting YouTube Live stream
# ✅ Stream completed successfully
```

---

## 📋 What You'll See

### Success Indicators
```
✅ Adding overlays to: output/story_video.mp4
   ✓ Adding logo (top-right corner)
   ✓ Adding lower-third: 'Maharashtra announces...'
✅ Overlay complete: output/final_with_overlay.mp4 (45.2 MB)

📡 Starting YouTube Live stream (Attempt 1/3)
📡 Video: output/final_with_overlay.mp4
✅ Stream completed successfully
```

### If Network Fails
```
📡 Starting YouTube Live stream (Attempt 1/3)
⚠️ Stream ended (code 1): Connection timeout
⏳ Waiting 5s before retry...

📡 Starting YouTube Live stream (Attempt 2/3)
✅ Stream completed successfully
```

---

## 📁 File Checklist

```
✅ app/overlay.py              - Created
✅ app/streamer.py             - Updated
✅ app/scheduler.py            - Updated (overlay integration)
✅ app/api.py                  - Updated (overlay params)

✅ assets/font.ttf             - Download from Google Fonts
✅ assets/logo.png             - Create via Canva (optional)
✅ assets/promo.mp4            - Already exists

✅ OVERLAY_GUIDE.md            - Comprehensive guide
✅ STREAMING_RECOVERY_GUIDE.md - Recovery guide
✅ PARTS_1_2_GUIDE.md          - Main guide
✅ setup_verify.py             - Setup checker
```

---

## 🔧 If Something Fails

### "Font not found"
```bash
# Download again
Invoke-WebRequest -Uri 'https://github.com/notofonts/devanagari/raw/main/fonts/NotoSansDevanagari/unhinted/NotoSansDevanagari-Regular.ttf' -OutFile 'assets/font.ttf'

# Verify
ls assets/font.ttf
```

### "Overlay command failed"
```bash
# Check FFmpeg
ffmpeg -version

# Check font working
ffmpeg -f lavfi -i color=c=blue:s=320x240:d=1 -vf "drawtext=fontfile=assets/font.ttf:text='TEST'" test.mp4
```

### "Streaming fails after 3 retries"
```bash
# Check RTMP URL
$env:YOUTUBE_RTMP_URL

# Verify YouTube channel is set for live
# YouTube Studio → Settings → Community → Channel → Go Live
```

### "Exit code shows: ModuleNotFoundError"
```bash
# Check overlay.py exists
ls app/overlay.py

# Check imports
python -c "from app.overlay import add_overlay; print('✅')"
```

---

## 🎯 Key Features Enabled

### Overlays Active ✅
```
Every story now has:
- Channel logo (top-right)
- Headline bar (bottom)
- Professional TV look
- Takes +5-10 sec per video
```

### Auto-Recovery Active ✅
```
Every stream now has:
- Auto-retry (up to 3 times)
- Network resilience
- 5-second delays between retries
- Smart logging
```

---

## 📊 Performance

| Task | Time |
|------|------|
| Overlay | +5-10s |
| Recovery retry | +5s (if needed) |
| Per story total | ~50-100s |
| No overhead | If network OK |

---

## 🎬 API Usage

### Stream with Overlay (if using API mode)
```bash
curl -X POST "http://localhost:8000/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "video_path": "output/video.mp4",
    "rtmp_url": "rtmp://...",
    "headline": "आजचे मुख्य बातमी",
    "add_overlay": true
  }'
```

---

## ✅ Deployment Checklist

Before going live:
- [ ] `python setup_verify.py` shows all ✅
- [ ] `assets/font.ttf` exists
- [ ] `assets/logo.png` created (optional)
- [ ] Environment variables set
- [ ] `python app/main.py tv` starts without errors
- [ ] Check logs for overlay messages
- [ ] Stream appears on YouTube with graphics
- [ ] Test network recovery (simulate failure)

---

## 📖 Full Documentation

For detailed information, see:

| File | Content |
|------|---------|
| **PARTS_1_2_GUIDE.md** | Overview of both features |
| **OVERLAY_GUIDE.md** | Complete overlay customization |
| **STREAMING_RECOVERY_GUIDE.md** | Recovery mechanism details |
| **IMPLEMENTATION_SUMMARY.md** | Technical implementation |
| **setup_verify.py** | Run to verify setup |

---

## 🚀 Production Setup

### Start Background Process
```bash
# PowerShell
Start-Process powershell -ArgumentList "-Command", "cd c:\VARTAPRAVAH-LATEST; python app/main.py tv; Read-Host"

# Linux/Mac
nohup python app/main.py tv > vartapravah.log 2>&1 &
```

### Monitor Logs
```bash
tail -f vartapravah.log | grep -E "Adding overlays|📡 Starting|✅ Stream"
```

### Check Status
```bash
ps aux | grep "python app/main.py tv"
```

---

## 🎉 You're All Set!

Your channel now has:
✅ Professional TV overlays  
✅ Auto-recovery streaming  
✅ Automatic everything  
✅ Production-ready setup

**Start TV mode and go live!** 📺✨

```bash
python app/main.py tv
```

---

**Need Help?** See documentation files above.  
**Verify Setup?** Run `python setup_verify.py`  
**Check Logs?** Run `tail -f vartapravah.log`

Your VARTAPRAVAH channel is ready! 🚀📺✨
