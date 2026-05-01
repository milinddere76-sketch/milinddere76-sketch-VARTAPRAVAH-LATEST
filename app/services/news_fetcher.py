import requests
from app import config

class NewsFetcher:
    def __init__(self):
        self.api_key = config.NEWS_API_KEY

    def fetch_marathi_news(self):
        """Fetches top headlines for India/Maharashtra news using NewsAPI."""
        try:
            # Primary: Top India Headlines
            url1 = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={self.api_key}"
            # Secondary: Maharashtra specific news
            url2 = f"https://newsapi.org/v2/everything?q=Maharashtra&sortBy=publishedAt&apiKey={self.api_key}"
            
            headlines = []
            
            # 1. Fetch India Top Headlines (NewsAPI)
            try:
                res1 = requests.get(url1, timeout=10)
                articles1 = res1.json().get("articles", [])[:10]
                headlines.extend([a.get("title", "") for a in articles1 if a.get("title")])
            except Exception:
                pass
            
            # 2. Fetch Maharashtra specific news (NewsAPI)
            try:
                res2 = requests.get(url2, timeout=10)
                articles2 = res2.json().get("articles", [])[:5]
                headlines.extend([a.get("title", "") for a in articles2 if a.get("title")])
            except Exception:
                pass
            
            # 3. FALLBACK: Google News RSS (Always works, no API key needed)
            if len(headlines) < 3:
                try:
                    rss_url = "https://news.google.com/rss/search?q=Maharashtra&hl=mr&gl=IN&ceid=IN:mr"
                    res_rss = requests.get(rss_url, timeout=10)
                    # Extracting titles from XML items (simple string find to avoid heavy xml libs)
                    titles = res_rss.text.split("<title>")[2:12] # Skip first which is channel title
                    for t in titles:
                        clean_t = t.split("</title>")[0]
                        if clean_t:
                            headlines.append(clean_t)
                except Exception:
                    pass
            
            return list(set(headlines))[:15] # Unique headlines, top 15
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []

# Keeping a functional interface if needed
def fetch_news():
    fetcher = NewsFetcher()
    return fetcher.fetch_marathi_news()
