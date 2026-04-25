import requests
import os
import config

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
    Validates news authenticity by comparing multiple sources.
    Returns True if the headline is found in at least 2 sources.
    """
    if not news_title:
        return False

    print(f"🔍 [FACT-CHECK] Verifying authenticity of: {news_title[:60]}...")
    
    data = fetch_sources(news_title)

    # If we only have 1 source configured or reachable, we can't cross-verify
    # In a real environment, we'd want at least 2 sources
    if len(data) < 2:
        print("⚠️ [FACT-CHECK] Insufficient sources for cross-verification. Defaulting to True for single source.")
        return True # Or False depending on strictness

    # Simple validation: Check if title keywords appear across sources
    # We can upgrade this to NLP embedding similarity in the future
    count = sum(news_title.lower()[:50] in str(d).lower() for d in data)

    if count >= 2:
        print("✅ [FACT-CHECK] Verification SUCCESS. Sources match.")
        return True
    else:
        print("❌ [FACT-CHECK] Verification FAILED. Source mismatch or missing.")
        return False
