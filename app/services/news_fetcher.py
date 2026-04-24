import requests
from app import config

class NewsFetcher:
    def __init__(self):
        self.api_key = config.NEWS_API_KEY

    def fetch_marathi_news(self):
        """Fetches top headlines for India/Marathi news using NewsAPI."""
        try:
            # Using the user's requested logic
            url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={self.api_key}"
            res = requests.get(url)
            articles = res.json().get("articles", [])[:5]
            
            # Extracting headlines
            return [article.get("title", "") for article in articles]
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []

# Keeping a functional interface if needed
def fetch_news():
    fetcher = NewsFetcher()
    return fetcher.fetch_marathi_news()
