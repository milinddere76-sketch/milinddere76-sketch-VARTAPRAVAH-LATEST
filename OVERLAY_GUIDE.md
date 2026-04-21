# 🎬 DYNAMIC TV OVERLAYS - Complete Guide

## What Are Overlays?

Professional TV overlays add:
- 📺 **Channel Logo** (top corner) - Branding
- 📰 **Lower-Third Bar** (bottom) - Headline text
- 📊 **Scrolling Ticker** (bottom) - Breaking news feed

---

## 🎯 Quick Start

### 1. Prepare Assets

Create `assets/` directory with:

```bash
mkdir -p assets

# 1. Channel Logo (transparent PNG)
#    - Size: 200×200 pixels (or larger, will be scaled)
#    - Format: PNG with transparency
#    - File: assets/logo.png

# 2. Font File (Devanagari support)
#    - Download: https://fonts.google.com/noto/specimen/Noto+Sans+Devanagari
#    - Extract: NotoSansDevanagari-Regular.ttf
#    - Place: assets/font.ttf

# 3. Optional: Lower-third background
#    - Size: 1920×300 pixels
#    - File: assets/lower_bg.png
```

**Download Recommended Font:**
```bash
# Linux/Mac
wget https://github.com/notofonts/devanagari/raw/main/fonts/NotoSansDevanagari/unhinted/NotoSansDevanagari-Regular.ttf
mv NotoSansDevanagari-Regular.ttf assets/font.ttf

# Windows - download manually and place in assets/
```

### 2. System Test

```python
from overlay import add_overlay

# Test overlay
success = add_overlay(
    "input_video.mp4",
    "output_with_overlay.mp4",
    headline="आजची मुख्य बातमी"
)

if success:
    print("✅ Overlays working!")
```

### 3. Enable in TV Mode

Automatically enabled in `app/scheduler.py`:
- ✅ Each story gets headline as lower-third
- ✅ Logo added to corner (if exists)
- ✅ Fallback works if assets missing

---

## 📁 Asset Structure

```
assets/
├── logo.png              # Channel logo (200×200 px, PNG)
├── lower_bg.png          # Lower-third background (optional)
├── font.ttf              # Devanagari font (REQUIRED for Marathi text)
├── promo.mp4             # Promo video (5-30 sec)
└── background.mp4        # Background loop (optional)
```

### Creating Assets

**Logo Design:**
- Use transparent background (PNG with alpha)
- 200×200 pixels minimum
- Include channel name/branding
- Tools: Photoshop, GIMP, Canva

**Font Setup:**
```bash
# Verify font installation
fc-list | grep -i devanagari

# Or check directly
ls -la assets/font.ttf
```

---

## 🎬 Three Overlay Modes

### Mode 1: Full Overlay (Logo + Lower-Third)

```python
from overlay import add_overlay

add_overlay(
    input_video="video.mp4",
    output_video="final.mp4",
    headline="मुख्य बातमी"
)
```

**Result:**
```
┌─ VARTAPRAVAH ─────────────────────────────────┐
│ [Logo]                                        │
│                                               │
│                                               │
│  ┌─────────────────────────────────────────┐  │
│  │ मुख्य बातमी                            │  │
│  └─────────────────────────────────────────┘  │
└───────────────────────────────────────────────┘
```

### Mode 2: Lower-Third Only

```python
from overlay import add_lower_third_only

add_lower_third_only(
    input_video="video.mp4",
    output_video="final.mp4",
    headline="लाइव्ह समाचार"
)
```

**Faster, no logo needed**

### Mode 3: Scrolling Ticker

```python
from overlay import add_ticker_only

add_ticker_only(
    input_video="video.mp4",
    output_video="final.mp4",
    ticker_text="ब्रेकिंग: राष्ट्रीय समाचार येथे येईल..."
)
```

**Result:**
```
Video scrolls →
ब्रेकिंग: राष्ट्रीय समाचार येथे येईल ← Text scrolls
```

---

## 🔧 API Usage

### Via REST API

```bash
# Stream with overlay
curl -X POST "http://localhost:8000/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "video_path": "output/video.mp4",
    "rtmp_url": "rtmp://...",
    "headline": "आजचे मुख्य बातमी",
    "add_overlay": true
  }'
```

### Via Python Code

```python
from overlay import add_overlay

# Step 1: Add overlays
add_overlay(
    "output/raw_video.mp4",
    "output/final_video.mp4",
    headline="मुख्य बातमी"
)

# Step 2: Stream
from streamer import stream_to_youtube
stream_to_youtube(
    "output/final_video.mp4",
    rtmp_url="rtmp://..."
)
```

---

## 🎨 Customization

### Font Settings

Edit `app/overlay.py`:

```python
lower_filter = (
    f"drawtext=fontfile={FONT_PATH}:"
    f"text='{headline}':"
    f"fontsize=48:"              # Larger text
    f"fontcolor=white:"
    f"x=20:y=h-80"
)
```

### Text Positioning

```python
# Bottom-left (current)
x=20:y=h-80

# Bottom-right
x=w-tw-20:y=h-80

# Top-left
x=20:y=20

# Top-right
x=w-tw-20:y=20

# Center-bottom
x=w/2-tw/2:y=h-80
```

### Colors

```python
# Common colors
fontcolor=white       # White text
fontcolor=yellow      # Yellow (for ticker)
fontcolor=red         # Red (for breaking)
fontcolor=0x00FF00    # Hex color (green)

# Background
boxcolor=black@0.7    # Black with 70% opacity
boxcolor=red@0.5      # Red with 50% opacity
```

### Animation Speed

For scrolling ticker:

```python
# Current speed (150 pixels per second)
x=w-mod(t*150\,w+tw)

# Slower (100 pixels/sec)
x=w-mod(t*100\,w+tw)

# Faster (200 pixels/sec)
x=w-mod(t*200\,w+tw)
```

---

## 🚀 Performance

### Processing Time

| Mode | Time | CPU |
|------|------|-----|
| Raw video | - | - |
| + Overlay | +5-10s | Medium |
| + Ticker | +5-10s | Medium |
| Full pipeline | ~25-30s | Normal |

### Optimization Tips

1. **Use lower-third only** if logo not essential
2. **Reduce video resolution** to 720p for faster processing
3. **Pre-process assets** to correct size/format
4. **Disable overlay** during heavy load (fallback auto-enabled)

---

## 🐛 Troubleshooting

### "Font file not found"

```bash
# Check font exists
ls -la assets/font.ttf

# If missing, download:
wget https://github.com/notofonts/devanagari/raw/main/fonts/NotoSansDevanagari/unhinted/NotoSansDevanagari-Regular.ttf -O assets/font.ttf
```

### "Text not displaying correctly"

```bash
# Verify FFmpeg supports Devanagari
ffmpeg -h full 2>&1 | grep -i "drawtext"

# Test with simple ASCII first
add_overlay("input.mp4", "output.mp4", headline="TEST")
```

### "Overlay files too large"

```bash
# Compress logo
ffmpeg -i assets/logo.png -vf "scale=200:200" assets/logo_small.png

# Update path in overlay.py
LOGO_PATH = "assets/logo_small.png"
```

### "Marathi text showing as boxes"

- **Font issue**: Ensure font.ttf supports Devanagari
- **Text encoding**: Verify text is UTF-8
- **FFmpeg version**: Update to latest (use `ffmpeg -version`)

---

## 📊 Advanced: Custom Filter

Combine multiple effects:

```python
filter_complex = (
    "[0:v][1:v]overlay=W-w-20:20,"      # Logo top-right
    "drawtext=fontfile={FONT_PATH}:"
    "text='Primary Headline':"
    "fontsize=48:fontcolor=white:"
    "x=20:y=h-150,"                      # First line
    "drawtext=fontfile={FONT_PATH}:"
    "text='Secondary text':"
    "fontsize=30:fontcolor=yellow:"
    "x=20:y=h-80"                        # Second line
)
```

---

## 🎯 Production Checklist

- [ ] Font file installed: `assets/font.ttf`
- [ ] Logo created: `assets/logo.png`
- [ ] Test overlay works: No FFmpeg errors
- [ ] Marathi text displays correctly
- [ ] Processing time acceptable (<10s per story)
- [ ] Output quality acceptable
- [ ] All assets organized in `assets/`
- [ ] Backup of original video files

---

## 📈 Real-World Examples

### Example 1: News Story with Headline

```python
from overlay import add_overlay

news_title = "महाराष्ट्रात नई शिक्षा धोरणाची घोषणा"
add_overlay(
    "output/story_raw.mp4",
    "output/story_final.mp4",
    headline=news_title[:50]  # Truncate for display
)
```

### Example 2: Breaking News with Red Ticker

```python
from overlay import add_ticker_only

breaking_news = "🚨 ब्रेकिंग: महत्वाची बातमी येथे येईल"
add_ticker_only(
    "output/breaking_raw.mp4",
    "output/breaking_final.mp4",
    ticker_text=breaking_news
)
```

### Example 3: Promo Loop

```python
# Promo doesn't need overlay (already branded)
from streamer import stream_to_youtube
stream_to_youtube("assets/promo.mp4", rtmp_url)
```

---

## 🔗 Integration Points

| Component | Overlay Support |
|-----------|-----------------|
| TV Mode | ✅ Auto-enabled |
| API Server | ✅ Optional via param |
| Pipeline Demo | ✅ Can add manually |
| Scheduler | ✅ Auto-enabled |

---

## 📝 API Response Examples

### Successful Overlay

```json
{
  "status": "success",
  "message": "Overlay added successfully",
  "video": "output/final_with_overlay.mp4",
  "processing_time": 8.5,
  "overlay_type": "full"
}
```

### Overlay Failed (Fallback)

```json
{
  "status": "partial",
  "message": "Overlay failed, streaming without effects",
  "video": "output/original_video.mp4",
  "error": "Font file not found",
  "fallback": true
}
```

---

## 🎬 Next Steps

1. **Download assets** - Logo, font, background
2. **Test locally** - Run `python app/overlay.py`
3. **Enable TV mode** - Already integrated, auto-works
4. **Monitor output** - Check for text quality
5. **Customize** - Adjust colors, fonts, positioning

---

**Status:** ✅ Production Ready | 🎨 Professional Overlays | 📺 TV Branded

Your channel now has professional TV overlays! 📺✨
