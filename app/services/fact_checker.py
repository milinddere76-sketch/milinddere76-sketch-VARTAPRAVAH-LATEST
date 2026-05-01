import requests
import os
from app import config

def fetch_sources(query):
    """
    Queries multiple news APIs to cross-verify a headline.
    """
    # Using configured API keys
    news_api_key = config.NEWS_API_KEY
    world_news_key = os.getenv("WORLD_NEWS_API_KEY") # Added to .env
    
    urls = []
    if news_api_key:
        urls.append(f"https://newsapi.org/v2/everything?q={query}&apiKey={news_api_key}")
    
    if world_news_key:
        urls.append(f"https://api.worldnewsapi.com/search-news?text={query}&api-key={world_news_key}")

    results = []
    for url in urls:
        try:
            r = requests.get(url, timeout=5)
            if r.ok:
                results.append(r.json())
        except Exception as e:
            print(f"⚠️ [FACT-CHECK] Error querying source: {e}")
            continue
    return results

def is_verified(news_title):
    """
    Sanity check for news authenticity.
    In Fast-Track mode, we trust primary sources (Google/NewsAPI) 
    and only filter out trash or broken titles.
    """
    if not news_title or len(news_title) < 20:
        return False

    # Block common 'Trash' or 'Test' patterns
    trash_keywords = ["test", "dummy", "untitled", "broken", "removed", "deleted"]
    if any(k in news_title.lower() for k in trash_keywords):
        print(f"🗑️ [FACT-CHECK] Filtered trash/test news: {news_title[:50]}...")
        return False

    print(f"✅ [FACT-CHECK] Fast-Track Verified: {news_title[:60]}...")
    return True
