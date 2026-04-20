# VartaPravah Bulletin Scheduler Guide

## Overview

The **Bulletin Scheduler** generates news videos at fixed times throughout the day, creating a professional broadcast schedule like traditional TV news channels.

## Bulletin Schedule

| Time | Type | Duration | Description |
|------|------|----------|-------------|
| **05:00 AM** | Morning | 10 min | Early morning headline bulletin |
| **12:00 PM** | Afternoon | 8 min | Midday news update |
| **05:00 PM** | Evening | 12 min | Prime evening bulletin |
| **09:00 PM** | Prime Time | 15 min | In-depth prime time news |
| **12:00 AM** | Night | 7 min | Late night brief bulletin |

---

## Integration Steps

### 1. Add Bulletin Scheduler to Requirements

Update `requirements.txt` (already included in VartaPravah):
```txt
# Existing dependencies...
threading  # Built-in, no install needed
```

### 2. Import in Main Application

```python
from encoder.bulletin_scheduler import BulletinScheduler
```

### 3. Initialize in FastAPI Startup

```python
# Global bulletin_scheduler
bulletin_scheduler = None

@app.on_event("startup")
def startup_event():
    global bulletin_scheduler
    
    # Wrapper function to pass to scheduler
    def generate_bulletin(bulletin_type):
        generate_news(bulletin_type=bulletin_type)
    
    # Initialize bulletin scheduler
    bulletin_scheduler = BulletinScheduler(generate_bulletin)
    bulletin_scheduler.start_scheduler()
    
    logger.info("Bulletin scheduler started")
```

### 4. Update generate_news Function

Modify to accept `bulletin_type` parameter:

```python
def generate_news(news_data=None, custom_path=None, bulletin_type=None):
    """Generate news with bulletin type support."""
    if not news_data:
        if news_queue:
            news_data = news_queue.pop(0)
        elif bulletin_type:
            # Generate bulletin-specific placeholder
            bulletin_info = BulletinScheduler.get_bulletin_info(bulletin_type)
            news_data = {
                'headline': f"🔴 {bulletin_info['name']}",
                'content': "नवीन बातम्या येत आहेत...",
                'category': bulletin_type,
                'breaking': bulletin_type == "prime_time"
            }
    
    # Rest of generation logic...
```

---

## API Endpoints

### 1. Get Bulletin Schedule

```bash
GET /bulletin/schedule
```

**Response:**
```json
{
  "schedule": {
    "05:00": "morning",
    "12:00": "afternoon",
    "17:00": "evening",
    "21:00": "prime_time",
    "00:00": "night"
  },
  "bulletin_info": {
    "morning": {
      "name": "Morning Bulletin",
      "description": "Early morning news (5:00 AM)",
      "duration": 10,
      "tone": "informative"
    }
    // ... more bulletins
  }
}
```

### 2. Get Current Bulletin Status

```bash
GET /bulletin/status
```

**Response:**
```json
{
  "current_time": "14:30",
  "current_bulletin_type": "afternoon",
  "current_bulletin_info": {
    "name": "Afternoon Bulletin",
    "description": "Midday news update (12:00 PM)",
    "duration": 8,
    "tone": "balanced"
  },
  "next_bulletin_time": "17:00",
  "next_bulletin_type": "evening",
  "next_bulletin_info": { ... },
  "scheduler_running": true
}
```

### 3. Generate Bulletin Immediately

```bash
POST /bulletin/generate/{bulletin_type}
```

**Parameters:**
- `bulletin_type`: morning, afternoon, evening, prime_time, or night

**Example:**
```bash
curl -X POST http://localhost:8000/bulletin/generate/evening
```

**Response:**
```json
{
  "status": "success",
  "message": "Generating evening bulletin",
  "bulletin_info": {
    "name": "Evening Bulletin",
    "description": "Evening news (5:00 PM)",
    "duration": 12,
    "tone": "comprehensive"
  }
}
```

### 4. Queue News for Next Bulletin

```bash
POST /bulletin/queue
```

**Request Body:**
```json
{
  "headline": "नए नियम लागू होने वाले हैं",
  "content": "नए नियम अगले सप्ताह से लागू होंगे...",
  "category": "राजनीति",
  "breaking": false
}
```

**Response:**
```json
{
  "status": "queued",
  "queue_length": 1,
  "next_bulletin": "17:00"
}
```

---

## Usage Examples

### Example 1: Automatic Daily Bulletins

Once the scheduler is running, bulletins are generated automatically at scheduled times:

```bash
# Scheduler monitors time in background
# At 05:00 AM: Morning bulletin generated automatically
# At 12:00 PM: Afternoon bulletin generated automatically
# And so on...
```

### Example 2: Force Generate Current Bulletin

```bash
# Get current bulletin type
curl http://localhost:8000/bulletin/status

# Force generate (e.g., it's currently 14:30, so afternoon)
curl -X POST http://localhost:8000/bulletin/generate/afternoon

# Check status
docker-compose logs -f app
```

### Example 3: Queue News for Next Bulletin

```bash
# Queue breaking news
curl -X POST http://localhost:8000/bulletin/queue \
  -H "Content-Type: application/json" \
  -d '{
    "headline": "महत्वाची घोषणा",
    "content": "नई घोषणा जारी की गई है...",
    "category": "महत्वपूर्ण",
    "breaking": true
  }'

# Next scheduled bulletin will use this queued news
```

### Example 4: Check What's Coming Next

```bash
# Get next bulletin time
curl http://localhost:8000/bulletin/status | jq '.next_bulletin_time, .next_bulletin_type'

# Output:
# "17:00"
# "evening"
```

---

## Configuration

### Customize Bulletin Times

Edit `bulletin_scheduler.py`:

```python
BULLETIN_SCHEDULE = {
    "05:00": "morning",     # Change to desired time
    "12:00": "afternoon",
    "17:00": "evening",
    "21:00": "prime_time",
    "00:00": "night"
}
```

### Customize Bulletin Info

```python
BULLETIN_INFO = {
    "morning": {
        "name": "Custom Name",
        "description": "Custom description",
        "duration": 10,
        "tone": "informative"
    }
}
```

### Change Check Interval

In `bulletin_scheduler.py` `_run_scheduler()` method:

```python
time.sleep(30)  # Check every 30 seconds (default)
# Change to:
time.sleep(60)  # Check every 60 seconds
```

---

## Docker Deployment

With Docker, bulletin scheduler works out of the box:

```bash
# Start with bulletin scheduling enabled
docker-compose up -d

# Check scheduler running
docker-compose logs -f app | grep -i bulletin

# Output:
# Bulletin scheduler thread started
# BULLETIN SCHEDULE
# 05:00 - Morning Bulletin: Early morning news...
```

---

## Monitoring

### View Bulletin Logs

```bash
# All bulletin activity
docker-compose logs app | grep -i bulletin

# Follow live
docker-compose logs -f app | grep -i bulletin
```

### Check Scheduler Status

```bash
# Quick status check
curl http://localhost:8000/bulletin/status

# Full schedule
curl http://localhost:8000/bulletin/schedule
```

### Manual Schedule Check

```python
# In Python
from encoder.bulletin_scheduler import BulletinScheduler

scheduler = BulletinScheduler(None)
print(scheduler.get_current_bulletin_type())     # Current type
print(scheduler.get_next_bulletin_time())        # Next time
```

---

## Troubleshooting

### Bulletins Not Generating

**Check 1:** Scheduler running?
```bash
docker-compose logs app | grep "Bulletin scheduler"
```

**Check 2:** Correct time format?
```bash
# Ensure bulletin times are HH:MM format
# In UTC/server timezone
```

**Check 3:** No errors in logs?
```bash
docker-compose logs app | grep ERROR
```

### Missing Bulletins

**Solution:** Queue news for next bulletin
```bash
# Queue current content
curl -X POST http://localhost:8000/bulletin/queue \
  -H "Content-Type: application/json" \
  -d '{"headline":"...", "content":"...", "category":"...", "breaking":false}'
```

### Bulletins Repeating

**Solution:** Scheduler includes duplicate prevention
- Each bulletin runs once per minute
- Monitor logs for duplicates
- If seen, check system time sync

---

## Production Setup

For 24/7 bulletin broadcasting:

1. **Start with Docker Compose Production:**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

2. **Enable Auto-Restart:**
```bash
docker update --restart unless-stopped vartapravah_app
```

3. **Monitor Stream Health:**
```bash
./stream-monitor.sh &
```

4. **Set Up Log Rotation:**
```bash
# Docker logs auto-rotate (see docker-compose.prod.yml)
```

5. **Queue News Periodically:**
```bash
# Via API calls or webhook integration
```

---

## Advanced: Custom Bulletin Logic

### Generate Bulletins with Custom Data

```python
# In your application
from encoder.bulletin_scheduler import BulletinScheduler

def custom_bulletin_generator(bulletin_type):
    # Fetch news from API
    news = fetch_from_news_api(bulletin_type)
    
    # Generate with custom content
    generate_news(news_data=news, bulletin_type=bulletin_type)

scheduler = BulletinScheduler(custom_bulletin_generator)
scheduler.start_scheduler()
```

### Integration with External News APIs

```python
import requests

def fetch_marathi_news():
    """Fetch news from Marathi news API."""
    response = requests.get("https://newsapi.org/v2/top-headlines?language=mr")
    articles = response.json()['articles']
    return [{
        'headline': article['title'],
        'content': article['description'],
        'category': 'News',
        'breaking': False
    } for article in articles]
```

---

## Summary

| Feature | Details |
|---------|---------|
| **Automatic Scheduling** | 5 daily bulletins at fixed times |
| **API Endpoints** | 4 endpoints for schedule/status/generate/queue |
| **Backward Compatible** | Works with existing news generation |
| **Flexible** | Customize times and content |
| **Production Ready** | Includes error handling and logging |
| **Docker Ready** | Pre-configured for Docker deployment |

---

**VartaPravah Bulletin Scheduler is production-ready for 24/7 automated news broadcasting! 📡**