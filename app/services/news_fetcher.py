import requests
import config

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
            
            # Fetch India Top Headlines
            res1 = requests.get(url1)
            articles1 = res1.json().get("articles", [])[:10]
            headlines.extend([a.get("title", "") for a in articles1])
            
            # Fetch Maharashtra specific news
            res2 = requests.get(url2)
            articles2 = res2.json().get("articles", [])[:5]
            headlines.extend([a.get("title", "") for a in articles2])
            
            return list(set(headlines))[:10] # Unique headlines, top 10
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []

# Keeping a functional interface if needed
def fetch_news():
    fetcher = NewsFetcher()
    return fetcher.fetch_marathi_news()
