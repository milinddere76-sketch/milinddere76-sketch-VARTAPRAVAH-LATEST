"""
VartaPravah News Fetcher Service

Multi-source news aggregation with:
- NewsAPI integration
- Google News RSS feeds
- Priority scoring (Maharashtra/India focused)
- Strong deduplication
- Marathi formatting (with AI upgrade path)
- Ticker generation for broadcast
"""

import requests
import feedparser
import hashlib
import logging
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# =========================
# CONFIGURATION
# =========================

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "YOUR_API_KEY")
MAX_NEWS = int(os.getenv("MAX_NEWS", "25"))
MIN_NEWS = int(os.getenv("MIN_NEWS", "5"))
TEMP_DIR = os.getenv("TEMP_DIR", "app/temp")

# Google News RSS sources (India focused)
RSS_SOURCES = [
    {
        "url": "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en",
        "name": "Google News - India"
    },
    {
        "url": "https://news.google.com/rss/search?q=Maharashtra+Marathi&hl=en-IN&gl=IN&ceid=IN:en",
        "name": "Google News - Maharashtra"
    },
    {
        "url": "https://news.google.com/rss/search?q=Mumbai&hl=en-IN&gl=IN&ceid=IN:en",
        "name": "Google News - Mumbai"
    }
]

# Cache for deduplication across session
seen_hashes = set()
last_fetch_time = None

# =========================
# DATA MODELS
# =========================

class NewsArticle(BaseModel):
    """Structured news article ready for anchor broadcast."""
    headline: str
    content: str
    category: str
    priority: int
    source: str
    timestamp: str
    language: str = "mr"  # Marathi
    is_breaking: bool = False
    region: str = "महाराष्ट्र"  # Maharashtra


# =========================
# NEWS API INTEGRATION
# =========================

def fetch_from_api() -> List[Dict]:
    """
    Fetch news from NewsAPI.org
    
    Returns top headlines from India with focus on Maharashtra
    """
    logger.info("📡 Fetching from NewsAPI...")
    
    articles = []
    
    try:
        # General India news
        url_india = f"https://newsapi.org/v2/top-headlines?country=in&pageSize=50&apiKey={NEWS_API_KEY}"
        response = requests.get(url_india, timeout=10)
        
        if response.status_code == 200:
            articles.extend(response.json().get("articles", []))
            logger.info(f"✅ Got {len(articles)} articles from NewsAPI")
        else:
            logger.warning(f"⚠️ NewsAPI returned status {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ NewsAPI fetch failed: {e}")
    
    return articles


# =========================
# RSS FEED INTEGRATION
# =========================

def fetch_from_rss() -> List[Dict]:
    """
    Fetch news from Google News RSS feeds
    
    Covers India, Maharashtra, Mumbai with regional priority
    """
    logger.info("📻 Fetching from RSS feeds...")
    
    articles = []
    
    for source in RSS_SOURCES:
        try:
            logger.info(f"  → {source['name']}")
            feed = feedparser.parse(source['url'])
            
            for entry in feed.entries:
                article = {
                    "title": entry.get("title", ""),
                    "description": entry.get("summary", ""),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "source": {
                        "name": source['name']
                    }
                }
                articles.append(article)
            
            logger.info(f"  ✅ Got {len(feed.entries)} entries")
        
        except Exception as e:
            logger.warning(f"  ❌ RSS fetch failed: {e}")
    
    logger.info(f"✅ Total RSS articles: {len(articles)}")
    return articles


# =========================
# PRIORITY SCORING SYSTEM
# =========================

def calculate_priority_score(text: str) -> int:
    """
    Score news based on relevance and importance
    
    Scoring:
    - Maharashtra/Mumbai region: +5
    - India-wide: +3
    - Breaking news: +2
    - Government/Politics: +2
    - Law & Order: +1
    """
    
    text_lower = text.lower()
    score = 0
    
    # Regional priority (Maharashtra focus)
    if "maharashtra" in text_lower or "महाराष्ट्र" in text:
        score += 5
    elif "mumbai" in text_lower or "मुंबई" in text:
        score += 5
    elif "pune" in text_lower or "पुणे" in text:
        score += 4
    elif "nagpur" in text_lower or "नागपूर" in text:
        score += 4
    
    # National interest
    if "india" in text_lower or "भारत" in text:
        score += 3
    
    # Breaking/Important news
    if "breaking" in text_lower or "latest" in text_lower:
        score += 2
    if "अग्रेसर" in text or "तातडीने" in text:  # Marathi for breaking
        score += 2
    
    # Government/Politics
    if "government" in text_lower or "election" in text_lower:
        score += 2
    if "मुख्यमंत्री" in text or "राजकारण" in text:
        score += 2
    
    # Law & Order
    if "crime" in text_lower or "police" in text_lower:
        score += 1
    if "गुन्हे" in text or "पोलीस" in text:
        score += 1
    
    return score


# =========================
# DEDUPLICATION SYSTEM
# =========================

def is_duplicate(headline: str, content: str) -> bool:
    """
    Check if news article is duplicate using MD5 hash
    
    Prevents same story from appearing multiple times
    """
    combined = f"{headline}|{content}".strip()
    article_hash = hashlib.md5(combined.encode()).hexdigest()
    
    if article_hash in seen_hashes:
        logger.debug(f"🔄 Duplicate detected: {headline[:50]}...")
        return True
    
    seen_hashes.add(article_hash)
    return False


def reset_duplicates():
    """Reset duplicate cache for new cycle."""
    global seen_hashes
    seen_hashes.clear()
    logger.info("🔄 Duplicate cache cleared")


# =========================
# MARATHI CONVERSION (BASIC)
# =========================

def to_marathi_basic(text: str) -> str:
    """
    Basic English to Marathi conversion
    
    ⚠️ UPGRADE PATH: Replace with AI model (Groq/OpenAI)
    See upgrade_to_marathi_ai() below
    """
    
    if not text:
        return text
    
    replacements = {
        # Places
        "India": "भारत",
        "India": "भारत",
        "Mumbai": "मुंबई",
        "Maharashtra": "महाराष्ट्र",
        "Delhi": "दिल्ली",
        "Pune": "पुणे",
        "Nagpur": "नागपूर",
        
        # Government
        "government": "सरकार",
        "Government": "सरकार",
        "Prime Minister": "पंतप्रधान",
        "Chief Minister": "मुख्यमंत्री",
        "President": "राष्ट्रपती",
        "Parliament": "संसद",
        "election": "निवडणूक",
        "Election": "निवडणूक",
        
        # General
        "news": "बातमी",
        "breaking": "अग्रेसर",
        "breaking news": "अग्रेसर बातमी",
        "latest": "सर्वशेष",
        "today": "आज",
        "police": "पोलीस",
        "crime": "गुन्हा",
        "court": "कोर्ट",
    }
    
    result = text
    for english, marathi in replacements.items():
        result = result.replace(english, marathi)
    
    return result


def to_marathi_ai(text: str, api_type: str = "groq") -> str:
    """
    Convert to Marathi using AI API
    
    Supports: Groq, OpenAI
    
    ⚠️ REQUIRES: Set GROQ_API_KEY or OPENAI_API_KEY in .env
    """
    
    api_key = None
    
    if api_type == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            logger.warning("⚠️ GROQ_API_KEY not set, using basic conversion")
            return to_marathi_basic(text)
        
        try:
            # Groq API call
            headers = {"Authorization": f"Bearer {api_key}"}
            marathi_prompt = """खालील बातमी शुद्ध, व्यावसायिक मराठी न्यूज अँकर शैलीत लिहा.
कोणतेही इंग्रजी शब्द वापरू नका. फक्त मराठी.

मूळ बातमी:
{}

शुद्ध मराठी:"""
            payload = {
                "model": "mixtral-8x7b-32768",
                "messages": [
                    {
                        "role": "user",
                        "content": marathi_prompt.format(text)
                    }
                ]
            }
            
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                marathi_text = response.json()["choices"][0]["message"]["content"]
                logger.info("✅ Converted to Marathi via Groq AI")
                return marathi_text
        
        except Exception as e:
            logger.warning(f"⚠️ Groq conversion failed: {e}, using basic conversion")
    
    elif api_type == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.warning("⚠️ OPENAI_API_KEY not set, using basic conversion")
            return to_marathi_basic(text)
        
        try:
            headers = {"Authorization": f"Bearer {api_key}"}
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "user",
                        "content": """खालील बातमी शुद्ध, व्यावसायिक मराठी न्यूज अँकर शैलीत लिहा.
कोणतेही इंग्रजी शब्द वापरू नका. फक्त मराठी.

मूळ बातमी:
{}

शुद्ध मराठी:""".format(text)
                    }
                ]
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                marathi_text = response.json()["choices"][0]["message"]["content"]
                logger.info("✅ Converted to Marathi via OpenAI")
                return marathi_text
        
        except Exception as e:
            logger.warning(f"⚠️ OpenAI conversion failed: {e}, using basic conversion")
    
    return to_marathi_basic(text)


# =========================
# CATEGORY DETECTION
# =========================

def detect_category(text: str) -> str:
    """
    Detect news category based on keywords
    
    Categories (in Marathi):
    - राजकारण (Politics)
    - गुन्हे (Crime)
    - व्यवसाय (Business)
    - खेळ (Sports)
    - हवामान (Weather)
    - आरोग्य (Health)
    - सामान्य (General)
    """
    
    text_lower = text.lower()
    
    if "election" in text_lower or "government" in text_lower or "minister" in text_lower:
        return "राजकारण"
    elif "crime" in text_lower or "police" in text_lower or "murder" in text_lower:
        return "गुन्हे"
    elif "market" in text_lower or "stock" in text_lower or "business" in text_lower:
        return "व्यवसाय"
    elif "sport" in text_lower or "match" in text_lower or "cricket" in text_lower:
        return "खेळ"
    elif "weather" in text_lower or "rain" in text_lower or "temperature" in text_lower:
        return "हवामान"
    elif "health" in text_lower or "covid" in text_lower or "hospital" in text_lower:
        return "आरोग्य"
    else:
        return "सामान्य"


# =========================
# NEWS FORMATTING & VALIDATION
# =========================

def format_and_validate_news(articles: List[Dict]) -> List[NewsArticle]:
    """
    Process, validate, and format articles into NewsArticle objects
    
    Steps:
    1. Extract headline and content
    2. Check for duplicates
    3. Calculate priority score
    4. Convert to Marathi
    5. Detect category
    6. Create structured NewsArticle
    """
    
    logger.info("📝 Processing and formatting news...")
    
    processed = []
    
    for article in articles:
        try:
            # Extract fields (handle different API formats)
            headline = article.get("title") or article.get("headline") or ""
            content = article.get("description") or article.get("content") or ""
            
            if not headline or len(headline.strip()) < 5:
                continue
            
            # Check for duplicates
            if is_duplicate(headline, content):
                continue
            
            # Calculate priority
            priority = calculate_priority_score(f"{headline} {content}")
            
            # Convert to Marathi (using AI or basic)
            marathi_headline = to_marathi_ai(headline, api_type="groq")
            marathi_content = to_marathi_ai(content, api_type="groq")
            
            # Detect category
            category = detect_category(f"{headline} {content}")
            
            # Check if breaking news
            is_breaking = priority >= 4
            
            # Create structured article
            news_article = NewsArticle(
                headline=marathi_headline,
                content=marathi_content,
                category=category,
                priority=priority,
                source=article.get("source", {}).get("name", "Unknown"),
                timestamp=datetime.now().strftime("%H:%M"),
                is_breaking=is_breaking,
                region="महाराष्ट्र"
            )
            
            processed.append(news_article)
        
        except Exception as e:
            logger.warning(f"⚠️ Failed to process article: {e}")
            continue
    
    # Sort by priority (descending)
    processed.sort(key=lambda x: x.priority, reverse=True)
    
    # Enforce min/max limits
    if len(processed) < MIN_NEWS:
        logger.warning(f"⚠️ Only {len(processed)} articles available (minimum: {MIN_NEWS})")
    
    final_list = processed[:MAX_NEWS]
    
    logger.info(f"✅ Final news count: {len(final_list)}")
    return final_list


# =========================
# MAIN NEWS FETCHER
# =========================

def get_marathi_news() -> List[NewsArticle]:
    """
    Main function: Fetch, process, and return Marathi news
    
    Pipeline:
    1. Fetch from NewsAPI
    2. Fetch from RSS feeds
    3. Combine and deduplicate
    4. Format as NewsArticle objects
    5. Sort by priority
    
    Returns: List of NewsArticle objects ready for TTS + Anchor video
    """
    
    global last_fetch_time
    
    logger.info("🗞️ VartaPravah News Fetcher Starting...")
    
    # Prevent rapid re-fetching
    if last_fetch_time and (datetime.now() - last_fetch_time).total_seconds() < 60:
        logger.warning("⏱️ Rate limit: Wait before fetching again")
        return []
    
    try:
        # Fetch from all sources
        api_articles = fetch_from_api()
        rss_articles = fetch_from_rss()
        
        # Combine
        all_articles = api_articles + rss_articles
        logger.info(f"📊 Total raw articles: {len(all_articles)}")
        
        # Process and format
        final_news = format_and_validate_news(all_articles)
        
        last_fetch_time = datetime.now()
        
        logger.info(f"✅ Final news ready for broadcast: {len(final_news)} articles")
        return final_news
    
    except Exception as e:
        logger.error(f"❌ News fetching failed: {e}")
        return []


# =========================
# TICKER GENERATION
# =========================

def generate_ticker(news_list: List[NewsArticle], output_path: Optional[str] = None) -> str:
    """
    Generate scrolling ticker text from news headlines
    
    Format: "Headline 1   |   Headline 2   |   Headline 3 ..."
    
    Output: Saved to file for graphics overlay
    """
    
    if not output_path:
        output_path = os.path.join(TEMP_DIR, "ticker.txt")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Create ticker text
    ticker_text = "   |   ".join([
        article.headline for article in news_list
    ])
    
    # Add repeat for smooth scrolling
    ticker_text = ticker_text + "   |   " + ticker_text
    
    # Write to file
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(ticker_text)
        
        logger.info(f"✅ Ticker generated: {output_path}")
        return ticker_text
    
    except Exception as e:
        logger.error(f"❌ Ticker generation failed: {e}")
        return ""


# =========================
# EXPORT FOR ANCHOR VIDEO
# =========================

def prepare_for_anchor_video(news_list: List[NewsArticle]) -> Dict:
    """
    Prepare news data in format ready for anchor video generation
    
    Returns JSON structure for TTS + Wav2Lip processing
    """
    
    return {
        "timestamp": datetime.now().isoformat(),
        "total_articles": len(news_list),
        "breaking_news_count": sum(1 for n in news_list if n.is_breaking),
        "articles": [
            {
                "headline": n.headline,
                "content": n.content,
                "category": n.category,
                "priority": n.priority,
                "is_breaking": n.is_breaking,
                "anchor_script": f"{n.headline}. {n.content}"  # Ready for TTS
            }
            for n in news_list
        ]
    }


# =========================
# TEST & DEBUG
# =========================

if __name__ == "__main__":
    import json
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    
    # Fetch news
    print("\n" + "="*60)
    print("🗞️ VartaPravah News Fetcher - Test Run")
    print("="*60 + "\n")
    
    news_list = get_marathi_news()
    
    print(f"\n📺 Final News ({len(news_list)} articles):\n")
    for idx, article in enumerate(news_list, 1):
        print(f"{idx}. [{article.category}] {article.headline}")
        print(f"   📌 Priority: {article.priority} | Source: {article.source}")
        print(f"   {article.content[:100]}...")
        print()
    
    # Generate ticker
    print("\n" + "="*60)
    print("📡 Generating Ticker...")
    print("="*60 + "\n")
    
    ticker = generate_ticker(news_list)
    print(f"Ticker: {ticker[:200]}...\n")
    
    # Prepare for anchor
    print("\n" + "="*60)
    print("🎬 Preparing for Anchor Video...")
    print("="*60 + "\n")
    
    anchor_data = prepare_for_anchor_video(news_list)
    print(json.dumps(anchor_data, ensure_ascii=False, indent=2))
