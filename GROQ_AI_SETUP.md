# 🧠 Groq AI Setup Guide for VARTAPRAVAH

## Overview

VARTAPRAVAH now uses **Groq AI** to generate professional Marathi news scripts. Groq provides:
- ✅ Fast AI inference (Llama 3.1 8B model)
- ✅ Free tier with generous limits
- ✅ Perfect for professional Marathi script generation
- ✅ No translation needed - AI generates native Marathi!

---

## Step 1: Get Groq API Key (Free)

### 1a. Create Groq Account
1. Go to: https://console.groq.com/
2. Sign up with email or Google
3. Verify email

### 1b. Get API Key
1. Click on "API Keys" in left sidebar
2. Click "Create API Key"
3. Copy the key (looks like: `gsk_...`)
4. **Keep it safe!** Don't share publicly

---

## Step 2: Configure .env File

Create or update `.env` file in project root:

```bash
# NewsAPI (required)
NEWSAPI_KEY=your_newsapi_key

# Groq API (for AI Marathi script generation)
GROQ_API_KEY=gsk_your_groq_key_here

# Optional: WorldNews API
WORLDNEWS_API_KEY=your_worldnews_key

# Optional: Google Cloud credentials
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```

---

## Step 3: Install Groq Package

```bash
# Already in requirements.txt, but manual install:
pip install groq

# Or update all dependencies:
pip install -r requirements.txt
```

---

## Step 4: Test Groq Setup

```bash
# Test if Groq works
python -c "
from script_generator import generate_marathi_script

news = [
    {'title': 'Maharashtra rainfall increases', 'description': 'Monsoon brings heavy rain to Maharashtra', 'source': 'PTI'}
]

script = generate_marathi_script(news, 'सकाळ')
print('✅ Groq working!')
print(script)
"
```

---

## Usage Examples

### Simple Function (Easy)
```python
from script_generator import generate_marathi_script

news_list = [
    {"title": "Title", "description": "Desc", "source": "PTI"},
    {"title": "Title 2", "description": "Desc 2", "source": "ANI"}
]

# Generate Marathi script with AI
script = generate_marathi_script(news_list, bulletin_type="सकाळ")
print(script)  # Perfect Marathi script!
```

### Class-Based (Advanced)
```python
from script_generator import ScriptGenerator
from news_fetcher import NewsFetcher

fetcher = NewsFetcher()
news = fetcher.fetch_all_news(limit=5)

generator = ScriptGenerator(use_groq=True)
bulletin = generator.generate_bulletin_script(news, max_bullets=5)
narration = generator.generate_full_narration(bulletin)
```

---

## Bulletin Types (Marathi)

Use these types when generating scripts:

```python
"सकाळ"   # Morning (6 AM)
"मध्य"   # Noon (12 PM)
"संध्या"  # Evening (5 PM)
"प्राइम" # Prime Time (8 PM)
"रात्र"   # Night (10 PM)
```

Example:
```python
# Morning bulletin
script = generate_marathi_script(news, "सकाळ")

# Prime time bulletin
script = generate_marathi_script(news, "प्राइम")
```

---

## API Pipeline

```
NewsAPI
   ↓
News Fetcher (Python)
   ↓
News List (Dict)
   ↓
Groq AI ← 🧠 BRAIN
   ↓
Professional Marathi Script
   ↓
TTS Engine (Coqui)
   ↓
Audio WAV
   ↓
Lip-Sync (Wav2Lip)
   ↓
Final Video MP4
   ↓
YouTube Streaming
```

---

## What Groq AI Does

### Input
```python
[
    {
        "title": "Maharashtra receives record rainfall",
        "description": "State breaks 50-year rainfall record with 250mm in 24 hours",
        "source": "PTI"
    },
    {
        "title": "Agricultural relief announced",
        "description": "Govt announces relief package for affected farmers",
        "source": "ANI"
    }
]
```

### Output (Groq AI Generated)
```
सकाळ बुलेटिन - वार्ताप्रवाह मध्ये आपले स्वागत आहे।

महाराष्ट्रात गेल्या २४ तासांत रेकॉर्ड पर्जन्य पात गेला आहे। राज्य मागील पंचास वर्षांत सर्वात जास्त २५० मिलीमीटर पर्जन्यपात झाल्याचे समजले जात आहे। कृषी विभागाकडून माहिती मिळताना, या पर्जन्यपातामुळे शेतकरी समाजाला चिंता वाटत आहे।

सरकारने पाणीपुरवठ्याने प्रभावित केलेल्या शेतकर्यांसाठी मदत पॅकेज जाहीर केला आहे। आर्थिक मदतीचे तपशील लवकरच जाहीर होतील असे अपेक्षित आहे।

अधिक अपडेटसाठी पाहत रहा वार्ताप्रवाह।
```

Perfect Marathi! No English mixed in!

---

## Troubleshooting

### "GROQ_API_KEY not found"
1. Create `.env` file in project root
2. Add: `GROQ_API_KEY=gsk_your_key`
3. Restart Python/IDE

### "Failed to authenticate"
- Check key is correct (copy from console.groq.com)
- Ensure no extra spaces/quotes around key

### "Rate limit exceeded"
- Groq free tier: ~30 requests per minute
- Wait a minute and try again
- Upgrade to Groq Pro if needed

### "Import error: No module named 'groq'"
```bash
pip install groq
```

### Groq not available, using fallback?
- This is normal if GROQ_API_KEY not set
- System falls back to simple template
- Set API key to enable AI

---

## API Limits (Free Tier)

| Limit | Value |
|-------|-------|
| Requests/Day | ~10,000 |
| Requests/Min | ~30 |
| Tokens/Day | Generous |
| Cost | FREE |

Perfect for 5 bulletins/day!

---

## Running Complete Pipeline with Groq

```bash
# 1. Start server
python app/main.py

# 2. Generate bulletin with AI (in another terminal)
curl -X POST http://localhost:8000/bulletin \
  -H "Content-Type: application/json" \
  -d '{"max_bullets": 5, "use_google_translate": false}'

# 3. Or run complete pipeline
curl -X POST http://localhost:8000/bulletin-pipeline \
  -H "Content-Type: application/json" \
  -d '{
    "max_bullets": 5,
    "use_google_translate": false,
    "rtmp_url": "rtmp://a.rtmp.youtube.com/live2/YOUR_KEY"
  }'
```

---

## Key Features of AI-Generated Scripts

✅ **Native Marathi** - No translation artifacts
✅ **Professional Tone** - News anchor style
✅ **Smart Intro/Outro** - Context-aware openings
✅ **Proper Flow** - Logical bulletin structure
✅ **Complete Sentences** - Not just bullet points
✅ **TTS-Ready** - Perfect for speech synthesis
✅ **Fast** - ~2-5 seconds per bulletin
✅ **Consistent Quality** - Every time

---

## Comparison: AI vs Template

### Template (Before)
```
1. Maharashtra receives record rainfall।
   State breaks 50-year rainfall record
   ही बातमी PTI कडून प्राप्त झाली आहे।
```

### AI (Now - with Groq)
```
महाराष्ट्रात गेल्या २४ तासांत रेकॉर्ड पर्जन्य पात गेला आहे। 
राज्य मागील पंचास वर्षांत सर्वात जास्त २५० मिलीमीटर पर्जन्यपात झाल्याचे समजले जात आहे।
```

Much better! 🎯

---

## Security Best Practices

❌ **Don't:**
- Commit `.env` to git
- Share GROQ_API_KEY in code
- Hardcode keys anywhere

✅ **Do:**
- Use `.env` file (in .gitignore)
- Rotate keys periodically
- Use environment variables in production
- Use GitHub Secrets for CI/CD

---

## Groq Docs

- Official Docs: https://console.groq.com/docs
- Python SDK: https://github.com/groq/groq-python
- Models: Llama 3.1 8B & 70B, Mixtral

---

## Support

If Groq not working:
1. Check .env file
2. Verify API key at console.groq.com
3. Check rate limits
4. Test with: `python app/script_generator.py`

---

**Status:** ✅ Production Ready with Groq AI
**Version:** 2.0 (AI-Powered)
**Last Updated:** 2024-01-20

Made with ❤️ for VARTAPRAVAH - Now with AI! 🧠✨
